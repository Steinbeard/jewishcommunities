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


# ---------------------------------------------------------------------------
# 2026-11-08: the Beit Midrash shelf (docs/implementation/2026-11-08-library-
# shelf-and-ledger.md). Book spines by binding tier, the Tanakh ark, the Shas
# case's volumes, the Prophets' and Writings' codices, the reading stand and
# the shelf plank. Every spine is SPINE_H tall; the binding tier sets its width
# and finish. Each tier is one strip of 12 frames: 4 colours for each genre in
# the order Parshanut, Talmudics, Machshavah (kehillah_lib_spine_frame_<flag>).
# Widths must match SPINE_WIDTH in scripts/kehillah_library_catalog.py.
# ---------------------------------------------------------------------------

SPINE_H = 80
SPINE_WIDTH = {1: 14, 2: 10, 3: 14, 4: 18, 5: 22, 6: 26, 7: 30}
GENRE_PALETTES = [
    [(150, 102, 38), (112, 70, 36), (118, 104, 44), (156, 78, 40)],   # Parshanut: honey, saddle, olive, burnt orange
    [(108, 28, 30), (150, 66, 34), (94, 32, 60), (90, 52, 32)],       # Talmudics: oxblood, rust, plum, umber
    [(46, 54, 112), (62, 86, 108), (30, 94, 98), (78, 58, 122)],      # Machshavah: indigo, slate, teal, violet
]
GOLD = (222, 178, 74, 255)
GOLD_LIGHT = (250, 222, 140, 255)


def mix(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def scale(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c[:3])


def shade_columns(im, x0, x1, y0, y1, strength=0.38):
    """Round a flat face into a spine: darker at the edges, lit in the middle."""
    px = im.load()
    w = x1 - x0
    for x in range(x0, x1):
        k = 0.74 + strength * math.sin(math.pi * (x - x0 + 0.5) / w)
        for y in range(y0, y1):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (min(255, round(r * k)), min(255, round(g * k)), min(255, round(b * k)), a)


def spine(tier, base):
    w, h = SPINE_WIDTH[tier] * SCALE, SPINE_H * SCALE
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = SCALE
    if tier == 1:  # kept to answer it: grey cloth wrapper with straps
        cloth = mix((128, 124, 116), base, 0.15)
        d.rectangle((0, 2 * S, w - 1, h - 1), fill=cloth + (255,))
        for y in (18, 58):
            d.rectangle((0, y * S, w - 1, (y + 4) * S), fill=(62, 58, 52, 255))
            d.rectangle((w // 2 - S, y * S - S, w // 2 + S, (y + 4) * S + S), fill=(150, 146, 136, 255))
        shade_columns(im, 0, w, 0, h)
    elif tier == 2:  # banned or suspect: a loose quire of pages tied with string
        page = (214, 204, 178)
        d.rectangle((0, 4 * S, w - 1, h - 1), fill=page + (255,))
        for y in range(6, SPINE_H, 3):
            d.line([(0, y * S), (w - 1, y * S)], fill=scale(page, 0.84) + (255,), width=S // 2)
        for y in range(9, SPINE_H, 7):
            d.rectangle((w - 1 - S, y * S, w - 1, (y + 2) * S), fill=(0, 0, 0, 0))
        d.rectangle((0, 40 * S, w - 1, 41 * S), fill=scale(base, 0.7) + (255,))
        d.rectangle((0, 44 * S, w - 1, 45 * S), fill=scale(base, 0.7) + (255,))
        shade_columns(im, 0, w, 0, h, 0.25)
    elif tier == 3:  # limp vellum, the cover curling at the head, a cord tie
        vel = mix((228, 216, 184), base, 0.12)
        d.rounded_rectangle((0, 3 * S, w - 1, h - 1), radius=4 * S, fill=vel + (255,))
        d.rectangle((0, 10 * S, w - 1, h - 1), fill=vel + (255,))
        d.rectangle((0, 38 * S, w - 1, 39 * S + S // 2), fill=(122, 82, 44, 255))
        d.rectangle((w // 2 - S, 39 * S, w // 2 + S, 47 * S), fill=(122, 82, 44, 255))
        d.line([(S, 14 * S), (w - S, 14 * S)], fill=scale(vel, 0.82) + (255,), width=S)
        shade_columns(im, 0, w, 0, h, 0.3)
    elif tier == 4:  # half-leather: leather head and tail, cloth sides
        cloth = mix(base, (176, 166, 146), 0.62)
        d.rectangle((0, 0, w - 1, h - 1), fill=cloth + (255,))
        for y0, y1 in ((0, 15), (65, 80)):
            d.rectangle((0, y0 * S, w - 1, y1 * S - 1), fill=base + (255,))
        for y in (15, 65):
            d.rectangle((0, y * S - S, w - 1, y * S), fill=scale(base, 0.6) + (255,))
        d.rectangle((S * 3, 30 * S, w - 1 - S * 3, 40 * S), fill=scale(base, 0.85) + (255,))
        shade_columns(im, 0, w, 0, h)
    elif tier == 5:  # tooled leather: a blind-tooled frame and raised bands
        d.rectangle((0, 0, w - 1, h - 1), fill=base + (255,))
        light = scale(base, 1.45) + (255,)
        d.rectangle((3 * S, 4 * S, w - 1 - 3 * S, h - 1 - 4 * S), outline=light, width=S)
        for y in (20, 40, 60):
            d.rectangle((0, y * S - S, w - 1, y * S + S), fill=scale(base, 0.62) + (255,))
            d.line([(0, y * S - S), (w - 1, y * S - S)], fill=light, width=S // 2)
        for cy in (12, 30, 50, 70):
            d.ellipse((w // 2 - 2 * S, cy * S - 2 * S, w // 2 + 2 * S, cy * S + 2 * S), outline=light, width=S // 2)
        shade_columns(im, 0, w, 0, h)
    elif tier == 6:  # gilt leather: gold bands and a gold-lettered label
        d.rectangle((0, 0, w - 1, h - 1), fill=base + (255,))
        for y in (8, 17, 52, 61, 70):
            d.rectangle((0, y * S - S, w - 1, y * S + S), fill=GOLD)
            d.line([(0, y * S - S), (w - 1, y * S - S)], fill=GOLD_LIGHT, width=S // 2)
        d.rectangle((3 * S, 24 * S, w - 1 - 3 * S, 45 * S), fill=scale(base, 0.45) + (255,), outline=GOLD, width=S)
        for y in (29, 34, 39):
            d.line([(6 * S, y * S), (w - 1 - 6 * S, y * S)], fill=GOLD_LIGHT, width=S)
        shade_columns(im, 0, w, 0, h)
    else:  # tier 7, the canon binding: near-black leather under heavy gold
        dark = scale(base, 0.38)
        d.rectangle((0, 0, w - 1, h - 1), fill=dark + (255,))
        d.rectangle((0, 0, w - 1, 2 * S), fill=GOLD)
        d.rectangle((0, h - 1 - 2 * S, w - 1, h - 1), fill=GOLD)
        for y in (7, 12, 64, 69):
            d.rectangle((0, y * S - S, w - 1, y * S + S), fill=GOLD)
            d.line([(0, y * S - S), (w - 1, y * S - S)], fill=GOLD_LIGHT, width=S // 2)
        d.rectangle((3 * S, 20 * S, w - 1 - 3 * S, 58 * S), outline=GOLD, width=S)
        cx, cy = w // 2, 39 * S
        r = min(w // 2 - 6 * S, 9 * S)
        d.polygon([(cx, cy - r * 2), (cx + r, cy), (cx, cy + r * 2), (cx - r, cy)], fill=GOLD, outline=GOLD_LIGHT)
        d.ellipse((cx - S * 2, cy - S * 2, cx + S * 2, cy + S * 2), fill=scale(base, 0.9) + (255,))
        shade_columns(im, 0, w, 0, h, 0.32)
    return im.resize((SPINE_WIDTH[tier], SPINE_H), Image.Resampling.LANCZOS)


for tier, width in SPINE_WIDTH.items():
    strip = Image.new("RGBA", (width * 12, SPINE_H), (0, 0, 0, 0))
    i = 0
    for palette in GENRE_PALETTES:
        for base in palette:
            strip.paste(spine(tier, base), (i * width, 0))
            i += 1
    strip.save(OUT / f"kehillah_spine_t{tier}.dds")


def dashed_outline(w, h, color=(170, 160, 140, 200), dash=4, inset=2):
    """A missing book: a dashed outline where it should stand (pixels at 1x)."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(inset, h, dash * 2):
        d.line([(0, y), (0, min(h - 1, y + dash - 1))], fill=color)
        d.line([(w - 1, y), (w - 1, min(h - 1, y + dash - 1))], fill=color)
    for x in range(inset, w - inset, dash * 2):
        d.line([(x, 0), (min(w - 1 - inset, x + dash - 1), 0)], fill=color)
    return im


dashed_outline(30, SPINE_H).save(OUT / "kehillah_spine_gap.dds")


def ribbon():
    w, h = 6 * SCALE, 20 * SCALE
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (w - 1, 0), (w - 1, h - 1), (w // 2, h - 4 * SCALE), (0, h - 1)], fill=(52, 150, 86, 255), outline=(26, 92, 50, 255))
    d.line([(w // 2, 0), (w // 2, h - 6 * SCALE)], fill=(120, 210, 140, 255), width=SCALE // 2)
    return im.resize((6, 20), Image.Resampling.LANCZOS)


ribbon().save(OUT / "kehillah_spine_ribbon.dds")


def big_volume(w, h, leather, bands, label=True):
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, H - 1), fill=leather + (255,))
    d.rectangle((0, 0, W - 1, 2 * S), fill=GOLD)
    d.rectangle((0, H - 1 - 2 * S, W - 1, H - 1), fill=GOLD)
    for y in bands:
        d.rectangle((0, y * S - S, W - 1, y * S + S), fill=GOLD)
        d.line([(0, y * S - S), (W - 1, y * S - S)], fill=GOLD_LIGHT, width=S // 2)
    if label:
        top, bot = round(h * 0.36), round(h * 0.56)
        d.rectangle((5 * S, top * S, W - 1 - 5 * S, bot * S), fill=(40, 16, 14, 255), outline=GOLD, width=S)
        for y in range(top + 4, bot - 2, 4):
            d.line([(9 * S, y * S), (W - 1 - 9 * S, y * S)], fill=GOLD_LIGHT, width=S)
    shade_columns(im, 0, W, 0, H, 0.34)
    return im.resize((w, h), Image.Resampling.LANCZOS)


# The Shas case: six great folios, two leathers alternating, and the gap.
SHAS_W, SHAS_H = 40, 118
shas = Image.new("RGBA", (SHAS_W * 3, SHAS_H), (0, 0, 0, 0))
shas.paste(big_volume(SHAS_W, SHAS_H, (64, 18, 18), (10, 18, 26, 92, 100, 108)), (0, 0))
shas.paste(big_volume(SHAS_W, SHAS_H, (60, 30, 18), (10, 18, 26, 92, 100, 108)), (SHAS_W, 0))
shas.paste(dashed_outline(SHAS_W, SHAS_H), (SHAS_W * 2, 0))
shas.save(OUT / "kehillah_lib_shas_volume.dds")

# The Prophets and the Writings: tall codices beside the ark, and the gap.
CODEX_W, CODEX_H = 34, 112
codex = Image.new("RGBA", (CODEX_W * 3, CODEX_H), (0, 0, 0, 0))
codex.paste(big_volume(CODEX_W, CODEX_H, (24, 36, 72), (10, 16, 96, 102)), (0, 0))
codex.paste(big_volume(CODEX_W, CODEX_H, (22, 58, 40), (10, 16, 96, 102)), (CODEX_W, 0))
codex.paste(dashed_outline(CODEX_W, CODEX_H), (CODEX_W * 2, 0))
codex.save(OUT / "kehillah_lib_codex.dds")


def ark(with_torah):
    w, h = 120, 150
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    wood, wood_dark, gilt = (104, 62, 28, 255), (58, 32, 14, 255), GOLD
    # the arched cabinet
    d.rectangle((0, 40 * S, W - 1, H - 1), fill=wood)
    d.pieslice((0, 0, W - 1, 80 * S), 180, 360, fill=wood)
    d.rectangle((10 * S, 46 * S, W - 1 - 10 * S, H - 1), fill=wood_dark)
    d.pieslice((10 * S, 10 * S, W - 1 - 10 * S, 82 * S), 180, 360, fill=wood_dark)
    d.arc((4 * S, 4 * S, W - 1 - 4 * S, 76 * S), 180, 360, fill=gilt, width=2 * S)
    d.line([(4 * S, 40 * S), (4 * S, H - 1)], fill=gilt, width=2 * S)
    d.line([(W - 1 - 4 * S, 40 * S), (W - 1 - 4 * S, H - 1)], fill=gilt, width=2 * S)
    # the curtain, drawn back to both sides
    d.polygon([(10 * S, 30 * S), (26 * S, 30 * S), (18 * S, 120 * S), (10 * S, 140 * S)], fill=(128, 26, 36, 255))
    d.polygon([(94 * S, 30 * S), (110 * S, 30 * S), (110 * S, 140 * S), (102 * S, 120 * S)], fill=(128, 26, 36, 255))
    # the tablets above
    d.rounded_rectangle((48 * S, 14 * S, 59 * S, 30 * S), radius=5 * S, fill=gilt)
    d.rounded_rectangle((61 * S, 14 * S, 72 * S, 30 * S), radius=5 * S, fill=gilt)
    if with_torah:
        # two rollers with silver finials, the scroll rolled on both
        for rx in (38, 74):
            d.rectangle((rx * S, 44 * S, (rx + 8) * S, 140 * S), fill=(92, 52, 22, 255))
            d.ellipse(((rx - 2) * S, 34 * S, (rx + 10) * S, 46 * S), fill=(200, 204, 210, 255), outline=(120, 124, 130, 255))
            d.rectangle(((rx - 1) * S, 132 * S, (rx + 9) * S, 136 * S), fill=(200, 204, 210, 255))
        for cx in (34, 70):
            d.rounded_rectangle((cx * S, 54 * S, (cx + 16) * S, 128 * S), radius=7 * S, fill=(232, 220, 190, 255), outline=(170, 150, 110, 255), width=S)
        d.rectangle((50 * S, 60 * S, 70 * S, 122 * S), fill=(240, 230, 204, 255))
        for y in range(64, 120, 5):
            d.line([(52 * S, y * S), (68 * S, y * S)], fill=(70, 60, 50, 255), width=S)
        d.rectangle((34 * S, 88 * S, 86 * S, 94 * S), fill=(30, 40, 96, 255))
    return im.resize((w, h), Image.Resampling.LANCZOS)


arks = Image.new("RGBA", (240, 150), (0, 0, 0, 0))
arks.paste(ark(True), (0, 0))
arks.paste(ark(False), (120, 0))
arks.save(OUT / "kehillah_lib_ark.dds")


def stand(with_book):
    w, h = 110, 120
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    wood, wood_dark = (112, 70, 34, 255), (70, 40, 18, 255)
    d.rectangle((49 * S, 44 * S, 61 * S, 112 * S), fill=wood)
    d.rectangle((30 * S, 110 * S, 80 * S, H - 1), fill=wood_dark)
    d.polygon([(8 * S, 46 * S), (102 * S, 46 * S), (96 * S, 36 * S), (14 * S, 36 * S)], fill=wood_dark)
    d.rectangle((8 * S, 46 * S, 102 * S, 50 * S), fill=wood)
    if with_book:
        d.polygon([(14 * S, 36 * S), (55 * S, 40 * S), (55 * S, 10 * S), (18 * S, 6 * S)], fill=(238, 228, 200, 255), outline=(150, 130, 96, 255))
        d.polygon([(96 * S, 36 * S), (55 * S, 40 * S), (55 * S, 10 * S), (92 * S, 6 * S)], fill=(232, 220, 190, 255), outline=(150, 130, 96, 255))
        for i in range(5):
            y = 13 + i * 5
            d.line([(22 * S, (y - 1) * S), (51 * S, (y + 1) * S)], fill=(80, 70, 60, 255), width=S)
            d.line([(59 * S, (y + 1) * S), (88 * S, (y - 1) * S)], fill=(80, 70, 60, 255), width=S)
        d.line([(55 * S, 10 * S), (55 * S, 40 * S)], fill=(120, 100, 70, 255), width=S)
    return im.resize((w, h), Image.Resampling.LANCZOS)


stands = Image.new("RGBA", (220, 120), (0, 0, 0, 0))
stands.paste(stand(True), (0, 0))
stands.paste(stand(False), (110, 0))
stands.save(OUT / "kehillah_lib_stand.dds")


def plank(w, h):
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, H - 1), fill=(96, 58, 26, 255))
    d.rectangle((0, 0, W - 1, 2 * S), fill=(150, 98, 50, 255))
    d.rectangle((0, H - 1 - 2 * S, W - 1, H - 1), fill=(52, 30, 12, 255))
    for i, x in enumerate(range(0, W, 37 * S)):
        d.line([(x, (3 + i % 3) * S), (x + 22 * S, (4 + i % 3) * S)], fill=(78, 46, 20, 255), width=S)
    return im.resize((w, h), Image.Resampling.LANCZOS)


plank(470, 8).save(OUT / "kehillah_lib_shelf_plank.dds")
plank(470, 12).save(OUT / "kehillah_lib_case_plank.dds")
