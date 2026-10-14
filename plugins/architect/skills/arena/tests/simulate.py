#!/usr/bin/env python3
"""Прогон турнира без агентов: каждое задание «выполняется» заглушкой.

Проверяет всю механику: фазы, отсев, раунды, финал, стресс-тест, учёт лимита,
остановку по потолку, продолжение и повторы при пропавшем результате.

    python3 tests/simulate.py            # все сценарии
"""
import io
import json
import os
import random
import re
import shutil
import sys
import tempfile
from contextlib import redirect_stdout

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SKILL)

import arena  # noqa: E402
from engine import budget, state as st  # noqa: E402


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        arena.main(argv)
    return buf.getvalue()


def fake_output(prompt_path, out_paths, rng):
    text = open(prompt_path, encoding="utf-8").read()
    for o in out_paths:
        if o.endswith(".json"):
            if "отборочного" in text:
                ids = re.search(r"ровно эти id: (.+)\.", text).group(1).split(", ")
                rng.shuffle(ids)
                data = {"ranking": ids, "notes": {}}
            elif "судья матча" in text:
                a = re.search(r"Стратегия (a\d+)\n", text).group(1)
                b = re.findall(r"Стратегия (a\d+)\n", text)[1]
                data = {"winner": rng.choice([a, b]), "scores": {}, "reason": "тест"}
            elif "член панели" in text:
                data = {"persona": "x", "prefer": "X"}
            else:
                ids = re.findall(r"Финалист (a\d+)", text)
                data = {"ranking": ids, "ready": {}, "reason": "тест"}
            os.makedirs(os.path.dirname(o), exist_ok=True)
            json.dump(data, open(o, "w", encoding="utf-8"), ensure_ascii=False)
        else:
            os.makedirs(os.path.dirname(o), exist_ok=True)
            open(o, "w", encoding="utf-8").write("заглушка\n")


def drive(max_steps=2000, drop=0.0, seed=1):
    rng = random.Random(seed)
    waves = 0
    for _ in range(max_steps):
        out = run(["next"])
        if out.startswith("DONE"):
            return "DONE", waves, out
        if out.startswith("BUDGET STOP") or out.startswith("STUCK"):
            return out.split()[0] + (" " + out.split()[1] if out.startswith("BUDGET") else ""), waves, out
        waves += 1
        state = st.load()
        for line in out.splitlines():
            if line.startswith("JOB "):
                jid = line.split(" | ")[0][4:]
                j = state["jobs"][jid]
                if rng.random() < drop:
                    continue
                fake_output(j["prompt"], j["outs"], rng)
    raise AssertionError("турнир не закончился")


def scenario(n, bold, scout=True, cap_total=None, drop=0.0):
    tmp = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tmp)
    try:
        open("task.md", "w").write("Тестовая задача")
        open("dossier.md", "w").write("Тестовое досье")
        args = ["init", "--agents", str(n), "--bold", str(bold), "--seed", "7", "--task-file", "task.md", "--dossier-file", "dossier.md"]
        if not scout:
            args.append("--no-scout")
        if cap_total:
            args += ["--cap-total", str(cap_total)]
        run(args)
        res, waves, out = drive(drop=drop)
        state = st.load()
        bdir = os.path.join(state["dir"], "briefs")
        for name in os.listdir(bdir):
            body = open(os.path.join(bdir, name), encoding="utf-8").read()
            assert "{{" not in body, f"незаполненное поле в брифе {name}"
        used = budget.total(state["budget"]["used"])
        plan_calls, _, _ = budget.plan(n, bold, scout=scout)
        return res, used, sum(plan_calls.values()), state, out
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ok = True

    def check(name, cond, info=""):
        nonlocal ok
        print(("OK   " if cond else "FAIL ") + name + (f" — {info}" if info else ""))
        ok = ok and cond

    res, used, planned, state, _ = scenario(4, 0.25)
    check("4 агента, две дорожки: доходит до итога", res == "DONE", f"вызовов {used}, план {planned}")
    check("4 агента: вызовов ровно по плану", used == planned)
    check("4 агента: два финалиста из разных дорожек", len(state["finalists"]) == 2 and
          {state["agents"][f]["lane"] for f in state["finalists"]} == {"safe", "bold"})

    res, used, planned, state, _ = scenario(32, 0.25)
    check("32 агента: доходит до итога", res == "DONE", f"вызовов {used}, план {planned}")
    check("32 агента: вызовов ровно по плану", used == planned)
    u = state["budget"]["used"]
    check("32 агента: модели распределены", u["opus"] > 0 and u["sonnet"] > u["opus"], str(u))

    res, used, planned, state, _ = scenario(9, 0.0, scout=False)
    check("9 агентов, одна дорожка, без разведки: итог и финалист-соперник", res == "DONE" and len(state["finalists"]) == 2, f"вызовов {used}, план {planned}")
    check("9 агентов: вызовов по плану", used == planned)

    res, used, planned, state, out = scenario(32, 0.25, cap_total=40)
    check("потолок 40: турнир останавливается", res.startswith("BUDGET"), f"потрачено {used}")
    check("потолок 40: не превышен", used <= 40)

    res, used, planned, state, _ = scenario(16, 0.25, drop=0.15)
    check("сбои 15% заданий: турнир всё равно доходит до итога или честно стопорится", res in ("DONE", "STUCK"), f"{res}, вызовов {used}, план {planned}")

    # продолжение после стопа по лимиту
    tmp = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tmp)
    try:
        open("task.md", "w").write("т")
        open("dossier.md", "w").write("д")
        run(["init", "--agents", "8", "--seed", "3", "--task-file", "task.md", "--dossier-file", "dossier.md", "--cap-total", "15"])
        r1, _, _ = drive()
        run(["budget", "--cap-total", "1000"])
        r2, _, _ = drive()
        check("стоп по лимиту, подняли потолок, продолжили до итога", r1.startswith("BUDGET") and r2 == "DONE")
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)

    print("\nВСЁ РАБОТАЕТ" if ok else "\nЕСТЬ ОШИБКИ")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
