"""Состояние турнира: чтение и атомарная запись arena.json, пути, указатель на последний прогон."""
import json
import os
import time

ROOT = ".arena"
LATEST = os.path.join(ROOT, "LATEST")


def run_dir(state):
    return state["dir"]


def path(state, *parts):
    return os.path.join(state["dir"], *parts)


def new_run_id():
    return time.strftime("%Y%m%d-%H%M%S")


def save(state):
    p = os.path.join(state["dir"], "arena.json")
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


def load(run=None):
    if run is None:
        if not os.path.exists(LATEST):
            raise SystemExit("Нет активного турнира. Сначала: arena.py init ...")
        with open(LATEST, encoding="utf-8") as fh:
            run = fh.read().strip()
    p = os.path.join(ROOT, run, "arena.json")
    if not os.path.exists(p):
        raise SystemExit(f"Не найден прогон {run}")
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def set_latest(run_id):
    os.makedirs(ROOT, exist_ok=True)
    with open(LATEST, "w", encoding="utf-8") as fh:
        fh.write(run_id)


def read(p, default=""):
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def filled(p):
    """Файл есть и не пустой."""
    return os.path.exists(p) and os.path.getsize(p) > 0


def log(state, msg):
    state.setdefault("history", []).append(time.strftime("%H:%M:%S ") + msg)
