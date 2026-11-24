# Han Kitab · 漢克塔布 — release v002 (21 November 2026)

© Computational Classnotes · CC BY-NC-SA 4.0 · Justice Node https://justice.compclassnotes.com/

A reader for Chinese Islamic classics, modelled on the Tutu Cat app (one HTML page, a manifest, a service worker
and icons) without the talking head.

## The app (`index.html`)

One fixed address, always the current app: https://lossofgenerality.github.io/han-kitab/ (no versioned app files).

- **Library** — the texts in this release.
- **Read** — *The Arabian Prophet* in English, in English + 中文 (the Chinese pages of 天方至聖實錄 beside each chapter,
  opened at the matching juan), or 中文 alone; the 1924 facsimile page by page (◀ ▶, arrow keys, contents by juan);
  the research report. Text size, read aloud with the device's voices, PDF and Markdown links.
- **History** — the history of the Han Kitab and of Sinification, from the research report (sections 1–3, 7, 8).
- **Gallery** — 45 photographs of mosques, tombs, calligraphy, Muslim quarters, markets and food across China (Wikimedia Commons, each with its author and licence; `gallery/CREDITS_v001.md`).
- **Search** — every text at once, English or Chinese, offline.
- **Ask** — questions about the Han Kitab, no key needed. Answers come through HanKitabKernel, which is given
  the most relevant passages; offline, the passages themselves are shown.
- **Downloads** — the editions and the unchanged original scans.
- **Install** — Chrome/Edge: *Install app*; iPhone/iPad: Share → Add to Home Screen. Works offline once opened
  (PDFs excepted).

## Cover

The Library opens with a page of Lan Zixi's 天方正學 (1861): the basmala and the letter alif drawn as the human form. The University of Manchester Library, Chinese Crawford 326, CC BY-NC-SA 4.0.

## Texts

| Text | File | Size | Notes |
|---|---|---|---|
| The Arabian Prophet, clear-text edition | `texts/ArabianProphet_Mason1921_v001.pdf` | 8.8 MB | 277 A5 pages, 20 original illustrations, original page numbers kept as [p. N]. Chinese characters the OCR could not read are marked [Chinese]. |
| — Markdown | `texts/ArabianProphet_Mason1921_v001.md` + `texts/plates/` | 566 KB | |
| 天方至聖實錄, 1924 printing, prefaces + juan 1–10 | `texts/TianfangZhishengShilu_1924_facsimile_v001.pdf` | 10.7 MB | The original pages, not a character changed; only specks removed and margins trimmed. Cover and copyright page added. |
| — page images for the app | `texts/zh_pages/page_001.png` … `page_295.png` | | 1000 px wide, black and white |
| Research report | `docs/HanKitab_Research_v001.pdf` · `.md` | 1.2 MB | |
| Original scan: The Arabian Prophet | `originals/ArabianProphet_Mason1921_original_scan_cu31924024748232.pdf` | 12.9 MB | Cornell copy, Internet Archive. Public domain. |
| Original scan: 天方至聖實錄 | `originals/TianfangZhishengShilu_1924_original_scan_NLC416-13jh005373-59385.pdf` | 10.2 MB | National Library of China copy, Wikimedia Commons. Public domain. |

## HanKitabKernel (Ask tab)

Deployed at `https://www.wolframcloud.com/obj/ccn2/HanKitabKernel` (set in the config block at the top of the app).
Same protocol as TUTUKernel. Code and test cells: `wolfram/HanKitabKernel_v002.nb` / `.wl`.

- **v002:** `status` and `chat` are open to readers without a key; answers are capped at 1,500 tokens, 12 messages,
  60,000 characters, Claude models only. Only `wolfram` (code evaluation) needs the owner's secret (`HanKitab/secret`,
  private; not in this repository).
- **Chat key:** read from the private cloud object `HanKitab/apikey`; until it is stored, from `LaplacianLab/apikey`.

## Build

```
python3 tools/make_mason_v001.py      # Mason clear text (needs the original scan as src.pdf)
python3 tools/clean_zh_pages_v001.py  # facsimile page cleaning
python3 tools/make_app.py             # index.html (and the service-worker cache name)
python3 tools/make_notebooks_v002.py  # kernel, operations log, development log, scripts notebooks
```

Logs: `wolfram/HanKitabOperationsLog_v002.nb` ((T) rewrites, (DO) runs), `wolfram/HanKitabDevelopmentLog_v002.nb`,
`wolfram/HanKitabScripts_v002.nb`; raw outputs in `records/`. Conventions: `docs/CCN_Acronyms_and_Conventions_v002.md`.

## Credits

Principal Investigator Lucval · Editors Dara, Lucia · Software FreeFormer ·
Agent Kirari-chan (キラリちゃん) · Programming: Hikari Noor Hoshino (星野ヌール).

© Computational Classnotes · CC BY-NC-SA 4.0. The 1724 text, the 1921 translation and the 1924 printing are in the public domain.
