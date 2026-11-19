"""Copy merged results into the port worktree, keeping each file's original BOM and CRLF line endings."""
import os, sys

MOD = r"C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\mod\jewishcommunities-1.21-port"
MERGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "merge")
FILES = {
    "common/activities/activity_types/pilgrimage.txt": "merged",
    "common/struggle/struggles/iberian_struggle_script.txt": "merged",
    "common/succession_election/00_pam_clerical_elective.txt": "merged",
    "common/decisions/dlc_decisions/ep_3/06_ep3_laamp_decisions.txt": "merged",
    "gui/shared/mapmodes.gui": "merged",
    "gui/window_character.gui": "merged",
    "gui/window_county_view.gui": "merged",
    "gui/window_domicile.gui": "merged",
    "gui/window_military.gui": "merged",
    "gui/window_my_realm.gui": "reins",
    "gui/window_title_appointment.gui": "merged",
}
for rel, kind in FILES.items():
    dst = os.path.join(MOD, rel)
    src = os.path.join(MERGE, rel.replace("/", "_") + "." + kind)
    orig = open(dst, "rb").read()
    bom = orig.startswith(b"\xef\xbb\xbf")
    text = open(src, encoding="utf-8-sig").read().replace("\r", "")
    if "<<<<<<<" in text or ">>>>>>>" in text:
        sys.exit(f"conflict markers left in {src}")
    data = text.replace("\n", "\r\n").encode("utf-8")
    open(dst, "wb").write((b"\xef\xbb\xbf" if bom else b"") + data)
    print(f"{rel}: {len(text.splitlines())} lines")
