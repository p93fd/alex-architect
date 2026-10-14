"""Колода карт стратегии: линза × метод × позиция. У каждого агента своя карта без повторов."""
import itertools
import json
import math
import os
import random

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(HERE, "data", "cards.json")
PERSONAS = os.path.join(HERE, "data", "personas.json")


def load_cards():
    with open(CARDS, encoding="utf-8") as fh:
        return json.load(fh)


def load_personas():
    with open(PERSONAS, encoding="utf-8") as fh:
        return json.load(fh)


def deal(rng, count, lane):
    """Раздать count карт дорожке lane ('safe' или 'bold').

    Линзы распределяются равномерно: ни одна линза не достаётся больше чем
    ceil(count / число линз) агентам, чтобы турнир не схлопнулся в одну мысль.
    """
    d = load_cards()
    stances = d["safe_stances"] if lane == "safe" else d["bold_stances"]
    combos = list(itertools.product(range(len(d["lenses"])), range(len(d["methods"])), range(len(stances))))
    if count > len(combos):
        raise SystemExit(f"Карт не хватает: нужно {count}, есть {len(combos)}")
    rng.shuffle(combos)
    per_lens = math.ceil(count / len(d["lenses"]))
    lens_used, method_used, picked = {}, {}, []
    for strict in (True, False):
        for c in combos:
            if len(picked) == count:
                break
            if c in picked:
                continue
            if strict and (lens_used.get(c[0], 0) >= per_lens or method_used.get(c[1], 0) >= math.ceil(count / len(d["methods"]))):
                continue
            picked.append(c)
            lens_used[c[0]] = lens_used.get(c[0], 0) + 1
            method_used[c[1]] = method_used.get(c[1], 0) + 1
    return [{"lens": d["lenses"][li], "method": d["methods"][mi], "stance": stances[si]} for li, mi, si in picked]


def rng_for(seed):
    return random.Random(seed)
