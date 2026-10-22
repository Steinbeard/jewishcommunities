"""Render the Kehillah bookmark art for the 867, 1066 and 1178 start
screens: a painted-style map drawn from the game's own heightmap and river
map, with each start's communities marked; one highlight overlay per
bookmark character; and the start-screen button and list icons.

Run:  python -I scripts/render_bookmark_art.py [bookmark_key ...]
With no arguments every bookmark in BOOKMARKS is rendered.
Reads the installed game's map_data; writes into gfx/interface/bookmarks/.
"""
import os
import sys
import warnings

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

warnings.filterwarnings("ignore")
Image.MAX_IMAGE_PIXELS = None

GAME = r"E:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game"
MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(MOD, "gfx", "interface", "bookmarks")
W, H = 1920, 1080

# Community seats: the capital province centroid of each host county, in
# provinces.png pixel coordinates.
CITIES = {
    "worms": (1406.3, 1487.0),
    "troyes": (1172.1, 1579.8),
    "granada": (748.4, 2376.2),
    "fez": (699.2, 2590.3),
    "sura": (3387.5, 2633.8),      # c_kufa
    "oria": (1982.8, 2221.3),      # c_lecce
    "sanaa": (3430.4, 3474.1),
    "lucca": (1544.9, 1943.6),
    "tiberias": (2966.2, 2651.3),
    "kairouan": (1557.4, 2541.9),
    "fustat": (2766.2, 2827.6),    # c_cairo
    "baghdad": (3378.1, 2537.0),
    "speyer": (1406.1, 1511.8),
    "posquieres": (1167.0, 1873.1),  # c_uses
    "toledo": (732.5, 2186.8),
    "itil": (3414.6, 1615.9),      # province 620, the Khagan's capital
}

# One entry per bookmark. Window: top-left (ox, oy) in provinces.png space
# and the scale from map pixels to the 1920x1080 image. Regions are the
# names the communities themselves used, placed in map coordinates. Seats
# are (city, label, label offset in image pixels). Characters map each
# bookmark character key to the city its highlight glows over.
BOOKMARKS = {
    "bm_1066_kehillah_worms": {
        "ox": 0, "oy": 1260, "scale": 0.697,
        "regions": (("Sefarad", (720, 2050)), ("Tzarfat", (950, 1720)),
                    ("Ashkenaz", (1580, 1420)), ("Maghreb", (1000, 2730))),
        "seats": (("worms", "Worms", (22, -6)), ("troyes", "Troyes", (22, -6)),
                  ("granada", "Granada", (22, -8)), ("fez", "Fez", (22, -6))),
        "characters": {
            "bookmark_kehillah_worms_isaac": "worms",
            "bookmark_kehillah_troyes_rashi": "troyes",
            "bookmark_kehillah_granada_joseph": "granada",
            "bookmark_kehillah_granada_david": "granada",
            "bookmark_kehillah_fez_rif": "fez",
        },
        "button": (760, 520),
    },
    # 867 centres on Bavel (Daniel, 2026-10-22: the Gaon belongs at the
    # centre). The western cities would stretch the map, so they sit in an
    # inset box in the top left, the way a printed atlas does it.
    "bm_867_kehillah": {
        "ox": 1165, "oy": 1283, "scale": 0.45,
        "insets": ({"map": (1360, 1840, 2160, 2680), "screen": (305, 85, 585, 379),
                    "cities": ("lucca", "oria", "kairouan"), "title": ""},),
        "regions": (("Bavel", (4600, 2800)), ("Eretz Yisrael", (2800, 2900)),
                    ("Kuzaria", (3300, 1450)), ("Teiman", (3500, 3300))),
        "seats": (("lucca", "Lucca", (22, -6)), ("oria", "Oria", (-72, -6)),
                  ("kairouan", "Kairouan", (22, -6)), ("tiberias", "Tiberias", (-60, 14)),
                  ("sura", "Sura", (-30, -40)), ("sanaa", "Sana'a", (-95, -6)),
                  ("itil", "Itil", (22, -6))),
        "characters": {
            "bookmark_kehillah_sura_amram": "sura",
            "bookmark_kehillah_tiberias_moshe": "tiberias",
            "bookmark_kehillah_oria_shefatiah": "oria",
            "bookmark_kehillah_lucca_kalonymus": "lucca",
            "bookmark_kehillah_kairouan_hananel": "kairouan",
            "bookmark_kehillah_eldad": "sanaa",
            "bookmark_kehillah_khagan_manasseh": "itil",
        },
        "button": (960, 520),
    },
    "bm_1178_kehillah": {
        "ox": 115, "oy": 1290, "scale": 0.55,
        "regions": (("Sefarad", (900, 2330)), ("Provence", (1150, 2010)),
                    ("Tzarfat", (930, 1700)), ("Ashkenaz", (1620, 1440)),
                    ("Mitzrayim", (2700, 2990)), ("Bavel", (3280, 2790))),
        "seats": (("speyer", "Speyer", (-110, -6)), ("troyes", "Troyes", (-100, 4)),
                  ("posquieres", "Posquières", (-150, -6)), ("toledo", "Toledo", (-40, 16)),
                  ("fustat", "Fustat", (-80, 18)), ("baghdad", "Baghdad", (-60, -42))),
        "characters": {
            "bookmark_kehillah_fustat_rambam": "fustat",
            "bookmark_kehillah_baghdad_samuel": "baghdad",
            "bookmark_kehillah_troyes_ri": "troyes",
            "bookmark_kehillah_speyer_judah": "speyer",
            "bookmark_kehillah_posquieres_raavad": "posquieres",
            "bookmark_kehillah_toledo_shoshan": "toledo",
        },
        "button": (900, 500),
    },
}
WATER = 4626  # heightmap value of the sea surface

# The active window; set per bookmark by use_window().
SCALE = 1.0
OX, OY = 0, 0
WIN_W, WIN_H = W, H


def use_window(cfg):
    global SCALE, OX, OY, WIN_W, WIN_H
    SCALE = cfg["scale"]
    OX, OY = cfg["ox"], cfg["oy"]
    WIN_W, WIN_H = W / SCALE, H / SCALE


def to_img(p):
    return ((p[0] - OX) * SCALE, (p[1] - OY) * SCALE)


def crop_resample(path, scale_src, resample):
    im = Image.open(path)
    box = (OX * scale_src, OY * scale_src,
           (OX + WIN_W) * scale_src, (OY + WIN_H) * scale_src)
    return im.crop(tuple(int(round(v)) for v in box)).resize((W, H), resample)


def smoothstep(x, lo, hi):
    t = np.clip((x - lo) / (hi - lo), 0, 1)
    return t * t * (3 - 2 * t)


def noise(seed, sigma):
    rng = np.random.default_rng(seed)
    n = ndi.gaussian_filter(rng.standard_normal((H, W)), sigma)
    return n / n.std()


def build_map(vignette=True):
    hm = np.array(crop_resample(GAME + "/map_data/heightmap.png", 2, Image.BILINEAR)).astype(np.float32)
    land = smoothstep(ndi.gaussian_filter(hm, 1.2), WATER - 500, WATER + 500)
    land_b = land > 0.5

    # Hillshade, light from the north-west, exaggerated for ridges.
    hs = ndi.gaussian_filter(hm, 2.0) / 255.0
    gy, gx = np.gradient(hs)
    shade = np.clip(0.5 + 0.9 * (-gx - gy) / 4.0, 0, 1)
    elev = smoothstep(hm, WATER, 26000)

    mottling = noise(1, 6) * 0.025 + noise(2, 1.2) * 0.012
    low = np.array([224, 207, 164], np.float32)
    high = np.array([178, 152, 108], np.float32)
    base = low[None, None] * (1 - elev[..., None]) + high[None, None] * elev[..., None]
    base = base * (0.80 + 0.40 * shade[..., None]) * (1 + mottling[..., None])
    # Mountains read as darker, more brown.
    base *= (1 - 0.10 * smoothstep(hm, 14000, 30000))[..., None]

    # Sea: distance from the coast drives colour and ripple lines.
    dist = ndi.distance_transform_edt(~land_b)
    sea_near = np.array([128, 150, 142], np.float32)
    sea_far = np.array([84, 108, 112], np.float32)
    k = np.exp(-dist / 70.0)[..., None]
    sea = sea_far[None, None] * (1 - k) + sea_near[None, None] * k
    sea = sea * (1 + (noise(3, 8) * 0.03 + noise(4, 1.5) * 0.015)[..., None])
    ripple = (np.sin(dist * (2 * np.pi / 13.0)) > 0.93) & (dist < 75) & (dist > 4)
    fade = np.clip(1 - dist / 75.0, 0, 1) * 0.35
    sea = sea * (1 - (ripple * fade)[..., None])

    img = base * land[..., None] + sea * (1 - land[..., None])

    # Coast line.
    edge = np.abs(ndi.gaussian_filter(land, 1.0) - land)
    edge = np.clip(ndi.maximum_filter(edge, 3) * 6, 0, 1)
    ink = np.array([92, 72, 46], np.float32)
    img = img * (1 - 0.8 * edge[..., None]) + ink[None, None] * (0.8 * edge[..., None])

    # Rivers.
    rv = np.array(crop_resample(GAME + "/map_data/rivers.png", 1, Image.NEAREST))
    river = (rv < 254) & (rv >= 5)
    river = ndi.binary_dilation(river, iterations=1) & land_b
    river_a = ndi.gaussian_filter(river.astype(np.float32), 0.7)
    rc = np.array([98, 126, 132], np.float32)
    img = img * (1 - 0.6 * river_a[..., None]) + rc[None, None] * (0.6 * river_a[..., None])

    # Parchment grain and a vignette.
    img *= (1 + noise(5, 0.8) * 0.012)[..., None]
    if vignette:
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        img *= (1 - 0.38 * smoothstep(r, 0.55, 1.35))[..., None]
    return img, land


def font(name, size):
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", name), size)


def spaced(draw, xy, text, fnt, fill, spacing):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def spaced_width(draw, text, fnt, spacing):
    return sum(draw.textlength(c, font=fnt) + spacing for c in text) - spacing


# ---------------------------------------------------------------------
# Start-screen layout. The bookmark screen draws its own interface over the
# art: the bookmark list on the left, the description panel top right, the
# date tabs at the top. A card is a portrait with a name banner and a
# subtitle; its footprint is measured from 2026-10-22 screenshots, relative
# to the character's `position` in common/bookmarks/bookmarks/.
# ---------------------------------------------------------------------
UI_ZONES = (
    ("bookmark list", (0, 0, 295, 1080)),
    ("description panel", (1480, 45, 1920, 545)),
    ("date tabs", (610, 0, 1290, 75)),
    ("bottom bar", (0, 1050, 1920, 1080)),
)


def card_rects(pos):
    x, y = pos
    return ((x + 90, y - 60, x + 250, y + 70),    # portrait
            (x, y + 70, x + 390, y + 135),        # name banner
            (x + 30, y + 135, x + 360, y + 200))  # subtitle and difficulty


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def read_positions(key):
    """Top-level character positions of one bookmark, from the bookmark file."""
    import re
    path = os.path.join(MOD, "common", "bookmarks", "bookmarks", "kehillah_bookmarks.txt")
    text = open(path, encoding="utf-8-sig").read()
    start = re.search(r"(?m)^" + key + r" = \{", text).end()
    depth, i = 1, start
    while depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    body = text[start:i]
    return {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(
        r'name = "(\w+)"[^{}]*?position = \{ (-?\d+) (-?\d+) \}', body)}


def seat_xy(cfg, city):
    """Image position of a seat: inside its inset box if it has one."""
    for inset in cfg.get("insets", ()):
        if city in inset["cities"]:
            (x0, y0, x1, y1), (s0, t0, s1, t1) = inset["map"], inset["screen"]
            x, y = CITIES[city]
            return (s0 + (x - x0) * (s1 - s0) / (x1 - x0), t0 + (y - y0) * (t1 - t0) / (y1 - y0))
    return to_img(CITIES[city])


def blocked(rect, cards, inset_ok=False, cfg=None):
    hits = [n for n, z in UI_ZONES if overlaps(rect, z)]
    hits += [c for c, rs in cards.items() if any(overlaps(rect, r) for r in rs)]
    if cfg and not inset_ok:
        hits += ["inset" for i in cfg.get("insets", ()) if overlaps(rect, i["screen"])]
    return hits


def check_layout(key, cfg):
    """Print every card that sits under the interface or another card, and
    every seat a card hides. Returns the card rectangles for the preview."""
    pos = read_positions(key)
    cards = {c: card_rects(p) for c, p in pos.items()}
    for c, rs in cards.items():
        for n, z in UI_ZONES:
            if any(overlaps(r, z) for r in rs):
                print(f"  LAYOUT {key}: {c} is under the {n}")
        for o, ors in cards.items():
            if o < c and any(overlaps(r, q) for r in rs for q in ors):
                print(f"  LAYOUT {key}: {c} overlaps {o}")
    for city, label, off in cfg["seats"]:
        cx, cy = seat_xy(cfg, city)
        dot = (cx - 11, cy - 11, cx + 11, cy + 11)
        text = (cx + off[0], cy + off[1], cx + off[0] + 15 * len(label), cy + off[1] + 30)
        for what, r in (("seat", dot), ("label", text)):
            hits = blocked(r, cards, inset_ok=True)
            if hits:
                print(f"  LAYOUT {key}: {city} {what} hidden by {', '.join(hits)}")
    return cards


def draw_inset(img, land, cfg):
    """Render each inset box's own map window and paste it, framed, into
    the main map arrays."""
    main = (SCALE, OX, OY)
    for inset in cfg.get("insets", ()):
        (x0, y0, x1, y1), (s0, t0, s1, t1) = inset["map"], inset["screen"]
        use_window({"ox": x0, "oy": y0, "scale": H / (y1 - y0)})
        sub, sub_land = build_map(vignette=False)
        cw = int(round((x1 - x0) * SCALE))
        size = (int(s1 - s0), int(t1 - t0))
        piece = Image.fromarray(np.clip(sub[:, :cw], 0, 255).astype(np.uint8)).resize(size, Image.LANCZOS)
        piece_land = Image.fromarray((sub_land[:, :cw] * 255).astype(np.uint8)).resize(size, Image.LANCZOS)
        img[int(t0):int(t0) + size[1], int(s0):int(s0) + size[0]] = np.array(piece, np.float32)
        land[int(t0):int(t0) + size[1], int(s0):int(s0) + size[0]] = np.array(piece_land, np.float32) / 255
        ink = np.array([92, 72, 46], np.float32)
        for k in range(4):  # frame
            img[int(t0) + k, int(s0):int(s1)] = ink
            img[int(t1) - 1 - k, int(s0):int(s1)] = ink
            img[int(t0):int(t1), int(s0) + k] = ink
            img[int(t0):int(t1), int(s1) - 1 - k] = ink
    SCALE_, OX_, OY_ = main
    use_window({"ox": OX_, "oy": OY_, "scale": SCALE_})
    return img, land


def annotate(img, cfg, cards):
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Regions, as the community itself named them. A label that a card, an
    # inset or the interface would cover is left out rather than half-shown.
    big = font("GARAIT.TTF", 46)
    for text, where in cfg["regions"]:
        centre = to_img(where)
        w = spaced_width(d, text, big, 14)
        rect = (centre[0] - w / 2, centre[1] - 25, centre[0] + w / 2, centre[1] + 30)
        hits = blocked(rect, cards, cfg=cfg)
        if hits:
            print(f"  skipped region label {text!r}: under {', '.join(hits)}")
            continue
        spaced(d, (centre[0] - w / 2, centre[1] - 25), text, big, (70, 52, 34, 165), 14)

    # Inset titles.
    small = font("GARAIT.TTF", 28)
    for inset in cfg.get("insets", ()):
        s0, t0, s1, t1 = inset["screen"]
        d.text((s0 + 12, t1 - 40), inset["title"], font=small, fill=(70, 52, 34, 220))

    # Seats.
    lab = font("GARABD.TTF", 26)
    for name, label, off in cfg["seats"]:
        cx, cy = seat_xy(cfg, name)
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(60, 40, 24, 230))
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=(226, 184, 74, 255))
        d.text((cx + off[0] + 1, cy + off[1] + 1), label, font=lab, fill=(244, 232, 200, 200))
        d.text((cx + off[0], cy + off[1]), label, font=lab, fill=(52, 34, 20, 255))

    return Image.alpha_composite(base, layer)


def layout_preview(bg, cards, path):
    """The art with the interface zones shaded and each card's footprint
    outlined, at 1024 px wide: a check that needs no game."""
    im = bg.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _, z in UI_ZONES:
        d.rectangle(z, fill=(20, 20, 30, 170))
    for c, rs in cards.items():
        for r in rs:
            d.rectangle(r, outline=(200, 30, 30, 255), width=3)
        d.text((rs[1][0] + 8, rs[1][1] + 10), c.replace("bookmark_kehillah_", ""),
               font=font("GARABD.TTF", 24), fill=(255, 255, 255, 255))
    Image.alpha_composite(im, layer).convert("RGB").resize((1024, 576)).save(path)


def overlay(land, cx, cy, sigma=95, strength=185):
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sigma ** 2)))
    a = (glow * land * strength).astype(np.uint8)
    out = np.zeros((H, W, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 244, 208, 104
    out[..., 3] = a
    return Image.fromarray(out, "RGBA")


def button(bg, centre, span=1100, size=(548, 140)):
    bw, bh = size
    h = int(span * bh / bw)
    cx, cy = centre
    box = (int(cx - span / 2), int(cy - h / 2), int(cx + span / 2), int(cy + h / 2))
    im = bg.crop(box).resize((bw, bh), Image.LANCZOS)
    a = np.array(im).astype(np.float32)
    yy, xx = np.mgrid[0:bh, 0:bw]
    edge = np.minimum(np.minimum(xx, bw - 1 - xx) / 40.0, np.minimum(yy, bh - 1 - yy) / 20.0)
    a[..., :3] *= (0.55 + 0.45 * np.clip(edge, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def save(im, *parts):
    path = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    print("wrote", path, os.path.getsize(path))


def render(key, cfg, check_only=False):
    use_window(cfg)
    cards = check_layout(key, cfg)
    if check_only:
        return
    img, land = build_map()
    img, land = draw_inset(img, land, cfg)
    bg = annotate(img, cfg, cards)
    save(bg, key + ".dds")
    layout = os.path.join(os.environ.get("TEMP", "."), f"kehillah_layout_{key}.png")
    layout_preview(bg, cards, layout)
    print("layout preview", layout)

    for character, city in cfg["characters"].items():
        in_inset = any(city in i["cities"] for i in cfg.get("insets", ()))
        save(overlay(land, *seat_xy(cfg, city), sigma=(60 if in_inset else 95 * SCALE / 0.9)),
             f"{key}_{character}.dds")

    save(button(bg, cfg["button"]), "start_buttons", key + ".dds")
    icons = os.path.join(MOD, "gfx", "interface", "icons")
    for sub, size in (("bookmark_buttons", (580, 160)), ("bookmark_big", (336, 152))):
        path = os.path.join(icons, sub, key + ".dds")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        button(bg, cfg["button"], size=size).save(path)
        print("wrote", path)
    preview = os.path.join(os.environ.get("TEMP", "."), f"kehillah_bg_preview_{key}.png")
    bg.convert("RGB").resize((1280, 720)).save(preview)
    print("preview", preview)


def main():
    args = sys.argv[1:]
    check_only = "--check" in args
    keys = [a for a in args if a != "--check"] or list(BOOKMARKS)
    for key in keys:
        print(key)
        render(key, BOOKMARKS[key], check_only)


if __name__ == "__main__":
    main()
