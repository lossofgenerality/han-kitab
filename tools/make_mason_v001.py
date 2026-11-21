#!/usr/bin/env python3
"""Rebuild Mason, The Arabian Prophet (1921) as clean Markdown with the original plates.
Input: src.pdf (Internet Archive scan cu31924024748232). Output: ArabianProphet_Mason1921_v001.md
© Computational Classnotes · CC BY-NC-SA 4.0 (this edition's processing; the 1921 text is public domain)
"""
import re, subprocess

SRC = "src.pdf"
NPAGES = 368

PLATES = {
    6:   ("Mosque and Minaret at Canton (the “Pagoda-without-ornament” mosque)", "Frontispiece"),
    19:  ("Facsimile of the Chinese title-page: 至聖實錄, “The True Annals of the Prophet”", "Facing p. ix"),
    31:  ("Map of Arabia in the time of the Prophet", "Facing p. 2"),
    67:  ("Mecca and the Kaaba", "p. 68"),
    100: ("The Black Stone at Mecca", "p. 83"),
    115: ("Page from a Moslem ritual, in Chinese and Arabic", "p. 84"),
    116: ("Part of the First Chapter of the Koran, with Chinese translation and transliteration", "Facing p. 114"),
    147: ("An Imam preaching in a Mosque", "p. 136"),
    171: ("Medina", "p. 146"),
    183: ("The Mihrab, or prayer-niche, of a Shanghai Mosque", "p. 171"),
    210: ("Ancient Moslem Grave-yard at Canton", "p. 218"),
    259: ("Interior of a Tientsin Mosque", "p. 240"),
    283: ("Plan of Mecca and the Kaaba", "p. 259"),
    303: ("The Kalima, etc.", "p. 260"),
    304: ("Parting Injunctions of the Prophet", "Facing p. 268"),
    313: ("Training School for Ahungs (Shanghai); Tomb of a Moslem Pioneer at Canton", "pp. 268, 276"),
    323: ("A Ming Dynasty Monument", "p. 277"),
    324: ("A Monument at Sianfu, Shensi, recording the building of a mosque", "p. 302"),
    351: ("Chinese Mohammedan Paraphernalia", "p. 302"),
}
PLATE_ONLY = set(PLATES) - {100}
BLANK = {1, 2, 3, 4, 5, 7, 8, 10, 20, 27, 28, 32, 68, 148, 172, 184, 209, 260, 284, 314, 352} | set(range(365, NPAGES + 1))
LINES_MODE = {7, 14, 23, 24, 25, 26, 364} | set(range(357, 364))

def page_text(p):
    return subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), SRC, "-"],
                          capture_output=True, text=True).stdout

FIX = [
    (r"\btlie\b", "the"), (r"\bTlie\b", "The"), (r"\btliis\b", "this"), (r"\bliis\b", "his"),
    (r"\bthfe\b", "the"), (r"\bwliich\b", "which"), (r"\bwlio\b", "who"), (r"\btliat\b", "that"),
    (r"\bTHB\b", "THE"), (r"■", ""), (r"\s+([,.;:!?])", r"\1"), (r"([,.;:])\s*[\-'’`]+(\s|$)", r"\1\2"),
    (r"(?<=\w)\^+|\^+(?=\w)", "[?]"), (r"\^+(\s*\^+)*", "[Chinese]"), (r" {2,}", " "),
]

def clean(s):
    for a, b in FIX:
        s = re.sub(a, b, s)
    s = s.replace("*", r"\*").replace("_", r"\_")
    return s.strip()

ROMAN = re.compile(r"^[ivxlcy]+$", re.I)
CHAP = re.compile(r"^\s*(CHAPTER|APPENDIX)\s+([IVXLnlH\]1]+)(\s.*)?$")
NOTE = re.compile(r"^\s{2,10}(\d{1,2}|[Il])\s?[.,]\s+\S")

def is_header(line):
    s = line.strip()
    if not s:
        return False
    toks = s.split()
    caps = re.sub(r"[^A-Za-z ]", "", " ".join(t for t in toks if not ROMAN.match(t) and not re.search(r"\d", t)))
    if len(caps) and caps.upper() == caps and (re.match(r"^\S{1,4}$", toks[0]) or re.match(r"^\S{1,4}$", toks[-1])):
        return True
    if caps.upper() == caps and len(s) < 60 and ("ARABIAN" in s or "APPENDIX" in s or "MOHAMMEDANISM" in s):
        return True
    return False

def header_pageno(line):
    toks = line.strip().split()
    for t in (toks[0], toks[-1]):
        d = re.sub(r"[^0-9]", "", t.replace("o", "0").replace("O", "0").replace("l", "1").replace("I", "1"))
        if d and len(d) <= 3:
            return int(d)
    return None

out = []
para = []
pending = []   # notes / plates to emit after the paragraph closes

def flush_para():
    global para
    if para:
        txt = ""
        for ln in para:
            if txt.endswith("-") and ln[:1].islower():
                txt = txt[:-1] + ln
            elif txt:
                txt += " " + ln
            else:
                txt = ln
        out.append(clean(txt) + "\n")
        para = []
    while pending:
        out.append(pending.pop(0))

def plate_md(p):
    cap, loc = PLATES[p]
    return f'<figure class="plate"><img src="plates/plate_{p:03d}.jpg" alt="{cap}"><figcaption>{cap} <span class="loc">(original {loc})</span></figcaption></figure>\n'

last_no = 0
for p in range(1, NPAGES + 1):
    if p in BLANK:
        continue
    if p in PLATE_ONLY:
        pending.append(plate_md(p))
        continue
    raw = page_text(p).splitlines()
    lines = [l.rstrip() for l in raw]
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        continue

    if p == 9:  # dedication only
        flush_para()
        out.append('<div class="dedication">To my Wife<br>who has bravely shared many years of pioneer missionary service with me<br>in West China</div>\n')
        continue

    if p in LINES_MODE:
        flush_para()
        block = []
        for l in lines:
            s = clean(l)
            if not s:
                continue
            if p >= 357 and block and (s[:1].islower() or s[:1].isdigit()) and not re.match(r"^[A-Z]$", s):
                block[-1] += " " + s
            else:
                block.append(s)
        cls = "index" if 357 <= p <= 363 else "lines"
        if p == 357:
            out.append("## Index\n")
            block = [b for b in block if b.upper() != "INDEX"]
        elif p > 357:
            block = [b for b in block if b.upper() != "INDEX" and not re.match(r"^\d{3}$", b)]
        out.append(f'<div class="{cls}">\n' + "<br>\n".join(block) + "\n</div>\n")
        continue

    # running header
    first = lines[0]
    pno = None
    if is_header(first) and not CHAP.match(first):
        pno = header_pageno(first)
        lines = lines[1:]
    if p == 100:
        # drop the vertical caption of the Black Stone plate
        lines = [l for l in lines if len(l.strip()) > 2]
    if pno is None or not (0 < pno - last_no <= 4):
        pno = last_no + 1 if p >= 29 else None
    if p >= 29:
        last_no = pno

    # split body / notes
    body, notes = lines, []
    for i, l in enumerate(lines):
        if i > 3 and NOTE.match(l):
            body, notes = lines[:i], lines[i:]
            break

    body = [l for l in body if not re.match(r"^\s*([ivxlc]{1,5}|\d{1,3})\s*$", l, re.I)]
    ind = [len(l) - len(l.lstrip()) for l in body if l.strip()]
    base = min(ind) if ind else 0
    if ind:
        from collections import Counter
        base = Counter(ind).most_common(1)[0][0]
    # page marker
    if pno:
        mark = f'<span class="pg">[p. {pno}]</span>'
    else:
        mark = ""
    started = False
    in_summary = False
    for l in body:
        if not l.strip():
            if in_summary:
                in_summary = False
                flush_para()
            continue
        m = CHAP.match(l)
        if m:
            flush_para()
            kind = m.group(1).title()
            num = m.group(2).replace("n", "II").replace("H", "II").replace("]", "I").replace("l", "I").replace("1", "I")
            if num == "IIII": num = "III"
            out.append(f"## {kind} {num}\n")
            in_summary = (kind == "Chapter")
            if in_summary:
                para.append("")  # summary paragraph
            continue
        s = l.strip()
        s = re.sub(r"^[ivxl]{1,4}\s{2,}(?=[A-Z\"'])", "", s)
        if s in ("THE ARABIAN PROPHET", "THE ARABIAN  PROPHET") and not started:
            continue
        if re.sub(r"\s+", " ", s) in ("FOREWORD", "PREFACE", "CONCERNING THE CHINESE AUTHOR"):
            s = re.sub(r"\s+", " ", s)
            flush_para()
            out.append(f"## {s.title()}\n")
            continue
        indent = len(l) - len(l.lstrip())
        if in_summary:
            para.append(s)
            continue
        prev_hy = bool(para) and para[-1].endswith("-")
        if indent >= base + 3 and para and not prev_hy and not s[:1].islower():
            flush_para()
        if not started and mark:
            s = mark + " " + s if not para else s
            if para:
                para[-1] += " " + mark
            started = True
        para.append(s)
    if not started and mark:
        para.append(mark)

    if notes:
        nl = []
        for l in notes:
            s = l.strip()
            if not s:
                continue
            if NOTE.match(l) or not nl:
                nl.append(s)
            else:
                if nl[-1].endswith("-") and s[:1].islower():
                    nl[-1] = nl[-1][:-1] + s
                else:
                    nl[-1] += " " + s
        pending.append('<div class="notes">' + "<br>\n".join(clean(n) for n in nl) + f' <span class="loc">(notes to p. {pno})</span></div>\n')
    if p == 100:
        pending.append(plate_md(100))

flush_para()

# fix summary paragraphs: italicise first paragraph right after a chapter heading
md = "\n".join(out)
md = re.sub(r"(## Chapter [IVXL]+\n\n)\s*([^\n<#][^\n]*)", lambda m: m.group(1) + "*" + m.group(2).strip() + "*", md)

illus = "\n".join(f"| {PLATES[p][0]} | {PLATES[p][1]} |" for p in sorted(PLATES))
front = f"""---
title: "The Arabian Prophet: A Life of Mohammed from Chinese and Arabic Sources"
---

<div class="titlepage">
<h1>The Arabian Prophet</h1>
<p class="sub">A Life of Mohammed from Chinese and Arabic Sources<br>A Chinese-Moslem Work</p>
<p>by <b>Liu Chai-lien</b> (Liu Zhi 劉智, Liu Jielian 劉介廉, c. 1660–c. 1730)<br>
Translation of <i>Tianfang zhisheng shilu</i> 天方至聖實錄 (completed 1724)</p>
<p>Translated by <b>Isaac Mason</b><br>of Friends' Foreign Mission Association, and Christian Literature Society for China;
Honorary Secretary, Royal Asiatic Society, North-China Branch</p>
<p>With Appendices on Chinese Mohammedanism<br>Foreword by Rev. Samuel M. Zwemer, F.R.G.S., of Cairo</p>
<p>Shanghai: Commercial Press, 1921</p>
</div>

<div class="ednote">

**About this edition (v001).** A clear-text re-setting of the 1921 edition, made from the Cornell University Library copy digitized by the Internet Archive (archive.org/details/cu31924024748232). The text was taken from the scan's OCR layer, with running heads removed, paragraphs re-joined, line-end hyphens removed and common OCR errors corrected. All twenty original illustrations are reproduced from the scan at their places in the book. Mason's footnotes are printed in smaller type after the paragraph where they fall, marked with the page they belong to. Original page numbers appear in the margin as [p. N] so that references to the 1921 edition still work.

*Limits:* the OCR could not read the Chinese characters that Mason quotes in the text and notes. Where a run of them was detected it is marked **[Chinese]**, and an unreadable character inside a word is marked **[?]**; some other places may still carry stray symbols. Check any Chinese terms, and any sentence that looks wrong, against the scan. Not every line has been proofread by hand.

The 1921 text is in the public domain. Edition and processing © Computational Classnotes · CC BY-NC-SA 4.0.

</div>

## List of Illustrations

| Illustration | Position in the 1921 edition |
|---|---|
{illus}

"""
md = front + md + "\n\n---\n\n*Edition v001 · prepared 2026 · © Computational Classnotes · CC BY-NC-SA 4.0 (1921 text public domain)*\n"
open("ArabianProphet_Mason1921_v001.md", "w").write(md)
print(len(md))
