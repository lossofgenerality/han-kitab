#!/usr/bin/env python3
"""Build the Han Kitab reader app (index.html) from the template and the texts in this repo.
Run from the repo root:  python3 tools/make_app.py
© Computational Classnotes · CC BY-NC-SA 4.0"""
import json, os, re, subprocess

OUT = "index.html"

def frag(md, opts=()):
    return subprocess.run(["pandoc", md, "-t", "html5", *opts], capture_output=True, text=True, check=True).stdout

def size(path):
    b = os.path.getsize(path)
    return f"{b / 1e6:.1f} MB" if b >= 1e6 else f"{b / 1e3:.0f} KB"

mason = frag("texts/ArabianProphet_Mason1921_v001.md", ["-f", "markdown-tex_math_dollars"])
mason = mason.replace('src="plates/', 'src="texts/plates/')
report = frag("docs/HanKitab_Research_v001.md", ["-f", "markdown"])
for s in (mason, report):
    assert "</template>" not in s

# Chinese facsimile: juan start pages (scan page numbers), found by reading the first column of each page
# (records/03_zh_juan_detection_ocr_v001.txt) and checked against the page images.
JUAN = [(1, "封面 Cover"), (2, "書名 Title"), (9, "年譜序 Preface"), (23, "重印序 Reprint preface"), (43, "卷目 Contents"),
        (51, "卷一 Juan 1"), (77, "卷二 Juan 2"), (97, "卷三 Juan 3"), (109, "卷四 Juan 4"), (123, "卷五 Juan 5"),
        (145, "卷六 Juan 6"), (163, "卷七 Juan 7"), (197, "卷八 Juan 8"), (231, "卷九 Juan 9"), (257, "卷十 Juan 10"),
        (295, "封底 Back cover")]
# Mason's chapters follow Liu Zhi's year-by-year order; this map opens the juan each chapter corresponds to (approximate).
MASON_MAP = {"top": 2, "list-of-illustrations": 2, "foreword": 9, "preface": 9, "concerning-the-chinese-author": 9,
             "chapter-i": 51, "chapter-ii": 109, "chapter-iii": 123, "chapter-iv": 145,
             "chapter-v": 163, "chapter-vi": 197, "chapter-vii": 231, "chapter-viii": 257}
npages = len([f for f in os.listdir("texts/zh_pages") if f.endswith(".png")])
FACS = {"dir": "texts/zh_pages", "pages": npages, "juan": [{"page": p, "label": l} for p, l in JUAN],
        "mason_map": MASON_MAP,
        "note": "Pages of the 1924 printing (prefaces and juan 1–10), unchanged. Mason condensed and selected, so the match with his chapters is by juan, not line by line."}

DL = [
    {"title": "The Arabian Prophet · clear-text edition v001",
     "desc": "Mason’s 1921 English translation of Liu Zhi, re-typeset with all twenty original illustrations. Edition © Computational Classnotes · CC BY-NC-SA 4.0; 1921 text public domain.",
     "files": [{"label": "PDF", "href": "texts/ArabianProphet_Mason1921_v001.pdf", "primary": True},
               {"label": "Markdown", "href": "texts/ArabianProphet_Mason1921_v001.md"}]},
    {"title": "天方至聖實錄 · facsimile v001",
     "desc": "Liu Zhi’s Chinese text, 1924 printing, prefaces and juan 1–10: the original pages unchanged, with a cover and copyright page added.",
     "files": [{"label": "PDF", "href": "texts/TianfangZhishengShilu_1924_facsimile_v001.pdf", "primary": True}]},
    {"title": "Han Kitab research report v001",
     "desc": "Publications, Chinese–English passages, glossary and a history of Sinification.",
     "files": [{"label": "PDF", "href": "docs/HanKitab_Research_v001.pdf", "primary": True},
               {"label": "Markdown", "href": "docs/HanKitab_Research_v001.md"}]},
    {"title": "Original scan · The Arabian Prophet (1921)",
     "desc": "Cornell University Library copy, digitized by the Internet Archive (cu31924024748232). Unchanged.",
     "files": [{"label": "Original PDF", "href": "originals/ArabianProphet_Mason1921_original_scan_cu31924024748232.pdf"}]},
    {"title": "Original scan · 天方至聖實錄 (1924)",
     "desc": "National Library of China copy, published on Wikimedia Commons (NLC416-13jh005373-59385). Unchanged.",
     "files": [{"label": "Original PDF", "href": "originals/TianfangZhishengShilu_1924_original_scan_NLC416-13jh005373-59385.pdf"}]},
]
for g in DL:
    for f in g["files"]:
        f["size"] = size(f["href"])

tpl = open("tools/app_template.html").read()
html = (tpl.replace("__MASON__", mason).replace("__REPORT__", report)
        .replace("__ZHDATA__", json.dumps({}, ensure_ascii=False))
        .replace("__FACSDATA__", json.dumps(FACS, ensure_ascii=False))
        .replace("__DLDATA__", json.dumps(DL, ensure_ascii=False))
        )
import hashlib
open(OUT, "w").write(html)
# service worker cache name follows the content, so installed copies update by themselves
h = hashlib.sha1(html.encode()).hexdigest()[:10]
sw = open("sw.js").read()
sw = re.sub(r"const VERSION = '[^']*';", f"const VERSION = 'hankitab-{h}';", sw)
open("sw.js", "w").write(sw)
print(OUT, len(html))
