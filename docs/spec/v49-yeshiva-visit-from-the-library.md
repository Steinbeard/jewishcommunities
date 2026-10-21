# V49: Planning a Yeshiva Visit from the Library

**Status: IMPLEMENTED AND LIVE-TESTED, FIXES RE-TESTED IN GAME — 2026-10-21 (built 2026-10-20).** Live results and fixes: [2026-10-21 test log](../testing/2026-10-21-v49-yeshiva-visit-live-test.md). Requested by Daniel on 2026-10-20: "click through the library view or through the event and select a particular book you want to study, see who owns it, and have it plug in the travel destination for you. Maybe you could make a copy while you're there and bring it back?" Builds on the Yeshiva Visit activity (`activity_kehillah_learn_torah_journey`, 2026-09-15/17) and [V48](v48-sefarim-acquisition.md)'s title-owned acquisitions. It adds a fourth acquisition route to V48 and does not change V48's other three. ROADMAP remains authoritative for shipped status.

## Decision

The Yeshiva Visit is no longer planned blind. The player chooses **a book**, sees **which communities hold it**, and the planner opens **with that community as the destination**. Arriving, the traveller can take up that book at once. If home lacks it, the traveller can **copy it and bring it back**.

## Player flow

**From the Library.** Selecting any work on the Books page (owned shelf, a corpus seder or the acquisition list) loads a **Held in Other Libraries** roster on its page: every other registered community holding the work, with its leader's portrait. Each row has **Travel to study**. That stores the community and work on the player as a plan (`kehillah_journey_plan_title`, `kehillah_journey_plan_work`) and opens the Yeshiva Visit planner.

**From an event.** The decision **Plan a Yeshiva Visit** fires `kehillah_learn_torah_journey.0010`. It suggests two unmastered works held elsewhere, preferring works home lacks, and names a community holding each. A suggestion sets the same plan. The other options are "choose a library myself", which clears any plan and opens the ordinary planner, and "not now". The event points to the Library for the full roster. It stays at four options under V42's rule.

**In the planner.** While the plan is valid (the title still has a holder and still holds the work), the activity's `is_location_valid` offers **only** that community's domicile, so the destination is filled in. If the plan has lapsed, the planner falls back to the ordinary field of libraries. The plan expires after `kehillah_journey_plan_days` (30) if the planner is closed unused. `on_start` moves the plan onto the activity and clears it from the host.

**On arrival.** `.0001` checks that the arrival community is the planned one and still holds the book. If so, it offers:
- **Take up [the book you came for]**;
- **First see what else their shelves hold** (`.0005`: the three shelf options, plus a way back);
- leave.

An unplanned visit shows the original four options unchanged.

**A copy to carry home.** Every study choice abroad now ends in `kehillah_journey_finish_study_effect`. When the destination holds the work, home lacks it and home has no acquisition underway, `.0006` offers:
- **Copy it yourself:** `minor_gold_value`. The stay lasts `kehillah_journey_self_copy_stay_days` (120). Delivery comes after `kehillah_journey_self_copy_days` (180).
- **Hire their scribes:** `medium_gold_value`, and the host community needs a Sofer's Workshop. Part of the fee reaches its leader. The stay lasts 30 days and delivery comes after 90.
- **Leave the exemplar.**

## Rules

- The copy is a normal V48 acquisition: one item in the home title's `kehillah_library_commission_work` list, the source title, a new `kehillah_library_commission_carried` route marker, and `kehillah_library.0003` fired on the **title**. Death on the road, succession, or the host later losing the book cannot cancel it. Only one acquisition at a time, as in V48. The Library shows the route under Acquisition Underway. V48's own routes now clear the new marker.
- Delivery is a fixed delay from the choice, not tied to the traveller physically reaching home. The activity system gives no "host arrived home" hook. A fixed delay is succession-safe; tying delivery to the traveller would not be.
- A plan for a work the traveller has already mastered is allowed. Re-reading uses the existing repeat-study result, and the copy offer is the reason to go.
- The activity stays player-only: `ai_will_do = 0`, the decision's `ai_will_do = 0`.
- The source never loses its exemplar, as in V48.

## Implementation

| Piece | File |
|---|---|
| Per-work roster load, roster check, travel action (generated) | `common/scripted_guis/kehillah_library_journey_gui.txt` |
| Planned-work study dispatcher, suggestion pools (generated) | `common/scripted_effects/kehillah_library_journey_generated_effects.txt` |
| Work-name custom locs (generated) | `common/customizable_localization/kehillah_library_journey_custom_loc.txt` |
| Plan, study, finish, carry-copy, pick-suggestion effects | `common/scripted_effects/kehillah_library_journey_effects.txt` |
| Can-plan, plan-valid, can-carry triggers | `common/scripted_triggers/kehillah_library_journey_triggers.txt` |
| Location filter, `on_start` and `on_complete` | `common/activities/activity_types/kehillah_learn_torah_journey.txt` |
| `.0001` planned options; `.0005`, `.0006`, `.0010`; hidden `.0007`, which runs every study abroad outside option tooltips (added 2026-10-21) | `events/kehillah_learn_torah_journey_events.txt` |
| Decision | `common/decisions/kehillah_yeshiva_visit_decisions.txt` |
| Book-page roster, carried route label | `gui/kehillah_domicile_library.gui` |
| Console probe | `event kehillah_sefer_debug.6` |

The generated files come from `scripts/kehillah_library_catalog.py`. A new catalog work gets its roster, travel action, study branch, suggestion entry and names automatically.

## Assumptions (live-tested 2026-10-21; see the test log)

All passed except number 2: the planner highlights only the planned community, but the player
still clicks it once. No engine hook pre-selects it, so this is accepted.

1. **`open_view_data` from a scripted GUI effect.** This is proven from a decision effect (Bet Din). It is assumed to behave the same from a scripted GUI and an event option.
2. **The planner pre-selects a sole valid location.** If it only lists it, the player still has one click and nothing else to choose.
3. **`is_location_valid` re-reads host variables when the planner opens.** The plan is set in the same click, before the view opens.
4. **`AddScope( 'target', Scope.Title.MakeScope )` on a variable-list item.** This mirrors vanilla's `Title.MakeScope` form, but no vanilla row passes a list item this way.
5. **Extending the phase from `.0006`'s `after`.** This relies on the established rule that a later `progress_activity_phase_after` overrides the ceiling.

## Verification gate

1. Generator twice, clean second run; `ck3-tiger` against the pre-edit baseline. *Done 2026-10-20: no new reports beyond the known 1.20-token false positive on `change_spiritual_fulfillment`, re-reached through the new call chain.*
2. 1066 Worms as a rabbi: select a work Worms lacks. The roster lists only other holders. **Travel to study** opens the planner with only that community. `event kehillah_sefer_debug.6` reports PLAN VALID.
3. Start the visit. On arrival the planned option names the book, and studying it offers `.0006`. Each copy option charges correctly (hired is disabled without the host's Sofer's Workshop). The Library shows the carried route. `event kehillah_sefer_debug.5` delivers the work.
4. The decision suggests two works with holders; "choose a library myself" opens the unfiltered planner.
5. Close the planner unused, wait past the expiry, reopen from the Activities menu: the ordinary field returns.
6. Check `error.log` for new `kehillah`, scripted-GUI or data-context errors. Record in `docs/testing/`.

## Follow-ups (not built)

- Rank holders and suggestions by travel distance. V48 also defers this.
- Show the planned book in the planner itself. Engine UI, no known hook.
