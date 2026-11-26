"""Insert Quarter terrain selections after the Western snow selection."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / 'common/domiciles/types/kehillah_domicile_types.txt'
SENTINEL = '\n\tdomicile_asset = {\n\t\ttrigger = {\n\t\t\tcompany_domicile_asian_asset_trigger = yes'
TERRAINS = (
    ('mountains', 'domicile_location = { terrain = mountains }', 'rough', 'rough'),
    ('desert', 'domicile_location = { OR = { terrain = desert terrain = desert_mountains } }', 'dry', 'dry'),
    ('wetlands', 'domicile_location = { terrain = wetlands }', 'green', 'green'),
    ('jungle', 'domicile_location = { terrain = jungle }', 'jungle', 'green'),
    ('coast', 'domicile_location.county = { is_coastal_county = yes }', 'urban', 'green'),
)


def main():
    text = FILE.read_text(encoding='utf-8')
    if 'kehillah_quarter_background_western_mountains.dds' in text:
        raise ValueError('Terrain assets already inserted')
    if text.count(SENTINEL) != 3:
        raise ValueError('Unexpected Asian asset layout')
    blocks = []
    for terrain, condition, foreground, ambience in TERRAINS:
        for region in ('western', 'mena'):
            region_trigger = ('company_domicile_western_asset_trigger = yes' if region == 'western' else
                              'NOR = { company_domicile_western_asset_trigger = yes company_domicile_asian_asset_trigger = yes }')
            blocks.append(f'''\n\tdomicile_asset = {{
\t\ttrigger = {{
\t\t\t{region_trigger}
\t\t\t{condition}
\t\t}}
\t\tbackground = "gfx/interface/window_domiciles/kehillah_quarter_background_{region}_{terrain}.dds"
\t\tforeground = "gfx/interface/window_domiciles/estate_background_{foreground}_terrain_foreground.dds"
\t\tambience = "event:/DLC/EP3/SFX/Ambience/2D/Domicile/ep3_amb_2d_domicile_{ambience}_lands"
\t}}\n''')
    intro = '\n\t# Terrain precedes coast when both apply; Western snow above takes priority.\n'
    text = text.replace(SENTINEL, intro + ''.join(blocks) + SENTINEL, 1)
    FILE.write_text(text, encoding='utf-8')
    print('Inserted 10 regional terrain assets')


if __name__ == '__main__':
    main()
