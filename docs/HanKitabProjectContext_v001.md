# Han Kitab · Project Context v001 (21 November 2026)

© Computational Classnotes · CC BY-NC-SA 4.0

## State
- Repo: https://github.com/lossofgenerality/han-kitab (main, release v001). Live page (after GitHub Pages is switched on): https://lossofgenerality.github.io/han-kitab/
- App: `HanKitab_v001.html` — Library, Read (English / English + 中文 / 中文), Search, Ask, Downloads, About; installable, offline.
- Texts: Mason, *The Arabian Prophet* (1921) clear-text edition v001; 天方至聖實錄 (1924) facsimile v001 (prefaces + juan 1–10); research report v001; both original scans unchanged in `originals/`.
- Kernel: HanKitabKernel deployed at https://www.wolframcloud.com/obj/ccn2/HanKitabKernel; app key in Desktop/Research/HanKitab/HanKitabKernel_SECRET_private.txt and cloud object HanKitab/secret (private).
- Notebooks: wolfram/ and Desktop/Research/HanKitab (Kernel, OperationsLog T001–T032 / DO001–DO008, DevelopmentLog, Scripts).

## Open tasks
1. Switch on GitHub Pages (Settings → Pages → Deploy from branch, main, / root), then check the live page.
2. 天方至聖實錄 juan 11–20: find a scan of the second half (NLC, CTEXT library or NDL) and add it the same way.
3. Proofread the Mason clear text; type in the Chinese characters marked [Chinese] from the scan.
4. A faithful typed Chinese text of 天方至聖實錄 (only by reading every page; machine reading was ~80 %).
5. More Han Kitab texts: 天方性理 (Commons NLC scans, ANU manuscript), 天方典禮 (ANU), 天方正學 (Commons).
6. Conventions files not yet made: Tutorial, Manual, Flowchart, Acronyms notebooks.

## How to resume
Clone the repo, run `python3 tools/make_app_v001.py` after any text change, bump to v002 (never overwrite), log new (T)/(DO) entries in `tools/make_notebooks_v002.py`, commit as Noor Hoshino, push, verify with `git ls-remote` and the live page, copy notebooks to Desktop/Research/HanKitab.
