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

## Spike: can a Kehillah leader hold land? (uncommitted edits, reverted)

**Edits, both reverted afterwards:** `require_landless` removed from `d_kehillah_worms` only, and
`church_holding` added to `kehillah_government`'s `valid_holdings`.

- **Play: no crash and no "unplayable character" assert.** The header comment on
  `require_landless` in `kehillah_landed_titles.txt` blames it for the old crash on Play. That
  appears to be outdated: implementation doc §8 found the real cause was `is_playable_character`,
  which the mod now overrides. A founded community's dynamic title has no `require_landless`
  either.
- **Isaac could not take the barony.** Granting `b_besensheim` (type `usurped`) logged no error.
  The engine gave the barony to a freshly generated lowborn instead, twice. Isaac stayed
  landless, independent, on the Kehillah government, with his Quarter. The likely cause is the
  government's `cannot_be_vassal_or_liege`: holding a barony in the Kaiser's realm would make him
  a vassal.
- **A side effect:** a lowborn became Isaac's primary heir ("Son is Losing Kehillah of Worms").
  Don't repeat this on a real save.
- **Earlier, without the spike edits (P1):** the same grant destroyed the Worms title, forced
  theocracy and made Isaac the Kaiser's vassal.
- **Conclusion:** landed Kehillot need the vassal relationship itself redesigned, that is,
  dropping `cannot_be_vassal_or_liege` and reworking the host charter (implementation doc §2a).
  That is a Track B-sized project, not a change to the Sanhedrin. The `holds_landed_title`
  trigger also read YES for a barony Isaac did not hold, so it is unreliable here.

## Spikes: the landed Nasi and the Gaon as head of rite (patch, reverted)

The code is preserved as `docs/spikes/2026-10-19-landed-nasi-and-gaonate.patch`.

**Spike edits:**
- `d_kehillah_worms` without `require_landless`.
- A landed `kehillah_nasi_government`: Rabbinic faith only, castle, city and temple holdings,
  no `cannot_be_vassal_or_liege`.
- A `d_kehillah_gaonate` title, set as `head_of_rite` on `rabbinic_faith`.
- Debug events .6-.8.
- A rewritten Sanhedrin hand-over.

**Landed Nasi (two runs): PASS for a landed holder.**
- Restoring while landless, then granting Isaac `c_worms` and switching him to the Nasi
  government, left him: on the Nasi government, with no theocracy and his domicile and
  buildings, landed and independent, holding Worms, `c_worms` and the Sanhedrin.
- Setting the head link made him the temporal head of faith, with no Game Over. That was stable
  past 1 January. The character window read "Communal Realm (Head of Faith)".

**FAIL at succession, in both runs:**
- **Run 1, the county followed the community.** The Worms successor took `c_worms` and the Nasi
  government. The elected Nasi (Rashi, landless) was forced into theocracy and lost his domicile.
- **Run 2, the county followed the Sanhedrin.** The new Nasi (Isaac ibn Ghiyyat of Lucena) got
  `c_worms`, the Nasi government and the head link, but he lost his domicile in the landless
  moment before the county reached him, and his primary title became the Sanhedrin. The Worms
  successor stayed on the Nasi government; the fix-up never ran, because his title arrived
  before his government changed.
- **What it shows:** no effect can create a domicile.

**Gaon as head of rite: PASS.**
- Granting the Gaonate to the Mainz leader made `rite:rabbinism.head_of_rite` the Mainz leader.
  He stayed on the Kehillah government with his domicile, unchanged after a month.
- **Per rite:** after Mainz joined Minhag Ashkenaz, he was Ashkenaz's head of rite.
- **A head of faith outranks him:** while Isaac was Nasi, Rabbinism had no separate head of rite.

Design consequences: [v47](../spec/v47-gaon-and-the-seat-of-the-sanhedrin.md).
