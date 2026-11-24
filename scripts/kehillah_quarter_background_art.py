"""Build the two 2412x1112 CK3 Jewish Quarter background textures.

Run: python scripts/kehillah_quarter_background_art.py
The base paintings stay untouched. Small, static figure clusters are packed
into the open street to make even a low-tier Quarter feel inhabited. DDS files
use DXT1, the same opaque texture format as vanilla estate backgrounds.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = (2412, 1112)
SHEET_EDGES = {
    "western": (0, 300, 575, 815, 1140, 1480, 1846),
    "mena": (0, 360, 700, 1000, 1370, 1790, 2172),
}
# (sheet cell, centre x, ground y, height in 1846x852 base scene pixels)
# All sites are ordinary passersby or objects, not a constructed specialisation.
AMBIENT_SITES = {
    "western": ((0, 765, 733, 64), (1, 440, 565, 64),
                (2, 470, 800, 51), (3, 1365, 398, 62),
                (4, 1285, 742, 63), (5, 1050, 800, 31)),
    "mena": ((0, 860, 720, 64), (1, 430, 548, 64),
             (2, 510, 797, 51), (3, 1360, 402, 62),
             (4, 1260, 737, 63), (5, 1050, 795, 31)),
}


def ambient_figure(region: str, index: int) -> Image.Image:
    sheet = Image.open(SOURCE / f"kehillah_quarter_ambient_figures_{region}.png").convert("RGBA")
    edges = SHEET_EDGES[region]
    crop = sheet.crop((edges[index], 0, edges[index + 1], sheet.height))
    pixels = np.asarray(crop).copy()
    pixels[pixels[:, :, 3] < 24] = (0, 0, 0, 0)
    crop = Image.fromarray(pixels, "RGBA")
    bounds = crop.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"Empty ambient figure cell {region} {index}")
    crop = crop.crop(bounds)
    # New figures should belong to the same soft palette as the town scene.
    color = ImageEnhance.Color(crop.convert("RGB")).enhance(0.82)
    color.putalpha(crop.getchannel("A"))
    return color


def build(region: str) -> None:
    name = f"kehillah_quarter_background_{region}"
    image = Image.open(SOURCE / f"{name}_v2.png").convert("RGBA")
    aspect_error = abs(image.width / image.height - SIZE[0] / SIZE[1])
    if aspect_error > 0.01:
        raise ValueError(f"Unexpected source aspect ratio for {name}: {image.size}")
    for index, centre_x, ground_y, height in AMBIENT_SITES[region]:
        figure = ambient_figure(region, index)
        width = round(figure.width * height / figure.height)
        figure = figure.resize((width, height), Image.Resampling.LANCZOS)
        image.alpha_composite(figure, (round(centre_x - width / 2), ground_y - height))
    image = image.convert("RGB")
    image.save(SOURCE / f"{name}_lived_v3.png")
    image = image.resize(SIZE, Image.Resampling.LANCZOS)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / f"{name}.dds", pixel_format="DXT1")


if __name__ == "__main__":
    for region_name in ("western", "mena"):
        build(region_name)
