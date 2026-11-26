"""Pack the painted Western winter art to the existing summer slot geometry."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'scripts/quarter_scene_sources'
OUTPUT = ROOT / 'gfx/interface/window_domiciles'
# Cuts lie in the gaps between buildings, including where their snow touches.
EDGES = {
    'synagogue': (0, 345, 690, 1120, 1620, 2171),
    'beit_midrash': (0, 365, 690, 1110, 1605, 2172),
    'kahal_house': (0, 625, 1250, 2172),
    'hekdesh': (0, 630, 1380, 2172),
    'market_stalls': (0, 568, 1265, 2172),
    'workshops': (0, 583, 1275, 2172),
    'bankers_row': (0, 720, 1425, 2172),
    'wall': (0, 405, 835, 1280, 1774),
    'funduq': (0, 440, 1040, 1774),
}


def cell(sheet, box):
    pixels = np.asarray(sheet.crop(box).convert('RGBA')).copy()
    # Remove the image generator's red/yellow alpha fringe and stray pixels.
    pixels[pixels[:, :, 3] < 32] = 0
    alpha = pixels[:, :, 3] >= 32
    labels, count = ndimage.label(alpha)
    sizes = np.bincount(labels.ravel())
    small = sizes < 35
    small[0] = True
    pixels[small[labels]] = 0
    image = Image.fromarray(pixels)
    bounds = image.getchannel('A').getbbox()
    if not bounds:
        raise ValueError(f'Empty crop {box}')
    return image.crop(bounds)


def main():
    bg = Image.open(SOURCES / 'kehillah_quarter_winter_western_background_imagegen.png').convert('RGB')
    bg.resize((2412, 1112), Image.Resampling.LANCZOS).save(
        OUTPUT / 'kehillah_quarter_background_western_winter.dds', pixel_format='DXT1')
    for family, edges in EDGES.items():
        source = 'walls_funduq' if family in ('wall', 'funduq') else family
        sheet = Image.open(SOURCES / f'kehillah_quarter_winter_western_{source}_imagegen.png')
        y0, y1 = ((0, 440) if family == 'wall' else (440, 887)) if source == 'walls_funduq' else (0, sheet.height)
        for index, (left, right) in enumerate(zip(edges, edges[1:])):
            stage = index if family == 'wall' else index + 1
            original = f'kehillah_quarter_v4_{family}_western_s{stage}'
            bounds = Image.open(OUTPUT / f'{original}.dds').getchannel('A').getbbox()
            if not bounds:
                raise ValueError(f'Empty summer sprite: {original}')
            art = cell(sheet, (left, y0, right, y1))
            art = art.resize((bounds[2] - bounds[0], bounds[3] - bounds[1]), Image.Resampling.LANCZOS)
            canvas = Image.new('RGBA', (512, 512))
            canvas.alpha_composite(art, bounds[:2])
            mask = Image.new('RGBA', (512, 512), (255, 255, 255, 0))
            mask.putalpha(canvas.getchannel('A').point(lambda x: 255 if x > 40 else 0))
            if family == 'wall' and stage == 0:
                ImageDraw.Draw(mask).rectangle(bounds, fill=(255, 255, 255, 255))
            stem = f'{original}_winter'
            canvas.save(OUTPUT / f'{stem}.dds')
            mask.save(OUTPUT / f'{stem}_mask.png')
            print(stem, bounds)


if __name__ == '__main__':
    main()
