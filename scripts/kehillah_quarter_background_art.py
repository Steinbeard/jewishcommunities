"""Build the two 2412x1112 CK3 Jewish Quarter background textures.

Run: python scripts/kehillah_quarter_background_art.py
Sources are generated paintings in scripts/quarter_scene_sources. The DDS files
use DXT1, the same opaque texture format as vanilla estate backgrounds.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = (2412, 1112)


def build(region: str) -> None:
    name = f"kehillah_quarter_background_{region}"
    image = Image.open(SOURCE / f"{name}.png").convert("RGB")
    aspect_error = abs(image.width / image.height - SIZE[0] / SIZE[1])
    if aspect_error > 0.01:
        raise ValueError(f"Unexpected source aspect ratio for {name}: {image.size}")
    image = image.resize(SIZE, Image.Resampling.LANCZOS)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / f"{name}.dds", pixel_format="DXT1")


if __name__ == "__main__":
    for region_name in ("western", "mena"):
        build(region_name)
