"""Composite actual Quarter DDS assets at declared slot geometry for layout QA.

Run: python scripts/kehillah_quarter_scene_preview.py
This is a static source preview, not CK3's interactive render or draw order.
"""

from pathlib import Path
import re

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
TYPE = (ROOT / "common/domiciles/types/kehillah_domicile_types.txt").read_text(encoding="utf-8-sig")
GFX = ROOT / "gfx/interface/window_domiciles"
OUT = ROOT / "docs/implementation/assets/kehillah_quarter_v5_layout_preview.png"
SCENE = (1206, 556)
SLOTS = (
    ("main_slot", "synagogue"),
    ("external_slot_1", "beit_midrash"),
    ("external_slot_2", "kahal_house"),
    ("external_slot_3", "hekdesh"),
    ("external_slot_4", "wall"),
    ("external_slot_5", "workshops"),
    ("external_slot_6", "bankers_row"),
    ("external_slot_7", "market_stalls"),
    ("external_slot_8", "funduq"),
)


def geometry(slot: str) -> tuple[int, int, int, int]:
    section = re.search(rf"\b{slot}\s*=\s*\{{(.*?)\n\s*\}}", TYPE, re.S)
    if not section:
        raise ValueError(f"Missing {slot}")
    position = re.search(r"position\s*=\s*\{\s*([\d.]+)%\s+([\d.]+)%", section[1])
    size = re.search(r"size\s*=\s*\{\s*([\d.]+)%\s+([\d.]+)%", section[1])
    if not position or not size:
        raise ValueError(f"Missing geometry for {slot}")
    return tuple(round(float(value) * dimension / 100) for value, dimension in zip(
        (*position.groups(), *size.groups()), (*SCENE, *SCENE)
    ))


def render(region: str, developed: bool) -> Image.Image:
    scene = Image.open(GFX / f"kehillah_quarter_background_{region}.dds").convert("RGBA")
    scene = scene.resize(SCENE, Image.Resampling.LANCZOS)
    for slot, family in SLOTS:
        level = "s3" if developed else "s0" if family == "wall" else "s1"
        sprite = Image.open(GFX / f"kehillah_quarter_v4_{family}_{region}_{level}.dds").convert("RGBA")
        x, y, width, height = geometry(slot)
        scene.alpha_composite(sprite.resize((width, height), Image.Resampling.LANCZOS), (x, y))
    return scene.convert("RGB")


def main() -> None:
    canvas = Image.new("RGB", (SCENE[0] * 2, SCENE[1] * 2))
    for row, region in enumerate(("western", "mena")):
        for column, developed in enumerate((False, True)):
            canvas.paste(render(region, developed), (column * SCENE[0], row * SCENE[1]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)


if __name__ == "__main__":
    main()
