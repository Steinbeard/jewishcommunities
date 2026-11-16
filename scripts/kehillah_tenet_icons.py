"""Export generated tenet art to CK3's native 260x400 DDS canvas."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("kehillah_reasoned_theology", "kehillah_scholarly_study",
         "kehillah_sacred_liturgy", "kehillah_covenant_community",
         "kehillah_sacred_homeland", "kehillah_witness")


def build():
    sheet = Image.open(ROOT / "scripts/tenet_icon_sources/kehillah_tenet_sheet.png").convert("RGBA")
    output = ROOT / "gfx/interface/icons/faith_tenets"
    output.mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(NAMES):
        if index < 5:
            art = sheet.crop((round(index * sheet.width / 5), 0,
                              round((index + 1) * sheet.width / 5), sheet.height))
        else:
            art = Image.open(ROOT / "scripts/tenet_icon_sources/kehillah_witness.png").convert("RGBA")
        art = art.crop(art.getchannel("A").getbbox())
        art.thumbnail((210, 300), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (260, 400), (0, 0, 0, 0))
        canvas.paste(art, ((260 - art.width) // 2, (400 - art.height) // 2))
        canvas.save(output / (name + ".dds"))


if __name__ == "__main__":
    build()
