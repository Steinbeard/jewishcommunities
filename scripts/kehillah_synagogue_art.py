"""Rebuild the two Synagogue domicile sprites from their transparent source PNGs.

Run from any directory: python scripts/kehillah_synagogue_art.py
The 512px DDS and matching alpha mask share a canvas so CK3's intersection
mask follows the painted silhouette. The source PNGs are kept for later edits.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = 512
BOTTOM_MARGIN = 24
MAX_WIDTH = 420
MAX_HEIGHT = 345


def build(region: str) -> None:
    name = f"kehillah_synagogue_{region}_v2"
    source = Image.open(SOURCE / f"{name}.png").convert("RGBA")
    alpha = source.getchannel("A")
    bounds = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if bounds is None:
        raise ValueError(f"Empty source art: {name}")
    source = source.crop(bounds)
    scale = min(MAX_WIDTH / source.width, MAX_HEIGHT / source.height)
    source = source.resize(
        (round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS
    )
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    x = (SIZE - source.width) // 2
    y = SIZE - BOTTOM_MARGIN - source.height
    canvas.alpha_composite(source, (x, y))

    # Vanilla masks are white RGB with alpha matching the texture silhouette.
    mask_alpha = canvas.getchannel("A").point(lambda value: 255 if value > 40 else 0)
    mask = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
    mask.putalpha(mask_alpha)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT / f"{name}.dds")
    mask.save(OUTPUT / f"{name}_mask.png")


if __name__ == "__main__":
    for region_name in ("western", "mena"):
        build(region_name)
