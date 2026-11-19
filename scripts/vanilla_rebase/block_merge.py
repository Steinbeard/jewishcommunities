"""Three-way merge each by-name override block: base 1.20 block, game 1.21 block, mod block.

usage: block_merge.py OVERRIDES_JSON OUTDIR [--apply] [--only key1,key2]
Reads xtiger_overrides output (with base). For every same_key entry whose verdict is combine/review:
  extracts the definition `key = {...}` from the mod file (at the reported line), the 1.20 file and
  the 1.21 file; runs git merge-file; writes OUTDIR/<n>_<key>.{base,game,mod,merged}.
With --apply, clean merges are written back into the mod file in place (bottom-up per file),
keeping the file's BOM and CRLF.
"""
import json, os, re, subprocess, sys
from collections import defaultdict

MOD = r"C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities-1.21-port"
BASE = r"D:\ck3-base-1.20\game"
NEW = r"E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game"

src, outdir = sys.argv[1], sys.argv[2]
apply = "--apply" in sys.argv
only = None
if "--only" in sys.argv:
    only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
os.makedirs(outdir, exist_ok=True)
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
    bom = b.startswith(b"\xef\xbb\xbf")
    t = b.decode("utf-8-sig", errors="replace")
    crlf = "\r\n" in t
    return t.replace("\r", "").split("\n"), bom, crlf


def block_at(lines, start):
    """lines[start] opens the block; return end index (inclusive)."""
    depth, seen = 0, False
    for j in range(start, len(lines)):
        c = code(lines[j])
        depth += c.count("{") - c.count("}")
        seen = seen or "{" in c
        if seen and depth <= 0:
            return j
    raise ValueError("unbalanced")


def find_block(lines, key, near=None):
    """Top-level (depth 0) `key = {` -- or, for sub-definitions inside a container, any depth."""
    pat = re.compile(r"^\s*" + re.escape(key) + r"\s*=\s*\{")
    cands = [i for i, l in enumerate(lines) if pat.match(code(l))]
    if near is not None:
        cands.sort(key=lambda i: abs(i - near))
    if not cands:
        return None
    s = cands[0]
    return s, block_at(lines, s)


todo = [e for e in d["same_key"] if e.get("rebase", {}).get("verdict") in ("combine", "review")]
if only:
    todo = [e for e in todo if e["key"] in only]
results, writes = [], defaultdict(list)
for n, e in enumerate(todo):
    key = e["key"]
    mod_path = os.path.join(MOD, e["file"])
    mlines, _, _ = read(mod_path)
    mb = find_block(mlines, key, near=e["line"] - 1)
    bl = os.path.join(BASE, e["overrides"])
    gl = os.path.join(NEW, e["overrides"])
    if not os.path.exists(bl) or not os.path.exists(gl):
        results.append((key, e["file"], "MISSING vanilla file " + e["overrides"]))
        continue
    blines, _, _ = read(bl)
    glines, _, _ = read(gl)
    bb, gb = find_block(blines, key), find_block(glines, key)
    if not (mb and bb and gb):
        results.append((key, e["file"], f"NOT FOUND mod={bool(mb)} base={bool(bb)} game={bool(gb)}"))
        continue
    stem = os.path.join(outdir, f"{n:02d}_{key}")
    parts = {"mod": mlines[mb[0]:mb[1] + 1], "base": blines[bb[0]:bb[1] + 1], "game": glines[gb[0]:gb[1] + 1]}
    for k, v in parts.items():
        open(f"{stem}.{k}", "w", encoding="utf-8", newline="\n").write("\n".join(v) + "\n")
    open(f"{stem}.merged", "w", encoding="utf-8", newline="\n").write("\n".join(parts["mod"]) + "\n")
    r = subprocess.run(["git", "merge-file", "-L", "mod", "-L", "base-1.20", "-L", "game-1.21",
                        f"{stem}.merged", f"{stem}.base", f"{stem}.game"])
    gchg = subprocess.run(["diff", "-w", f"{stem}.base", f"{stem}.game"], capture_output=True, text=True).stdout
    gcount = sum(1 for l in gchg.splitlines() if l[:1] in "<>")
    status = "CLEAN" if r.returncode == 0 else f"CONFLICT x{r.returncode}"
    if gcount == 0:
        status = "GAME-UNCHANGED(ws)"
    results.append((key, e["file"], f"{status} game-lines={gcount} verdict={e['rebase']['verdict']}"))
    if r.returncode == 0 and gcount and apply:
        merged = open(f"{stem}.merged", encoding="utf-8").read().rstrip("\n").split("\n")
        writes[mod_path].append((mb[0], mb[1], merged))

for key, f, s in results:
    print(f"{s:45} {key:58} {f.split('/')[-1]}")

if apply:
    for path, edits in writes.items():
        lines, bom, crlf = read(path)
        for s, e, new in sorted(edits, reverse=True):
            lines[s:e + 1] = new
        text = "\n".join(lines)
        if crlf:
            text = text.replace("\n", "\r\n")
        open(path, "wb").write((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
        print(f"wrote {len(edits)} block(s) into {os.path.relpath(path, MOD)}")
