"""Build the Quarter's regional, staged domicile building sprites and masks.

Run: python scripts/kehillah_quarter_building_art.py
The PNG sources are already isolated; this step only scales and packs them
onto CK3's 512px canvas and derives the matching intersection masks.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = 512
BOTTOM_MARGIN = 24
FAMILIES = {
    "synagogue": (1, 3, 5),
    "beit_midrash": (1, 3, 5),
    "wall": (1, 3),
    "wall_site": (0,),
}
BOUNDS = {
    "synagogue": (420, 345),
    "beit_midrash": (370, 320),
    "wall": (360, 280),
    "wall_site": (360, 160),
}


def build(family: str, region: str, stage: int) -> None:
    source_name = (
        f"kehillah_synagogue_{region}_v2"
        if family == "synagogue" and stage == 1
        else f"kehillah_{family}_{region}_s{stage}"
    )
    output_name = f"kehillah_{family}_{region}_s{stage}"
    image = Image.open(SOURCE / f"{source_name}.png").convert("RGBA")
    bounds = image.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
    if bounds is None:
        raise ValueError(f"Empty source art: {source_name}")
    image = image.crop(bounds)
    max_width, max_height = BOUNDS[family]
    scale = min(max_width / image.width, max_height / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
    )
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((SIZE - image.width) // 2, SIZE - BOTTOM_MARGIN - image.height))
    mask = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    mask_alpha = canvas.getchannel("A").point(lambda value: 255 if value > 40 else 0)
    if family == "wall_site":
        # The open passage is transparent but should still be clickable.
        from PIL import ImageDraw
        bounds = mask_alpha.getbbox()
        if bounds:
            ImageDraw.Draw(mask_alpha).rectangle(bounds, fill=255)
    mask.putalpha(mask_alpha)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT / f"{output_name}.dds")
    mask.save(OUTPUT / f"{output_name}_mask.png")


if __name__ == "__main__":
    for family_name, stages in FAMILIES.items():
        for region_name in ("western", "mena"):
            for stage_number in stages:
                build(family_name, region_name, stage_number)
