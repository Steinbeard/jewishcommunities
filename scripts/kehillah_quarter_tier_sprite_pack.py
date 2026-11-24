"""Pack reviewed Quarter tier sheets into CK3 domicile DDS sprites and hit masks.

Run: python scripts/kehillah_quarter_tier_sprite_pack.py

The sheet art is retained unchanged. Each generated sprite is placed on a
transparent 512px canvas with one scale shared by every tier of its family,
so upgrading visibly grows the building without moving its ground baseline.
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
    "beit_midrash": (370, 325),
    "kahal_house": (340, 290),
    "hekdesh": (345, 275),
    "market_stalls": (370, 230),
    "workshops": (350, 275),
    "bankers_row": (330, 275),
    "funduq": (365, 285),
    "wall": (350, 260),
}
MANUAL_CUTS = {
    ("beit_midrash", "mena"): (413, 790, 1180, 1577),
    ("wall", "mena"): (395, 830, 1320),
}
SIZE = 512
BOTTOM_MARGIN = 22


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
        size = (max(1, round(cell.width * scale)), max(1, round(cell.height * scale)))
        cell = cell.resize(size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        canvas.alpha_composite(cell, ((SIZE - cell.width) // 2, SIZE - BOTTOM_MARGIN - cell.height))
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
