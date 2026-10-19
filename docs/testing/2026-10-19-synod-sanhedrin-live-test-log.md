# Live test log: synods, Minhag Ashkenaz and the Sanhedrin, 2026-10-19

**Status:** the final build (73ce2de) passed. Every earlier Sanhedrin build failed with Game Over.
The history is kept here because it records engine rules this mod has to live with.

## Method

- **Driver:** a Sonnet subagent on the primary monitor, through the AGI-CK3 winkeys shims.
- **Launch:** a fresh `-debug_mode -develop` launch each run, 1066 Worms bookmark, playing Isaac
  HaLevi (9000002).
- **Evidence:** console probes (`kehillah_synod_debug.1-5` and run files), every one tagged with
  the character through `debug_log_scopes`, plus `error.log` diffs against a post-start baseline.
- **Starting state:** the first run killed Daniel's Rashi game (PID 7748) with his permission.
- **Boot stall:** direct launches stalled at "Initializing Game" for 5-25 minutes and cleared
  with periodic window clicks. This is the known stall, not a mod problem.
- **Mouse offset:** the winkeys mouse shim needs X multiplied by 1.8 on this virtual desktop. The
  shim guide does not say so yet.

## V45 synod and rite: PASS

- **Rites at game start:** Rabbinism is polygamous, and vanilla's yearly monogamy event is
  suppressed.
- **The 1066 synod:** `kehillah_synod.0001` fires on 1066.10.15. Its text and tooltips render.
  Option 1 founds Minhag Ashkenaz (monogamous, with Ashkenazi culture), and Worms joins it while
  Lucena stays Rabbinist and polygamous.
- **Fixed during testing:** the founding first ran inline in the option, and building the
  tooltip logged about 99,000 "Failed to fetch a valid rite" errors. It now runs from the hidden
  event `kehillah_synod.0002` (commit 40f8c2e). The retest logged none.
- **Bet Din intents:** Justice, Synod and Sanhedrin are all listed. Sanhedrin is greyed out, and
  its tooltip renders.

## V46 Sanhedrin: the failures, and what each one proved

| Build | Head of faith | Result | What it proved |
|---|---|---|---|
| 4ae97ce | spiritual, landless title | Game Over; primary title later flipped to the Sanhedrin | The Nasi is forced onto theocracy and loses his domicile. |
| (probe) | (same) | `change_government` back reverts at once; it sticks only after `remove_religious_head_title` (test D) and `doctrine_no_head` (test G) | The head-of-faith link is the cause. Holding the title is not. |
| 40f8c2e | + faith `theocracy_government_type = kehillah_government` | Game Over | That field had no effect. |
| 7647d59 | temporal + lay clergy | Game Over | Setting the head moves the faith's main rite to the head's rite (Minhag Ashkenaz). The doctrines had been set on the old main rite. |
| 355ebb8 | doctrines on every rite | Game Over; "Trying to set illegal government" | Even a temporal head with lay clergy is forced onto theocracy when landless. |
| (probe) | temple barony for Isaac | Game Over: community title destroyed, theocracy, vassal of the Kaiser | Kehillah leaders cannot hold land as built (`require_landless`, government, vassalage). |
| d353438 | `kehillah_nasi_government` (theocracy mechanic, Kehillah domicile and flag) | Game Over; the switch to it was accepted before the head link, then forced to generic theocracy and refused back as illegal | See the C0 diagnostic below. |
| **73ce2de** | **no engine head for a landless Nasi** | **PASS** | See below. |

**Other things learned along the way:**
- A Nasi forced onto theocracy loses the Worms title's succession: both titles were **vacant** after his death in four runs.
- PAM strips elector titles from non-theocratic rulers yearly. The mod's override (`kehillah_pam_strip_cardinalate_override.txt`) keeps the seats; checked after 1 January in several runs.
- Seat titles errored ("no preferred capital") until the capital was set before `set_landless_title`.

## Final build 73ce2de: PASS

- **C0, diagnostic:** `faith:rabbinic_faith.faith_theocratic_goverment_type` is vanilla
  `theocracy_government`. The faith-level `theocracy_government_type = kehillah_nasi_government`
  in `kehillah_judaism_faith_names.txt` was **ignored**. Vanilla sets this field only at religion
  level (`00_christianity.txt`), so the Nasi government was never actually reached by the engine.
- **C2, restoring:**
  - No Game Over; the primary title stays on Worms.
  - Kehillah government and domicile kept, with all nine buildings.
  - The faith has no head; seats exist (Mainz holds one).
- **C3, after about three months:** unchanged. The character window shows "Nasi Isaac of Kehillah
  of Worms", "Communal Realm", 2 titles.
- **C4:** seats survive 1 January.
- **C5, succession:**
  - Killing the player Nasi offers "Continue as Parnas Nimrod" (Worms), who is playable on the
    Kehillah government with all nine buildings.
  - The Sanhedrin is elected to Rashi of Troyes, who stays on the Kehillah government with his
    domicile. No vacancies.
- **C6, errors:** two vanilla tributary lines after the death. No government, domicile or
  doctrine errors.

## Open

- **The landed (king) head-of-faith path** is untested; there is no Jewish king in 1066.
- **A "Relocate De Jure Capital" decision** appeared after restoring. It is probably vanilla's,
  for a duchy holder (the Sanhedrin is now a titular duchy). Not yet looked at.
- **The Synod and Sanhedrin intents** were not run through a full Bet Din sitting.
- **The religion-level `theocracy_government_type`** has not been tried; see v46 §10.
