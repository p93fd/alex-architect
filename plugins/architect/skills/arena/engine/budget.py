"""Лимит: учёт вызовов по моделям, потолок, расчёт плана до старта."""
import math

MODELS = ("sonnet", "opus", "haiku")


def empty_used():
    return {m: 0 for m in MODELS}


def total(used):
    return sum(used.values())


def fits(state, wave_models):
    """Сколько заданий из волны помещается в потолок. wave_models — список моделей по порядку."""
    b = state["budget"]
    used = dict(b["used"])
    ok = 0
    for m in wave_models:
        if b.get("cap_total") is not None and total(used) + 1 > b["cap_total"]:
            break
        if m == "opus" and b.get("cap_opus") is not None and used["opus"] + 1 > b["cap_opus"]:
            break
        used[m] += 1
        ok += 1
    return ok


def charge(state, model):
    state["budget"]["used"][model] += 1


def lane_sizes(n, bold_share):
    bold = 0
    if bold_share > 0 and n >= 4:
        bold = max(2, round(n * bold_share))
        bold = min(bold, n - 2)
    return n - bold, bold


def after_screen(size, batch=8):
    if size <= 4:
        return size, 0
    batches = math.ceil(size / batch)
    keep = 0
    rest = size
    for _ in range(batches):
        b = min(batch, rest)
        keep += math.ceil(b / 2)
        rest -= b
    return keep, batches


def plan(n, bold_share, scout=True, worker="sonnet", judge="opus"):
    """Минимальное число вызовов (без повторов) по моделям и раундам."""
    calls = {m: 0 for m in MODELS}
    lines = []
    if scout:
        calls[worker] += 2
        lines.append(f"разведка рынка: 2 ({worker})")
    calls[worker] += n
    lines.append(f"решения: {n} ({worker})")
    safe, bold = lane_sizes(n, bold_share)
    rounds_total = 0
    finalists = 0
    for name, size in (("надёжные", safe), ("смелые", bold)):
        if size == 0:
            continue
        keep, batches = after_screen(size)
        if batches:
            calls[judge] += batches
            lines.append(f"отсев {name}: {size} → {keep}, судей {batches} ({judge})")
        s = keep
        r = 0
        while s > 1:
            m = s // 2
            calls[worker] += 4 * m
            calls[judge] += m
            r += 1
            s = s - m
        rounds_total = max(rounds_total, r)
        lines.append(f"раунды {name}: {r}")
        finalists += 1
    finalists = 2
    calls[worker] += 5 + 2 * finalists + 2 * finalists  # панель, финмодель+аудит, стресс-атака+укрепление
    lines.append(f"панель покупателей 5, финмодель 2, ров и соответствие 2, стресс-тест 4 ({worker})")
    calls[judge] += 2
    lines.append(f"итоговый судья 1 и упаковка результата 1 ({judge})")
    return calls, rounds_total, lines
