"""Copy exported genes into matching history DNA and bookmark portraits.

Bookmarks have separate portrait definitions. Preserve the card's portrait ID,
clothing, and props. Rashi retains the fuller beard from the mod's older DNA.
"""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DNA = ROOT / "common/dna_data/kehillah_dna.txt"
BOOKMARK = ROOT / "common/bookmark_portraits/kehillah_bookmark_portraits.txt"


def block(text: str, opener: str) -> tuple[int, int]:
    start = text.index(opener)
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return start, i + 1
    raise ValueError(f"Unclosed block: {opener}")


def apply_export(source_path: str, dna_key: str, bookmark_key: str,
                 beard_from_previous: bool = False) -> None:
    source = (ROOT / source_path).read_text(encoding="utf-8")
    start, end = block(source, "\tgenes={")
    gene_lines = source[start:end].splitlines()[1:-1]
    entries = {}
    for line in gene_lines:
        match = re.fullmatch(r"\s*(\w+)=\{.*\}", line)
        if not match:
            raise ValueError(f"Invalid gene line: {line}")
        entries[match.group(1)] = line.strip()

    if len(entries) < 100 or len(entries) != len(gene_lines):
        raise ValueError("Incomplete or duplicate exported genes")

    genes = {
        key: value
        for key, value in entries.items()
        if key.startswith(("gene_", "face_detail_", "expression_"))
        or key in {
            "hair_color", "skin_color", "eye_color", "complexion",
            "eye_accessory", "teeth_accessory", "eyelashes_accessory",
            "beards", "hairstyles",
        }
    }

    history = DNA.read_text(encoding="utf-8-sig")
    start, end = block(history, f"{dna_key} = {{")
    old_history = history[start:end]
    if beard_from_previous:
        beard = re.search(r'^\s*beards=\{.*\}', old_history, re.MULTILINE)
        if not beard:
            raise ValueError(f"No original beard for {dna_key}")
        genes["beards"] = beard.group().strip()

    replacement = (
        f"{dna_key} = {{\n\tportrait_info = {{\n\t\tgenes = {{\n"
        + "\n".join(f"\t\t\t{line}" for line in genes.values())
        + "\n\t\t}\n\t}\n\tenabled = yes\n}"
    )
    DNA.write_text(history[:start] + replacement + history[end:], encoding="utf-8-sig")

    portrait = BOOKMARK.read_text(encoding="utf-8-sig")
    start, end = block(portrait, f"{bookmark_key}={{")
    card = portrait[start:end]
    gene_start, gene_end = block(card, "genes={")
    previous = card[gene_start:gene_end]
    outfit_keys = {
        "legwear", "clothes", "headgear", "clothes_hoods", "cloaks",
        "secondary_headgears", "props_left", "props_right", "gene_cloak",
    }
    outfit = []
    for line in previous.splitlines()[1:-1]:
        match = re.match(r"\s*(\w+)=\{", line)
        if match and match.group(1) in outfit_keys:
            outfit.append(line.strip())

    replacement = "genes={\n" + "\n".join(
        f"\t\t{line}" for line in (*genes.values(), *outfit)
    ) + "\n }"
    card = card[:gene_start] + replacement + card[gene_end:]
    BOOKMARK.write_text(portrait[:start] + card + portrait[end:], encoding="utf-8")
    print(f"Applied {len(genes)} exported genes to {dna_key} and {bookmark_key}")


apply_export("docs/data/kehillah_granada_vanilla_yosef_persistent_dna.txt",
             "kehillah_dna_joseph_naghrilla", "bookmark_kehillah_granada_joseph")
apply_export("docs/data/kehillah_vanilla_rashi_persistent_dna.txt",
             "kehillah_dna_rashi", "bookmark_kehillah_troyes_rashi",
             beard_from_previous=True)
