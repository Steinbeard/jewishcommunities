# Uploading the pre-alpha privately to the Steam Workshop

**Status:** written 2026-11-16 for the first Discord pre-alpha. **First upload done
2026-11-17**: Workshop item **3841299043**
(`https://steamcommunity.com/sharedfiles/filedetails/?id=3841299043`), built from
`sefarim-reviews-cherem-and-crisis-politics@b29688c`. Step 3 below is corrected to match the
launcher (2026.14) screens as they actually appeared.

**2026-11-17: 0.1.1-prealpha** (CK3 1.21, no Roads to Power needed) is staged from branch `ck3-1.21-port`.
The staging script now takes `supported_version` from the dev `descriptor.mod`.

## Why not upload the dev folder

The launcher uploads **the whole mod folder**. `mod/jewishcommunities` is about 270 MB, and half
of that is `.git`. It also has docs, build scripts, AGENTS.md, CLAUDE.md, BLOCKERS.md and
ROADMAP.md. None of these should go to players. Upload a clean copy instead.

## 1. Stage the release copy

```
python scripts/kehillah_build_release.py
```

This creates (or refreshes) a sibling mod:

- `mod/jewishcommunities_prealpha/` holds only `common/ events/ gfx/ gui/ history/ localization/`,
  a `thumbnail.png` (from `docs/release/thumbnail.png`), a `descriptor.mod` and
  `RELEASE_INFO.txt`, which records the branch and commit it was built from. About 215 MB.
- `mod/jewishcommunities_prealpha.mod` is its launcher entry, named
  **"Jewish Communities (Pre-Alpha)"**, version `0.1-prealpha`.

Options: `--version 0.1.1-prealpha`, `--name "..."`.

**It builds whatever is checked out in the dev repo.** On 2026-11-16 that was
`sefarim-reviews-cherem-and-crisis-politics`, 189 commits ahead of `master`. Build from the
branch you actually mean to ship.

## 2. Smoke-test the staged copy (do not skip)

xTiger on the staged copy gives the same totals as the dev mod (330 reports: 0 fatal, 32 errors,
the known baseline). That does not prove it boots. Before uploading:

1. In the launcher, make a playset with **only** "Jewish Communities (Pre-Alpha)". **Never enable
   it together with the dev "Jewish Communities"**, because they define the same things.
2. Boot, open each of the three Kehillah start screens, and start Worms 1066.
3. Run a few months at speed 5. Check that
   `Documents/Paradox Interactive/Crusader Kings III/logs/error.log` has no new
   `kehillah` errors beyond the usual baseline.

## 3. Upload through the Paradox launcher

1. **Close and reopen the launcher**, so it rereads the new `.mod` file. An open launcher can
   cache an old copy of the descriptor and write it back.
2. Go to **Mod library** (left sidebar), then the **Upload mod** button at the top right.
3. In the **Mods** dropdown choose **Jewish Communities (Pre-Alpha)** (near the bottom of the
   list). Check that **Directory** ends in `mod\jewishcommunities_prealpha`.
4. Under **Upload to**, switch from the preselected **Paradox Mods** to **Steam Workshop**.
   Paradox Mods has no private option to rely on.
5. The form has only Suggested game version (filled from the descriptor), Mod ID (leave empty
   for a new item) and **Description**: paste
   `docs/release/steam-workshop-description.bbcode.txt`. There are no thumbnail or tag fields;
   both come from the descriptor (`picture="thumbnail.png"`, a 640×640 PNG under 1 MB).
6. Click **Upload mod**. 216 MB took under a minute (five progress steps). When it finishes, the launcher writes `remote_file_id="…"` into the `.mod` file. The
   staging script keeps that ID, so every later upload **updates** the same Workshop item.

## 4. Make it private: set the visibility at once

Open the item on Steam (launcher link, or Steam, then Workshop, then Your Files). Under **Owner
Controls, Set visibility**, choose:

| Visibility | Who can see and subscribe | Use it for |
|---|---|---|
| **Unlisted** | Anyone with the link; it never appears in search or browsing | **Recommended for Discord testers** |
| Friends-only | Only your Steam friends | Only if every tester is a Steam friend |
| Hidden (private) | Only you | Uploading, checking the page, before sharing |

If you can, set it to **Hidden** before anyone sees it, check the page, then switch it to
**Unlisted** and post the link on Discord.

- **New Steam uploaders:** Steam may require you to accept the **Steam Workshop Legal
  Agreement** before the item can be anything but hidden. The item page shows a banner if so.
- An Unlisted link can be passed on. That is fine for a friendly test group. Do not treat it
  as secret.

## 5. Images on the Workshop page

Add screenshots as **Add/edit images & videos**, then **Images**, on the item page, not inside
the description. The current set is `docs/images/*.jpg`. `docs/release/screenshot-shot-list.md`
lists the newer screens that still need capturing.

## 6. Shipping an update

1. Commit in the dev repo, then rerun `python scripts/kehillah_build_release.py --version 0.1.N-prealpha`.
2. Smoke-test (step 2).
3. Close and reopen the launcher, choose **Upload mod**, then the same mod, and add a change note.
   It updates the existing item.
4. Post the change note on Discord, and **remind testers that old saves may not load.**

## Fallback: Discord zip

If the Workshop route stalls, zip `mod/jewishcommunities_prealpha/` with its `.mod` file
(change the `path=` line to the tester's own mod folder). Testers unzip both into their
`Documents/Paradox Interactive/Crusader Kings III/mod/` folder. The archive is about 215 MB,
over Discord's attachment limit, so share it through Google Drive or a similar service.

## Optional: make the download smaller

The 22 bookmark portraits in `gfx/interface/bookmarks/` are **uncompressed** 8 MB DDS files,
about 180 MB of the 215. Re-saving them as BC3/DXT5 would cut the upload to about 60 MB with no
visible change. This is not needed for a pre-alpha.
