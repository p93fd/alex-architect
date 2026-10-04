#!/usr/bin/env python3
"""Монтажёр: разговорное видео -> готовый вертикальный рилс.

Команды:
  words-from-segments seg.json words.json   фразы с таймкодами -> слова с таймкодами
  transcript words.json                     компактная расшифровка для чтения
  render plan.json                          полный монтаж по плану
  gen-insert kind out.mp4 [сек] [seed]      вставка без стоков: particles | sphere | network

Новое в плане: "cold_open": {"src": [с, по]} — сильный момент в начало;
"grade": "warm" | "none"; "speed": 1.06; "sfx": true; "titles": [{"text": "…", "src_t": 12.3, "dur": 2.2}].

words.json: [{"w": "слово", "s": 1.20, "e": 1.55}, ...]  (время исходника, сек)
seg.json:   [{"text": "фраза", "start": 1.2, "end": 3.4}, ...]
"""
import json, math, os, re, subprocess, sys, shutil
from statistics import median

FPS = 30
W, H = 1080, 1920
FILLERS = {"э", "ээ", "эээ", "эм", "ээм", "мм", "ммм", "хм", "а-а"}
FILLER_PHRASES = [["как", "бы"], ["так", "сказать"], ["типа"], ["короче"]]
VOWELS = set("аеёиоуыэюяaeiouy")


def run(cmd, quiet=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(" ".join(cmd) + "\n" + r.stderr[-3000:])
        raise SystemExit(1)
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
             "-of", "json", path])
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    return {"dur": float(d["format"]["duration"]), "w": v["width"] if v else 0, "h": v["height"] if v else 0}


def norm(w):
    return re.sub(r"[^\wё-]", "", w.lower())


def q(t):  # на сетку кадров
    return round(t * FPS) / FPS


# ---------- расшифровка ----------
def words_from_segments(seg_path, out_path):
    segs = json.load(open(seg_path, encoding="utf-8"))
    out = []
    for sg in segs:
        toks = sg["text"].split()
        if not toks:
            continue
        weights = [max(1, sum(c in VOWELS for c in t.lower())) + 0.3 for t in toks]
        total, t = sum(weights), float(sg["start"])
        span = float(sg["end"]) - t
        for tok, wt in zip(toks, weights):
            d = span * wt / total
            out.append({"w": tok, "s": round(t, 3), "e": round(t + d * 0.92, 3)})
            t += d
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"слов: {len(out)} -> {out_path}")


def print_transcript(words_path):
    words = json.load(open(words_path, encoding="utf-8"))
    line, start = [], None
    for i, w in enumerate(words):
        if start is None:
            start = w["s"]
        line.append(w["w"])
        gap = words[i + 1]["s"] - w["e"] if i + 1 < len(words) else 9
        if gap > 0.6 or len(line) >= 14 or re.search(r"[.!?]$", w["w"]):
            print(f"[{start:6.1f}] {' '.join(line)}" + (f"   (пауза {gap:.1f})" if 0.6 < gap < 9 else ""))
            line, start = [], None


# ---------- план нарезки ----------
def in_ranges(t, ranges):
    return any(a <= t <= b for a, b in ranges)


def pick_words(words, plan):
    keep = plan.get("keep") or [[0, 1e9]]
    cut = plan.get("cut") or []
    fillers = set(FILLERS) | {norm(x) for x in plan.get("extra_fillers", [])}
    kept = [w for w in words if in_ranges((w["s"] + w["e"]) / 2, keep) and not in_ranges((w["s"] + w["e"]) / 2, cut)]
    if plan.get("remove_fillers", True):
        n = [norm(w["w"]) for w in kept]
        drop = set(i for i, x in enumerate(n) if x in fillers)
        for ph in FILLER_PHRASES:
            L = len(ph)
            for i in range(len(n) - L + 1):
                if n[i:i + L] == ph:
                    drop.update(range(i, i + L))
        kept = [w for i, w in enumerate(kept) if i not in drop]
    return kept


def build_segments(kept, plan, src_dur):
    gap_keep = plan.get("max_gap", 0.18)   # сколько паузы оставить между словами
    pad = 0.07
    segs = []
    for w in kept:
        s, e = max(0, w["s"] - pad), min(src_dur, w["e"] + pad)
        if segs and s - segs[-1][1] <= gap_keep:
            segs[-1][1] = max(segs[-1][1], e)
        else:
            segs.append([s, e])
    out = []
    for s, e in segs:
        s, e = q(s), q(e)
        if e - s >= 2 / FPS:
            out.append([s, e])
    return out


def map_time(t, segs, offs):
    for (s, e), o in zip(segs, offs):
        if s - 0.02 <= t <= e + 0.02:
            return o + min(max(t - s, 0), e - s)
    # между сегментами -> к началу следующего
    for (s, e), o in zip(segs, offs):
        if t < s:
            return o
    return offs[-1] + (segs[-1][1] - segs[-1][0])


# ---------- кадр под лицо ----------
def face_track(src, info, step=0.5):
    import cv2
    cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(src)
    pts, t = [], 0.0
    while t < info["dur"]:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        if not ok:
            break
        sc = 480 / max(fr.shape[:2])
        sm = cv2.resize(fr, None, fx=sc, fy=sc)
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        f = cas.detectMultiScale(g, 1.15, 5, minSize=(int(40 * sc * 2), int(40 * sc * 2)))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2] * r[3])
            pts.append((t, (x + w / 2) / sm.shape[1], (y + h / 2) / sm.shape[0]))
        t += step
    cap.release()
    return pts


def seg_center(pts, s, e, default):
    xs = [p[1] for p in pts if s - 0.5 <= p[0] <= e + 0.5]
    ys = [p[2] for p in pts if s - 0.5 <= p[0] <= e + 0.5]
    return (median(xs), median(ys)) if xs else default


def crop_expr(info, cx, cy, zoom):
    sw, sh = info["w"], info["h"]
    if sw / sh > W / H:          # исходник шире 9:16
        ch = sh / zoom
        cw = ch * W / H
    else:
        cw = sw / zoom
        ch = cw * H / W
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    x = min(max(cx * sw - cw / 2, 0), sw - cw)
    y = min(max(cy * sh - ch * 0.42, 0), sh - ch)   # лицо чуть выше центра
    return f"crop={cw}:{ch}:{int(x)}:{int(y)},scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"


# ---------- субтитры ----------
def ass_color(hexc, alpha="00"):
    h = hexc.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def ass_time(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def clean_word(w):
    w = w.replace("{", "(").replace("}", ")")
    w = re.sub(r"[,.;:…]+$", "", w)
    return w.upper()


def make_ass(owords, plan, total, path):
    st = plan.get("style", {})
    font = st.get("font", "Noto Sans CJK JP Black")
    size = st.get("size", 82)
    accent = ass_color(st.get("accent", "#FFD400"))
    white = ass_color(st.get("color", "#FFFFFF"))
    marginv = st.get("margin_v", 560)
    maxw = st.get("words_per_chunk", 3)
    maxc = st.get("chars_per_chunk", 18)
    keys = {norm(k) for k in plan.get("highlight", [])}
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,{font},{size},{white},{white},&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,7,4,2,60,60,{marginv},1
Style: Hook,{font},{st.get('hook_size', 76)},{white},{white},&H30000000,&H30000000,-1,0,0,0,100,100,0,0,3,22,0,8,90,90,{st.get('hook_margin_v', 250)},1
Style: Title,{font},{st.get('title_size', 64)},{white},{white},&H20000000,&H20000000,-1,0,0,0,100,100,0,0,3,20,0,8,90,90,{st.get('title_margin_v', 330)},1
Style: Cta,{font},{st.get('cta_size', 70)},{white},{white},&H30000000,&H30000000,-1,0,0,0,100,100,0,0,3,22,0,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    # чанки
    chunks, cur = [], []
    for i, w in enumerate(owords):
        cur.append(w)
        nxt = owords[i + 1] if i + 1 < len(owords) else None
        chars = sum(len(x["w"]) + 1 for x in cur)
        brk = (nxt is None or len(cur) >= maxw or chars + len(nxt["w"]) > maxc
               or nxt["s"] - w["e"] > 0.3 or re.search(r"[.!?,:;—]$", w["w"]))
        if brk:
            chunks.append(cur)
            cur = []
    for ci, ch in enumerate(chunks):
        c_end = ch[-1]["e"] + 0.12
        if ci + 1 < len(chunks):
            nxt_s = chunks[ci + 1][0]["s"]
            c_end = nxt_s if nxt_s - c_end < 0.35 else c_end
        has_key = any(norm(w["w"]) in keys for w in ch)
        for i, w in enumerate(ch):
            s = w["s"] if i else ch[0]["s"]
            e = ch[i + 1]["s"] if i + 1 < len(ch) else c_end
            if e - s < 0.04:
                continue
            parts = []
            for j, x in enumerate(ch):
                t = clean_word(x["w"])
                if j == i:
                    parts.append(f"{{\\c{accent}\\fscx114\\fscy114\\t(0,110,\\fscx100\\fscy100)}}{t}{{\\c{white}\\fscx100\\fscy100}}")
                elif norm(x["w"]) in keys:
                    parts.append(f"{{\\c{accent}}}{t}{{\\c{white}}}")
                else:
                    parts.append(t)
            pre = ""
            if i == 0:
                z = 70 if has_key else 82
                pre = f"{{\\fscx{z}\\fscy{z}\\t(0,110,\\fscx100\\fscy100)}}"
            ev.append(f"Dialogue: 1,{ass_time(s)},{ass_time(e)},Sub,,0,0,0,,{pre}{' '.join(parts)}")
    hook = plan.get("hook")
    if hook:
        txt = hook["text"].replace("{", "(").replace("}", ")").replace("\n", "\\N")
        ev.append(f"Dialogue: 2,{ass_time(0)},{ass_time(hook.get('dur', 2.8))},Hook,,0,0,0,,"
                  f"{{\\fad(0,200)\\fscx92\\fscy92\\t(0,150,\\fscx100\\fscy100)}}{txt.upper() if hook.get('upper', True) else txt}")
    for tt in plan.get("_titles", []):
        txt = tt["text"].replace("{", "(").replace("}", ")").replace("\n", "\\N")
        ev.append(f"Dialogue: 3,{ass_time(tt['t'])},{ass_time(tt['t'] + tt['dur'])},Title,,0,0,0,,"
                  f"{{\\fad(120,160)\\fscx90\\fscy90\\t(0,140,\\fscx100\\fscy100)}}{txt.upper()}")
    cta = plan.get("cta")
    if cta:
        d = cta.get("dur", 3)
        txt = cta["text"].replace("\n", "\\N")
        ev.append(f"Dialogue: 2,{ass_time(total - d)},{ass_time(total)},Cta,,0,0,0,,{{\\fad(200,0)}}{txt.upper()}")
    open(path, "w", encoding="utf-8").write(hdr + "\n".join(ev) + "\n")



GRADES = {
    "warm": ",eq=contrast=1.06:saturation=1.12:gamma=1.02,colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.04:bm=-0.04:rh=0.02:bh=-0.02",
    "none": "",
}


def add_sfx(base, work, whoosh_t, pop_t, vol):
    """Подмешивает синтезированные звуки в дорожку: свист на переходах, щелчок на плашках."""
    whoosh_t = [t for t in whoosh_t if t is not None and t >= 0]
    pop_t = [t for t in pop_t if t is not None and t >= 0]
    if not whoosh_t and not pop_t:
        return base
    wh, pp = os.path.join(work, "whoosh.wav"), os.path.join(work, "pop.wav")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=d=0.5:c=pink:a=0.8:r=48000",
         "-af", "bandpass=f=1400:w=1100,afade=t=in:d=0.3:curve=exp,afade=t=out:st=0.32:d=0.18,volume=1.6", "-ac", "2", wh])
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "sine=f=620:d=0.09:r=48000",
         "-af", "afade=t=in:d=0.004,afade=t=out:st=0.02:d=0.07,volume=0.9", "-ac", "2", pp])
    cmd, fc, labs = ["ffmpeg", "-y", "-i", base], [], []
    k = 1
    for t in whoosh_t:
        cmd += ["-i", wh]
        fc.append(f"[{k}:a]adelay={int(max(0, t - 0.28) * 1000)}:all=1,volume={vol}[s{k}]")
        labs.append(f"[s{k}]"); k += 1
    for t in pop_t:
        cmd += ["-i", pp]
        fc.append(f"[{k}:a]adelay={int(t * 1000)}:all=1,volume={vol * 0.8}[s{k}]")
        labs.append(f"[s{k}]"); k += 1
    fc.append(f"[0:a]{''.join(labs)}amix=inputs={len(labs) + 1}:duration=first:normalize=0[a]")
    out = os.path.join(work, "base_sfx.mkv")
    run(cmd + ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "pcm_s16le", out])
    return out


def gen_insert(kind, out, dur=3.0, seed=7):
    """Вставка без стоков: particles (частицы), sphere (сфера из точек), network (сеть связей)."""
    import numpy as np, cv2
    rng = np.random.default_rng(seed)
    n = int(dur * FPS)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    bg = np.zeros((H, W, 3), np.float32)
    bg[..., 0] = 26 - 14 * yy
    bg[..., 1] = 14 - 6 * yy
    bg[..., 2] = 10 + 10 * yy
    amber, cream = (60, 170, 255), (190, 225, 255)
    p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if kind == "sphere":
        m = 1100
        i = np.arange(m) + 0.5
        phi, th = np.arccos(1 - 2 * i / m), np.pi * (1 + 5 ** 0.5) * i
        P = np.stack([np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)], 1)
    else:
        m = 170 if kind == "particles" else 70
        P = rng.uniform(-1, 1, (m, 3)).astype(np.float32)
        V = rng.normal(0, 0.0016, (m, 3)).astype(np.float32)
    for f in range(n):
        a = f / max(1, n - 1)
        img = np.zeros((H, W, 3), np.uint8)
        if kind == "sphere":
            ry, rx = a * 1.5 + 0.4, 0.35
            R = np.array([[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]]) @ \
                np.array([[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]])
            Q = P @ R.T
            rad = 380 * (0.92 + 0.08 * a)
            for x, y, z in Q:
                d = (z + 1) / 2
                cv2.circle(img, (int(W / 2 + x * rad), int(H * 0.44 + y * rad)), 2 + int(4 * d),
                           tuple(int(c * (0.25 + 0.75 * d)) for c in amber), -1, cv2.LINE_AA)
        else:
            Q = P + V * f
            Q[:, 2] = ((Q[:, 2] + 1 + f * 0.004) % 2) - 1
            pts = []
            for x, y, z in Q:
                d = (z + 1) / 2
                px, py = int(W / 2 + x * W * 0.62 * (0.6 + 0.6 * d)), int(H / 2 + y * H * 0.55 * (0.6 + 0.6 * d))
                pts.append((px, py, d))
            if kind == "network":
                for i1 in range(len(pts)):
                    for i2 in range(i1 + 1, len(pts)):
                        dx, dy = pts[i1][0] - pts[i2][0], pts[i1][1] - pts[i2][1]
                        dist = (dx * dx + dy * dy) ** 0.5
                        if dist < 250:
                            k = (1 - dist / 250) * 0.6
                            cv2.line(img, pts[i1][:2], pts[i2][:2], tuple(int(c * k) for c in cream), 1, cv2.LINE_AA)
            for px, py, d in pts:
                col = amber if (px + py) % 3 else cream
                cv2.circle(img, (px, py), 3 + int(9 * d * d), tuple(int(c * (0.3 + 0.7 * d)) for c in col), -1, cv2.LINE_AA)
        glow = cv2.GaussianBlur(img, (0, 0), 14)
        fr = np.clip(bg + img.astype(np.float32) + glow.astype(np.float32) * 1.3, 0, 255).astype(np.uint8)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    print(out)

# ---------- рендер ----------
def render(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    base_dir = os.path.dirname(os.path.abspath(plan_path))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base_dir, p)
    src = P(plan["source"])
    work = P(plan.get("work", "work"))
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    info = probe(src)
    words = json.load(open(P(plan["words"]), encoding="utf-8"))
    kept = pick_words(words, plan)
    segs = build_segments(kept, plan, info["dur"])
    if not segs:
        raise SystemExit("нечего монтировать: пустой список слов")

    # кадрирование
    pts = face_track(src, info) if plan.get("face_track", True) else []
    gx = median([p[1] for p in pts]) if pts else 0.5
    gy = median([p[2] for p in pts]) if pts else 0.4
    zin = plan.get("punch_zoom", 1.12)
    base_zoom = plan.get("base_zoom", 1.0)
    every = plan.get("zoom_every", 3.5)
    punch_src = plan.get("punch_at", [])  # моменты исходника, где нужен резкий зум

    grade = GRADES.get(plan.get("grade", "warm"), "")
    cold = plan.get("cold_open")
    timeline = []
    if cold:
        timeline.append([q(float(cold["src"][0])), q(float(cold["src"][1])), "cold"])
    timeline += [[s, e, "main"] for s, e in segs]
    n_cold = 1 if cold else 0
    files, offs, t_out, since, zoomed = [], [], 0.0, 0.0, False
    for i, (s, e, kind) in enumerate(timeline):
        dur = round((e - s) * FPS) / FPS
        if since >= every:
            zoomed, since = not zoomed, 0.0
        z = zin if zoomed else base_zoom
        if kind == "cold" or any(s <= p <= e for p in punch_src):
            z = max(z, zin + 0.08)
        cx, cy = seg_center(pts, s, e, (gx, gy))
        vf = crop_expr(info, cx, cy, z) + grade
        f = os.path.join(work, f"seg{i:04d}.mkv")
        run(["ffmpeg", "-y", "-ss", f"{s:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vf", vf,
             "-af", f"aresample=48000,apad,atrim=0:{dur:.3f},afade=t=in:d=0.015,afade=t=out:st={max(0, dur - 0.02):.3f}:d=0.02",
             "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
             "-c:a", "pcm_s16le", "-ac", "2", f])
        files.append(f)
        offs.append(t_out)
        t_out += dur
        since += dur
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    base = os.path.join(work, "base.mkv")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])
    total = probe(base)["dur"]
    main_offs = offs[n_cold:]
    cold_end = main_offs[0] if cold and main_offs else 0.0

    # слова в новом времени
    owords = []
    if cold:
        cs, ce = timeline[0][0], timeline[0][1]
        for w in words:
            m = (w["s"] + w["e"]) / 2
            if cs <= m <= ce and norm(w["w"]) not in FILLERS:
                s2 = max(0.0, w["s"] - cs)
                owords.append({"w": w["w"], "s": s2, "e": max(min(ce - cs, w["e"] - cs), s2 + 0.06)})
    for w in kept:
        s, e = map_time(w["s"], segs, main_offs), map_time(w["e"], segs, main_offs)
        owords.append({"w": w["w"], "s": s, "e": max(e, s + 0.06)})
    json.dump(owords, open(os.path.join(work, "words_out.json"), "w", encoding="utf-8"), ensure_ascii=False)
    plan["_titles"] = [{"text": t["text"], "dur": t.get("dur", 2.2),
                        "t": t["t"] if "t" in t else map_time(t["src_t"], segs, main_offs)} for t in plan.get("titles", [])]
    ass = os.path.join(work, "subs.ass")
    make_ass(owords, plan, total, ass)

    # звуки: мягкий свист на переходах и вставках, щелчок на плашках
    if plan.get("sfx", True):
        ins_t = [i["t"] if "t" in i else map_time(i["src_t"], segs, main_offs) for i in plan.get("inserts", [])]
        whoosh_t = ([cold_end] if cold else []) + ins_t
        pop_t = [t["t"] for t in plan["_titles"]]
        base = add_sfx(base, work, whoosh_t, pop_t, plan.get("sfx_vol", 0.5))

    # вставки + музыка + субтитры
    cmd = ["ffmpeg", "-y", "-i", base]
    fc, vlast, n = [], "[0:v]", 1
    for k, ins in enumerate(plan.get("inserts", [])):
        t0 = ins["t"] if "t" in ins else map_time(ins["src_t"], segs, main_offs)
        d = ins.get("dur", 2.5)
        d = min(d, total - t0)
        if d <= 0.3:
            continue
        f = P(ins["file"])
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            cmd += ["-loop", "1", "-t", f"{d + 0.5:.2f}", "-i", f]
            frames = int(d * FPS) + 15
            src_chain = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
                         f"zoompan=z='min(zoom+0.0009,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}")
        else:
            cmd += ["-stream_loop", "-1", "-t", f"{d + 0.5:.2f}", "-i", f]
            src_chain = f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        mode = ins.get("mode", "fill")
        lab = f"i{k}"
        common = (f"trim=0:{d:.3f},setpts=PTS-STARTPTS+{t0:.3f}/TB,format=yuva420p,"
                  f"fade=t=in:st={t0:.3f}:d=0.12:alpha=1,fade=t=out:st={t0 + d - 0.12:.3f}:d=0.12:alpha=1")
        if mode == "cinema" and not f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            fc.append(f"[{n}:v]fps={FPS},split[{lab}a][{lab}b]")
            fc.append(f"[{lab}a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:2,eq=brightness=-0.18[{lab}bg]")
            fc.append(f"[{lab}b]scale={W}:-2,setsar=1[{lab}fg]")
            fc.append(f"[{lab}bg][{lab}fg]overlay=(W-w)/2:(H-h)/2,{common}[{lab}]")
        else:
            fc.append(f"[{n}:v]{src_chain},setsar=1,{common}[{lab}]")
        fc.append(f"{vlast}[{lab}]overlay=eof_action=pass:enable='between(t,{t0:.3f},{t0 + d:.3f})'[v{k}]")
        vlast = f"[v{k}]"
        n += 1
    fc.append(f"{vlast}ass={ass}[vout]")

    mus = plan.get("music")
    if mus:
        cmd += ["-stream_loop", "-1", "-i", P(mus["file"])]
        vol = mus.get("vol", 0.18)
        fc.append(f"[0:a]asplit[va][vs]")
        fc.append(f"[{n}:a]aresample=48000,volume={vol},atrim=0:{total:.3f},afade=t=in:d=0.8,"
                  f"afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[m]")
        fc.append("[m][vs]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=400[md]")
        fc.append("[va][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    else:
        fc.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[aout]")

    out = P(plan.get("out", "reel.mp4"))
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
    run(cmd)
    sp = float(plan.get("speed", 1.06))
    if abs(sp - 1.0) > 0.005:
        fast = out.rsplit(".", 1)[0] + "_sp.mp4"
        run(["ffmpeg", "-y", "-i", out, "-filter_complex", f"[0:v]setpts=PTS/{sp}[v];[0:a]atempo={sp}[a]",
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", fast])
        os.replace(fast, out)
        total = probe(out)["dur"]
    tg = out.rsplit(".", 1)[0] + "_tg.mp4"
    if os.path.getsize(out) <= 45 * 1024 * 1024:
        shutil.copyfile(out, tg)
    else:
        kb = int(min(6000, 45 * 8 * 1024 / total - 160))
        run(["ffmpeg", "-y", "-i", out, "-c:v", "libx264", "-preset", "medium", "-b:v", f"{kb}k", "-maxrate", f"{kb}k",
             "-bufsize", f"{kb * 2}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", tg])

    # обложка и лист кадров для проверки
    run(["ffmpeg", "-y", "-ss", "0.6", "-i", out, "-frames:v", "1", "-q:v", "2", out.rsplit(".", 1)[0] + "_cover.jpg"])
    step = max(total / 18, 0.5)
    sheet = out.rsplit(".", 1)[0] + "_check.jpg"
    run(["ffmpeg", "-y", "-i", out, "-vf", f"fps=1/{step:.3f},scale=216:384,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=6x3",
         "-frames:v", "1", sheet])
    lufs = run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", lufs)
    print(json.dumps({
        "out": out, "sheet": sheet, "src_sec": round(info["dur"], 1), "out_sec": round(total, 1),
        "cuts": len(segs), "mb": round(os.path.getsize(out) / 1048576, 1), "tg_mb": round(os.path.getsize(tg) / 1048576, 1), "removed_sec": round(info["dur"] - total, 1),
        "words_dropped": len(words) - len(kept), "face_points": len(pts), "lufs": m[-1] if m else None,
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "words-from-segments":
        words_from_segments(a[1], a[2])
    elif a[0] == "transcript":
        print_transcript(a[1])
    elif a[0] == "render":
        render(a[1])
    elif a[0] == "gen-insert":
        gen_insert(a[1], a[2], float(a[3]) if len(a) > 3 else 3.0, int(a[4]) if len(a) > 4 else 7)
    else:
        print(__doc__)