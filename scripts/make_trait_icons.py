"""Generate CK3 trait icons: AI image -> background removed -> cropped -> 120x120 DDS.

Usage:
  python scripts/make_trait_icons.py                      # every trait in the prompts file
  python scripts/make_trait_icons.py kohen levite         # just these
  python scripts/make_trait_icons.py kohen --from-image my.png   # skip generation, process a file
  python scripts/make_trait_icons.py --reprocess          # rebuild DDS from saved sources, no API calls

Needs OPENAI_API_KEY in the environment (never put it in the repo) and `pip install rembg[cpu]`.
Raw generations are kept in scripts/trait_icon_sources/ so icons can be rebuilt without paying again.
"""
import argparse
import base64
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "scripts" / "trait_icon_prompts.json"
SOURCES = ROOT / "scripts" / "trait_icon_sources"
OUT_DIR = ROOT / "gfx" / "interface" / "icons" / "traits"
ICON_SIZE = 120
MARGIN = 0.08
API_URL = "https://api.openai.com/v1/images/generations"


def generate(prompt, model):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set.")
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1,
        "background": "transparent",
        "output_format": "png",
    }).encode()
    req = urllib.request.Request(API_URL, body, {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode(errors='replace')}")
    return Image.open(io.BytesIO(base64.b64decode(data["data"][0]["b64_json"]))).convert("RGBA")


def has_transparency(img):
    alpha = img.getchannel("A")
    lo, _ = alpha.getextrema()
    if lo > 200:
        return False
    return sum(1 for a in alpha.getdata() if a < 16) > img.width * img.height * 0.05


def strip_background(img):
    if has_transparency(img):
        return img
    from rembg import new_session, remove
    # rembg's default model (bria_rmbg) exhausts memory on this machine; u2net is light.
    return remove(img, session=new_session("u2net")).convert("RGBA")


def crop_and_square(img):
    bbox = img.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if bbox is None:
        sys.exit("Nothing left after background removal.")
    img = img.crop(bbox)
    side = round(max(img.size) * (1 + 2 * MARGIN))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
    return canvas


def write_icon(name, img):
    # Square, opaque sources are already finished game icons with their own
    # background. Preserve that background instead of sending it through
    # background removal; older transparent source art still uses the cutout
    # and padding path below.
    if img.width == img.height and img.getchannel("A").getextrema()[0] > 200:
        icon = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    else:
        icon = crop_and_square(strip_background(img)).resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.dds"
    icon.save(path)
    print(f"wrote {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("traits", nargs="*", help="icon names from the prompts file (default: all)")
    ap.add_argument("--from-image", help="process this image instead of generating (one trait only)")
    ap.add_argument("--reprocess", action="store_true", help="rebuild from saved sources, no API calls")
    ap.add_argument("--model", default="gpt-image-1")
    args = ap.parse_args()

    cfg = json.loads(PROMPTS.read_text(encoding="utf-8"))
    names = args.traits or list(cfg["icons"])
    unknown = [n for n in names if n not in cfg["icons"]]
    if unknown and not args.from_image:
        sys.exit(f"Not in {PROMPTS.name}: {', '.join(unknown)}")
    if args.from_image and len(names) != 1:
        sys.exit("--from-image needs exactly one trait name.")

    SOURCES.mkdir(parents=True, exist_ok=True)
    for name in names:
        src = SOURCES / f"{name}.png"
        if args.from_image:
            img = Image.open(args.from_image).convert("RGBA")
            img.save(src)
        elif args.reprocess:
            if not src.exists():
                print(f"skip {name}: no saved source")
                continue
            img = Image.open(src).convert("RGBA")
        else:
            img = generate(f"{cfg['style']} Subject: {cfg['icons'][name]}", args.model)
            img.save(src)
        write_icon(name, img)


if __name__ == "__main__":
    main()
