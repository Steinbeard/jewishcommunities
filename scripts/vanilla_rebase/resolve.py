"""Resolve git merge-file conflict hunks by index.

usage: resolve.py MERGED_FILE CHOICES
CHOICES is a comma list, one per conflict in order: ours | theirs | both (ours then theirs) | rboth (theirs then ours)
Writes the file in place; refuses if the number of choices does not match the number of conflicts.
"""
import sys

path, choices = sys.argv[1], sys.argv[2].split(",")
lines = open(path, encoding="utf-8-sig").read().split("\n")
out, i, n = [], 0, 0
while i < len(lines):
    if lines[i].startswith("<<<<<<< "):
        ours, theirs, j = [], [], i + 1
        while not lines[j].startswith("======="):
            ours.append(lines[j]); j += 1
        j += 1
        while not lines[j].startswith(">>>>>>> "):
            theirs.append(lines[j]); j += 1
        if n >= len(choices):
            sys.exit(f"more conflicts than choices ({len(choices)})")
        c = choices[n]
        out += {"ours": ours, "theirs": theirs, "both": ours + theirs, "rboth": theirs + ours}[c]
        n += 1
        i = j + 1
    else:
        out.append(lines[i]); i += 1
if n != len(choices):
    sys.exit(f"{n} conflicts but {len(choices)} choices")
open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"{path}: resolved {n}")
