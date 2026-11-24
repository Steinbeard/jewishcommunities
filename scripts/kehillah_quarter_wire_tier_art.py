"""Point every Western/MENA Quarter exterior tier at its v4 packed sprite.

Run after kehillah_quarter_tier_sprite_pack.py. This deliberately leaves the
Asian asset branch and all gameplay/building definitions unchanged.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
BUILDINGS = ROOT / "common" / "domiciles" / "buildings" / "kehillah_domicile_buildings.txt"
TEXTURES = ROOT / "gfx" / "interface" / "window_domiciles"
FAMILIES = {
    "synagogue": ("synagogue", range(1, 6)),
    "beit_midrash": ("beit_midrash", range(1, 6)),
    "countinghouse": ("kahal_house", range(1, 4)),
    "hekdesh": ("hekdesh", range(1, 4)),
    "market_stalls": ("market_stalls", range(1, 4)),
    "workshops": ("workshops", range(1, 4)),
    "bankers_row": ("bankers_row", range(1, 4)),
    "funduq": ("funduq", range(1, 4)),
    "wall": ("wall", range(1, 4)),
    "wall_site": ("wall", range(0, 1)),
}
ASSET = re.compile(r"(?ms)^\tasset = \{\r?\n.*?^\t\}")
LINE = re.compile(r'(?m)^(\t\t(?:texture|intersectionmask_texture) = ")[^"]+("\r?$)')


def update_asset(asset: str, family: str, region: str, stage: int) -> str:
    stem = f"kehillah_quarter_v4_{family}_{region}_s{stage}"
    for extension in (".dds", "_mask.png"):
        if not (TEXTURES / f"{stem}{extension}").is_file():
            raise FileNotFoundError(TEXTURES / f"{stem}{extension}")
    lines = LINE.findall(asset)
    if len(lines) != 2:
        raise ValueError(f"Expected texture and mask in asset for {stem}")
    texture = f"gfx/interface/window_domiciles/{stem}.dds"
    mask = f"gfx/interface/window_domiciles/{stem}_mask.png"
    asset, n_texture = re.subn(
        r'(?m)^(\t\ttexture = ")[^"]+("\r?$)',
        lambda match: match.group(1) + texture + match.group(2), asset,
    )
    asset, n_mask = re.subn(
        r'(?m)^(\t\tintersectionmask_texture = ")[^"]+("\r?$)',
        lambda match: match.group(1) + mask + match.group(2), asset,
    )
    if (n_texture, n_mask) != (1, 1):
        raise ValueError(f"Failed to wire {stem}")
    return asset


def main() -> None:
    with BUILDINGS.open("r", encoding="utf-8", newline="") as file:
        content = file.read()
    count = 0
    for code_family, (sprite_family, stages) in FAMILIES.items():
        for stage in stages:
            identifier = f"kehillah_{code_family}_{stage:02d}"
            head = re.search(rf"(?m)^{identifier} = \{{\r?$", content)
            if not head:
                raise ValueError(f"Missing building: {identifier}")
            next_head = re.search(r"(?m)^kehillah_[a-z0-9_]+ = \{\r?$", content[head.end():])
            end = head.end() + next_head.start() if next_head else len(content)
            section = content[head.start():end]
            assets = list(ASSET.finditer(section))
            if len(assets) != 3:
                raise ValueError(f"Expected 3 regional assets for {identifier}: {len(assets)}")
            replacements = []
            for match in assets:
                asset = match.group()
                if "company_domicile_western_asset_trigger" in asset:
                    region = "western"
                elif "company_domicile_asian_asset_trigger" in asset:
                    continue
                else:
                    region = "mena"
                replacements.append((match.start(), match.end(), update_asset(asset, sprite_family, region, stage)))
                count += 1
            if len(replacements) != 2:
                raise ValueError(f"Expected Western and MENA assets for {identifier}")
            for start, stop, new_asset in reversed(replacements):
                section = section[:start] + new_asset + section[stop:]
            content = content[:head.start()] + section + content[end:]
    if count != 64:
        raise ValueError(f"Expected 64 regional asset references, got {count}")
    with BUILDINGS.open("w", encoding="utf-8", newline="") as file:
        file.write(content)
    print(f"Wired {count} regional Quarter art references")


if __name__ == "__main__":
    main()
