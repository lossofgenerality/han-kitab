#!/usr/bin/env python3
"""Conservative OCR spelling fixes: a lower-case word unknown to the dictionary and rare in the book
is replaced only by a single-edit candidate that is a dictionary word AND occurs >=3 times in the book."""
import re, sys, collections, json
from spellchecker import SpellChecker
sp = SpellChecker(distance=1)
src = sys.argv[1]
md = open(src).read()
# protect html tags
parts = re.split(r"(<[^>]+>)", md)
words = collections.Counter(w for i, p in enumerate(parts) if i % 2 == 0 for w in re.findall(r"[A-Za-z]+", p))
low = collections.Counter({w: c for w, c in words.items() if w.islower()})
fixes = {}
for w, c in low.items():
    if c > 2 or len(w) < 4 or w in sp:
        continue
    cands = [x for x in sp.edit_distance_1(w) if x in sp and low.get(x, 0) >= 3]
    if len(cands) == 1 or (cands and max(cands, key=lambda x: low[x]) and sorted(cands, key=lambda x: -low[x])[0]):
        best = sorted(cands, key=lambda x: -low[x])
        if best and (len(best) == 1 or low[best[0]] >= 3 * low[best[1]]):
            fixes[w] = best[0]
BLOCK = {"othe","ther","thei","ohammed","cometo","losa","elie","aith","doesn","couldn","sheeps","ardour","ither","hter","thos",
         "erid","recognise","laine","ching","appl","mits","coun","oach","nien","pened","teing","ived"}
for b in BLOCK: fixes.pop(b, None)
fixes.update({"liad":"had","tlien":"then","rnan":"man","moming":"morning","arrd":"and","ajid":"and","atid":"and","pened":"opened","teing":"being","ived":"lived"})
def sub(p):
    return re.sub(r"\b([a-z]+)\b", lambda m: fixes.get(m.group(1), m.group(1)), p)
out = "".join(sub(p) if i % 2 == 0 else p for i, p in enumerate(parts))
open(src, "w").write(out)
json.dump(fixes, open("records_spellfixes_v001.json", "w"), ensure_ascii=False, indent=0)
print(len(fixes)); print(list(fixes.items())[:60])
