"""Paint the Kehillah Quarter's building scenes (art level 3, Quarter spec section 10).

CK3 draws each domicile building as a painted, transparent 512x512 texture
plus a PNG intersection mask (white where the building is), in
gfx/interface/window_domiciles/. This script generates one per building
family and region from the prompts in kehillah_quarter_scene_prompts.json,
removes the background, and writes both files under
gfx/interface/window_domiciles/kehillah_<family>_<region>.dds / _mask.png.

The buildings file still points at vanilla merchant-company art (level 1).
After a run, point a family's `asset` blocks at the new files (the
paths are printed).

    python scripts/kehillah_quarter_scene_art.py                 # every family and region
    python scripts/kehillah_quarter_scene_art.py synagogue       # one family
    python scripts/kehillah_quarter_scene_art.py --reprocess     # rebuild from saved sources

Needs OPENAI_API_KEY in the environment (never in the repo) and
`pip install rembg[cpu]`, as scripts/make_trait_icons.py does. Raw
generations are kept in scripts/quarter_scene_sources/ so the textures can
be rebuilt without paying again.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_trait_icons import generate, strip_background  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "scripts" / "kehillah_quarter_scene_prompts.json"
SOURCES = ROOT / "scripts" / "quarter_scene_sources"
OUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = 512


def finish(img):
    img = strip_background(img)
    bbox = img.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    img = img.crop(bbox)
    scale = (SIZE * 0.92) / max(img.size)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.paste(img, ((SIZE - img.width) // 2, SIZE - img.height - 8), img)
    mask = canvas.getchannel("A").point(lambda a: 255 if a > 40 else 0).convert("RGBA")
    return canvas, mask


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("families", nargs="*")
    ap.add_argument("--reprocess", action="store_true")
    ap.add_argument("--model", default="gpt-image-1")
    args = ap.parse_args()
    cfg = json.loads(PROMPTS.read_text(encoding="utf-8"))
    families = args.families or list(cfg["families"])
    SOURCES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for fam in families:
        for region, regional in cfg["regions"].items():
            name = f"kehillah_{fam}_{region}"
            src = SOURCES / f"{name}.png"
            if args.reprocess:
                if not src.exists():
                    print("skip", name)
                    continue
                img = Image.open(src).convert("RGBA")
            else:
                prompt = f"{cfg['style']} {regional} Subject: {cfg['families'][fam]}"
                img = generate(prompt, args.model)
                img.save(src)
            tex, mask = finish(img)
            tex.save(OUT / f"{name}.dds")
            mask.save(OUT / f"{name}_mask.png")
            print("wrote", f"gfx/interface/window_domiciles/{name}.dds", "and _mask.png")


if __name__ == "__main__":
    main()
