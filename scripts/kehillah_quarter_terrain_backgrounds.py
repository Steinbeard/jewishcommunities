"""Pack the ten painted terrain backgrounds into CK3's estate DDS format."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'scripts/quarter_scene_sources'
OUTPUT = ROOT / 'gfx/interface/window_domiciles'


def main():
    for region in ('western', 'mena'):
        for terrain in ('mountains', 'desert', 'wetlands', 'jungle', 'coast'):
            stem = f'kehillah_quarter_background_{region}_{terrain}'
            path = SOURCE / f'{stem}_study.png'
            image = Image.open(path).convert('RGB')
            if abs(image.width / image.height - 2412 / 1112) > 0.01:
                raise ValueError(f'Unexpected background aspect ratio: {path}')
            image.resize((2412, 1112), Image.Resampling.LANCZOS).save(
                OUTPUT / f'{stem}.dds', pixel_format='DXT1')
            print(stem)


if __name__ == '__main__':
    main()
