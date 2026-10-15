"""Build the small, deterministic DDS strips used by the Beit Midrash shelf.

Run with Pillow from the repository root.  Frames are 1-indexed in CK3 GUI.
The source stays here so the borders can be revised without repainting a DDS.
"""

from pathlib import Path
from PIL import Image, ImageDraw
import math


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "gfx/interface/icons/kehillah_library"
OUT.mkdir(parents=True, exist_ok=True)
SCALE = 4


def xy(value):
    return round(value * SCALE)


def rank_frame(metal, shine, shade, jewel, ornament):
    size = 64 * SCALE
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # A narrow dark interior preserves the book artwork; the metallic rim
    # remains legible even at the 56-pixel shelf size.
    d.rounded_rectangle((xy(2), xy(2), xy(62), xy(62)), radius=xy(7), fill=(20, 18, 18, 160), outline=shade, width=xy(3))
    d.rounded_rectangle((xy(5), xy(5), xy(59), xy(59)), radius=xy(5), outline=metal, width=xy(3))
    d.rounded_rectangle((xy(8), xy(8), xy(56), xy(56)), radius=xy(3), outline=shine, width=xy(1))
    for cx, cy in ((7, 7), (57, 7), (7, 57), (57, 57)):
        r = 3 if ornament >= 2 else 2
        d.ellipse((xy(cx-r), xy(cy-r), xy(cx+r), xy(cy+r)), fill=metal, outline=shine, width=xy(1))
    if ornament >= 2:
        for x, y in ((32, 5), (32, 59), (5, 32), (59, 32)):
            d.polygon([(xy(x), xy(y-3)), (xy(x+3), xy(y)), (xy(x), xy(y+3)), (xy(x-3), xy(y))], fill=shade, outline=shine)
    if ornament >= 3:
        for x in (20, 44):
            d.arc((xy(x-7), xy(1), xy(x+7), xy(16)), 190, 350, fill=shine, width=xy(1))
            d.arc((xy(x-7), xy(48), xy(x+7), xy(63)), 10, 170, fill=shine, width=xy(1))
    if jewel:
        d.polygon([(xy(32), xy(3)), (xy(36), xy(7)), (xy(32), xy(11)), (xy(28), xy(7))], fill=jewel, outline=shine)
    return im.resize((64, 64), Image.Resampling.LANCZOS)


def ring_frame(total, mastered):
    size = 32 * SCALE
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    box = (xy(4), xy(4), xy(28), xy(28))
    gap = 5
    for i in range(total):
        start = -90 + i * 360 / total + gap
        end = -90 + (i + 1) * 360 / total - gap
        color = (93, 184, 103, 255) if i < mastered else (79, 81, 75, 220)
        d.arc(box, start, end, fill=color, width=xy(5))
    if mastered == total:
        d.line([(xy(11), xy(16)), (xy(15), xy(20)), (xy(22), xy(12))], fill=(160, 234, 148, 255), width=xy(2), joint="curve")
    return im.resize((32, 32), Image.Resampling.LANCZOS)


rank_specs = [
    ((196, 153, 61, 255), (250, 220, 133, 255), (77, 48, 72, 255), (146, 70, 150, 255), 3),  # imperial
    ((192, 152, 65, 255), (241, 207, 117, 255), (77, 54, 31, 255), (155, 46, 44, 255), 2),  # royal
    ((148, 167, 186, 255), (219, 229, 230, 255), (46, 69, 96, 255), None, 2),              # ducal
    ((151, 112, 73, 255), (205, 161, 106, 255), (65, 51, 43, 255), None, 1),              # comital
]
rank = Image.new("RGBA", (64 * len(rank_specs), 64))
for index, spec in enumerate(rank_specs):
    rank.paste(rank_frame(*spec), (index * 64, 0))
rank.save(OUT / "kehillah_sefer_rank_frames.dds")

for total in (1, 4, 6):
    strip = Image.new("RGBA", (32 * (total + 1), 32))
    for mastered in range(total + 1):
        strip.paste(ring_frame(total, mastered), (mastered * 32, 0))
    strip.save(OUT / f"kehillah_mastery_ring_{total}.dds")
