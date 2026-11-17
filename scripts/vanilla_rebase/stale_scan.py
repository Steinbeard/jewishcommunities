"""For every by-name override: vanilla lines present in BOTH 1.20 and 1.21 that the mod's current block lacks.
Those are either deliberate removals or stale-copy losses. Prints one section per definition.
usage: stale_scan.py OVERRIDES_JSON
"""
import json, os, re, sys
from collections import Counter

MOD = r"C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities-1.21-port"
BASE = r"D:\ck3-base-1.20\game"
NEW = r"E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game"
raw = json.load(open(sys.argv[1], encoding="utf-8"))
d = json.loads(raw[0]["text"]) if isinstance(raw, list) else raw


def code(l):
    q = False
    for i, ch in enumerate(l):
        if ch == '"':
            q = not q
        if ch == "#" and not q:
            return l[:i]
    return l


def read(p):
    return open(p, encoding="utf-8-sig", errors="replace").read().replace("\r", "").split("\n")


def block(lines, key, near=None):
    pat = re.compile(r"^\s*" + re.escape(key) + r"\s*=\s*\{")
    c = [i for i, l in enumerate(lines) if pat.match(code(l))]
    if not c:
        return None
    if near is not None:
        c.sort(key=lambda i: abs(i - near))
    s = c[0]; depth = 0; seen = False
    for j in range(s, len(lines)):
        cc = code(lines[j]); depth += cc.count("{") - cc.count("}"); seen = seen or "{" in cc
        if seen and depth <= 0:
            return lines[s:j + 1]


norm = lambda l: " ".join(code(l).split())
for e in d["same_key"]:
    if e["similarity"] < 30:
        continue  # lists that merge or full rewrites
    m = block(read(os.path.join(MOD, e["file"])), e["key"], e["line"] - 1)
    bp, gp = os.path.join(BASE, e["overrides"]), os.path.join(NEW, e["overrides"])
    if not (m and os.path.exists(bp) and os.path.exists(gp)):
        continue
    b, g = block(read(bp), e["key"]), block(read(gp), e["key"])
    if not (b and g):
        continue
    cm = Counter(norm(l) for l in m)
    stable = Counter(norm(l) for l in b) & Counter(norm(l) for l in g)
    missing = [(k, v - cm[k]) for k, v in stable.items() if k and k not in ("{", "}") and v > cm[k]]
    if missing:
        print(f"## {e['key']}  ({e['file'].split('/')[-1]}): {sum(v for _, v in missing)} stable vanilla line(s) absent")
        for k, v in missing[:12]:
            print(f"    {'x'+str(v) if v > 1 else '  '} {k[:130]}")
        if len(missing) > 12:
            print(f"    ... {len(missing) - 12} more")
