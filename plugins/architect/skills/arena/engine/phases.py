"""Машина фаз турнира.

Порядок: scout → spawn → screen → round (attack → defend → judge, по обеим дорожкам) →
final (панель, финмодель, аудит) → stress_attack → stress_defend → verdict → package → done.

Каждое задание — это файл-бриф и файлы-результаты. Задание выполнено, когда все результаты
на месте и (для судей) валидны. Лимит списывается в момент выдачи задания в волну.
"""
import json
import math
import os

from . import briefs, budget, deck, state as st

JUDGE_PHASES = {"screen", "judge", "verdict"}
JSON_PHASES = {"screen", "judge", "persona", "verdict"}
MAX_ATTEMPTS = {"judge": 3, "screen": 3, "verdict": 3}

LANE_TEXT = {
    "safe": ("надёжная", "Стратегия должна быть реализуема основателем в ближайшие месяцы и выдержать жёсткую проверку цифрами."),
    "bold": ("смелая", "Думай масштабнее, чем принято на рынке. Смелость не отменяет цифр: смелую стратегию тоже проверят на деньги и реализуемость, но судят её против других смелых."),
}


# ---------- общие помощники ----------

def ab(state, *parts):
    return os.path.abspath(st.path(state, *parts))


def common_values(state):
    return {
        "task": st.read(st.path(state, "task.md")),
        "dossier": st.read(st.path(state, "dossier.md"), "(досье не передано)"),
        "arena_dir": os.path.abspath(state["dir"]),
        "rubric": ab(state, "rubric.md"),
        "scout_market": ab(state, "scout", "market.md") if state["scout"] else "(разведки нет)",
        "scout_voice": ab(state, "scout", "voice.md") if state["scout"] else "(разведки нет)",
        "n": state["n"],
    }


def card_values(agent):
    c = agent["card"]
    return {
        "lens_name": c["lens"]["name"], "lens_how": c["lens"]["how"],
        "method_name": c["method"]["name"], "method_how": c["method"]["how"],
        "stance_name": c["stance"]["name"], "stance_how": c["stance"]["how"],
    }


def add_job(state, job_id, phase, model, template, values, outs):
    safe_id = job_id.replace(":", "_")
    prompt_path = ab(state, "briefs", safe_id + ".md")
    v = dict(common_values(state))
    v.update(values)
    st.write(prompt_path, briefs.fill(briefs.T[template], v))
    state["jobs"][job_id] = {
        "phase": phase, "stage": state["phase_key"], "model": model, "prompt": prompt_path,
        "outs": [os.path.abspath(o) for o in outs], "attempts": 0, "status": "pending",
    }


def phase_jobs(state, stage=None):
    stage = stage or state["phase_key"]
    return {k: j for k, j in state["jobs"].items() if j["stage"] == stage}


def valid(job):
    for o in job["outs"]:
        if not st.filled(o):
            return False
    if job["phase"] in JSON_PHASES:
        try:
            with open(job["outs"][0], encoding="utf-8") as fh:
                json.load(fh)
        except (ValueError, OSError):
            return False
    return True


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def worker(state):
    return state["models"]["worker"]


def judge_model(state):
    return state["models"]["judge"]


# ---------- создание заданий по фазам ----------

def make_scout(state):
    add_job(state, "scout:market", "scout", worker(state), "scout_market", {"out": ab(state, "scout", "market.md")}, [st.path(state, "scout", "market.md")])
    add_job(state, "scout:voice", "scout", worker(state), "scout_voice", {"out": ab(state, "scout", "voice.md")}, [st.path(state, "scout", "voice.md")])


def make_spawn(state):
    for aid, a in state["agents"].items():
        out = st.path(state, "solutions", f"{aid}.r0.md")
        name, how = LANE_TEXT[a["lane"]]
        v = {"agent": aid, "out": os.path.abspath(out), "lane_name": name, "lane_how": how}
        v.update(card_values(a))
        add_job(state, f"spawn:{aid}", "spawn", worker(state), "competitor", v, [out])
        a["sol"] = os.path.abspath(out)


def make_screen(state):
    made = False
    for lane, L in state["lanes"].items():
        alive = L["alive"]
        if len(alive) <= 4:
            continue
        batches = [alive[i:i + 8] for i in range(0, len(alive), 8)]
        L["screen"] = []
        for bi, ids in enumerate(batches, 1):
            keep = math.ceil(len(ids) / 2)
            out = st.path(state, "screen", f"{lane}-b{bi}.json")
            listing = "\n".join(f"- {i}: {state['agents'][i]['sol']}" for i in ids)
            add_job(state, f"screen:{lane}:b{bi}", "screen", judge_model(state), "screen",
                    {"count": len(ids), "keep": keep, "list": listing, "ids": ", ".join(ids),
                     "batch": f"{lane}-b{bi}", "out": os.path.abspath(out)}, [out])
            L["screen"].append({"ids": ids, "keep": keep, "out": os.path.abspath(out)})
            made = True
    return made


def pair_lanes(state):
    rng = deck.rng_for(f"{state['seed']}-{state['round'] + 1}")
    state["round"] += 1
    for lane, L in state["lanes"].items():
        if len(L["alive"]) <= 1:
            L["matches"], L["byes"] = [], []
            continue
        ids = list(L["alive"])
        rng.shuffle(ids)
        L["byes"] = [ids.pop()] if len(ids) % 2 else []
        L["matches"] = [{"id": f"r{state['round']}-{lane}-m{k + 1}", "a": ids[2 * k], "b": ids[2 * k + 1]} for k in range(len(ids) // 2)]


def make_attack(state):
    r = state["round"]
    for lane, L in state["lanes"].items():
        for m in L["matches"]:
            for me, opp in ((m["a"], m["b"]), (m["b"], m["a"])):
                out = st.path(state, "rounds", f"{m['id']}-{me}-on-{opp}.attack.md")
                v = {"agent": me, "round": r, "match": m["id"], "target": opp,
                     "target_solution": state["agents"][opp]["sol"], "own_solution": state["agents"][me]["sol"],
                     "out": os.path.abspath(out)}
                v.update(card_values(state["agents"][me]))
                add_job(state, f"r{r}:{m['id']}:attack:{me}", "attack", worker(state), "attacker", v, [out])
                m.setdefault("attacks_on", {})[opp] = os.path.abspath(out)


def make_defend(state):
    r = state["round"]
    for lane, L in state["lanes"].items():
        for m in L["matches"]:
            for me, opp in ((m["a"], m["b"]), (m["b"], m["a"])):
                dout = st.path(state, "rounds", f"{m['id']}-{me}.defense.md")
                sout = st.path(state, "solutions", f"{me}.r{r}.md")
                v = {"agent": me, "round": r, "match": m["id"], "attacker": opp,
                     "own_solution": state["agents"][me]["sol"], "attacks": m["attacks_on"][me],
                     "defense_out": os.path.abspath(dout), "solution_out": os.path.abspath(sout)}
                v.update(card_values(state["agents"][me]))
                add_job(state, f"r{r}:{m['id']}:defend:{me}", "defend", worker(state), "defender", v, [dout, sout])
                m.setdefault("defense", {})[me] = os.path.abspath(dout)
                m.setdefault("revised", {})[me] = os.path.abspath(sout)


def make_judge(state):
    r = state["round"]
    for lane, L in state["lanes"].items():
        for m in L["matches"]:
            a, b = m["a"], m["b"]
            out = st.path(state, "rounds", f"{m['id']}.verdict.json")
            v = {"match": m["id"], "round": r, "first": a, "second": b,
                 "first_solution": m["revised"][a], "first_attacks": m["attacks_on"][a], "first_defense": m["defense"][a],
                 "second_solution": m["revised"][b], "second_attacks": m["attacks_on"][b], "second_defense": m["defense"][b],
                 "out": os.path.abspath(out)}
            add_job(state, f"r{r}:{m['id']}:judge", "judge", judge_model(state), "judge", v, [out])
            m["verdict"] = os.path.abspath(out)


def finalists(state):
    lanes = state["lanes"]
    champs = [L["alive"][0] for L in lanes.values() if len(L["alive"]) == 1 and L["size"] > 0]
    if len(champs) >= 2:
        return champs[:2]
    only = next(L for L in lanes.values() if L["size"] > 0)
    out = [only["alive"][0]]
    if only.get("runner_up"):
        out.append(only["runner_up"])
    return out


def make_final(state):
    fs = finalists(state)
    state["finalists"] = fs
    if len(fs) == 2:
        x, y = fs
        for p in deck.load_personas():
            out = st.path(state, "final", f"panel-{p['id']}.json")
            add_job(state, f"final:panel:{p['id']}", "persona", worker(state), "persona",
                    {"persona_id": p["id"], "persona_name": p["name"], "persona_who": p["who"], "persona_asks": p["asks"],
                     "x_solution": state["agents"][x]["sol"], "y_solution": state["agents"][y]["sol"], "out": os.path.abspath(out)}, [out])
    for f in fs:
        fo = st.path(state, "final", f"finance-{f}.md")
        add_job(state, f"final:finance:{f}", "final", worker(state), "finance",
                {"solution": state["agents"][f]["sol"], "finalist": f, "out": os.path.abspath(fo)}, [fo])
        ao = st.path(state, "final", f"audit-{f}.md")
        add_job(state, f"final:audit:{f}", "final", worker(state), "audit",
                {"solution": state["agents"][f]["sol"], "finalist": f, "out": os.path.abspath(ao)}, [ao])


def panel_paths(state):
    return ", ".join(ab(state, "final", f"panel-{p['id']}.json") for p in deck.load_personas()
                     if os.path.exists(st.path(state, "final", f"panel-{p['id']}.json"))) or "(панели нет)"


def make_stress_attack(state):
    for f in state["finalists"]:
        out = st.path(state, "final", f"stress-{f}.md")
        add_job(state, f"stress:attack:{f}", "stress_attack", worker(state), "stress_attack",
                {"solution": state["agents"][f]["sol"], "finance": ab(state, "final", f"finance-{f}.md"),
                 "audit": ab(state, "final", f"audit-{f}.md"), "panel": panel_paths(state), "finalist": f,
                 "out": os.path.abspath(out)}, [out])


def make_stress_defend(state):
    for f in state["finalists"]:
        dout = st.path(state, "final", f"hardening-{f}.md")
        sout = st.path(state, "solutions", f"{f}.final.md")
        add_job(state, f"stress:defend:{f}", "stress_defend", worker(state), "stress_defend",
                {"solution": state["agents"][f]["sol"], "finance": ab(state, "final", f"finance-{f}.md"),
                 "audit": ab(state, "final", f"audit-{f}.md"), "panel": panel_paths(state),
                 "stress": ab(state, "final", f"stress-{f}.md"), "finalist": f,
                 "defense_out": os.path.abspath(dout), "solution_out": os.path.abspath(sout)}, [dout, sout])
        state["agents"][f]["final_sol"] = os.path.abspath(sout)


def finalists_block(state):
    lines = []
    for f in state["finalists"]:
        lane = LANE_TEXT[state["agents"][f]["lane"]][0]
        lines.append(f"Финалист {f} ({lane} дорожка):\n"
                     f"- финальная стратегия: {state['agents'][f].get('final_sol', state['agents'][f]['sol'])}\n"
                     f"- финансовая модель: {ab(state, 'final', f'finance-{f}.md')}\n"
                     f"- аудит защиты и соответствия: {ab(state, 'final', f'audit-{f}.md')}\n"
                     f"- стресс-тест: {ab(state, 'final', f'stress-{f}.md')}\n"
                     f"- укрепление после стресс-теста: {ab(state, 'final', f'hardening-{f}.md')}")
    lines.append(f"Голоса панели покупателей и инвестора: {panel_paths(state)}")
    return "\n\n".join(lines)


def make_verdict(state):
    out = st.path(state, "final", "verdict.json")
    add_job(state, "verdict", "verdict", judge_model(state), "verdict",
            {"finalists_block": finalists_block(state), "out": os.path.abspath(out)}, [out])


def make_package(state):
    out = st.path(state, "result.md")
    add_job(state, "package", "package", judge_model(state), "package",
            {"finalists_block": finalists_block(state), "verdict": ab(state, "final", "verdict.json"),
             "out": os.path.abspath(out)}, [out])


# ---------- сбор итогов фаз ----------

def collect_screen(state):
    for lane, L in state["lanes"].items():
        if not L.get("screen"):
            continue
        keep_all = []
        for b in L["screen"]:
            data = load_json(b["out"])
            ranking = [i for i in data.get("ranking", []) if i in b["ids"]]
            ranking += [i for i in b["ids"] if i not in ranking]
            keep_all += ranking[:b["keep"]]
        cut = [i for i in L["alive"] if i not in keep_all]
        L["alive"] = keep_all
        st.log(state, f"отсев {lane}: прошли {len(keep_all)}, выбыли {len(cut)}")


def collect_judge(state):
    for lane, L in state["lanes"].items():
        winners = []
        for m in L["matches"]:
            data = load_json(m["verdict"])
            w = data.get("winner", "")
            if w not in (m["a"], m["b"]):
                w = next((x for x in (m["a"], m["b"]) if x in str(w)), m["a"])
                st.log(state, f"{m['id']}: победитель записан неточно, распознан как {w}")
            loser = m["b"] if w == m["a"] else m["a"]
            for x in (m["a"], m["b"]):
                state["agents"][x]["sol"] = m["revised"][x]
            state["agents"][loser]["alive"] = False
            winners.append(w)
            L["last_loser"] = loser
            m["winner"] = w
        if L["matches"]:
            L["alive"] = winners + L["byes"]
            if len(L["alive"]) == 1:
                L["runner_up"] = L["last_loser"]
        st.log(state, f"раунд {state['round']} {lane}: осталось {len(L['alive'])}")


def lanes_done(state):
    return all(len(L["alive"]) <= 1 for L in state["lanes"].values())


# ---------- переходы ----------

ORDER = ["scout", "spawn", "screen", "attack", "defend", "judge", "final", "stress_attack", "stress_defend", "verdict", "package", "done"]


def enter(state, key):
    """Перейти в фазу key и создать её задания. Возвращает False, если фаза пустая."""
    state["phase_key"] = key
    if key == "scout":
        make_scout(state)
    elif key == "spawn":
        make_spawn(state)
    elif key == "screen":
        return make_screen(state)
    elif key == "attack":
        pair_lanes(state)
        make_attack(state)
    elif key == "defend":
        make_defend(state)
    elif key == "judge":
        make_judge(state)
    elif key == "final":
        make_final(state)
    elif key == "stress_attack":
        make_stress_attack(state)
    elif key == "stress_defend":
        make_stress_defend(state)
    elif key == "verdict":
        make_verdict(state)
    elif key == "package":
        make_package(state)
    return True


def advance(state):
    """Закрыть текущую фазу и открыть следующую непустую."""
    key = state["phase_key"]
    if key == "screen":
        collect_screen(state)
    if key == "judge":
        collect_judge(state)
    if key == "stress_defend":
        for f in state["finalists"]:
            state["agents"][f]["sol"] = state["agents"][f]["final_sol"]

    nxt = {"scout": "spawn", "spawn": "screen", "screen": "attack", "judge": "attack"}.get(key)
    if nxt is None:
        nxt = ORDER[ORDER.index(key) + 1]

    while True:
        if nxt == "screen" and not enter(state, "screen"):
            nxt = "attack"
            continue
        if nxt == "attack" and lanes_done(state):
            nxt = "final"
            continue
        if nxt != "screen":
            enter(state, nxt)
        return


# ---------- волны ----------

def sync(state):
    for j in phase_jobs(state).values():
        if j["status"] != "done" and valid(j):
            j["status"] = "done"


def fallback(state, job_id, job):
    """Задание не получилось после всех попыток."""
    if job["phase"] in JUDGE_PHASES:
        return False
    for o in job["outs"]:
        if not st.filled(o):
            st.write(o, "NO OUTPUT\n")
    job["status"] = "done"
    st.log(state, f"{job_id}: нет результата после {job['attempts']} попыток, записано NO OUTPUT")
    return True


def next_step(state):
    """Возвращает (тип, данные): ('wave', [(id, job)]), ('budget', info), ('stuck', id), ('done', path)."""
    while True:
        if state["phase_key"] == "done":
            return "done", ab(state, "result.md")
        sync(state)
        jobs = phase_jobs(state)
        todo = []
        for jid, j in jobs.items():
            if j["status"] == "done":
                continue
            limit = MAX_ATTEMPTS.get(j["phase"], 2)
            if j["attempts"] >= limit:
                if not fallback(state, jid, j):
                    return "stuck", jid
                continue
            todo.append((jid, j))
        if not todo:
            advance(state)
            continue
        wave = todo[: state["wave"]]
        ok = budget.fits(state, [j["model"] for _, j in wave])
        if ok == 0:
            return "budget", dict(state["budget"])
        wave = wave[:ok]
        for jid, j in wave:
            j["attempts"] += 1
            j["status"] = "dispatched"
            budget.charge(state, j["model"])
        state["waves"] += 1
        return "wave", wave
