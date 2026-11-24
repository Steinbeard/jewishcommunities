"""Match composed Quarter concept scenes to each region's level-one palette.

Run: python scripts/kehillah_quarter_color_grade.py
This is a deterministic color-calibration step before sprite extraction. The
original imagegen masters stay intact; graded siblings are written beside them.
"""

from pathlib import Path
from shutil import copyfile

import numpy as np
from PIL import Image, ImageDraw
from skimage.color import lab2rgb, rgb2lab


SOURCE = Path(__file__).resolve().parent / "quarter_scene_sources"
STAGES = (1, 2, 3, 4, 5)
SKYLINE_ROWS = slice(0, 170)


def lab_image(path: Path) -> np.ndarray:
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    if rgb.shape != (852, 1846, 3):
        raise ValueError(f"Unexpected Quarter render dimensions: {path}")
    return rgb2lab(rgb)


def skyline_median(lab: np.ndarray) -> np.ndarray:
    # The skyline remains background in all stage renders. Its median is a
    # robust color reference even if individual houses were redrawn slightly.
    return np.median(lab[SKYLINE_ROWS].reshape(-1, 3), axis=0)


def grade(region: str) -> None:
    reference = SOURCE / f"kehillah_quarter_master_{region}_cued_s1.png"
    target = skyline_median(lab_image(reference))
    for stage in STAGES:
        source = SOURCE / f"kehillah_quarter_master_{region}_cued_s{stage}.png"
        output = SOURCE / f"kehillah_quarter_master_{region}_graded_s{stage}.png"
        if stage == 1:
            copyfile(source, output)
            print(f"{region} {stage}: reference, no shift")
            continue
        lab = lab_image(source)
        shift = np.clip(target - skyline_median(lab), -8.0, 8.0)
        corrected = lab2rgb(lab + shift)
        Image.fromarray(np.uint8(np.rint(corrected * 255)), "RGB").save(output)
        residual = skyline_median(lab_image(output)) - target
        if np.max(np.abs(residual)) > 0.75:
            raise ValueError(f"Palette calibration failed for {output}: {residual}")
        print(f"{region} {stage}: Lab shift {shift.round(2)}, residual {residual.round(2)}")


def make_preview() -> None:
    # Two regional columns and all five development stages, at half size.
    preview = Image.new("RGB", (1846, 5 * 446), "#1c1a16")
    draw = ImageDraw.Draw(preview)
    for row, stage in enumerate(STAGES):
        for column, region in enumerate(("western", "mena")):
            source = SOURCE / f"kehillah_quarter_master_{region}_graded_s{stage}.png"
            scene = Image.open(source).convert("RGB").resize((923, 426))
            x, y = column * 923, row * 446
            draw.text((x + 12, y + 3), f"{region.upper()}  /  LEVEL {stage}", fill="#e8ddc6")
            preview.paste(scene, (x, y + 20))
    output = SOURCE.parent.parent / "docs/implementation/assets/kehillah_quarter_normalized_all_levels.png"
    preview.save(output)
    print(f"preview: {output}")


if __name__ == "__main__":
    for region_name in ("western", "mena"):
        grade(region_name)
    make_preview()
