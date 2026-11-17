"""Re-apply the mod's window_domicile.gui edits onto the 1.21 file.

Mod edits (diff of 1.20.1 base vs mod):
  - every bookmark tab / building-panel opener also clears 'kehillah_lib_panel_open'
  - a Kehillah library tab after the last vanilla bookmark tab
  - the window's _hide state clears the library variables
  - the attached library widget as the window's last child
1.21 adds Debtors and Artifacts tabs; they get the same clear line, and our tab clears them.
"""
import re, sys

ours_p, theirs_p, out_p = sys.argv[1:4]
ours = open(ours_p, encoding="utf-8-sig").read().split("\n")
new = open(theirs_p, encoding="utf-8-sig").read().split("\n")

# Blocks taken verbatim from the mod copy (1-based line numbers of the mod's file).
def block(a, b):
    return ours[a - 1:b]

tab = block(216, 238)
hide = block(271, 276)
widget = block(1698, 1747)
assert tab[0].strip().startswith("### KEHILLAH LIBRARY") or "button_tab_vertical_bookmark" in tab[1], tab[:2]
assert all("kehillah_lib" in l for l in hide), hide
assert "Kehillah addition" in widget[0] and widget[-1].strip() == "}", (widget[0], widget[-1])

# Our tab must also clear the two 1.21 tabs.
tab = [l for l in tab]
for i, l in enumerate(tab):
    if "Clear( 'bookmark_disciples' )" in l:
        ind = l[: len(l) - len(l.lstrip())]
        tab[i + 1:i + 1] = [ind + "onclick = \"[GetVariableSystem.Clear( 'bookmark_debtors' )]\"",
                            ind + "onclick = \"[GetVariableSystem.Clear( 'bookmark_artifacts' )]\""]
        break
else:
    sys.exit("tab: disciples clear line not found")

out = []
clear_added = 0
opener = re.compile(r"""onclick = "\[GetVariableSystem\.(Toggle\( 'bookmark_\w+' \)|Set\( 'show_building_panel', 'true' \))\]\"""")
for l in new:
    out.append(l)
    if opener.search(l):
        ind = l[: len(l) - len(l.lstrip())]
        out.append(ind + "onclick = \"[GetVariableSystem.Clear( 'kehillah_lib_panel_open' )]\"")
        clear_added += 1

# Insert our tab after the last vanilla bookmark tab: the artifacts tab block.
start = next(i for i, l in enumerate(out) if "### DOMICILE BOOKMARK ARTIFACTS" in l)
depth, i = 0, start + 1
while True:
    depth += out[i].count("{") - out[i].count("}")
    i += 1
    if depth == 0 and "{" in "".join(out[start + 1:i]):
        break
out[i:i] = [""] + tab
tab_at = i

# Window-level _hide state: the first "name = _hide" at two tabs of indentation.
h = next(i for i, l in enumerate(out) if l == "\t\tname = _hide")
s = next(i for i in range(h, h + 6) if out[i].strip() == "using = Sound_WindowHide_Standard")
out[s + 1:s + 1] = hide

# The library widget: last child of the window, i.e. before the column-0 "}" that closes `window = {`.
w0 = next(i for i, l in enumerate(out) if l.startswith("window = {"))
depth = 0
for j in range(w0, len(out)):
    depth += out[j].count("{") - out[j].count("}")
    if depth == 0:
        break
assert out[j] == "}", repr(out[j])
out[j:j] = [""] + widget

open(out_p, "w", encoding="utf-8-sig", newline="\n").write("\n".join(out))
print(f"clear lines added: {clear_added}; tab at line {tab_at + 2}; widget before line {j + 2}")
