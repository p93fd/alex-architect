#!/usr/bin/env python3
"""Выжимка чата для архива: из файла сессии Claude Code (.jsonl) оставляет только живой разговор.

Выкидывает выводы инструментов, код, служебные напоминания и ответы агентов.
Результат — markdown, который потом сжимается до решений и кладётся в архив в Notion.

    python3 -I archive.py <сессия.jsonl> [выход.md]
"""
import json
import re
import sys

NOISE = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
    return ""


def turns(path):
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("isSidechain"):
            continue
        m = e.get("message") or {}
        role = m.get("role")
        if role not in ("user", "assistant"):
            continue
        t = NOISE.sub("", text_of(m.get("content"))).strip()
        if not t or t.startswith("[Request interrupted"):
            continue
        yield role, e.get("timestamp", "")[:16].replace("T", " "), t


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    lines = []
    for role, ts, t in turns(src):
        who = "Александр" if role == "user" else "Claude"
        lines.append(f"### {who} · {ts}\n{t}\n")
    md = "\n".join(lines)
    if out:
        open(out, "w", encoding="utf-8").write(md)
    print(f"символов в разговоре: {len(md)}")


if __name__ == "__main__":
    main()
