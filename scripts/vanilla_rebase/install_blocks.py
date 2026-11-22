"""Write hand-resolved blocks (blocks/NN_key.merged) back into the mod files in place.

usage: install_blocks.py OVERRIDES_JSON BLOCKDIR key1,key2,...
"""
import json, os, re, sys
from collections import defaultdict

MOD = r"C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities-1.21-port"
src, bdir, keys = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
raw = json.load(open(src, encoding="utf-8"))
d = json.loads(raw[0]["text"]) if isinstance(raw, list) else raw


def code(l):
    q = False
    for i, ch in enumerate(l):
        if ch == '"':
            q = not q
        if ch == "#" and not q:
            return l[:i]
    return l


def read(path):
    b = open(path, "rb").read()
    t = b.decode("utf-8-sig")
    return t.replace("\r", "").split("\n"), b.startswith(b"\xef\xbb\xbf"), "\r\n" in t


def find_block(lines, key, near):
    pat = re.compile(r"^\s*" + re.escape(key) + r"\s*=\s*\{")
    cands = sorted((i for i, l in enumerate(lines) if pat.match(code(l))), key=lambda i: abs(i - near))
    s = cands[0]
    depth, seen = 0, False
    for j in range(s, len(lines)):
        c = code(lines[j]); depth += c.count("{") - c.count("}"); seen = seen or "{" in c
        if seen and depth <= 0:
            return s, j


todo = [e for e in d["same_key"] if e.get("rebase", {}).get("verdict") in ("combine", "review")]
files = {f.split("_", 1)[1].rsplit(".", 1)[0]: os.path.join(bdir, f) for f in os.listdir(bdir) if f.endswith(".merged")}
writes = defaultdict(list)
for e in todo:
    if e["key"] not in keys:
        continue
    merged = open(files[e["key"]], encoding="utf-8").read().rstrip("\n").split("\n")
    if any(l.startswith(("<<<<<<<", ">>>>>>>", "=======")) for l in merged):
        sys.exit(f"markers left in {e['key']}")
    bal = sum(code(l).count("{") - code(l).count("}") for l in merged)
    if bal:
        sys.exit(f"unbalanced braces ({bal}) in {e['key']}")
    path = os.path.join(MOD, e["file"])
    lines, _, _ = read(path)
    s, t = find_block(lines, e["key"], e["line"] - 1)
    writes[path].append((s, t, merged, e["key"]))
for path, edits in writes.items():
    lines, bom, crlf = read(path)
    for s, t, new, k in sorted(edits, reverse=True):
        lines[s:t + 1] = new
    text = "\n".join(lines)
    if crlf:
        text = text.replace("\n", "\r\n")
    open(path, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    print(f"{os.path.relpath(path, MOD)}: {', '.join(e[3] for e in edits)}")
