"""Copy portraits written by the game's dump_bookmark_portraits into
common/bookmark_portraits/kehillah_bookmark_portraits.txt.

Start a game at a Kehillah bookmark date, type dump_bookmark_portraits in the
console, then run:

    python -I scripts/kehillah_import_bookmark_dumps.py <dump folder>

Each bookmark_kehillah_*.txt in the dump folder replaces the block of the same
key in the mod's portrait file, so the start-screen card shows exactly what
the character looks like in that game. Keys the dump does not contain are
left as they are. Dumps of vanilla bookmark characters are ignored.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "common/bookmark_portraits/kehillah_bookmark_portraits.txt"


def find_block(text: str, key: str) -> tuple[int, int]:
    match = re.search(r"^%s=\{" % re.escape(key), text, re.M)
    if not match:
        raise KeyError(key)
    depth = 0
    for i in range(match.end() - 1, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return match.start(), i + 1
    raise ValueError(f"Unclosed block: {key}")


def main() -> None:
    dump_dir = Path(sys.argv[1])
    raw = TARGET.read_bytes()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    replaced = []
    for dump in sorted(dump_dir.glob("bookmark_kehillah_*.txt")):
        key = dump.stem
        source = dump.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        s, e = find_block(source, key)
        start, end = find_block(text, key)
        text = text[:start] + source[s:e] + text[end:]
        replaced.append(key)
    if crlf:
        text = text.replace("\n", "\r\n")
    TARGET.write_bytes(text.encode("utf-8"))
    print("replaced:", ", ".join(replaced) or "nothing")


if __name__ == "__main__":
    main()
