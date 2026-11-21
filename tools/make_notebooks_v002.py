#!/usr/bin/env python3
"""Write the Han Kitab Wolfram notebooks (plain Notebook[] expressions, ASCII-escaped) into wolfram/.
  HanKitabKernel_v002.nb          deploy + test HanKitabKernel
  HanKitabOperationsLog_v002.nb   (T) rewrites u x v -> u y v and (DO) runs with indexed iterations
  HanKitabDevelopmentLog_v002.nb  how the work was built: trials, results, fixes, glossary
  HanKitabScripts_v002.nb         every script and the app template, one cell each
Run from the repo root: python3 tools/make_notebooks_v002.py
© Computational Classnotes · CC BY-NC-SA 4.0"""
import glob, os

def esc(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == "\\": out.append("\\\\")
        elif ch == '"': out.append('\\"')
        elif ch == "\n": out.append("\\n")
        elif ch == "\t": out.append("    ")
        elif o < 32: continue
        elif o < 128: out.append(ch)
        elif o <= 0xFFFF: out.append("\\:%04x" % o)
        else: out.append("\\|%06x" % o)
    return "".join(out)

def cell(text, style): return 'Cell["%s", "%s"]' % (esc(text), style)
COPY = "© Computational Classnotes · CC BY-NC-SA 4.0"

def notebook(path, cells):
    body = ",\n".join(cells + [cell(COPY, "Text")])
    open(path, "w", encoding="ascii").write(
        "(* Content-type: application/vnd.wolfram.mathematica *)\n(* " + esc(COPY) + " *)\n"
        "Notebook[{\n" + body + "\n}, WindowTitle -> \"" + esc(os.path.basename(path)) + "\"]\n")

# ---------- 1. kernel ----------
wl = open("wolfram/HanKitabKernel_v002.wl", encoding="utf-8").read()
blocks = [b.strip() for b in wl.split("\n\n") if b.strip()]
cells = [cell("HanKitabKernel v002", "Title"),
         cell("Wolfram Cloud chat proxy for the Han Kitab reader. Same protocol as TUTUKernel and LaplacianLabKernel (CCN Cloud Kit). Deployed at https://www.wolframcloud.com/obj/ccn2/HanKitabKernel on 21 Nov 2026. The chat key is read from the private cloud object LaplacianLab/apikey; the app key (secret) is stored privately as HanKitab/secret and in HanKitabKernel_SECRET_private.txt in the Desktop folder. Never commit the secret.", "Text")]
for b in blocks:
    if "CloudPut[" in b and "apikey" in b:
        cells.append(cell("Step 1 (only if the key is not stored yet). Paste the key, evaluate once, then delete the key from this cell and save the notebook, so the key is not kept in the file.", "Text"))
    if b.startswith("(*") and b.endswith("*)"):
        cells.append(cell(b[2:-2].strip(), "Text"))
    else:
        cells.append(cell(b, "Input"))
cells += [cell("Tests (DO012). Each cell is self-contained; no key is needed for status and chat.", "Section"),
          cell('u = "https://www.wolframcloud.com/obj/ccn2/HanKitabKernel";\n'
               'URLExecute[HTTPRequest[u, <|"Method" -> "POST", "Body" -> {"mode" -> "status"}|>], "RawJSON"]', "Input"),
          cell('u = "https://www.wolframcloud.com/obj/ccn2/HanKitabKernel";\n'
               'pl = BaseEncode[ExportByteArray[<|"max_tokens" -> 1500, "system" -> "Answer in one short sentence.", "messages" -> {<|"role" -> "user", "content" -> "Who wrote \u5929\u65b9\u6027\u7406?"|>}|>, "RawJSON", "Compact" -> True]];\n'
               'ch = URLExecute[HTTPRequest[u, <|"Method" -> "POST", "Body" -> {"mode" -> "chat", "payload_b64" -> pl}|>], "RawJSON"];\n'
               'If[KeyExistsQ[ch, "text_b64"], {ch["stop_reason"], ByteArrayToString[BaseDecode[ch["text_b64"]]]}, ch]', "Input"),
          cell('u = "https://www.wolframcloud.com/obj/ccn2/HanKitabKernel";\n'
               'URLExecute[HTTPRequest[u, <|"Method" -> "POST", "Body" -> {"mode" -> "wolfram", "key" -> CloudGet["HanKitab/secret"], "code" -> "{$VersionNumber, 1 + 1}"}|>], "RawJSON"]', "Input")]
notebook("wolfram/HanKitabKernel_v003.nb", cells)

# ---------- 2. operations log ----------
T = [  # (index, file, u, x, v, y, why)
 ("T001", "tools/make_mason_v001.py", 'CHAP = re.compile(r"^\\s*(CHAPTER|APPENDIX)\\s+(', '[IVXLnl1]+)\\b(.*)$")', '', '[IVXLnlH\\]1]+)(\\s.*)?$")', 'OCR read IX as "]X" and XII as "XH"'),
 ("T002", "tools/make_mason_v001.py", 'num = m.group(2).replace("n", "II")', '', '.replace("l", "I")', '.replace("H", "II").replace("]", "I")', 'normalise chapter numerals'),
 ("T003", "tools/make_mason_v001.py", 'caps = re.sub(r"[^A-Za-z ]", "", ', 's', ')', '" ".join(t for t in toks if not ROMAN.match(t) and not re.search(r"\\d", t))', 'headers such as "ii FOREWORD" were not recognised'),
 ("T004", "tools/make_mason_v001.py", '    # page marker', '', '', 'body = [l for l in body if not re.match(r"^\\s*([ivxlc]{1,5}|\\d{1,3})\\s*$", l)] + base indent (most common indent)', 'drop page-number lines; measure indent from the page base'),
 ("T005", "tools/make_mason_v001.py", 'if indent >= ', '3', ' and para:', 'base + 3 and para and not prev_hy and not s[:1].islower()', 'false paragraph breaks from ragged OCR layout'),
 ("T006", "tools/make_mason_v001.py", 's = l.strip()\\n', '', '        if s in', 's = re.sub(r"^[ivxl]{1,4}\\s{2,}(?=[A-Z\\"\'])", "", s)\\n', 'roman page numbers glued to the next line'),
 ("T007", "tools/make_mason_v001.py", 'ROMAN = re.compile(r"^[ivxlc', '', ']+$", re.I)', 'y', 'OCR reads vii as "yii"; also re.I on the footer filter and whitespace-normalised headings'),
 ("T008", "tools/make_mason_v001.py", 'BLANK = {1, 2, 3, 4, 5, ', '', '8,', '7, ', 'drop the OCR copy of the title page (a new title page is set)'),
 ("T009", "tools/make_mason_v001.py", 'FIX = [ ... ', '', '(r"\\^+(\\s*\\^+)*", "[Chinese]")', '(r"(?<=\\w)\\^+|\\^+(?=\\w)", "[?]"), ', 'an unreadable letter inside a word was being labelled [Chinese]'),
 ("T010", "tools/mason_book_v001.css", 'font-family: ', '"Noto Serif","Noto Serif CJK SC",serif;', '', '"Crimson Text","Liberation Serif","Noto Serif CJK TC",serif; font-size: 11.5pt;', 'Noto Serif not installed: CJK font gave full-width apostrophes'),
 ("T011", "tools/spellfix_mason_v001.py", 'def sub(p):', '', '', 'BLOCK = {...27 words...}; fixes.update({"liad":"had","tlien":"then","rnan":"man",...})', 'automatic choices that were wrong (liad->lead, tlien->lien, rnan->ran)'),
 ("T012", "plates (rotation table)", 'rot = {6:-90, ', '67:90, 171:90, 183:90', ', 210:-90, ...}', '67:-90, 171:-90, 183:-90', 'three photographs came out upside down'),
 ("T013", "plates", 'plate 351 ', '(as scanned)', '', 'rotate -90', 'plate was sideways'),
 ("T014", "plates", 'im.crop((0,int(h*', '0.12', '),w,int(h*0.80)))', '0.17', 'Black Stone crop included a line of text'),
 ("T015", "tools/clean_zh_pages_v001.py", "json.dump({'W': ", "W, 'H': H", ", 'pages': log}", "int(W), 'H': int(H)", 'numpy integers are not JSON serialisable (also box values)'),
 ("T016", "tools/zh_facsimile_front_v001.html", '<span>', '点', '</span>', '點', 'traditional form of the Justice Node seal'),
 ("T017", "tools/zh_facsimile_front_v001.html", '<div class="seal">...</div>', '', '', '<div ...>CCN 制作</div>', 'seal caption as on other CCN works'),
 ("T018", "tools/app_template_v001.html", '.lightbox{position:fixed', '', '', '.viewer{...} .dl{...} ', 'styles for the page viewer and downloads'),
 ("T019", "tools/app_template_v001.html", 'Ask</button>', '', '\\n', '\\n<button ... data-v="downloads">Downloads</button>', 'Downloads tab (user request: originals for public download)'),
 ("T020", "tools/app_template_v001.html", '__ZHDATA__</script>', '', '', '<script id="dl-data">__DLDATA__</script><script id="facs-data">__FACSDATA__</script>', 'data blocks filled by make_app'),
 ("T021", "tools/app_template_v001.html", 'const DOCS = [', 'two entries', '];', 'three entries incl. facsimile (facs: true)', 'Chinese facsimile as its own text'),
 ("T022", "tools/app_template_v001.html", "$('#mdLink').href = ", 'd.md;', '', "d.md || '#'; hide when none; language switch only for Mason", 'facsimile has no Markdown'),
 ("T023", "tools/app_template_v001.html", 'const d = DOCS.find((x) => x.id === current);', '', '', '\\nif (d.facs) { renderFacs(); return; }', 'render the facsimile'),
 ("T024", "tools/app_template_v001.html", 'function zhBlock(z, s) {', '', '', 'if (current === "mason" && FACS.pages) return makeViewer(...)', 'Chinese pane = page viewer at the matching juan'),
 ("T025", "tools/app_template_v001.html", 'docSel.onchange', '', '', 'makeViewer, renderFacs, keyboard paging, downloads list', 'viewer and downloads code'),
 ("T026", "tools/app_template_v001.html", 'Never give personal details about the people who make this app.', '', '', 'AI-honesty answer + privacy referral to Lucia Valente', 'EMAIL-CONTEXT rules'),
 ("T027", "tools/app_template_v001.html", 'go(k) { ... ', 'preload always', '', 'preload only after the reader turns a page; img.loading = lazy', 'avoid loading 70 pages when the parallel view opens'),
 ("T028", "tools/app_template_v001.html", '.par .zhpane{', '', 'font-family', 'align-self:start;', 'sticky viewer inside the grid'),
 ("T029", "tools/app_template_v001.html", "if (h[0] === 'read')", '', '', "if (h[2] ...) lang = h[2]; ", '#read/mason/par links (and headless test)'),
 ("T030", "tools/app_template_v001.html", '.btn.primary{', '', '', '.btn{text-decoration:none;display:inline-block}', 'download links were underlined'),
 ("T031", "tools/app_template_v001.html", 'max_tokens: ', '900', ', system: PERSONA', '1500', 'DO006[3]: empty reply at the token limit'),
 ("T032", "tools/make_app_v001.py", 'MASON_MAP = {', '', '"foreword": 9,', '"top": 2, "list-of-illustrations": 2, ', 'title section opened the cover, not the title page'),
 ("T033", "wolfram/HanKitabKernel_v002.wl", 'Which[\n', '', '     #key =!= secret,', '#mode === "status", <|"chat_ready" ..., "open_chat" -> True|>,\n #mode === "chat", ... (moved above the key check)\n', 'readers ask without a key; only code evaluation stays behind the secret'),
 ("T034", "wolfram/HanKitabKernel_v002.wl", '"key" -> "String"', '', ',', ' -> ""', 'key optional'),
 ("T035", "wolfram/HanKitabKernel_v002.wl", '"max_tokens" -> Clip[..., {1, ', '4096', '}]', '1500', 'limit spend on an open address; also at most 12 messages and 60 000 characters'),
 ("T036", "wolfram/HanKitabKernel_v002.wl", 'With[{', 'keyObj = CloudObject["HanKitab/apikey"]', ', secret = ...}', 'keyObjs = {CloudObject["HanKitab/apikey"], CloudObject["LaplacianLab/apikey"]}', 'use HanKitab/apikey once it is stored; until then the LaplacianLab key'),
 ("T037", "tools/app_template_v002.html", '<div class="keyrow">', '<span ...>Offline…</span><input id="keyIn"…><button id="connectBtn">Connect</button>', '</div>', '<span id="ccnState">Connecting to CCN Cloud…</span>', 'no key box for readers'),
 ("T038", "tools/app_template_v002.html", 'async function ccnConnect() {', 'if (!ccnKey) return false; … mode wolfram check …', '}', 'kernelCall({ mode: "status" }); auto-connect on load and when back online', 'automatic connection'),
 ("T039", "tools/app_template_v002.html", "new URLSearchParams(", "{ key: ccnKey, ...params }", ")", "params", 'no key sent'),
 ("T040", "sw.js, manifest.webmanifest, index.html", "HanKitab_", "v001", ".html", "v002", 'point installs and the redirect at the v002 app; cache hankitab-v002'),
 ("T041", "app files", "OUT = ", 'f"HanKitab_{VERSION}.html"', "", '"index.html"', 'editor: no app versioning; one fixed URL, overwritten each time. HanKitab_v001.html removed; template and builder renamed app_template.html, make_app.py'),
 ("T043", "tools/app_template.html", "", "the About line on Ask answers, the AI/Claude/Anthropic wording in Ask, the MODEL setting and the credit title", "", "(removed; neutral wording: 'Connected to CCN Cloud.'; the kernel chooses the model)", 'editor request; the guide still answers honestly if asked whether it is a person'),
 ("T044", "tools/app_template.html", "DOCS.forEach((d) => {\n", "", "      const h = ...getElementById(d.tpl)", "      if (!d.tpl) return;\n", 'search and Ask failed (null template) once the facsimile was added; found in the live test DO010[2]'),
 ("T045", "tools/app_template.html", "const hits = search(", "words longer than 3 letters, all required", ", 6);", "key words without stop-words (Liu, Zhi kept), any may match", 'Ask found no passage for "Who was Liu Zhi?" (DO010[3])'),
 ("T046", "tools/make_notebooks_v002.py (kernel tests)", "pl = BaseEncode[", 'StringToByteArray[ExportString[..., "RawJSON", ...]]', "];", 'ExportByteArray[..., "RawJSON", ...]', 'test failed in the notebook: u and secret were defined in another cell, and the Chinese question was UTF-8 encoded twice; each test cell is now self-contained (HanKitabKernel_v003.nb)'),
 ("T047", "tools/app_template.html", "const ctx = hits.map((h, i) => `[${i + 1}] ", "${title} · ${section}", ": ${text}`", "Source: <full source line> Section: <section> (a footnote by Isaac Mason).", 'Ask was unsure whether a footnote was Mason\'s; each passage now carries its source'),
 ("T048", "tools/app_template.html", 'data-v="search"', '', '', 'History tab: sections 1, 2, 3, 7 and 8 of the research report, with its own contents list', 'editor: add the history research to the site'),
 ("T042", "sw.js", "const VERSION = '", "hankitab-v002", "';", "hankitab-<sha1 of index.html, 10 hex>", 'cache name set automatically by make_app.py'),
]
DO = [  # (index, what, [(iteration, result)], record)
 ("DO001", "OCR trials on 天方至聖實錄 p. 10", [("1", "tesseract chi_tra psm 5: unusable"), ("2", "tesseract jpn_vert psm 5: ~55 %"), ("3", "cells -> one line, chi_tra psm 7: ~70 %"), ("4", "+ ring punctuation removed: ~70 %"), ("5", "single cells psm 10: ~65 %"), ("6", "RapidOCR PP-OCRv3: ~80 %, simplified forms")], "records/04_ocr_trials_v001.md"),
 ("DO002", "fold-label OCR (right margin) on 295 cleaned pages", [("1–295", "no labels found: margin was trimmed away")], "records/03_zh_juan_detection_ocr_v001.txt"),
 ("DO003", "first-column OCR on 295 pages to find juan headings", [("1–295", "found 序 p. 9, 重印序 p. 23, 卷目 p. 43, 卷一…卷十 pp. 51, 77, 97, 109, 123, 145, 163, 197, 231, 257")], "records/03_zh_juan_detection_ocr_v001.txt"),
 ("DO004", "Mason clear-text build (tools/make_mason_v001.py)", [("1", "19 headings, false paragraph breaks"), ("2", "23 headings after T001–T002"), ("3", "front matter fixed (T003–T007)"), ("4", "295 page markers, gaps only at plate pages"), ("5", "PDF 338 pp."), ("6", "PDF 278 pp. with Crimson Text (T010)"), ("7", "PDF 277 pp., 8.8 MB after T008")], "texts/ArabianProphet_Mason1921_v001.md"),
 ("DO005", "spelling pass (tools/spellfix_mason_v001.py)", [("1", "121 automatic fixes"), ("2", "97 after review (T011)")], "records/01_mason_spellfixes_v001.json"),
 ("DO006", "HanKitabKernel tests", [("1", "bad key refused"), ("2", "{15., 2}, chat_ready True"), ("3", "max_tokens 60: empty text"), ("4", "max_tokens 1500: correct answer")], "records/05_kernel_tests_v001.md"),
 ("DO007", "app headless browser tests (Chrome, localhost)", [("1", "#library: renders, no console errors"), ("2", "#read/mason"), ("3", "#read/facs: viewer at 卷一 p. 51"), ("4", "#downloads: 5 rows with sizes"), ("5", "#read/mason/par: English + page viewer"), ("6", "390×844 mobile: facsimile readable")], "records/06_app_screens_v001.png"),
 ("DO009", "HanKitabKernel v002 tests", [("1", "status without key: chat_ready True, open_chat True"), ("2", "wolfram 1+1 without key: refused"), ("3", "wolfram 1+1 with secret: 2"), ("4", "chat without key: answer received")], "records/07_kernel_v002_tests_v001.md"),
 ("DO010", "live page test, v002 (GitHub Pages, built-in browser)", [("1", "status: Connected, no key box"), ("2", "Ask failed: null template -> T044"), ("3", "no passages -> T045"), ("4", "answer citing the report"), ("5", "Search Black Stone: 11"), ("6", "7 downloads: 200"), ("7", "no Claude/Anthropic in the page")], "records/08_live_v002_test_v001.md"),
 ("DO011", "own chat key", [("1", "HanKitab/apikey stored, owner-only"), ("2", "open chat answered using it")], "records/09_own_chat_key_v001.md"),
 ("DO012", "kernel notebook tests (v003 cells, run in the local kernel)", [("1", "status"), ("2", "chat in Chinese"), ("3", "code with secret")], "records/10_kernel_notebook_tests_v001.md"),
 ("DO013", "History tab and source labels", [("1", "headless: History renders sections 1, 2, 3, 7, 8 with contents"), ("2", "live: Ask on the Black Stone credits Mason's footnote")], "records/11_history_tab_v001.png"),
 ("DO008", "facsimile PDF build", [("1", "img2pdf from PNG: 297 pp., 18.0 MB"), ("2", "CCITT G4 TIFF: 297 pp., 10.7 MB")], "texts/TianfangZhishengShilu_1924_facsimile_v001.pdf"),
]
cells = [cell("Han Kitab · Operations Log v002", "Title"),
         cell("Every code change is written as (T) u x v → u y v: u is the text just before the change, x the text removed, v the text just after it, y the text put in. Every run or test is a (DO) entry with its iterations [i]. Raw outputs are in records/. Conventions: docs/CCN_Acronyms_and_Conventions_v002.md.", "Text"),
         cell("(T) Rewrites", "Section")]
for idx, f, u, x, v, y, why in T:
    cells.append(cell(f"{idx} · {f}", "Subsection"))
    cells.append(cell(f"u = {u}\nx = {x if x else '(empty: insertion)'}\nv = {v if v else '(empty)'}\ny = {y}\nwhy: {why}", "Program"))
cells.append(cell("(DO) Runs", "Section"))
for idx, what, its, rec in DO:
    cells.append(cell(f"{idx} · {what}", "Subsection"))
    cells.append(cell("\n".join(f"[{i}] {r}" for i, r in its) + f"\nraw output: {rec}", "Program"))
cells.append(cell("Operations data as a Wolfram expression", "Section"))
q = lambda t: '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'
data = "opsT = {" + ", ".join("<|\"index\" -> %s, \"file\" -> %s, \"why\" -> %s|>" % (q(i), q(f), q(w)) for i, f, u, x, v, y, w in T) + "};\n" \
       "opsDO = {" + ", ".join("<|\"index\" -> %s, \"what\" -> %s, \"iterations\" -> %d|>" % (q(i), q(w), len(it)) for i, w, it, r in DO) + "};\n{Length[opsT], Length[opsDO]}"
cells.append(cell(data, "Input"))
notebook("wolfram/HanKitabOperationsLog_v002.nb", cells)

# ---------- 3. development log ----------
dev = [
 ("Title", "Han Kitab · Development Log v002"),
 ("Text", "How the Han Kitab reader and its editions were built on 20–21 November 2026. v002 (21 Nov): Ask is open to readers without a key (section 6)."),
 ("Section", "1. Research report"),
 ("Text", "Web research on the Han Kitab corpus, authors, editions and the history of Sinification; written as docs/HanKitab_Research_v001.md and rendered to PDF with pandoc and headless Chrome. Chinese passages are short public-domain excerpts with new English translations; unverified items are flagged in the report."),
 ("Section", "2. The Arabian Prophet (Mason 1921), clear-text edition"),
 ("Text", "Source: Internet Archive scan cu31924024748232 (Cornell copy), 368 pages, with an OCR text layer. tools/make_mason_v001.py reads each page with pdftotext -layout, removes running heads and page-number lines, splits footnotes from body text, rejoins paragraphs and hyphenated words, marks unreadable Chinese as [Chinese] and unreadable letters as [?], and keeps the original page numbers as [p. N]. Plates were cut from the scan at 200 dpi, trimmed and turned upright. tools/spellfix_mason_v001.py makes cautious one-edit spelling fixes, checked by hand (records/01). Trials and fixes: Operations Log T001–T014, DO004–DO005."),
 ("Section", "3. 天方至聖實錄 (1924), facsimile"),
 ("Text", "Source: National Library of China scan on Wikimedia Commons, NLC416-13jh005373-59385, 295 pages (prefaces, contents, juan 1–10). Text recognition was tried with Tesseract and RapidOCR (DO001, records/04); at best about 80 % of characters were right and some came out in simplified form. The user decided: copy the pages as they are and add only a cover and copyright page. tools/clean_zh_pages_v001.py removes specks of 6 pixels or fewer, trims each page to its printed area and centres it on one page size; nothing else is touched. The PDF uses CCITT G4 images (10.7 MB). Juan start pages were found by reading the first column of every page (DO003)."),
 ("Section", "4. The app (HanKitab_v002.html)"),
 ("Text", "Modelled on the TUTUcat repository (single index.html + manifest + service worker + icons), without the talking head. Tabs: Library, Read (English, English + 中文 with the Chinese page viewer opened at the matching juan, or 中文 alone; text size; read aloud with browser voices), Search (offline, across all texts), Ask (HanKitabKernel chat with passages from the texts; offline it returns the passages), Downloads (editions and the unchanged original scans), About. Built by tools/make_app_v002.py from tools/app_template_v002.html. Tests: DO007."),
 ("Section", "5. HanKitabKernel"),
 ("Text", "Same design as TUTUKernel / LaplacianLabKernel. Deployed from the user's signed-in Wolfram kernel to https://www.wolframcloud.com/obj/ccn2/HanKitabKernel, reusing the private chat key object LaplacianLab/apikey and a new private secret HanKitab/secret. Tests DO006: the chat needs max_tokens well above 60 (T031)."),
 ("Section", "6. v002: open Ask"),
 ("Text", "The editor asked that readers should not have to enter a key, as the readership is small. HanKitabKernel v002 answers mode status and mode chat without a key; only mode wolfram (code evaluation) still needs the secret. To protect the account on an open address, answers are capped at 1500 tokens, a request may carry at most 12 messages and 60 000 characters, and only Claude models are allowed. The chat key is read from HanKitab/apikey once it is stored, otherwise from LaplacianLab/apikey. The app connects by itself (mode status) and shows no key box (T033–T040, DO009–DO010)."),
 ("Section", "Glossary"),
 ("Text", "Han Kitab 漢克塔布: Chinese-language Islamic books. juan 卷: a fascicle or chapter of a Chinese book. 天方至聖實錄: Liu Zhi's life of the Prophet. Facsimile: the pages reproduced as images, unchanged. OCR: machine reading of text from images. CCITT G4: lossless compression for black-and-white images. PWA: a web page that can be installed like an app. (T) / (DO): see docs/CCN_Acronyms_and_Conventions_v002.md."),
]
notebook("wolfram/HanKitabDevelopmentLog_v002.nb", [cell(t, s) for s, t in dev])

# ---------- 4. scripts ----------
cells = [cell("Han Kitab · Scripts v002", "Title"),
         cell("Every script and template used to build this release, one cell each (Program style). The files themselves are in tools/ and wolfram/.", "Text")]
for f in sorted(glob.glob("tools/*.py") + glob.glob("tools/*.html") + glob.glob("tools/*.css") + ["sw.js", "manifest.webmanifest", "wolfram/HanKitabKernel_v002.wl"]):
    cells.append(cell(f, "Section"))
    cells.append(cell(open(f, encoding="utf-8").read(), "Program"))
notebook("wolfram/HanKitabScripts_v002.nb", cells)
print("notebooks written")
