"""Build the two 2412x1112 CK3 Jewish Quarter background textures.

Run: python scripts/kehillah_quarter_background_art.py
The base paintings stay untouched. Residential infill, ordinary street props,
and static figures make a starter Quarter feel inhabited without implying that
an optional institution has already been built. DDS uses vanilla's DXT1 format.
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
PROP_EDGES = (0, 435, 870, 1305, 1740, 2172)
# Ground-level props sit beside paths or background houses, away from the
# modular building footprints. Donkey cell 3 is reserved for a later pass.
PROP_SITES = (
    (0, 690, 675, 78),  # communal well, near the walking residents
    (1, 305, 602, 48),  # baskets beside the left lane
    (2, 1400, 280, 48), # produce near the rear stalls
    (4, 1485, 655, 60), # washing beside the right-side garden
)
INFILL_EDGES = (0, 1086, 2172)
# Both clusters sit behind upgradeable sprites. The second house row now
# occupies the rear court behind the Synagogue, where its roof remains visible
# and the foreground Synagogue covers its lower edge.
INFILL_SITES = (
    (0, 585, 470, 145),
    (1, 815, 385, 145),
)


def sheet_cell(region: str, kind: str, edges: tuple[int, ...], index: int) -> Image.Image:
    sheet = Image.open(SOURCE / f"kehillah_quarter_{kind}_{region}.png").convert("RGBA")
    crop = sheet.crop((edges[index], 0, edges[index + 1], sheet.height))
    pixels = np.asarray(crop).copy()
    pixels[pixels[:, :, 3] < 24] = (0, 0, 0, 0)
    if kind == "residential_infill":
        # Image-generation's transparent cutouts have a few stray red edge
        # pixels; remove them before scaling into the town painting.
        fringe = ((pixels[:, :, 0] > 180) & (pixels[:, :, 1] < 85)
                  & (pixels[:, :, 2] < 85))
        pixels[fringe] = (0, 0, 0, 0)
    crop = Image.fromarray(pixels, "RGBA")
    bounds = crop.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"Empty {kind} cell {region} {index}")
    crop = crop.crop(bounds)
    # New figures should belong to the same soft palette as the town scene.
    color = ImageEnhance.Color(crop.convert("RGB")).enhance(0.82)
    color.putalpha(crop.getchannel("A"))
    return color


def place(image: Image.Image, figure: Image.Image, centre_x: int, ground_y: int, height: int) -> None:
    width = round(figure.width * height / figure.height)
    figure = figure.resize((width, height), Image.Resampling.LANCZOS)
    image.alpha_composite(figure, (round(centre_x - width / 2), ground_y - height))


def build(region: str) -> None:
    name = f"kehillah_quarter_background_{region}"
    image = Image.open(SOURCE / f"{name}_v2.png").convert("RGBA")
    aspect_error = abs(image.width / image.height - SIZE[0] / SIZE[1])
    if aspect_error > 0.01:
        raise ValueError(f"Unexpected source aspect ratio for {name}: {image.size}")
    for index, centre_x, ground_y, height in INFILL_SITES:
        place(image, sheet_cell(region, "residential_infill", INFILL_EDGES, index), centre_x, ground_y, height)
    for index, centre_x, ground_y, height in PROP_SITES:
        place(image, sheet_cell(region, "street_props", PROP_EDGES, index), centre_x, ground_y, height)
    for index, centre_x, ground_y, height in AMBIENT_SITES[region]:
        place(image, sheet_cell(region, "ambient_figures", SHEET_EDGES[region], index), centre_x, ground_y, height)
    image = image.convert("RGB")
    image.save(SOURCE / f"{name}_lived_v4.png")
    image = image.resize(SIZE, Image.Resampling.LANCZOS)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / f"{name}.dds", pixel_format="DXT1")


if __name__ == "__main__":
    for region_name in ("western", "mena"):
        build(region_name)
