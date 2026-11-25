"""Pack reviewed Quarter tier sheets into CK3 domicile DDS sprites and hit masks.

Run: python scripts/kehillah_quarter_tier_sprite_pack.py

The sheet art is retained unchanged. Each generated sprite is placed on a
transparent 512px canvas with a common family scale. The first Hekdesh stage
gets a modest lift so it is legible at the same scene scale as its neighbors.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
PREVIEW = ROOT / "docs" / "implementation" / "assets"
REGIONS = ("western", "mena")
FAMILIES = {
    "synagogue": 5,
    "beit_midrash": 5,
    "kahal_house": 3,
    "hekdesh": 3,
    "market_stalls": 3,
    "workshops": 3,
    "bankers_row": 3,
    "funduq": 3,
    "wall": 4,  # site 0 plus walls 1-3
}
MAX_BOUNDS = {
    "synagogue": (420, 350),
    "beit_midrash": (450, 390),
    "kahal_house": (390, 330),
    "hekdesh": (430, 335),
    "market_stalls": (450, 280),
    "workshops": (430, 335),
    "bankers_row": (380, 320),
    "funduq": (430, 335),
    "wall": (400, 300),
}
MANUAL_CUTS = {
    ("beit_midrash", "mena"): (413, 790, 1180, 1577),
    ("wall", "mena"): (395, 830, 1320),
}
SIZE = 512
# CK3 puts a slot's label near its top, then maps the full 512px sprite
# canvas into that slot. Earlier art sat on the canvas bottom, leaving a
# large empty band between labels and low-tier buildings. These margins
# lift each painted building while allowing later tiers to grow downward.
BOTTOM_MARGIN = {
    "synagogue": (35, 35, 35, 35, 35),
    "beit_midrash": (200, 180, 160, 140, 120),
    "kahal_house": (200, 170, 140),
    "hekdesh": (220, 185, 150),
    "market_stalls": (185, 175, 165),
    "workshops": (220, 185, 150),
    "bankers_row": (190, 165, 140),
    "funduq": (205, 180, 155),
    "wall": (210, 190, 165, 135),
}
MAIN_WIDTH_CORRECTION = 0.72


def visible_runs(alpha: np.ndarray, expected: int) -> list[tuple[int, int]]:
    projection = (alpha > 80).sum(axis=0)
    active = projection > 8
    starts = np.flatnonzero(active & ~np.r_[False, active[:-1]])
    ends = np.flatnonzero(active & ~np.r_[active[1:], False]) + 1
    runs = [(int(a), int(b)) for a, b in zip(starts, ends)]
    # A window or a pair of open entrance posts can form adjacent components.
    while len(runs) > expected:
        gaps = [runs[i + 1][0] - runs[i][1] for i in range(len(runs) - 1)]
        index = int(np.argmin(gaps))
        runs[index : index + 2] = [(runs[index][0], runs[index + 1][1])]
    if len(runs) != expected:
        raise ValueError(f"Expected {expected} sprite runs; found {runs}")
    return runs


def sheet_cells(family: str, region: str) -> list[Image.Image]:
    if family in ("wall", "funduq"):
        sheet = Image.open(
            SOURCES / f"kehillah_quarter_walls_funduq_{region}_concept.png"
        ).convert("RGBA")
        y0, y1 = (0, 430) if family == "wall" else (430, sheet.height)
        strip = sheet.crop((0, y0, sheet.width, y1))
    else:
        strip = Image.open(
            SOURCES / f"kehillah_quarter_tier_sheet_{family}_{region}.png"
        ).convert("RGBA")
    count = FAMILIES[family]
    cuts = MANUAL_CUTS.get((family, region))
    if cuts:
        edges = (0, *cuts, strip.width)
        cells = [strip.crop((edges[i], 0, edges[i + 1], strip.height)) for i in range(count)]
    else:
        alpha = np.asarray(strip.getchannel("A"))
        runs = visible_runs(alpha, count)
        cells = [strip.crop((max(0, a - 8), 0, min(strip.width, b + 8), strip.height)) for a, b in runs]
    cleaned = []
    for cell in cells:
        pixels = np.asarray(cell).copy()
        # Imagegen places bright red/yellow noise at alpha 1-5 around edges.
        # Remove low-alpha pixels before resizing to prevent DDS bleed.
        pixels[pixels[:, :, 3] < 24] = (0, 0, 0, 0)
        cell = Image.fromarray(pixels, "RGBA")
        bounds = cell.getchannel("A").getbbox()
        if not bounds:
            raise ValueError(f"Empty {family} {region} sheet cell")
        cleaned.append(cell.crop(bounds))
    return cleaned


def pack(cells: list[Image.Image], family: str, region: str) -> list[Image.Image]:
    max_width, max_height = MAX_BOUNDS[family]
    scale = min(
        max_width / max(cell.width for cell in cells),
        max_height / max(cell.height for cell in cells),
    )
    packed = []
    for index, cell in enumerate(cells):
        stage_scale = scale
        if family == "hekdesh" and index == 0:
            # The generated first stage has a much smaller footprint than
            # its siblings; fill more of the fixed slot without redrawing it.
            stage_scale *= min(1.33, 420 / (cell.width * scale))
        if family == "workshops" and index == 0:
            # Give the first craft stall a readable footprint while keeping
            # it smaller than the second and third stages.
            stage_scale *= min(1.23, 310 / (cell.width * scale))
        width = cell.width * stage_scale
        if family == "synagogue":
            # CK3's main slot is 28% wide but only 34.5% high; mapping a
            # square texture into it otherwise makes the hall look squat.
            width *= MAIN_WIDTH_CORRECTION
        size = (max(1, round(width)), max(1, round(cell.height * stage_scale)))
        cell = cell.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        bottom = BOTTOM_MARGIN[family][index]
        y = SIZE - bottom - cell.height
        if y < 0:
            raise ValueError(f"{family} {region} stage {index} does not fit its canvas")
        canvas.alpha_composite(cell, ((SIZE - cell.width) // 2, y))
        alpha = canvas.getchannel("A")
        mask_alpha = alpha.point(lambda value: 255 if value > 40 else 0)
        if family == "wall" and index == 0:
            # Preserve a generous click target between the entrance posts.
            bounds = mask_alpha.getbbox()
            if bounds:
                ImageDraw.Draw(mask_alpha).rectangle(bounds, fill=255)
        mask = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 0))
        mask.putalpha(mask_alpha)
        suffix = f"s{index if family == 'wall' else index + 1}"
        stem = f"kehillah_quarter_v4_{family}_{region}_{suffix}"
        OUTPUT.mkdir(parents=True, exist_ok=True)
        canvas.save(OUTPUT / f"{stem}.dds")
        mask.save(OUTPUT / f"{stem}_mask.png")
        packed.append(canvas)
    return packed


def main() -> None:
    contact = Image.new("RGB", (SIZE * 5, SIZE * 9 * 2), "#c7ad82")
    draw = ImageDraw.Draw(contact)
    for row, family in enumerate(FAMILIES):
        for region_index, region in enumerate(REGIONS):
            cells = sheet_cells(family, region)
            packed = pack(cells, family, region)
            y = (row * 2 + region_index) * SIZE
            draw.text((8, y + 8), f"{family} / {region}", fill="black")
            for column, canvas in enumerate(packed):
                contact.paste(canvas, (column * SIZE, y), canvas)
            print(f"packed {family} {region}: {len(packed)}")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    contact.resize((1280, 4608), Image.Resampling.LANCZOS).save(
        PREVIEW / "kehillah_quarter_v4_sprite_contact.png"
    )


if __name__ == "__main__":
    main()
