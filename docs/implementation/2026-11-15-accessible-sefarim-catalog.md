# Accessible Sefarim Catalog

**Status: BUILT; source checks pass, xTiger has no report in changed files, manual Ledger check pending — 2026-11-15.** Implements Daniel's interim direction that every historical work which has entered circulation remains findable through the Ledger even when no registered library owns it. It defers the proposed social, perk-driven, and loss-aware discovery system in [the discovery specification](../spec/2026-11-15-sefer-discovery.md).

## Change

`known_lines` and `rite_known_lines` in `scripts/kehillah_library_catalog.py` now add no extra knowledge gate. The generated Ledger lists every work that passes its normal availability rule:

- fixed historical works appear on or after their catalog circulation date;
- named works stay absent until their in-game author has written them; and
- generic authored slots stay absent until a character has used the slot.

The existing V48 acquisition action already allows a circulated work with no registered holder to use its distant scholarly-network fallback. This change exposes that route instead of hiding an otherwise eligible book behind ownership, mastery, or standing.

It does not create a copy, change a work's standing in any rite, bypass commission cost or delay, or represent a decision about whether a physically lost manuscript may later be recovered. The latter is explicitly future design work.

## Checks

- Regenerated with `python scripts/kehillah_library_catalog.py`; a second `--check` pass succeeded.
- xTiger reported no finding in `kehillah_library_catalog_list_effects.txt`. Its fatal/error/warning/untidy totals remained `0/66/112/37`; the general tips total changed from 124 to 132 while unrelated shared-worktree work was in progress.
- In a 1066 Rabbinic save, open the Ledger and confirm *Hekhalot Rabbati* and *Sefer ha-Razim* are visible and offer **Seek a copy** despite no local copy; confirm future named works and unused authored slots remain absent.
