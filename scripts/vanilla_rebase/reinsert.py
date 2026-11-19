"""Re-apply the mod's edits to a vanilla file onto the new game version, hunk by hunk.

usage: reinsert.py BASE OURS THEIRS OUT
For each hunk of difflib(base -> ours):
  insert : find the base lines just before (or just after) the hunk in THEIRS, by unique
           whitespace-insensitive match of a growing context window; insert our lines there.
  replace/delete : find the base lines being replaced in THEIRS (unique match); if found
           unchanged, swap them for ours; otherwise report as MANUAL.
Writes OUT and prints one line per hunk: OK / MANUAL with positions.
"""
import difflib, sys

base_p, ours_p, theirs_p, out_p = sys.argv[1:5]
rd = lambda p: open(p, encoding="utf-8-sig").read().replace("\r", "").split("\n")
base, ours, theirs = rd(base_p), rd(ours_p), rd(theirs_p)
norm = lambda l: " ".join(l.split())
nt = [norm(l) for l in theirs]


def find_unique(seq):
    """Positions in theirs where the normalised seq occurs; seq is a list of lines."""
    s = [norm(l) for l in seq]
    if not any(s):
        return []
    hits = []
    for i in range(len(nt) - len(s) + 1):
        if nt[i:i + len(s)] == s:
            hits.append(i)
            if len(hits) > 1:
                break
    return hits


def anchor_before(i1):
    """theirs index *after* which base[:i1] ends, using growing context."""
    for k in range(3, 40):
        if i1 - k < 0:
            break
        h = find_unique(base[i1 - k:i1])
        if len(h) == 1:
            return h[0] + k
        if not h:
            break
    return None


def anchor_after(i2):
    for k in range(3, 40):
        if i2 + k > len(base):
            break
        h = find_unique(base[i2:i2 + k])
        if len(h) == 1:
            return h[0]
        if not h:
            break
    return None


ops = [o for o in difflib.SequenceMatcher(None, base, ours, autojunk=False).get_opcodes() if o[0] != "equal"]
edits = []  # (theirs_start, theirs_end, new_lines, label)
report = []
for tag, i1, i2, j1, j2 in ops:
    new_lines = ours[j1:j2]
    label = f"base {i1+1}-{i2} -> mod {j1+1}-{j2} ({tag}, +{j2-j1}/-{i2-i1})"
    if all(not norm(l) for l in new_lines + base[i1:i2]):
        report.append(f"SKIP  {label}: whitespace only")
        continue
    if tag == "insert":
        p = anchor_before(i1)
        if p is None:
            p = anchor_after(i2)
        if p is None:
            report.append(f"MANUAL {label}: no unique anchor")
            continue
        edits.append((p, p, new_lines, label))
        report.append(f"OK    {label}: insert at theirs {p+1}")
    else:
        old = base[i1:i2]
        h = find_unique(old) if len([l for l in old if norm(l)]) >= 2 else []
        if len(h) != 1:
            # short replaced span: anchor on context around it, require the span unchanged
            a = anchor_before(i1)
            if a is not None and [norm(l) for l in theirs[a:a + len(old)]] == [norm(l) for l in old]:
                h = [a]
        if len(h) == 1:
            edits.append((h[0], h[0] + len(old), new_lines, label))
            report.append(f"OK    {label}: replace theirs {h[0]+1}-{h[0]+len(old)}")
        else:
            report.append(f"MANUAL {label}: replaced vanilla lines changed or not unique in 1.21")

edits.sort(key=lambda e: (e[0], e[1]))
for a, b in zip(edits, edits[1:]):
    if b[0] < a[1]:
        report.append(f"OVERLAP {a[3]} / {b[3]}")
out = list(theirs)
for s, e, lines, _ in reversed(edits):
    out[s:e] = lines
open(out_p, "w", encoding="utf-8-sig", newline="\n").write("\n".join(out))
print("\n".join(report))
print(f"hunks: {len(ops)}, applied: {len(edits)}, manual: {sum(r.startswith('MANUAL') for r in report)}")
