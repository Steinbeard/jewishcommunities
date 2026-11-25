"""Derive the winter Quarter background from the finished summer painting.

Run after scripts/kehillah_quarter_background_art.py:
    python scripts/kehillah_quarter_winter_art.py [western|mena ...]

This is a scripted PLACEHOLDER, not painted art: it lays snow over roofs and
open ground, mutes the greenery and cools the light. The composition is the
summer painting's, pixel for pixel, so every building slot and click mask
lined up against the summer background still lines up in winter. Replace the
output with a painted winter scene of the same layout when one exists.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "quarter_scene_sources"
OUTPUT = ROOT / "gfx" / "interface" / "window_domiciles"
SIZE = (2412, 1112)
SNOW = np.array((236.0, 241.0, 250.0))
SHADOW = np.array((176.0, 190.0, 214.0))


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def noise(shape: tuple[int, int], scale: int, seed: int) -> np.ndarray:
    """Soft value noise in 0..1, so snow cover is patchy rather than flat."""
    rng = np.random.default_rng(seed)
    small = rng.random((shape[0] // scale + 2, shape[1] // scale + 2))
    img = Image.fromarray((small * 255).astype(np.uint8)).resize(
        (shape[1], shape[0]), Image.Resampling.BICUBIC)
    return np.asarray(img, dtype=np.float32) / 255.0


def winterise(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    hi = rgb.max(axis=2)
    lo = rgb.min(axis=2)
    sat = (hi - lo) / np.maximum(hi, 1.0)
    shape = lum.shape

    # Linework and deep shadow keep their ink: snow only settles on
    # mid-to-light painted surfaces.
    lit = smoothstep(45.0, 115.0, lum)

    # Terracotta and slate roofs: warm, reddish surfaces.
    roof = smoothstep(0.18, 0.40, sat) * smoothstep(1.10, 1.45, r / np.maximum(g, 1.0))
    # Open ground: the pale sandy courtyard and paths.
    ground = (1.0 - smoothstep(0.38, 0.62, sat)) * smoothstep(105.0, 150.0, lum)
    # Foliage: green-dominant pixels.
    green = smoothstep(0.0, 18.0, g - np.maximum(r, b) + 6.0) * smoothstep(0.10, 0.30, sat)

    # Snow lies on the upper faces: favour pixels whose neighbour above is
    # darker (a top edge), which picks out ridges, eaves and wall-tops.
    above = np.roll(lum, 3, axis=0)
    top_edge = smoothstep(4.0, 30.0, lum - above)
    patch = noise(shape, 22, 7) * 0.6 + noise(shape, 6, 11) * 0.4

    cover = np.maximum.reduce((
        roof * (0.78 + 0.20 * patch),
        ground * (0.74 + 0.24 * patch),
        green * 0.40 * patch,
        top_edge * 0.55,
    ))
    cover = np.clip(cover * lit, 0.0, 0.94)
    # Soften the mask so snow reads as drifts, not per-pixel speckle.
    cover = np.asarray(
        Image.fromarray((cover * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)),
        dtype=np.float32) / 255.0

    # Shade the snow with the painting's own light: darker painted areas get
    # blue-grey snow, lighter ones near-white.
    shade = smoothstep(90.0, 210.0, lum)[..., None]
    snow_colour = SHADOW + (SNOW - SHADOW) * shade

    # Winter light: desaturate, mute foliage, cool the whole scene.
    grey = lum[..., None].repeat(3, axis=2)
    base = rgb + (grey - rgb) * (0.38 + 0.25 * green[..., None])
    base = base * np.array((0.93, 0.97, 1.06))
    base = base * (1.0 - 0.10 * green[..., None])

    out = base + (snow_colour - base) * cover[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def build(region: str) -> None:
    name = f"kehillah_quarter_background_{region}"
    summer = Image.open(SOURCE / f"{name}_lived_v4.png")
    winter = winterise(summer)
    winter.save(SOURCE / f"{name}_winter_v1.png")
    winter = winter.resize(SIZE, Image.Resampling.LANCZOS)
    winter.save(OUTPUT / f"{name}_winter.dds", pixel_format="DXT1")


if __name__ == "__main__":
    for region_name in sys.argv[1:] or ("western",):
        build(region_name)
