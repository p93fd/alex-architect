#!/usr/bin/env python3
"""Арена стратегий Александра. Вся бухгалтерия турнира идёт через этот файл.

Команды:
  plan    --agents N [--bold 0.25] [--no-scout]       сколько вызовов и на каких моделях
  init    --agents N --task-file F --dossier-file F    начать турнир
          [--bold 0.25] [--seed S] [--no-scout] [--wave 10]
          [--cap-total N] [--cap-opus N] [--worker sonnet] [--judge opus]
  next                                                 следующая волна заданий или итог
  status                                               где турнир, сколько потрачено
  budget  [--cap-total N] [--cap-opus N]               посмотреть или поднять потолок
  result                                               путь к итоговому документу
"""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import budget, deck, phases, state as st  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def cmd_plan(a):
    calls, rounds, lines = budget.plan(a.agents, a.bold, scout=not a.no_scout, worker=a.worker, judge=a.judge)
    safe, bold = budget.lane_sizes(a.agents, a.bold)
    print(f"Турнир: {a.agents} агентов (надёжных {safe}, смелых {bold}), раундов до {rounds} на дорожку.")
    for line in lines:
        print("  - " + line)
    tot = sum(calls.values())
    print("Вызовов минимум: " + str(tot) + " — " + ", ".join(f"{m} {c}" for m, c in calls.items() if c))
    print("Повторы при сбоях добавляют сверху, обычно 5–10%.")


def cmd_init(a):
    for f in (a.task_file, a.dossier_file):
        if not os.path.exists(f):
            raise SystemExit(f"Нет файла {f}")
    run_id = st.new_run_id()
    d = os.path.join(st.ROOT, run_id)
    os.makedirs(d, exist_ok=False)
    shutil.copy(a.task_file, os.path.join(d, "task.md"))
    shutil.copy(a.dossier_file, os.path.join(d, "dossier.md"))
    shutil.copy(os.path.join(HERE, "data", "rubric.md"), os.path.join(d, "rubric.md"))
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
    rng = deck.rng_for(seed)
    safe_n, bold_n = budget.lane_sizes(a.agents, a.bold)
    agents, lanes = {}, {}
    k = 0
    for lane, cnt in (("safe", safe_n), ("bold", bold_n)):
        ids = []
        for card in deck.deal(rng, cnt, lane) if cnt else []:
            k += 1
            aid = f"a{k:02d}"
            agents[aid] = {"lane": lane, "card": card, "alive": True, "sol": None}
            ids.append(aid)
        lanes[lane] = {"size": cnt, "alive": ids, "matches": [], "byes": []}
    state = {
        "id": run_id, "dir": d, "n": a.agents, "seed": seed, "wave": a.wave, "scout": not a.no_scout,
        "models": {"worker": a.worker, "judge": a.judge},
        "budget": {"cap_total": a.cap_total, "cap_opus": a.cap_opus, "used": budget.empty_used()},
        "agents": agents, "lanes": lanes, "jobs": {}, "round": 0, "waves": 0,
        "phase_key": None, "finalists": [], "history": [],
    }
    phases.enter(state, "scout" if state["scout"] else "spawn")
    st.save(state)
    st.set_latest(run_id)
    print(f"Турнир {run_id} создан: {a.agents} агентов (надёжных {safe_n}, смелых {bold_n}), seed {seed}.")
    cap = state["budget"]
    print(f"Потолок: всего {cap['cap_total'] or 'без потолка'}, opus {cap['cap_opus'] or 'без потолка'}.")
    print("Дальше: arena.py next")


def cmd_next(a):
    state = st.load(a.run)
    kind, data = phases.next_step(state)
    st.save(state)
    used = state["budget"]["used"]
    spent = f"потрачено: всего {budget.total(used)} (sonnet {used['sonnet']}, opus {used['opus']}, haiku {used['haiku']})"
    if kind == "wave":
        print(f"WAVE {state['waves']} · фаза {state['phase_key']} · раунд {state['round']} · заданий {len(data)} · {spent}")
        for jid, j in data:
            print(f"JOB {jid} | model={j['model']} | prompt={j['prompt']}")
        print("Запусти все задания волны одним сообщением (Agent, subagent_type general-purpose, model из строки,")
        print("prompt: «Прочитай <prompt> и выполни в точности. Это весь твой бриф.»). Дождись всех, потом: arena.py next")
    elif kind == "budget":
        print(f"BUDGET STOP · фаза {state['phase_key']} · {spent}")
        print(f"Потолок: всего {data['cap_total']}, opus {data['cap_opus']}. Состояние сохранено.")
        print("Продолжить: поднять потолок (arena.py budget --cap-total N) и снова arena.py next, хоть в другой день.")
    elif kind == "stuck":
        print(f"STUCK · задание {data} не дало валидного результата после всех попыток. Судью не заменяю сам.")
        print("Скажи пользователю и предложи: перезапустить задание или остановить турнир.")
    else:
        print(f"DONE · {spent}")
        print(f"Итог: {data}")
        print(f"Вердикт: {os.path.abspath(st.path(state, 'final', 'verdict.json'))}")


def cmd_status(a):
    state = st.load(a.run)
    used = state["budget"]["used"]
    print(f"Турнир {state['id']} · фаза {state['phase_key']} · раунд {state['round']} · волн {state['waves']}")
    for lane, L in state["lanes"].items():
        if L["size"]:
            print(f"  {lane}: осталось {len(L['alive'])} из {L['size']}")
    print(f"  потрачено: всего {budget.total(used)} · " + ", ".join(f"{m} {c}" for m, c in used.items()))
    print(f"  потолок: всего {state['budget']['cap_total']}, opus {state['budget']['cap_opus']}")
    for line in state["history"][-5:]:
        print("  " + line)


def cmd_budget(a):
    state = st.load(a.run)
    if a.cap_total is not None:
        state["budget"]["cap_total"] = a.cap_total
    if a.cap_opus is not None:
        state["budget"]["cap_opus"] = a.cap_opus
    st.save(state)
    cmd_status(a)


def cmd_result(a):
    state = st.load(a.run)
    print(os.path.abspath(st.path(state, "result.md")))


def main(argv=None):
    p = argparse.ArgumentParser(description="Арена стратегий")
    sub = p.add_subparsers(dest="cmd", required=True)

    def models(sp):
        sp.add_argument("--worker", default="sonnet", choices=budget.MODELS)
        sp.add_argument("--judge", default="opus", choices=budget.MODELS)

    sp = sub.add_parser("plan")
    sp.add_argument("--agents", type=int, default=32)
    sp.add_argument("--bold", type=float, default=0.25)
    sp.add_argument("--no-scout", action="store_true")
    models(sp)

    sp = sub.add_parser("init")
    sp.add_argument("--agents", type=int, default=32)
    sp.add_argument("--bold", type=float, default=0.25)
    sp.add_argument("--seed", type=int)
    sp.add_argument("--no-scout", action="store_true")
    sp.add_argument("--wave", type=int, default=10)
    sp.add_argument("--cap-total", type=int)
    sp.add_argument("--cap-opus", type=int)
    sp.add_argument("--task-file", required=True)
    sp.add_argument("--dossier-file", required=True)
    models(sp)

    for name in ("next", "status", "result"):
        s = sub.add_parser(name)
        s.add_argument("--run")
    s = sub.add_parser("budget")
    s.add_argument("--run")
    s.add_argument("--cap-total", type=int)
    s.add_argument("--cap-opus", type=int)

    a = p.parse_args(argv)
    {"plan": cmd_plan, "init": cmd_init, "next": cmd_next, "status": cmd_status,
     "budget": cmd_budget, "result": cmd_result}[a.cmd](a)


if __name__ == "__main__":
    main()
