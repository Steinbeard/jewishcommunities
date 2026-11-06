# Kehillah advice lessons

**Status: BUILT, NOT LIVE-TESTED — 2026-11-06.** xTiger reports nothing on the new files and the total stays at the 15-error baseline. Daniel will run the checklist below.

## What this adds

Two lessons in vanilla's Reactive Advice system, each opened from a top-bar alert:

- **Advice: Leading a Kehillah** (`kehillah_welcome_advice`): seven steps for anyone on `kehillah_government`. It covers the community, the pillars, the Quarter, council and households, the host, succession, and first moves.
- **Advice: A Community of Your Own** (`kehillah_road_advice`): one step for an adventurer of a rabbinic-authority Jewish faith, pointing to Found a Jewish Community. Its gate matches that decision's `is_shown`.

Files:

- `common/tutorial_lessons/kehillah_welcome_advice.txt`
- `common/important_actions/kehillah_welcome_advice.txt`
- `localization/english/kehillah_welcome_advice_l_english.yml`

## How vanilla's systems compare

Reactive Advice is how vanilla teaches a government or playstyle, as in `reactive_advice_landless_adventurer` and `reactive_advice_welcome_to_japan`. The other systems fit worse:

- The guided tutorial is tied to its own tutorial starts and cannot be used in multiplayer.
- Ruler Objectives score advice against titles in a region, and a Kehillah is not landed.

## Limits to remember

- Lesson progress is saved per machine in `tutorial.txt`, not per save. A player who finishes the lesson at Worms will not see it again at Troyes.
- Players with Show Reactive Advice off never get the alert. The lessons leave `shown_in_encyclopedia` at its default of yes so they can be reread, but it is unconfirmed that modded lessons appear on the Advice page.
- Reactive lessons cannot pause the game or change game state.
- To retest, use Reset Reactive Advice, which resets all advice, or remove the lesson from `tutorial.txt`.

## Not in this pass

- **Game concepts.** The mod has none, so lesson text uses plain terms. Concepts for Kehillah, the pillars and the Bet Din would let it use linked terms.
- **Situational tips,** such as a first Bet Din, a vacant office, or a first succession.
- **A crisis tip.** This waits until the crisis redesign has been playtested. The welcome lesson only says where a crisis appears.

## Test checklist

As Isaac of Worms:

1. The alert "Advice: Leading a Kehillah" appears in the top bar and does not force a popup.
2. All seven steps open, with no raw keys or blank text. Back and Skip work, and "decisions" on the last step is a link.
3. Highlights land on visible widgets: Realm tab (step 2), Council tab (step 4), Decisions tab (step 7).
4. **Step 3 is the riskiest:** `hud_camp_button` is visible for a Kehillah and opens the Jewish Quarter. If it is not visible, remove the highlight and name the place in the text.
5. The Realm tab shows the three pillars, as step 2 says.
6. After "I Understand" the alert does not return.
7. The lesson appears on the encyclopedia's Advice page and reads properly.
8. The adventurer alert does not appear.
9. `error.log` has no new lines naming either lesson.

As Yosef of Rouen:

10. The alert "Advice: A Community of Your Own" appears, and the Kehillah welcome alert does not.
11. Read Later and I Understand both show, and the Decisions tab highlights.
12. Found a Jewish Community is in his decisions list. If it is not there at the start, consider delaying the tip.
