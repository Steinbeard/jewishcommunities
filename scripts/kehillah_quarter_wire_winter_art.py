"""Add seasonal Western art before each existing Western building asset."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / 'common/domiciles/buildings/kehillah_domicile_buildings.txt'
ASSET = re.compile(r'(?ms)^\tasset = \{\r?\n.*?^\t\}')
TRIGGER = 'trigger = { company_domicile_western_asset_trigger = yes }'
WINTER_TRIGGER = '''trigger = {
            company_domicile_western_asset_trigger = yes
            domicile_location = {
                OR = {
                    has_province_modifier = winter_normal_modifier
                    has_province_modifier = winter_harsh_modifier
                }
            }
        }'''


def main():
    content = FILE.read_text(encoding='utf-8')
    if '_western_s1_winter.dds' in content:
        raise ValueError('Winter assets already wired')
    count = 0

    def add(match):
        nonlocal count
        asset = match.group()
        if TRIGGER not in asset:
            return asset
        texture = re.search(r'kehillah_quarter_v4_[a-z_]+_western_s\d+\.dds', asset)
        mask = re.search(r'kehillah_quarter_v4_[a-z_]+_western_s\d+_mask\.png', asset)
        if not texture or not mask:
            raise ValueError('Unexpected Western asset: ' + asset)
        winter_texture = texture.group().replace('.dds', '_winter.dds')
        winter_mask = mask.group().replace('_mask.png', '_winter_mask.png')
        for name in (winter_texture, winter_mask):
            if not (ROOT / 'gfx/interface/window_domiciles' / name).is_file():
                raise FileNotFoundError(name)
        winter = asset.replace(TRIGGER, WINTER_TRIGGER).replace(texture.group(), winter_texture).replace(mask.group(), winter_mask)
        count += 1
        return winter + '\n' + asset

    updated = ASSET.sub(add, content)
    if count != 32:
        raise ValueError(f'Expected 32 Western assets, found {count}')
    FILE.write_text(updated, encoding='utf-8')
    print(f'Added {count} winter assets')


if __name__ == '__main__':
    main()
