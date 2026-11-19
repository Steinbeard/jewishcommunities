# Community leadership styles

**Status: PROTOTYPE BUILT 2026-11-15; source/xTiger checked, live UI and succession checks UNRUN.**
Requested by Daniel. Supersedes the fixed skill weights in V1 section 5 only; does not change the appointment pool, government, laws, faith eligibility, gender rules, endorsements, candidate investment or existing scholarly trait/piety bonuses.

## Design

The community title stores its mandate: Scholarly (1), Political (2), or Commercial (3). An absent value means Scholarly, preserving the previous skill weights. Leaders may change the style while adult, free and capable; a change locks the **seat** for ten years. The current leader remains in office. Succession does not clear the mandate or its lock. Choosing the current style is a no-op and cannot renew the lock. This initial prototype has no switching fee, forced resignation, building requirements or historical assignments.

| Style | Candidate Learning / Stewardship / Diplomacy weights | Community benefit | UI color |
|---|---|---|---|
| Scholarly | 3 / 2 / 0.5 | +60 Greatness baseline | Gold #C6A052 |
| Political | 1 / 1 / 3 | +60 Stability baseline | Slate blue #6485A6 |
| Commercial | 1 / 3 / 1 | +60 Prosperity baseline | Green #579568 |

Weights read `scope:title` (the seat being contested), never a candidate's home community. Other appointment terms still apply; scholarship and piety remain qualifications even in political/commercial communities. Favoring a style does not guarantee a matching successor.

The baseline bonus feeds existing seasonal convergence and normal pillar consequences. It gives no instant points or repeatable currency payout. Political leadership improves protection indirectly through Stability; Commercial supports existing Prosperity effects; Scholarly supports existing Greatness effects. The styles are an institutional priority, not a prohibition on other pursuits. The main tradeoff is foregoing the other two bonuses. The number is centralized in `kehillah_leadership_baseline_bonus` for tuning. Pillar breakdown hovers include the new contributor.

AI communities review their weakest current pillar quarterly when unlocked: Stability wins ties, then Prosperity, then Greatness. They use the same guarded effects as the player. If their mandate already fits their weakest pillar, no change and no cooldown occurs. There is no world scan or daily work.

## Interface

The Domain tab places one compact panel between the Quarter card and the existing pillar overview. It has a current-style heading, an available/locked status line, and three equally sized tinted buttons with matching color strips. A pressed state plus an explicit Current label identifies the active choice without relying on color. Each button states its baseline benefit and explains candidate weighting, gradual pillar change, ten-year commitment and incumbent continuity on hover. Current and unavailable options are disabled. The status displays the expiry year; the authoritative timed variable retains the exact ten-year expiry.

Files are additive `kehillah_leadership_style_*` script/GUI files with three small integrations: appointment weights, pillar baselines/breakdown tooltips, and the Domain panel instance. No generated catalogs, law files, title history, or existing succession lifecycle effects were changed. Existing concurrent candidacy edits in `kehillah_leadership.txt` are preserved.

## Validation and manual checks

xTiger before/after: **0 fatal, 25 errors, 96 warnings, 37 untidy, 135 tips**, unchanged; no diagnostics in new leadership files. Existing copied-native GUI warnings remain baseline findings. Five focused regression checks (`python scripts/test_kehillah_leadership_styles.py`) pass and cover skill ranking, fallback weights, guarded GUI/AI mutation, seat-owned cooldown, and baseline/tooltip integration. These are source checks, not proof of engine succession or rendering.

A Luna live tester found no xTiger game tools; CIM process inspection was denied. No game was launched, controlled or captured. Live checks remain required before treating succession as verified:

1. Start Worms in 1066; open Domain. Verify all three tinted buttons fit, Scholarly is Current, status says available, and hovers name the correct effects. Repeat at the normal UI scale and minimum supported resolution, checking scrolling and text wrapping.
2. Choose Political. Verify the Current indicator and status update immediately, all choices disable, Stability baseline gains 60, and Greatness baseline loses 60. Current pillar values must not jump. Run `event kehillah_leadership_debug.1` and inspect the three bonus values.
3. Attempt the same guarded effect/another style from the console while locked; verify no change or payout. Save/reload, then succeed to a different eligible leader. The title must retain style and lock; inspect candidate skill contributions against the same seat before and after.
4. Advance beyond the exact ten-year anniversary. Verify only other styles enable; choose Commercial and check the new lock and exchanged baseline bonuses. A newly installed save with no style must use Scholarly without missing-variable errors.
5. Observe AI communities with each different weakest pillar. Verify one change at most per ten years, no same-style lock renewal, and no tooltip-related log flood.

Git delivery is blocked by read-only `.git` metadata in this session. Work remains in the shared checkout on its existing branch; no branch switch, reset, clean or unrelated staging was attempted. Review the focused new files and three integration areas separately from concurrent ledger/candidacy changes when committing.


## 2026-11-15 follow-up: selection, effect summary and reminder

**Status: BUILT; seven source regressions pass; xTiger remains at 0 fatal, 25 errors and 96 warnings; live rendering/reminder checks pending.** Supersedes the original Interface paragraph and the initial-selection behavior above.

Selected buttons now use a stronger style-colored fill, a matching top edge and the native pressed state. There is no per-button Current label. The selected button stays visually enabled while locked; clicking it is a guarded no-op, so it cannot renew the mandate. Other options remain disabled until expiry. Buttons are shorter, with the effects of the selected choice listed persistently below: the pillar baseline bonus, all three succession skill weights, and the reminder that pillar gains are gradual and other qualifications still count.

An absent title style is now explicitly **unchosen** in the UI, with no selected button. Legacy scholarly scoring and its existing baseline bonus still apply until a selection is made, and the effect summary says so. The first Scholarly choice is permitted and writes style 1 plus the same ten-year lock as any other choice. AI communities also record that first selection through the shared effects, including when their weakest pillar calls for Scholarly. An existing explicit style is retained without another reminder.

An inline nudge appears while unchosen. A native suggested action, **Choose a leadership style**, appears when the leader can act and opens My Realm's Domain tab using the treasury alert's established route. Its creation condition ends once the title has a style. There is no recurring event popup.

Additional live checks: on a save with no style, confirm no button looks selected, the fallback effects are visible, and the reminder opens Domain; choose Scholarly first and confirm the reminder clears, gold styling appears and a ten-year mandate begins. Repeat for Political/Commercial, then save/reload. Check the active button remains bright while alternatives are locked; clicking it must not extend the expiry. Succession still uses the `kehillah_leadership_*_weight` script values in the appointment score, as confirmed by source audit; actual runtime succession remains unverified.

## Addendum 2026-11-16 — Camp Purpose design language

**Status: BUILT; xTiger clean (no new reports), live UI check pending.**

`gui/kehillah_leadership_style.gui` now follows the adventurer Camp Purpose
grid (vanilla `widget_realm_law_camp_purpose`): a centred label and three
illustrated 160px tiles with a dark caption band. Unchosen tiles read "Follow
the Scholars / Parnasim / Merchants"; the chosen tile is pressed, glows and
reads "We Are Scholars! / Parnasim! / Merchants!". This replaces the earlier
slate/gold/green colour washes. Choice logic, tooltips, status and effects
text are unchanged. Art is vanilla's own 300px illustration set:
`camp_purpose_scholars` (Scholarly), `powerful_family_bonus/service` — a sealed
edict scroll, read as a charter of privileges (Political) — and
`theme_administration_types/icon_civilian_administration` — a market (Commercial).
Bespoke art can replace these by texture path alone.

Live checks: tiles render and caption in Domain; choosing one glows it and
starts the mandate; locked tiles show disabled with the tooltip; no
`error.log` lines on hover.

**Addendum 2026-11-17:** the tile picker made the Domain tab misaligned (Daniel, live). It now sits at the top of the Laws tab, above the charter (`vbox_my_realm_laws_body` in `gui/window_my_realm.gui`), as Camp Purpose does for adventurers. Live check: the tiles render there and the Domain tab lines up again.
