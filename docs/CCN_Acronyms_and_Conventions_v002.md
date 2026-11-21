# CCN Acronyms and Project Conventions

*Reusable across Computational Classnotes projects · v002 · first written for the CCN Fugue Composer · copied into Han Kitab, 21 November 2026*

Copy this file into a new project and follow it from the first commit. When a new acronym or rule is added, write a new version (`_v002`, …) and keep the old one.

## 1. Acronyms and tags

### (T) — Term rewriting / string rewriting

A rewriting system is an alphabet Σ (for strings) or a set of function symbols (for terms), together with rules l → r. One step replaces an occurrence of l by r and leaves the context alone.

- String rewriting: u l v → u r v, where u and v are the unchanged context.
- Term rewriting: a subterm that matches l under a substitution σ (a binding of the pattern variables) is replaced by σ(r). Example: f[g[a], b] /. g[z_] :> h[z, z] gives f[h[a, a], b].
- Normal form: a term with no rule left to apply. The system terminates if every sequence of steps is finite. It is confluent if the normal form does not depend on the order in which the rules are applied.
- In the operations log, every code change is written as **u x v → u y v**. u is the text just before the change, x the text removed, v the text just after it, and y the text put in its place. An empty x means an insertion; an empty y means a deletion.
- Each change gets an index: T001, T002, … . The index keeps counting across versions of the log.
- In the Wolfram Language: StringReplace rewrites substrings. /. and //. rewrite expressions. //. on a string only matches the whole string.

### (DO) — Do[ ] and other loops

A loop evaluates the same body many times. Each run of the body is one iteration, and the counting variable is the loop index.

- Do[expr, {i, imin, imax}] evaluates expr for i = imin, …, imax. Nested iterators are written Do[expr, {i, …}, {j, …}]. Do returns Null.
- For[start, test, incr, body] is the C-style loop. While[test, body] is for a number of iterations not known in advance. Table[expr, {i, …}] collects the values into a list.
- A loop invariant is a statement that is true before and after every iteration. It is how one argues that a loop is correct.
- In the operations log, every run, test or trial is one entry: DO001, DO002, … . Each iteration is listed with its index [i] and its result, and the raw output is saved in records/.
- Loops inside the program itself are tagged DO-A.

### Other abbreviations used in the logs

- **vNNN**: the version index of a file (v001, v002, …). Higher means newer; old versions are kept.
- **records/NN_…**: raw outputs of trials and tests, numbered in the order they were made.
- **DO-A**: an algorithm loop (inside the program), as opposed to a DO run of the program.
- **parity test**: two implementations (for example Python and JavaScript) run on the same inputs; their outputs must be byte-identical.

## 2. Working rules

- **Never overwrite.** Every file created gets an index (`name_v001.ext`), and each change makes the next index. This includes outputs the programs write.
- **Nothing on the screen.** Code, interim steps, trial outputs, explanations and definitions go into files (.py, .wl, .nb, .md, records/). The chat only says what was done and where it is.
- **No notebooks displayed in the session.** A notebook's content (code, outputs, definitions, diagrams) is never shown in the chat. It goes only into the notebooks and the logs (operations log, development log, records/).
- **Notebooks go to the Desktop folder** for the project (for Han Kitab, Desktop/Research/HanKitab), as well as to the repo.
- **Commits** are authored and committed as `Noor Hoshino <noor@compclassnotes.com>`, with no Co-Authored-By or Claude-Session lines.
- **Copyright**: every piece of work carries `© Computational Classnotes · CC BY-NC-SA 4.0`.
- **Check before saying "pushed".** Verify the commit on the remote (git ls-remote) and open the live page (GitHub Pages) before telling the user.
- **Test before shipping.** Wolfram code is run in a kernel. Each port gets a parity test against the reference implementation. UI pages get a headless browser test.

## 3. Files and logs every project needs

Replace `<P>` with the project's short name (here `HanKitab`). Every file ends in `_vNNN`.

| File | What it is | How it is made |
|---|---|---|
| `README.md` | Short pointer to the latest version of everything | Edited by hand at each release |
| `README_vNNN.md` | Full documentation of that release | New version at each release |
| `VERSIONS_vNNN.md` | Table of every file, its version, its date and what changed | One more row per new file; new version each time |
| `index.html` + `.nojekyll` | GitHub Pages entry; redirects to the latest UI | Updated at each UI release |
| `records/` + `records/README_vNNN.md` | Raw outputs of every trial and test, plus screenshots, numbered NN_… | Saved as the work is done |
| `wolfram/<P>OperationsLog_vNNN.nb` | The (T) rewrites u x v → u y v and the (DO) runs with indexed iterations | `tools/make_opslog_vNNN.py`; the data also as `records/NN_opslog_vNNN_data_v001.wl` |
| `wolfram/<P>DevelopmentLog_vNNN.nb` | How the code was built over time: trials, results, fixes, glossary | `tools/make_devlog_vNNN.py` |
| `wolfram/<P>Tutorial_vNNN.nb` | Tutorial; every Input cell tested in a kernel | `tools/make_notebooks_vNNN.py` |
| `wolfram/<P>_vNNN_Manual_vNNN.nb` + `docs/….md` + `docs/….pdf` | Programmer's manual of the .wl, function by function and variable by variable | `tools/make_manual_vNNN.py`, `manual_vNNN.css`, `manual_topdf_vNNN.py` |
| `wolfram/<P>Flowchart_vNNN.nb` + `docs/<P>Flowchart_vNNN.pdf/.svg/_300dpi.png` + `docs/<P>CallGraph_vNNN.*` | How the program runs, each stage with the functions it triggers, and the full call graph | `tools/make_flowchart_vNNN.py` (reads the .wl; Graphviz) |
| `wolfram/<P>Acronyms_vNNN.nb` + `docs/<P>Acronyms_vNNN.md` | Definitions of the acronyms and tags, with tested examples | `tools/make_acronyms_vNNN.py` |
| `docs/CCN_Acronyms_and_Conventions_vNNN.md` + `.nb` | This file | Copied into each project |
| `docs/<P>ProjectContext_vNNN.md` + `.nb` | Where the project stands: state, files, open tasks, how to resume | Written when work stops |

The tools in a repo (`tools/make_*.py`) can be copied to another project. Change the file names and the source they read.

## 4. Starting a new project

1. Create the repo and the Desktop folder. Copy this file (as `docs/CCN_Acronyms_and_Conventions_v001.md`) and the tools you need.
2. Write the first code as `_v001`, a `README.md`, `README_v001.md` and `VERSIONS_v001.md`.
3. From the first change on, log every rewrite as (T) and every run as (DO), and save the raw outputs in records/.
4. At each release: bump the versions, update VERSIONS and README, commit as Noor Hoshino, push, check the remote and the live page, and copy the notebooks to the Desktop folder.
5. When work stops: write `<P>ProjectContext_vNNN`.

---
© Computational Classnotes · CC BY-NC-SA 4.0
