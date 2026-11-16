"""Build the minimal native pilgrimage overlay and three revival tenet icons.

Review the copied pilgrimage definition against the installed game on upgrades.
The overlay preserves all native behavior and adds one host intent plus a
completion hook while the activity scope still exists.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game")
TENETS = ("tenet_kehillah_messianic_hope", "tenet_kehillah_prophetic_revelation", "tenet_kehillah_temple_service")


def build():
    path = ROOT / "common/activities/activity_types/pilgrimage.txt"
    # Same filename replaces the native file without a duplicate definition.
    # Preserve local additions if this override already exists.
    source = path if path.exists() else GAME / "common/activities/activity_types/pilgrimage.txt"
    pilgrimage = source.read_text(encoding="utf-8-sig")
    old = "intents = { reflection_intent altruism_intent zealot_intent }"
    if "kehillah_offer_sacrifice_intent" not in pilgrimage:
        assert pilgrimage.count(old) == 1
        pilgrimage = pilgrimage.replace(old, "intents = { reflection_intent altruism_intent zealot_intent kehillah_offer_sacrifice_intent }")
    assert pilgrimage.count("\ton_complete = {") == 1
    if "kehillah_complete_sacrifice_intent_effect" not in pilgrimage:
        pilgrimage = pilgrimage.replace("\ton_complete = {", "\ton_complete = {\n        kehillah_complete_sacrifice_intent_effect = yes", 1)
    path.write_text(pilgrimage, encoding="utf-8-sig", newline="\r\n")
    sheet = Image.open(ROOT / "scripts/tenet_icon_sources/kehillah_revival_sheet.png").convert("RGBA")
    output = ROOT / "gfx/interface/icons/faith_tenets"
    for i, key in enumerate(TENETS):
        art = sheet.crop((round(i * sheet.width / 3), 0, round((i + 1) * sheet.width / 3), sheet.height))
        art = art.crop(art.getchannel("A").getbbox())
        art.thumbnail((210, 300), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (260, 400), (0, 0, 0, 0))
        canvas.paste(art, ((260 - art.width) // 2, (400 - art.height) // 2))
        canvas.save(output / (key.removeprefix("tenet_") + ".dds"))


if __name__ == "__main__":
    build()
