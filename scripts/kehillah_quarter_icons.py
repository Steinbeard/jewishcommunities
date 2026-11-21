"""Draw the Kehillah Quarter's building icons (2026-11-20).

Vanilla's domicile building icons are flat dark glyphs, 124x125 RGBA DDS
(gfx/interface/icons/domicile_building/). These are drawn to match, at four
times the size and scaled down, so they stay crisp. Deterministic: rerun to
rebuild every icon; edit a glyph function to redraw one.

    python scripts/kehillah_quarter_icons.py            # write the DDS icons
    python scripts/kehillah_quarter_icons.py --preview  # also a preview sheet
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "gfx" / "interface" / "icons" / "domicile_building"
W, H = 124, 125
S = 4
INK = (24, 22, 20, 255)
CUT = (0, 0, 0, 0)


def P(*pts):
    return [(round(x * S), round(y * S)) for x, y in pts]


def R(x0, y0, x1, y1):
    return (round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S))


def canvas():
    im = Image.new("RGBA", (W * S, H * S), CUT)
    return im, ImageDraw.Draw(im)


def arch(d, x0, y0, x1, y1, fill):
    """An arched opening or panel: a rectangle with a round top."""
    r = (x1 - x0) / 2
    d.rectangle(R(x0, y0 + r, x1, y1), fill=fill)
    d.pieslice(R(x0, y0, x1, y0 + 2 * r), 180, 360, fill=fill)


def ring(d, cx, cy, r, w, fill=INK):
    d.ellipse(R(cx - r, cy - r, cx + r, cy + r), outline=fill, width=round(w * S))


# --- the glyphs -----------------------------------------------------------------

def synagogue():
    im, d = canvas()
    d.rectangle(R(14, 58, 110, 108), fill=INK)                     # body
    d.polygon(P((8, 60), (62, 30), (116, 60)), fill=INK)            # roof
    d.rectangle(R(8, 106, 116, 114), fill=INK)                     # step
    # the tablets on the gable
    arch(d, 50, 10, 61, 30, INK)
    arch(d, 63, 10, 74, 30, INK)
    for x in (52, 65):
        d.line(R(x, 21, x + 7, 21), fill=CUT, width=S)
        d.line(R(x, 25, x + 7, 25), fill=CUT, width=S)
    arch(d, 52, 66, 72, 106, CUT)                                   # door
    for x in (22, 90):
        arch(d, x, 68, x + 12, 90, CUT)                             # windows
    ring(d, 62, 50, 5, 2.2, CUT)                                    # rose window
    return im


def beit_midrash():
    im, d = canvas()
    # an open book on a lectern
    d.polygon(P((10, 36), (60, 46), (60, 78), (10, 68)), fill=INK)
    d.polygon(P((114, 36), (64, 46), (64, 78), (114, 68)), fill=INK)
    for i in range(4):
        y = 50 + i * 6
        d.line(P((18, y - 4), (54, y + 3)), fill=CUT, width=round(1.6 * S))
        d.line(P((106, y - 4), (70, y + 3)), fill=CUT, width=round(1.6 * S))
    d.polygon(P((24, 82), (100, 82), (90, 90), (34, 90)), fill=INK)  # rest
    d.rectangle(R(57, 90, 67, 112), fill=INK)                      # stem
    d.rectangle(R(38, 110, 86, 116), fill=INK)                     # foot
    # an oil lamp's flame above
    d.ellipse(R(56, 14, 68, 30), fill=INK)
    d.polygon(P((56, 22), (62, 4), (68, 22)), fill=INK)
    return im


def kahal_house():
    im, d = canvas()
    d.polygon(P((8, 44), (62, 14), (116, 44)), fill=INK)            # pediment
    d.rectangle(R(12, 44, 112, 52), fill=INK)                      # entablature
    for x in (18, 40, 74, 96):
        d.rectangle(R(x, 54, x + 10, 100), fill=INK)               # columns
    d.rectangle(R(50, 60, 74, 100), fill=INK)                      # door wall
    arch(d, 55, 66, 69, 100, CUT)
    d.rectangle(R(8, 100, 116, 108), fill=INK)
    d.rectangle(R(4, 108, 120, 114), fill=INK)
    ring(d, 62, 33, 6, 2.4, CUT)                                    # the seal
    return im


def hekdesh():
    im, d = canvas()
    # a charity box (pushke) and a coin
    d.rounded_rectangle(R(24, 52, 100, 112), radius=6 * S, fill=INK)
    d.rectangle(R(18, 46, 106, 56), fill=INK)
    d.rounded_rectangle(R(46, 49, 78, 53), radius=S, fill=CUT)      # slot
    d.ellipse(R(48, 8, 76, 36), fill=INK)                          # coin
    ring(d, 62, 22, 9, 1.6, CUT)
    d.rectangle(R(40, 70, 84, 74), fill=CUT)                        # band
    d.rectangle(R(40, 88, 84, 92), fill=CUT)
    return im


def kosher_market():
    im, d = canvas()
    d.rectangle(R(12, 20, 112, 30), fill=INK)                      # awning top
    for i in range(6):                                              # scallops
        x = 12 + i * 100 / 6
        d.pieslice(R(x, 22, x + 100 / 6, 44), 0, 180, fill=INK)
    d.rectangle(R(16, 30, 22, 112), fill=INK)                      # posts
    d.rectangle(R(102, 30, 108, 112), fill=INK)
    d.rectangle(R(10, 86, 114, 96), fill=INK)                      # counter
    d.rectangle(R(16, 96, 108, 112), fill=INK)
    # a jug and a loaf on the counter
    d.ellipse(R(30, 58, 52, 86), fill=INK)
    d.rectangle(R(37, 50, 45, 62), fill=INK)
    ring(d, 54, 70, 6, 2.5)
    d.ellipse(R(66, 66, 98, 86), fill=INK)
    for x in (74, 82, 90):
        d.line(R(x, 70, x - 3, 80), fill=CUT, width=round(1.5 * S))
    return im


def craft_row():
    im, d = canvas()
    # an anvil and a hammer
    d.polygon(P((14, 70), (98, 70), (110, 62), (110, 76), (88, 82), (32, 82)), fill=INK)
    d.rectangle(R(44, 82, 74, 100), fill=INK)
    d.polygon(P((30, 100), (88, 100), (94, 112), (24, 112)), fill=INK)
    d.polygon(P((70, 18), (84, 10), (104, 44), (90, 52)), fill=INK)  # head
    d.polygon(P((42, 56), (50, 64), (92, 34), (86, 28)), fill=INK)    # haft
    return im


def bankers_row():
    im, d = canvas()
    # a balance and a stack of coins
    d.rectangle(R(59, 14, 65, 98), fill=INK)
    d.rectangle(R(40, 98, 84, 106), fill=INK)
    d.rectangle(R(30, 106, 94, 112), fill=INK)
    d.rectangle(R(16, 22, 108, 27), fill=INK)
    d.ellipse(R(56, 8, 68, 20), fill=INK)
    for cx in (24, 100):
        d.line(R(cx, 27, cx - 12, 56), fill=INK, width=round(1.8 * S))
        d.line(R(cx, 27, cx + 12, 56), fill=INK, width=round(1.8 * S))
        d.chord(R(cx - 18, 46, cx + 18, 66), 0, 180, fill=INK)
    for i in range(3):                                              # coins
        y = 40 - i * 7
        d.ellipse(R(88, y, 112, y + 10), fill=INK)
        d.ellipse(R(91, y + 2, 109, y + 7), fill=CUT)
        d.ellipse(R(91, y + 3, 109, y + 8), fill=INK)
    return im


def funduq():
    im, d = canvas()
    # a lateen-rigged ship
    d.polygon(P((8, 82), (116, 82), (100, 104), (24, 104)), fill=INK)
    d.rectangle(R(58, 18, 63, 84), fill=INK)
    d.polygon(P((30, 76), (98, 10), (66, 78)), fill=INK)
    d.line(P((24, 80), (104, 8)), fill=INK, width=round(2.2 * S))
    for x in (36, 54, 72, 90):
        d.ellipse(R(x, 88, x + 6, 94), fill=CUT)
    d.arc(R(4, 106, 40, 120), 200, 340, fill=INK, width=round(2.5 * S))
    d.arc(R(44, 106, 80, 120), 200, 340, fill=INK, width=round(2.5 * S))
    d.arc(R(84, 106, 120, 120), 200, 340, fill=INK, width=round(2.5 * S))
    return im


def wall_and_gates():
    im, d = canvas()
    for x in (8, 84):                                               # towers
        d.rectangle(R(x, 26, x + 32, 114), fill=INK)
        for k in range(3):
            d.rectangle(R(x + k * 12, 16, x + k * 12 + 8, 26), fill=INK)
        arch(d, x + 11, 40, x + 21, 58, CUT)
    d.rectangle(R(38, 44, 86, 114), fill=INK)                      # gatehouse
    for k in range(4):
        d.rectangle(R(38 + k * 13, 34, 38 + k * 13 + 8, 44), fill=INK)
    arch(d, 46, 64, 78, 114, CUT)                                   # gate
    for x in (52, 59, 66, 73):
        d.rectangle(R(x, 70, x + 2, 114), fill=INK)                # portcullis
    return im


def kosher_butchers():
    im, d = canvas()
    # the shochet's knife (chalaf): a long straight blade, square-ended
    d.polygon(P((10, 58), (92, 58), (92, 70), (10, 70)), fill=INK)
    d.rounded_rectangle(R(90, 54, 118, 74), radius=4 * S, fill=INK)
    d.ellipse(R(100, 60, 106, 66), fill=CUT)
    d.line(P((14, 64), (86, 64)), fill=CUT, width=round(1.2 * S))
    # a whetstone below
    d.rounded_rectangle(R(30, 84, 94, 100), radius=4 * S, fill=INK)
    return im


def kosher_winery():
    im, d = canvas()
    # a cluster of grapes with a leaf
    pts = [(62, 46), (50, 52), (74, 52), (40, 62), (62, 60), (84, 62),
           (50, 72), (74, 72), (62, 82), (56, 92), (68, 92), (62, 102)]
    for cx, cy in pts:
        d.ellipse(R(cx - 9, cy - 9, cx + 9, cy + 9), fill=INK)
    for cx, cy in pts:
        d.arc(R(cx - 6, cy - 6, cx + 2, cy + 2), 200, 270, fill=CUT, width=S)
    d.rectangle(R(60, 18, 64, 40), fill=INK)                       # stem
    d.polygon(P((64, 30), (96, 14), (110, 30), (92, 42), (70, 40)), fill=INK)
    d.line(P((70, 36), (100, 24)), fill=CUT, width=round(1.2 * S))
    return im


def trade_dyers():
    im, d = canvas()
    d.polygon(P((22, 64), (102, 64), (92, 112), (32, 112)), fill=INK)  # vat
    d.rectangle(R(16, 58, 108, 66), fill=INK)
    d.rectangle(R(30, 80, 94, 84), fill=CUT)
    d.rectangle(R(8, 16, 116, 22), fill=INK)                        # pole
    d.polygon(P((30, 22), (58, 22), (54, 50), (34, 46)), fill=INK)   # cloth
    d.polygon(P((66, 22), (94, 22), (92, 44), (70, 48)), fill=INK)
    for x, y in ((40, 52), (78, 52)):                                # drops
        d.ellipse(R(x, y, x + 6, y + 8), fill=INK)
    return im


def trade_silk_weavers():
    im, d = canvas()
    # a spool and a running thread
    d.rectangle(R(30, 22, 74, 30), fill=INK)
    d.rectangle(R(30, 96, 74, 104), fill=INK)
    d.rectangle(R(38, 30, 66, 96), fill=INK)
    for y in range(36, 92, 7):
        d.line(R(38, y, 66, y + 3), fill=CUT, width=round(1.2 * S))
    d.line(P((66, 60), (84, 52), (96, 64), (88, 80), (104, 92), (116, 84)),
           fill=INK, width=round(2.4 * S), joint="curve")
    return im


def trade_goldsmiths():
    im, d = canvas()
    ring(d, 62, 78, 30, 9)                                          # the ring
    d.polygon(P((44, 40), (80, 40), (90, 30), (62, 8), (34, 30)), fill=INK)  # gem
    d.line(P((34, 30), (90, 30)), fill=CUT, width=round(1.4 * S))
    d.line(P((52, 30), (62, 8), (72, 30)), fill=CUT, width=round(1.4 * S))
    return im


def trade_tanners():
    im, d = canvas()
    d.rectangle(R(10, 10, 114, 16), fill=INK)                      # frame
    d.rectangle(R(10, 108, 114, 114), fill=INK)
    d.rectangle(R(10, 10, 16, 114), fill=INK)
    d.rectangle(R(108, 10, 114, 114), fill=INK)
    d.polygon(P((30, 30), (48, 24), (62, 32), (76, 24), (94, 30), (90, 56), (98, 80),
                (84, 98), (62, 92), (40, 98), (26, 80), (34, 56)), fill=INK)  # hide
    for x, y in ((30, 30), (94, 30), (26, 80), (98, 80), (62, 32), (62, 92)):
        tx = 16 if x < 62 else (108 if x > 62 else x)
        ty = y if x != 62 else (16 if y < 62 else 108)
        d.line(P((x, y), (tx, ty)), fill=INK, width=round(1.4 * S))
    return im


def trade_glassmakers():
    im, d = canvas()
    d.ellipse(R(28, 52, 96, 114), fill=INK)                        # flask body
    d.rectangle(R(54, 18, 70, 60), fill=INK)                       # neck
    d.rectangle(R(48, 12, 76, 20), fill=INK)                       # lip
    d.arc(R(38, 62, 70, 100), 120, 200, fill=CUT, width=round(2.5 * S))  # shine
    return im


def trade_clothiers():
    im, d = canvas()
    # folded cloth and shears
    for k in range(3):
        y = 80 + k * 11
        d.rounded_rectangle(R(14, y, 110, y + 9), radius=3 * S, fill=INK)
    ring(d, 36, 30, 11, 4)
    ring(d, 36, 58, 11, 4)
    d.polygon(P((45, 34), (110, 66), (106, 72), (44, 42)), fill=INK)
    d.polygon(P((45, 54), (110, 62), (108, 56), (44, 46)), fill=INK)
    return im


def trade_apothecaries():
    im, d = canvas()
    d.chord(R(16, 40, 108, 108), 0, 180, fill=INK)                  # mortar bowl
    d.rectangle(R(16, 70, 108, 76), fill=INK)
    d.polygon(P((44, 106), (80, 106), (88, 114), (36, 114)), fill=INK)
    d.polygon(P((70, 70), (100, 10), (110, 16), (82, 74)), fill=INK)  # pestle
    d.ellipse(R(96, 4, 114, 20), fill=INK)
    return im


GLYPHS = {
    "synagogue": synagogue, "beit_midrash": beit_midrash, "kahal_house": kahal_house,
    "hekdesh": hekdesh, "kosher_market": kosher_market, "craft_row": craft_row,
    "bankers_row": bankers_row, "funduq": funduq, "wall_and_gates": wall_and_gates,
    "kosher_butchers": kosher_butchers, "kosher_winery": kosher_winery,
    "trade_dyers": trade_dyers, "trade_silk_weavers": trade_silk_weavers,
    "trade_goldsmiths": trade_goldsmiths, "trade_tanners": trade_tanners,
    "trade_glassmakers": trade_glassmakers, "trade_clothiers": trade_clothiers,
    "trade_apothecaries": trade_apothecaries,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    icons = {}
    for name, fn in GLYPHS.items():
        icon = fn().resize((W, H), Image.LANCZOS)
        icon.save(OUT / f"kehillah_{name}.dds")
        icons[name] = icon
        print("wrote", OUT / f"kehillah_{name}.dds")
    if "--preview" in sys.argv:
        cols = 6
        rows = math.ceil(len(icons) / cols)
        sheet = Image.new("RGBA", (cols * (W + 16), rows * (H + 16)), (200, 190, 170, 255))
        for i, icon in enumerate(icons.values()):
            sheet.alpha_composite(icon, ((i % cols) * (W + 16) + 8, (i // cols) * (H + 16) + 8))
        path = ROOT / "docs" / "implementation" / "assets" / "kehillah-quarter-icons-preview.png"
        sheet.save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
