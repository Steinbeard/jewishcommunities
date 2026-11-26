"""Pack the two Jerusalem skyline paintings into CK3 domicile textures."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'scripts/quarter_scene_sources'
OUTPUT = ROOT / 'gfx/interface/window_domiciles'


def main():
    for landmark in ('dome', 'temple'):
        image = Image.open(SOURCE / f'kehillah_quarter_jerusalem_{landmark}_imagegen.png').convert('RGB')
        if abs(image.width / image.height - 2412 / 1112) > 0.01:
            raise ValueError(f'Unexpected {landmark} image proportions')
        image.resize((2412, 1112), Image.Resampling.LANCZOS).save(
            OUTPUT / f'kehillah_quarter_jerusalem_{landmark}.dds', pixel_format='DXT1')
        print(f'Packed Jerusalem {landmark}')


if __name__ == '__main__':
    main()
