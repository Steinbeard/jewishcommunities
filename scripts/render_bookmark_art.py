"""Render the 1066 Kehillah bookmark art: a painted-style map of Francia,
the Rhineland and al-Andalus, drawn from the game's own heightmap and river
map, with the three starting communities marked; one highlight overlay per
bookmark character; and the two start-screen buttons.

Run:  python -I scripts/render_bookmark_art.py
Reads the installed game's map_data; writes into gfx/interface/bookmarks/.
"""
import os
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

# Window onto the game map, in provinces.png pixel coordinates.
SCALE = 0.9
OX, OY = 394, 1302
WIN_W, WIN_H = W / SCALE, H / SCALE

# Community seats (province centroids in provinces.png space).
CITIES = {
    "worms": (1406.3, 1487.0),
    "troyes": (1172.1, 1579.8),
    "granada": (748.4, 2376.2),
}
WATER = 4626  # heightmap value of the sea surface


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


def build_map():
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


def annotate(img):
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Regions, as the community itself named them.
    big = font("GARAIT.TTF", 46)
    for text, centre, alpha in (
        ("Sefarad", (300, 690), 165),
        ("Tzarfat", (600, 470), 165),
        ("Ashkenaz", (1090, 215), 165),
    ):
        w = spaced_width(d, text, big, 14)
        spaced(d, (centre[0] - w / 2, centre[1] - 25), text, big, (70, 52, 34, alpha), 14)

    # Seats.
    lab = font("GARABD.TTF", 26)
    for name, label, off in (
        ("worms", "Worms", (22, -6)),
        ("troyes", "Troyes", (-100, 4)),
        ("granada", "Granada", (22, -8)),
    ):
        cx, cy = to_img(CITIES[name])
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(60, 40, 24, 230))
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=(226, 184, 74, 255))
        d.text((cx + off[0] + 1, cy + off[1] + 1), label, font=lab, fill=(244, 232, 200, 200))
        d.text((cx + off[0], cy + off[1]), label, font=lab, fill=(52, 34, 20, 255))

    return Image.alpha_composite(base, layer)


def overlay(land, cx, cy, sigma=95, strength=185):
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sigma ** 2)))
    a = (glow * land * strength).astype(np.uint8)
    out = np.zeros((H, W, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 244, 208, 104
    out[..., 3] = a
    return Image.fromarray(out, "RGBA")


def button(bg, centre, span=1100):
    h = int(span * 140 / 548)
    cx, cy = centre
    box = (int(cx - span / 2), int(cy - h / 2), int(cx + span / 2), int(cy + h / 2))
    im = bg.crop(box).resize((548, 140), Image.LANCZOS)
    a = np.array(im).astype(np.float32)
    yy, xx = np.mgrid[0:140, 0:548]
    edge = np.minimum(np.minimum(xx, 547 - xx) / 40.0, np.minimum(yy, 139 - yy) / 20.0)
    a[..., :3] *= (0.55 + 0.45 * np.clip(edge, 0, 1))[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def save(im, *parts):
    path = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    print("wrote", path, os.path.getsize(path))


def main():
    img, land = build_map()
    bg = annotate(img)
    save(bg, "bm_1066_kehillah_worms.dds")
    save(bg, "bm_1066_kehillah_founder_test.dds")

    worms, troyes, granada = (to_img(CITIES[k]) for k in ("worms", "troyes", "granada"))
    save(overlay(land, *worms), "bm_1066_kehillah_worms_bookmark_kehillah_worms_isaac.dds")
    save(overlay(land, *troyes), "bm_1066_kehillah_worms_bookmark_kehillah_troyes_rashi.dds")
    save(overlay(land, *granada, sigma=110), "bm_1066_kehillah_worms_bookmark_kehillah_granada_joseph.dds")
    save(overlay(land, 1300, 520, sigma=140, strength=110),
         "bm_1066_kehillah_founder_test_bookmark_kehillah_founder_test.dds")

    save(button(bg, (860, 440)), "start_buttons", "bm_1066_kehillah_worms.dds")
    save(button(bg, (1250, 600)), "start_buttons", "bm_1066_kehillah_founder_test.dds")
    bg.convert("RGB").resize((1280, 720)).save(os.path.join(os.environ.get("TEMP", "."), "kehillah_bg_preview.png"))


if __name__ == "__main__":
    main()
