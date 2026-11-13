# DLC dependencies, and the Iberian Struggle

**Status:** 2026-11-09. DLC audit (sections 1–2): current as of this date. Section 3's first-pass
Iberian Struggle connections were built and **reverted the same day** at Daniel's request (flat
per-phase pillar terms were not wanted). The replacement is a proposal,
[v53](../spec/v53-sepharad-and-the-iberian-struggle.md). Section 3 is kept as a record of what was tried.

## 1. What DLC the mod needs today

Audited by searching the mod for `has_dlc_feature`, `has_*_dlc_trigger` (vanilla's wrappers in
`common/scripted_triggers/00_has_dlc_scripted_triggers.txt`) and `requires_dlc_flag`.

| DLC | Feature key | Status in this mod | Where |
|---|---|---|---|
| **Roads to Power** | `roads_to_power` / `landless_adventurer` | **Hard requirement in practice.** All three Kehillah bookmarks carry `requires_dlc_flag = landless_adventurer`; the Kehillah government is `landless_playable = yes`. Founding a community from an adventurer camp and Step Down are also gated on it. Task contracts (translation, etc.) and the AI-probe activity are gated separately. | `common/bookmarks/bookmarks/kehillah_bookmarks.txt`, `common/governments/kehillah_government.txt`, `kehillah_found_community_decisions.txt`, `kehillah_departure_decisions.txt`, `kehillah_task_contracts.txt`, `kehillah_ai_probe.txt` |
| Royal Court | `royal_court` | Optional. Book artifacts (Write a Book, translation "keep the true copy") are skipped without it. | `kehillah_book_effects.txt`, `kehillah_translation_effects.txt` |
| Legends of the Dead | `legends_of_the_dead` | Optional. The epidemic pulse is skipped. | `kehillah_on_actions.txt` |
| By God Alone | `by_god_alone` | Optional. Only affects two vanilla-trigger overrides (Mass Conversion, portraits), which keep vanilla's own gate. | `kehillah_mass_conversion_override.txt`, `kehillah_portrait_overrides.txt` |
| All Under Heaven | `all_under_heaven` | Optional; inside a copied vanilla council task. | `kehillah_vanilla_task_overrides.txt` |
| **The Fate of Iberia** | `the_fate_of_iberia` | **Optional** (new, below). | `kehillah_struggle_*` |

So the only DLC a player must own is Roads to Power. Every other dependency already degrades
cleanly.

Whether the Kehillah government could run without Roads to Power at all (domiciles and
`landless_playable` without the DLC) has not been tested. The bookmarks block it today, so it is
moot unless someone wants to try lifting that requirement.

## 2. How to make a feature optional

CK3 has no "optional dependency" in `descriptor.mod`. A mod always loads; it switches content
off **at runtime**. Four tools, from most to least preferred:

1. **Gate on the thing, not the DLC, when the thing only exists with the DLC.** Struggles,
   situations and the great steppe only start when their DLC is present, and a game rule can
   remove them too. `exists = struggle:iberian_struggle` (or `struggle:iberian_struggle ?= {...}`)
   covers no-DLC, rule-off and struggle-ended in one check. Iterators such as
   `every_character_struggle` are naturally empty without the DLC.
2. **`has_dlc_feature = <key>`, or vanilla's `has_<x>_dlc_trigger` wrappers** in `is_shown`,
   `potential`, `trigger`, `limit`. Use `is_shown` (not `is_valid`) on decisions and interactions,
   so a player without the DLC never sees a greyed-out button.
3. **GUI: `HasDlcFeature('<key>')`** in a `visible = "[...]"` expression (vanilla does this in
   `gui/hud.gui`, `gui/shared/mapmodes.gui`).
4. **Bookmarks: `requires_dlc_flag`**, which is what the Kehillah bookmarks use.

A player can also turn a struggle off with vanilla's own game rule (`struggle_iberia`); rule 1
respects that automatically. A mod game rule (`common/game_rules/kehillah_game_rules.txt`)
would only be needed to switch off the mod's *own* use of a DLC while keeping the DLC.

**Don't** override vanilla DLC files (e.g. `iberian_struggle_script.txt`) to add content. The
override loads for players without the DLC too, and breaks on every vanilla patch. Everything below
reads the struggle or calls its public effects. Nothing is overridden.

**Revised the same day, 2026-11-09:** the mod *does* now override `iberian_struggle_script.txt`,
to give the struggle catalysts of its own. See [v53](../spec/v53-sepharad-and-the-iberian-struggle.md)
section 6b. The paragraph above overstated the risk. The override loads harmlessly without the
DLC, because the struggle never starts. The real costs are refreshing the file after each CK3
patch and conflicting with other mods that override the same file.

## 3. The Iberian Struggle: first-pass connections (REVERTED 2026-11-09)

Files: `common/scripted_triggers/kehillah_struggle_triggers.txt`,
`common/script_values/kehillah_struggle_values.txt`,
`common/customizable_localization/kehillah_struggle_custom_loc.txt`,
`common/scripted_effects/kehillah_struggle_effects.txt`,
`common/on_action/kehillah_struggle_on_actions.txt`,
`localization/english/kehillah_struggle_l_english.yml`; edits to the three baselines in
`kehillah_script_values.txt`, the three pillar tooltips in `kehillah_breakdown_l_english.yml`, and
`kehillah_translation_deliver_effect`.

**Which communities.** A Kehillah whose Quarter (`domicile.domicile_location`) is in
`world_europe_west_iberia`, the struggle's own region, while `struggle:iberian_struggle` exists
(`kehillah_under_iberian_struggle_trigger`). A landless Kehillah can't be "involved" by vanilla's
rules, which count the counties a culture or faith holds, so region membership is used instead.

**A. The phase shapes the pillars** (baseline terms, shown in each pillar's tooltip as "Iberian
Struggle (Phase): ±N", same pattern as "Holy war preached"):

| Phase | Prosperity | Stability | Greatness |
|---|---|---|---|
| Opportunity | +40 | −20 | – |
| Hostility | −30 | −100 × the lord's protection | – |
| Compromise | – | +30 | – |
| Conciliation | – | +30 | +60 |

These are first guesses. Tune them in `kehillah_struggle_values.txt`.

**B. A notice when the phase changes.** Each quarter the community's title records the phase
(`var:kehillah_iberia_last_phase`). When it changes, or the struggle ends, the player gets a
community-news message. The first quarter only records the phase. Transition states keep the
last phase.

**C. The Kehillah can push the struggle.** When a Commissioned Translation is delivered faithfully
(success or triumph), and the commissioning ruler is *involved* in a struggle whose current phase
lists `catalyst_learned_new_language_important`, that catalyst fires for the ruler, the same way
vanilla's Learn Language scheme fires it. In Iberia that pushes Opportunity toward Conciliation and
Hostility toward Compromise. The Persian struggle gets the same treatment if its phase lists the
catalyst. Without the DLC there are no struggles, so nothing happens.

**Not done (candidates for later):** Sephardi-specific events per phase; letting a Hostility
phase raise mob/pogrom danger directly (today it acts only through Stability); a Kehillah-side
decision that spends gold or prestige on a conciliation catalyst; and reacting to the struggle's
ending decisions (e.g. a Hostility ending as a trigger for Phase 4 expulsion).

## 4. Testing

Not applicable: the build was reverted before any live test.
