"""Stage a clean, player-facing copy of the mod for Steam Workshop upload.

Usage (from anywhere):
    python scripts/kehillah_build_release.py [--version 0.1-prealpha] [--name "..."]

What it does
------------
The Paradox launcher's "Upload mod" sends the *whole* mod folder. The dev
checkout is ~270 MB, more than half of it `.git`, plus docs, build scripts,
agent notes and BLOCKERS.md that players should never download. This script
copies only what the game reads into a sibling folder:

    mod/jewishcommunities_prealpha/          <- upload THIS one
    mod/jewishcommunities_prealpha.mod       <- launcher entry for it

and writes a release descriptor with a thumbnail.

Re-running it refreshes the game files but keeps `remote_file_id` (which the
launcher writes after the first upload) so later uploads update the same
Workshop item instead of creating a new one.

Do not enable the dev mod and the pre-alpha copy in the same playset: they
define the same things.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MOD_DIR = REPO.parent
RELEASE_SLUG = "jewishcommunities_prealpha"
RELEASE_DIR = MOD_DIR / RELEASE_SLUG
RELEASE_MOD_FILE = MOD_DIR / f"{RELEASE_SLUG}.mod"

# Folders the game actually reads. Anything else stays out of the upload.
GAME_DIRS = ["common", "events", "gfx", "gui", "history", "localization"]
THUMBNAIL_SRC = REPO / "docs" / "release" / "thumbnail.png"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.py", "*.md", "Thumbs.db", ".DS_Store")


def read_remote_id(path: Path) -> str | None:
    if not path.exists():
        return None
    m = re.search(r'remote_file_id\s*=\s*"?(\d+)"?', path.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else None


def git_commit() -> str:
    try:
        sha = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], text=True).strip()
        branch = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        # Untracked game files count too: they would ship without being in any commit.
        dirty = subprocess.check_output(["git", "-C", str(REPO), "status", "--porcelain", "--", *GAME_DIRS], text=True).strip()
        return f"{branch}@{sha}" + (" (uncommitted changes!)" if dirty else "")
    except Exception:
        return "unknown"


def supported_version() -> str:
    # Follow the dev descriptor, so a game-version bump there reaches the release.
    m = re.search(r'supported_version\s*=\s*"([^"]+)"', (REPO / "descriptor.mod").read_text(encoding="utf-8-sig"))
    if not m:
        raise SystemExit("descriptor.mod has no supported_version")
    return m.group(1)


def descriptor(name: str, version: str, remote_id: str | None, path: Path | None) -> str:
    lines = [
        f'version="{version}"',
        "tags={",
        '\t"Religion"',
        '\t"Gameplay"',
        '\t"Events"',
        '\t"Historical"',
        "}",
        f'name="{name}"',
        'picture="thumbnail.png"',
        f'supported_version="{supported_version()}"',
    ]
    if path is not None:
        lines.append(f'path="{path.as_posix()}"')
    if remote_id:
        lines.append(f'remote_file_id="{remote_id}"')
    return "\n".join(lines) + "\n"


def write_no_bom(path: Path, text: str) -> None:
    # The launcher chokes on a BOM in .mod files; always write plain UTF-8.
    path.write_bytes(text.encode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="0.1-prealpha")
    ap.add_argument("--name", default="Jewish Communities (Pre-Alpha)")
    args = ap.parse_args()

    if not THUMBNAIL_SRC.exists():
        print(f"Missing {THUMBNAIL_SRC}", file=sys.stderr)
        return 1

    remote_id = read_remote_id(RELEASE_DIR / "descriptor.mod") or read_remote_id(RELEASE_MOD_FILE)

    RELEASE_DIR.mkdir(exist_ok=True)
    # Clear only the folders this script owns, so stale files never linger.
    for d in GAME_DIRS:
        target = RELEASE_DIR / d
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(REPO / d, target, ignore=IGNORE)
    shutil.copy2(THUMBNAIL_SRC, RELEASE_DIR / "thumbnail.png")

    write_no_bom(RELEASE_DIR / "descriptor.mod", descriptor(args.name, args.version, remote_id, None))
    write_no_bom(RELEASE_MOD_FILE, descriptor(args.name, args.version, remote_id, RELEASE_DIR))
    build = git_commit()
    write_no_bom(RELEASE_DIR / "RELEASE_INFO.txt", f"{args.name} {args.version}\nBuilt from {build}\n")

    size = sum(f.stat().st_size for f in RELEASE_DIR.rglob("*") if f.is_file())
    thumb_kb = (RELEASE_DIR / "thumbnail.png").stat().st_size / 1024
    print(f"Staged {args.name} {args.version} from {build}")
    print(f"  folder:   {RELEASE_DIR}")
    print(f"  launcher: {RELEASE_MOD_FILE}")
    print(f"  size:     {size / 1_048_576:.0f} MB, thumbnail {thumb_kb:.0f} KB")
    print(f"  remote_file_id: {remote_id or '(none yet: first upload creates the Workshop item)'}")
    if "uncommitted" in build:
        print("  WARNING: the dev checkout has uncommitted changes; this build includes them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
