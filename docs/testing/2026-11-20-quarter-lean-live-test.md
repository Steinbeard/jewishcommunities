**Status:** live test run 2026-11-20 by a delegated agent through the xtiger MCP tools. CK3 1.21.0.3, the Worms 1066 bookmark, text only. It covers the Quarter-tracks work up to commit `ff17f88` (spec sections 14-15) and the pillars R2 work.

# Quarter tracks: lean live test

| Step | Result |
|---|---|
| Boot to Worms | pass, about 112 s, no crash |
| `kehillah_quarter_debug.1-5` | pass, with no new `error.log` lines |
| Succession: kill the Worms leader | pass |

**What the probes showed:**
- the allowance went from 2 to 3+ once the Kahal House reached tier 3;
- town trade went from none to small after Workshops and Dye Vats;
- the county modifier "Jewish Craftsmen" was applied;
- the wall licence was granted from the host's dynasty;
- the Bond Chest collection ran.

**Succession:**
- the heir (Nachshon) leads Worms and the player kept control;
- the heir's domicile has the Synagogue 5, the Kahal House 3, Workshops, Dye Vats, the Kosher Market, the Butchers and the Yeshiva;
- probe .1 on the new leader shows the same state;
- no mod errors.

**Findings and fixes:**
1. **The Mikvah was not placed in seeded starts:** 15× "Domicile has no free building slots: 'kehillah_mikvah_01'". The Synagogue's tier 1 had one internal slot, and the Sofer took it. **Fixed:** the Synagogue's tiers 1-2 now have 2 internal slots.
2. **County Prosperity read "under 20" in 1066.** The history files show 1.21 counties start at `prosperity_level` 3-24, the same scale as the old development, since vanilla converted 1:1. **Fixed:** the earlier migration's doubled thresholds were reverted. The mod's own files now read `prosperity_level` with the original development numbers. The county modifier raises Prosperity *growth*, so the level moving slowly is expected.
3. **Not ours to fix now (1.21 triage):**
   - "Unknown effect: add_great_building" in `kehillah_scripted_effects.txt` (the Kairouan yeshiva hall). 1.21 turned great buildings into great districts (`add_great_district`); this needs a port, not a rename;
   - `kehillah_start_eminence_effects.txt` is not UTF-8 with BOM (pre-existing).
