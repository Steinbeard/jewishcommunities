"""Build the small, deterministic DDS strips used by the Beit Midrash shelf.

Run with Pillow from the repository root.  Frames are 1-indexed in CK3 GUI.
The source stays here so the borders can be revised without repainting a DDS.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features
import math
import json
import hashlib
import random


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
# Paint source retained alongside the generated DDS strips. Crops are detected
# by the transparent gutters, so the CK3 sprite dimensions stay exact.
SPINE_ATLAS = OUT / "kehillah_spine_art_atlas.png"
painted = Image.open(SPINE_ATLAS).convert("RGBA") if SPINE_ATLAS.exists() else None
painted_books = []
if painted:
    alpha = painted.getchannel("A")
    occupied = [sum(alpha.getpixel((x, y)) > 100 for y in range(painted.height)) > painted.height // 6 for x in range(painted.width)]
    start = None
    for x, on in enumerate(occupied + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            crop = painted.crop((start, 0, x, painted.height))
            painted_books.append(crop.crop(crop.getbbox()))
            start = None
    if len(painted_books) != 12:
        raise ValueError(f"Expected 12 isolated book spines in {SPINE_ATLAS}, found {len(painted_books)}")

# Material and degree of tooling follow standing. Colour remains a gentler
# genre cue; the permanent title cartouche is generated separately below.
PAINTED_BY_TIER = {
    1: (0, 11, 3, 0),       # wrappers
    2: (7, 7, 7, 7),        # bound quires
    3: (3, 11, 0, 3),       # limp vellum
    4: (1, 6, 8, 1),        # plain leather
    5: (8, 5, 2, 4),        # tooling
    6: (2, 5, 4, 10),       # gilt
    7: (9, 10, 2, 5),       # canon
}
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
    # Restrained, repeatable variation in the surface breaks up the flat colour
    # without changing the silhouette that communicates the rite's standing.
    rng = random.Random((tier, *base).__repr__())
    texture = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(texture)
    for _ in range(round(w * h / 700)):
        x, y = rng.randrange(w), rng.randrange(h)
        td.line((x, y, min(w - 1, x + rng.randrange(2, 13)), y), fill=(240, 212, 155, rng.randrange(6, 24)), width=1)
    im = Image.alpha_composite(im, texture)
    return im.resize((SPINE_WIDTH[tier], SPINE_H), Image.Resampling.LANCZOS)


def painted_spine(tier, base, index):
    source = painted_books[index].resize((SPINE_WIDTH[tier] * SCALE, SPINE_H * SCALE), Image.Resampling.LANCZOS)
    wash = Image.new("RGB", source.size, base)
    colour = Image.blend(source.convert("RGB"), wash, 0.14 if tier <= 3 else 0.21)
    colour.putalpha(source.getchannel("A"))
    return colour.resize((SPINE_WIDTH[tier], SPINE_H), Image.Resampling.LANCZOS)


for tier, width in SPINE_WIDTH.items():
    strip = Image.new("RGBA", (width * 12, SPINE_H), (0, 0, 0, 0))
    i = 0
    for palette in GENRE_PALETTES:
        for variant, base in enumerate(palette):
            art = painted_spine(tier, base, PAINTED_BY_TIER[tier][variant]) if painted_books else spine(tier, base)
            strip.paste(art, (i * width, 0))
            i += 1
    strip.save(OUT / f"kehillah_spine_t{tier}.dds")


# A work retains this small painted spine cartouche when the rite changes its
# binding. The abbreviated title is selected from its stable catalog key; the
# generated slots use their number. The full name remains on hover.
order = json.loads((ROOT / "scripts/kehillah_library_catalog.json").read_text(encoding="utf-8"))["order"]
font_path = "C:/Windows/Fonts/frank.ttf"
try:
    mark_font = ImageFont.truetype(font_path, 8 * SCALE)
except OSError:
    # The repository is normally regenerated on Windows; DejaVu is a portable
    # fallback that also contains Hebrew glyphs.
    mark_font = ImageFont.truetype("DejaVuSans.ttf", 8 * SCALE)

HEBREW_MARKS = {
    "work_targum_onkelos": "תא", "work_mekhilta": "מכ",
    "work_genesis_rabbah": "בר", "work_pirkei_derabbi_eliezer": "פא",
    "work_mishnah": "מש", "work_bavli_zeraim": "בז",
    "work_bavli_moed": "במ", "work_bavli_nashim": "בנ",
    "work_bavli_nezikin": "בזנ", "work_bavli_kodashim": "בק",
    "work_bavli_tahorot": "בט", "work_yerushalmi_zeraim": "יז",
    "work_yerushalmi_moed": "ימ", "work_yerushalmi_nashim": "ינ",
    "work_yerushalmi_nezikin": "ינז", "work_halakhot_gedolot": "הג",
    "work_sefer_yetzirah": "סי", "work_hekhalot_rabbati": "הר",
    "work_shiur_qomah": "שק", "work_sefer_harazim": "סר",
    "work_emunot_vedeot": "אד", "work_chovot_halevavot": "חל",
    "work_kuzari": "כוז", "work_tanakh_torah": "ת",
    "work_tanakh_neviim": "נ", "work_tanakh_ketuvim": "כ",
    "work_tosefta": "תו", "work_seder_rav_amram": "סע",
    "work_iggeret_rav_sherira": "אש", "work_rabbenu_hananel": "רח",
    "work_mekor_hayyim": "מח", "work_anan_sefer_hamitzvot": "מצ",
    "work_kitab_alanwar": "אנ", "work_yefet_commentary": "יפ",
    "work_rashi_torah": "רת", "work_rashi_talmud": "רש",
    "work_hilkhot_harif": "רי", "work_mishneh_torah": "מת",
    "work_moreh_nevukhim": "מנ", "work_sefer_habahir": "בה",
    "work_sefer_hasidim": "חס", "work_tosafot": "תס",
    "work_zohar": "זה",
}


def hebrew_number(n):
    """A compact Hebrew numeral for the catalog's numbered authored slots."""
    if n == 15:
        return "טו"
    if n == 16:
        return "טז"
    tens = ("", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ")
    ones = ("", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט")
    return "ק" * (n // 100) + tens[(n % 100) // 10] + ones[n % 10]


def paint_hebrew(draw, xy, label, **kwargs):
    if features.check("raqm"):
        draw.text(xy, label, font=mark_font, anchor="mm", direction="rtl", **kwargs)
    else:
        # Hebrew letters do not join; reverse the visual order if Pillow has
        # no bidi renderer, as on this machine.
        draw.text(xy, label[::-1], font=mark_font, anchor="mm", **kwargs)
mark_w, mark_h = 16, 20
marks = Image.new("RGBA", (mark_w * len(order), mark_h), (0, 0, 0, 0))
for index, work in enumerate(order):
    if work.startswith("work_authored_"):
        letters = hebrew_number(int(work.rsplit("_", 1)[1]))
    else:
        letters = HEBREW_MARKS[work]
    seed = hashlib.sha256(work.encode()).digest()
    patch = Image.new("RGBA", (mark_w * SCALE, mark_h * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(patch)
    ink = (231, 194, 116, 245) if not work.startswith("work_authored_") else (213, 188, 143, 235)
    d.rounded_rectangle((SCALE, 2*SCALE, 15*SCALE, 18*SCALE), radius=2*SCALE, fill=(35, 25, 23, 210), outline=ink, width=SCALE)
    paint_hebrew(d, (8*SCALE, 9*SCALE), letters, fill=ink, stroke_width=0)
    for x in (4, 12):
        if seed[x] % 2:
            d.ellipse((x*SCALE-SCALE//2, 16*SCALE, x*SCALE+SCALE//2, 17*SCALE), fill=ink)
    marks.paste(patch.resize((mark_w, mark_h), Image.Resampling.LANCZOS), (index * mark_w, 0))
marks.save(OUT / "kehillah_spine_marks.dds")


def dashed_outline(w, h, color=(58, 36, 20, 235), dash=4, inset=2, fill=(40, 24, 12, 78)):
    """A missing book: a dashed outline where it should stand (pixels at 1x).
    2026-11-11 (Daniel: "the missing book indicators darker"): dark walnut on
    the light oak back panel, over a faint shadow where the volume would stand."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((1, 1, w - 2, h - 1), fill=fill)
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


# 2026-11-11 (Daniel: "does the glow look a little off?"): the mastered halo.
# Vanilla's Glow_Standard on the book art lit the label plates from behind
# (they are part-transparent) and was too faint at the edges. This is a soft
# green ring drawn over the art, its inner edge on the book's own edge (the GUI
# places it 10 px out on every side), its middle transparent. Drawn as
# Corneredstretched with spriteborder 12, so the ring keeps its width on any book.
def mastered_halo(size=48, out=10, inner=2, color=(120, 232, 110), peak=0.95):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    lo, hi = out, size - 1 - out
    for y in range(size):
        for x in range(size):
            dx = max(lo - x, 0, x - hi)
            dy = max(lo - y, 0, y - hi)
            d = math.hypot(dx, dy)
            if d > 0:
                a = peak * max(0.0, 1 - d / out) ** 1.4
            else:
                edge = min(x - lo, hi - x, y - lo, hi - y)
                a = peak * max(0.0, 1 - edge / inner) if edge < inner else 0.0
            if a > 0:
                px[x, y] = color + (round(255 * a),)
    return im


mastered_halo().save(OUT / "kehillah_lib_mastered_halo.dds")


def big_volume(w, h, leather, bands, label=True, sigil=None):
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
        if sigil:
            paint_hebrew(d, (W//2, (top+bot)*S//2), sigil, fill=GOLD_LIGHT)
        else:
            for y in range(top + 4, bot - 2, 4):
                d.line([(9 * S, y * S), (W - 1 - 9 * S, y * S)], fill=GOLD_LIGHT, width=S)
    shade_columns(im, 0, W, 0, H, 0.34)
    return im.resize((w, h), Image.Resampling.LANCZOS)


def painted_volume(w, h, source_index, sigil):
    if not painted_books:
        return big_volume(w, h, (58, 31, 25), (10, 18, h - 18, h - 10), sigil=sigil)
    im = painted_books[source_index].resize((w * SCALE, h * SCALE), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(im)
    cx, cy = w * SCALE // 2, h * SCALE // 2
    d.rounded_rectangle((cx - 13*SCALE, cy - 11*SCALE, cx + 13*SCALE, cy + 11*SCALE),
                        radius=2*SCALE, fill=(48, 28, 24, 215), outline=(205, 164, 86, 255), width=SCALE)
    paint_hebrew(d, (cx, cy), sigil, fill=GOLD_LIGHT)
    return im.resize((w, h), Image.Resampling.LANCZOS)


# The Shas case: a distinct cartouche on each order, plus the empty slot.
SHAS_W, SHAS_H = 40, 118
shas = Image.new("RGBA", (SHAS_W * 7, SHAS_H), (0, 0, 0, 0))
for i, name in enumerate(("זר", "מו", "נש", "נז", "קד", "טה")):
    leather = ((64, 18, 18), (60, 30, 18), (69, 27, 37), (65, 39, 25), (67, 24, 27), (70, 31, 23))[i]
    # 2026-11-11 (Daniel: "make all the volumes of the Talmud match"): one
    # binding for the whole set, the order's cartouche the only difference.
    shas.paste(painted_volume(SHAS_W, SHAS_H, 2, name), (SHAS_W * i, 0))
shas.paste(dashed_outline(SHAS_W, SHAS_H), (SHAS_W * 6, 0))
shas.save(OUT / "kehillah_lib_shas_volume.dds")

# The Prophets and the Writings: tall codices beside the ark, and the gap.
CODEX_W, CODEX_H = 34, 112
codex = Image.new("RGBA", (CODEX_W * 3, CODEX_H), (0, 0, 0, 0))
codex.paste(painted_volume(CODEX_W, CODEX_H, 9, "נ"), (0, 0))
codex.paste(painted_volume(CODEX_W, CODEX_H, 5, "כ"), (CODEX_W, 0))
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


def centrepiece_crops(filename):
    source = OUT / filename
    if not source.exists():
        return None
    im = Image.open(source).convert("RGBA")
    alpha = im.getchannel("A")
    occupied = [sum(alpha.getpixel((x, y)) > 100 for y in range(im.height)) > im.height // 8 for x in range(im.width)]
    ranges, start = [], None
    for x, on in enumerate(occupied + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            ranges.append((start, x))
            start = None
    if len(ranges) != 2:
        raise ValueError(f"Expected an ark and a lectern in {source}, found {ranges}")
    result = []
    for left, right in ranges:
        cut = im.crop((left, 0, right, im.height))
        result.append(cut.crop(cut.getbbox()))
    return result


furnished = centrepiece_crops("kehillah_centrepiece_art_atlas.png")
empty = centrepiece_crops("kehillah_centrepiece_empty_atlas.png")
arks = Image.new("RGBA", (240, 150), (0, 0, 0, 0))
arks.paste(furnished[0].resize((120, 150), Image.Resampling.LANCZOS) if furnished else ark(True), (0, 0))
arks.paste(empty[0].resize((120, 150), Image.Resampling.LANCZOS) if empty else ark(False), (120, 0))
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
stands.paste(furnished[1].resize((110, 120), Image.Resampling.LANCZOS) if furnished else stand(True), (0, 0))
stands.paste(empty[1].resize((110, 120), Image.Resampling.LANCZOS) if empty else stand(False), (110, 0))
stands.save(OUT / "kehillah_lib_stand.dds")


# ---------------------------------------------------------------------------
# 2026-11-11 (Daniel: "revise the bookshelf design to make it feel more
# aesthetically pleasing ... like it's a real bookshelf maybe, with light wood
# background panels"): a bookcase. Light oak boards behind the books (tiled as
# the shelf viewport's own background), a darker oak frame around it, oak
# shelves with a lip, a soft shadow under each shelf, and walnut caption plates
# so the captions stay legible on light wood. All deterministic.
# ---------------------------------------------------------------------------
OAK_BACK = (186, 140, 90)
OAK_FRAME = (124, 80, 42)
OAK_SHELF = (158, 110, 62)


def _clamp(v):
    return max(0, min(255, int(round(v))))


def case_back(size=256, boards=4):
    """Vertical oak boards, tileable both ways: grain runs down each board and
    is periodic in y; seams fall on the tile edges."""
    rng = random.Random(1066)
    im = Image.new("RGBA", (size, size))
    px = im.load()
    bw = size // boards
    params = []
    for b in range(boards):
        tint = rng.uniform(-10, 10)
        params.append((tint, [(rng.uniform(0.18, 0.42), rng.uniform(0, 6.28), rng.uniform(0.5, 1.6), rng.uniform(0, 6.28))
                              for _ in range(5)]))
    for x in range(size):
        b, bx = divmod(x, bw)
        tint, waves = params[b]
        for y in range(size):
            t = 2 * math.pi * y / size
            g = 0.0
            for f, ph, amp, ph2 in waves:
                g += math.sin(bx * f + ph + amp * math.sin(t * 2 + ph2))
            g /= len(waves)
            k = 0.80 + 0.06 * g + tint / 255
            col = [OAK_BACK[i] * k for i in range(3)]
            # board edges: a dark seam, a lit edge beside it
            if bx == 0:
                col = [c * 0.62 for c in col]
            elif bx == 1:
                col = [c * 1.08 for c in col]
            elif bx == bw - 1:
                col = [c * 0.84 for c in col]
            px[x, y] = (_clamp(col[0]), _clamp(col[1]), _clamp(col[2]), 255)
    return im


def case_frame(size=64, border=10):
    """The case's frame as a nine-slice: oak, lit on its outer top-left edge,
    shadowed on its inner edge where it meets the back panel; clear middle."""
    rng = random.Random(1492)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    for y in range(size):
        for x in range(size):
            d_out = min(x, y, size - 1 - x, size - 1 - y)
            if d_out >= border:
                continue
            horiz = min(y, size - 1 - y) < min(x, size - 1 - x)
            grain = math.sin((x if horiz else y) * 0.9 + (y if horiz else x) * 0.05 + rng.uniform(-0.25, 0.25))
            k = 0.95 + 0.05 * grain
            if d_out < 2:
                k *= 1.22 if (x < size // 2 or y < size // 2) and d_out == 0 else 0.8
            if d_out >= border - 2:
                k *= 0.7
            col = [OAK_FRAME[i] * k for i in range(3)]
            px[x, y] = (_clamp(col[0]), _clamp(col[1]), _clamp(col[2]), 255)
    return im


def plank(w, h):
    """An oak shelf seen from the front: a lit top edge, the face, a dark lip."""
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, H - 1), fill=OAK_SHELF + (255,))
    d.rectangle((0, 0, W - 1, 2 * S), fill=(206, 160, 104, 255))
    d.rectangle((0, H - 1 - 2 * S, W - 1, H - 1), fill=(84, 52, 24, 255))
    rng = random.Random(w * 31 + h)
    for _ in range(w // 9):
        x = rng.randrange(0, W)
        y = rng.randrange(3 * S, max(3 * S + 1, H - 3 * S))
        d.line([(x, y), (x + rng.randrange(18, 60) * S, y + rng.choice((-1, 0, 1)) * S // 2)],
               fill=(136, 92, 50, 255), width=max(1, S // 2))
    return im.resize((w, h), Image.Resampling.LANCZOS)


def shelf_shadow(w=32, h=16):
    """The shadow a shelf casts on the back panel below it: dark at the top."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    for y in range(h):
        a = 0.58 * (1 - y / (h - 1)) ** 1.6
        for x in range(w):
            px[x, y] = (24, 14, 6, _clamp(255 * a))
    return im


def caption_plate(w=64, h=24, border=6):
    """A walnut plate with a thin gilt edge for captions on the light wood."""
    W, H, S = w * SCALE, h * SCALE, SCALE
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, W - 1, H - 1), radius=4 * S, fill=(48, 30, 18, 236), outline=(176, 136, 70, 255), width=S)
    d.rounded_rectangle((2 * S, 2 * S, W - 1 - 2 * S, H - 1 - 2 * S), radius=3 * S, outline=(92, 62, 34, 255), width=S)
    return im.resize((w, h), Image.Resampling.LANCZOS)


case_back().save(OUT / "kehillah_lib_case_back.dds")
case_frame().save(OUT / "kehillah_lib_case_frame.dds")
plank(486, 12).save(OUT / "kehillah_lib_shelf_plank.dds")
plank(486, 14).save(OUT / "kehillah_lib_case_plank.dds")
shelf_shadow().save(OUT / "kehillah_lib_shelf_shadow.dds")
caption_plate().save(OUT / "kehillah_lib_caption_plate.dds")
