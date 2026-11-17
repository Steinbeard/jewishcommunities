"""Render the 640x640 Workshop thumbnail (docs/release/thumbnail.png).

Usage: python scripts/kehillah_make_thumbnail.py docs/release/thumbnail.png
Uses the 1066 bookmark map and the vanilla ce_menorah emblem.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

MOD = r"C:/Users/Daniel/Documents/Paradox Interactive/Crusader Kings III/mod/jewishcommunities/"
GAME = r"E:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/"
OUT = sys.argv[1]
W = H = 640
SS = 2  # supersample for smooth edges
w, h = W * SS, H * SS

# --- background: the 1066 bookmark map, Troyes/Worms down to Granada/Fez ---
bm = Image.open(MOD + "gfx/interface/bookmarks/bm_1066_kehillah_worms.dds").convert("RGB")
bg = bm.crop((460, 0, 1460, 1000)).resize((w, h), Image.LANCZOS)

# warm it and knock it back so the banner and title read first
bg = Image.blend(bg, Image.new("RGB", (w, h), (70, 48, 30)), 0.30)

# vignette + a dark band at the bottom for the title
mask = Image.new("L", (w, h), 0)
d = ImageDraw.Draw(mask)
for i in range(60):
    t = i / 60
    d.rectangle([int(t * w * 0.12), int(t * h * 0.10), w - int(t * w * 0.12), h - int(t * h * 0.10)], fill=int(255 * t))
mask = mask.filter(ImageFilter.GaussianBlur(60 * SS))
dark = Image.new("RGB", (w, h), (18, 12, 8))
bg = Image.composite(bg, dark, mask)

grad = Image.new("L", (1, h))
for y in range(h):
    t = max(0.0, (y / h - 0.52) / 0.48)
    grad.putpixel((0, y), int(235 * min(1, t ** 1.1)))
bg = Image.composite(dark, bg, grad.resize((w, h)))
canvas = bg.convert("RGBA")

# --- the Kehillah banner: green CK3-style shield with a gold menorah ---
bw, bh = int(250 * SS), int(300 * SS)
bx, by = (w - bw) // 2, int(40 * SS)

def banner_shape(width, height, inset=0):
    m = Image.new("L", (width, height), 0)
    dd = ImageDraw.Draw(m)
    i = inset
    pts = [(i, i), (width - i, i), (width - i, int(height * 0.70)), (width // 2, height - i), (i, int(height * 0.70))]
    dd.polygon(pts, fill=255)
    return m

shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sm = banner_shape(bw, bh)
shadow.paste((0, 0, 0, 170), (bx + 6 * SS, by + 10 * SS), sm)
canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14 * SS)))

gold = (214, 172, 92)
outer = banner_shape(bw, bh)
inner = banner_shape(bw, bh, inset=9 * SS)
canvas.paste(gold + (255,), (bx, by), outer)

# green field with a soft top-light
field = Image.new("RGBA", (bw, bh), (34, 96, 58, 255))
shade = Image.new("L", (bw, bh))
for y in range(bh):
    for_x = 0
    shade.paste(int(70 * (y / bh)), (0, y, bw, y + 1))
field = Image.composite(Image.new("RGBA", (bw, bh), (14, 52, 30, 255)), field, shade)
canvas.paste(field, (bx, by), inner)

# thin inner gold line
line = ImageChops.subtract(banner_shape(bw, bh, inset=17 * SS), banner_shape(bw, bh, inset=20 * SS))
canvas.paste(gold + (200,), (bx, by), line)

# menorah: vanilla colored emblem, alpha as the shape, recoloured gold with a shadow
men = Image.open(GAME + "gfx/coat_of_arms/colored_emblems/ce_menorah.dds").convert("RGBA")
alpha = men.split()[3]
bbox = alpha.getbbox()
alpha = alpha.crop(bbox)
mw = int(bw * 0.70)
mh = int(alpha.height * mw / alpha.width)
alpha = alpha.resize((mw, mh), Image.LANCZOS)
mx = bx + (bw - mw) // 2
my = by + int(bh * 0.40) - mh // 2
msh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
msh.paste((0, 0, 0, 150), (mx + 3 * SS, my + 5 * SS), alpha)
canvas.alpha_composite(msh.filter(ImageFilter.GaussianBlur(4 * SS)))
goldfill = Image.new("RGBA", (mw, mh))
for y in range(mh):
    t = y / mh
    c = tuple(int(a + (b - a) * t) for a, b in zip((246, 214, 140), (176, 128, 56)))
    goldfill.paste(c + (255,), (0, y, mw, y + 1))
canvas.paste(goldfill, (mx, my), alpha)

# --- title ---
d = ImageDraw.Draw(canvas)
title_font = ImageFont.truetype("C:/Windows/Fonts/BOOKOSB.TTF", 56 * SS)
sub_font = ImageFont.truetype("C:/Windows/Fonts/pala.ttf", 25 * SS)

def centred(text, y, font, fill, shadow=True):
    tw = d.textlength(text, font=font)
    x = (w - tw) / 2
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 2 * SS, y + 3 * SS), text, font=font, fill=(0, 0, 0, 220))
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3 * SS)))
    ImageDraw.Draw(canvas).text((x, y), text, font=font, fill=fill)

centred("Jewish", 388 * SS, title_font, (240, 214, 160))
centred("Communities", 446 * SS, title_font, (240, 214, 160))
# rule between title and subtitle
ry = 528 * SS
d = ImageDraw.Draw(canvas)
d.line([(w // 2 - 120 * SS, ry), (w // 2 - 14 * SS, ry)], fill=gold + (200,), width=2 * SS)
d.line([(w // 2 + 14 * SS, ry), (w // 2 + 120 * SS, ry)], fill=gold + (200,), width=2 * SS)
d.ellipse([w // 2 - 5 * SS, ry - 5 * SS, w // 2 + 5 * SS, ry + 5 * SS], fill=gold + (230,))
centred("A Crusader Kings III mod", 548 * SS, sub_font, (222, 206, 178))
centred("Pre-Alpha", 584 * SS, sub_font, (190, 160, 110), shadow=False)

out = canvas.convert("RGB").resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True)
import os
print(OUT, out.size, os.path.getsize(OUT) // 1024, "KB")
