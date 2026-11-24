# Bet Din: arguments, citations, votes, and visible progress

**Status: proposal, 2026-11-24; not implemented.** Daniel's direction supersedes the *per-case choice, citation timing, tally, and resolution display* in `v5-bet-din-conference.md` and `2026-11-23-bet-din-citation-strength-and-risk.md`. It does not change the activity's host, bench selection, docket eligibility, or case premises. The older specs and the current implementation remain the record of what the game actually does until this design is built and live-tested.

## Player experience

For each case, every seated judge follows the same sequence:

1. **Choose an argument.** The case offers two or three distinct positions, normally a ruling favoring each party and, where the facts support it, a bounded investigation or compromise. Each option names its skill challenge, current success chance, likely stress change, material cost, and the factors affecting those values. No option is unlocked solely by a high skill, `just`, or another favorable trait. A capable judge is better at arguing any position that suits their abilities; they are not handed a universally best ruling.
2. **Choose one citation.** A second screen offers *no citation*, the best suitable well-known mastered work, and the best suitable uncommon mastered work if one exists. Show the actual work's name, standing, how widely it is mastered, the resulting argument chance and potential contribution, and a clear warning if the convening community's rite bans it. An unavailable category is shown disabled with its reason. One work must never appear twice. Citing is optional; judges without a relevant mastered work can still argue.
3. **Hear the argument.** Resolve the challenge after the citation choice. Immediately tell the player whether the judge's argument held, which evidence or opposition defeated or supported it, the contribution earned, stress and resource consequences, and whether a banned citation raised cherem concern. A failed check does not silently turn a vote into the opposite position.
4. **See the panel.** Once all judges have acted, show each judge's position, cited work or none, argument chance, success or failure, and contribution. Show the winning position and why its combined arguments prevailed. Only then apply the case result and update the conference's running score.

The player sees their own choice and feedback. AI judges use the same choice, citation, and challenge rules. If more than one judge is player-controlled, each receives their own screens before the panel result. Missing or ineligible seats are omitted; the existing quorum rule still governs whether a hearing can proceed.

## Choice design for the case pool

Keep **at most three argument options** on the first screen. Do not add separate buttons for Learning, Diplomacy, `just`, a scholar, a steward, and citing a work. Those are factors in the challenge or on the citation screen. Two options are enough when a third would be a generic safe answer. Prefer three only when the middle course has a real cost or risk of its own: time, treasury, delay to relief, loss of evidence, or an uncertain compromise. Both sides should have a plausible case; hidden facts may make a choice mistaken, but must not create a permanently optimal visible choice.

Each case profile should define, per argument: the position it supports, a short verb-led action, primary skill, optional secondary skill, evidence being tested, direct cost or delay, stress alignment, and fact-sensitive consequences. Reuse the 100 authored scenes and outcomes, but review all their options against this schema. Reword the existing 8/4/2 cost pattern where it makes investigation automatically superior. No case should be converted by swapping in three generic lines of prose.

Traits and lifestyles change *how well a judge can make a particular argument*, not whether it exists. Examples: Diligent helps audit records but may add stress when a judge refuses to inspect them; Just helps an even hearing but can add stress when favoring a powerful party without proof; a Mystic path helps interpret a disputed mystical text but does not improve every debt claim; Diplomacy helps reconcile witnesses while Learning helps interpret a difficult document. Stress should follow CK3's character behavior, with the actual gain or loss visible before selection. Traits can also pull in opposite directions. A bonus never hides a large direct cost, and a high skill never guarantees success.

## Challenge and citation numbers

Use script values for all tunable numbers. The following are **initial targets for implementation and playtesting**, not claims about the current build:

| Part | Initial rule |
| --- | --- |
| Argument base | 40–50% depending on the case and the chosen action, with both party-favoring options in the same starting band. |
| Skill | +2 percentage points per point of primary skill above 10, or −2 below 10, capped at ±20; a relevant secondary skill may add up to ±5. |
| Traits and lifestyle | Case-specific, usually ±5–10 each, combined cap ±15. List every active modifier in the tooltip. |
| Situation | A documented fact, available witness, delay, or obstruction may shift the chance by up to ±15. Do not reveal the hidden fact in the pre-choice tooltip. |
| Citation | A known, respected work chiefly improves reliability; an uncommon work may offer a smaller reliability gain but a larger contribution when the argument succeeds. A banned work remains selectable with explicit cherem risk. |
| Final chance | Clamp to 10–90%. Show the exact current percentage after all known modifiers, and update it on the citation screen before confirmation. |

The citation screen should use the existing mastered-work, order-coverage, standing, master-count, and host-rite ban systems. Select one eligible **well-known** candidate by highest reliability, then standing, then a stable ID; select one **uncommon** candidate by highest potential contribution, then reliability, then stable ID. The categories must be defined by a script value for the master-count threshold. The Mishnah's current standing adjustment remains an input to ranking unless a later balance pass changes it explicitly. Exclude an unknown work even if a different judge owns it. A known but banned work is eligible and visibly risky.

The old citation system makes a separate reliability roll and adds a source tally to the whole case. Replace that with a citation modifier to *this judge's argument chance* and an optional contribution bonus on success. This keeps one plainly explained success chance on the choice. A failed argument gets no citation contribution; a banned work still incurs its stated cherem consequence when used. Do not let the rarity bonus overcome a very low argument chance without a meaningful risk. A source's standing, rarity, and ban status should appear as separate tooltip lines so the player can see the tradeoff.

The first argument screen shows the **uncited chance**, labeled as such; the citation screen shows the **final chance** for each available source and for no citation. If CK3 cannot recompute an exact displayed percentage in this event flow, implementation must use a script value/breakdown or `random_list` modifier presentation that matches the actual roll. Do not put hand-written percentages in localization. Verify the displayed breakdown against a scripted probe at several skill, trait, and book states.

## Votes and case result

Each judge casts one vote for the position chosen, even if their argument fails. A successful argument contributes a small base weight plus skill- and source-based strength; a failed argument contributes at most a minimal vote weight, with a possible penalty for an especially weak or contradicted claim. Clamp individual contributions so one exceptional judge cannot erase two sound opposing arguments by default. Add contributions **by position**, not to a shared tally before the winner is known. The position with the greatest combined weight wins; a tie goes to the position with more judges, then to the existing presiding-judge tie break. This preserves a meaningful vote while allowing a compelling minority argument to persuade the panel.

The case-quality score comes from the *winning position's combined successful argument strength*, adjusted for how well that position fits the discovered facts, and then mapped to the existing good/great case thresholds. Losing arguments and failed citations do not inflate it. A narrow or poorly supported win may still settle the dispute but yield a weak court result. The case's direct resource, relationship, and stress effects follow the winning ruling and each judge's own action as appropriate; avoid charging every judge's proposed resource cost when only one proposal is enacted.

Store a compact record for each seat on the activity: position, cited work, displayed chance, roll result, contribution, and stress result. Clear it after the panel screen and log; do not leak one case's state into the next. Save the case outcome and all three votes in the activity log, including AI actions. The panel screen must handle a missing seat without a blank name or vote.

## Conference progress display

Add a Bet Din progress bar to the activity window, visible while the docket is underway. It should show the **current session score against the thresholds for adequate, strong, and landmark results**, the number of cases heard and remaining, and a breakdown of how completed cases changed the score. Label it *current standing* or *projected outcome*, not a guaranteed final success chance: future cases and choices have not been rolled. Before the first resolved case, show an unscored state rather than a false 0% prediction. Update after the panel result, not while an unresolved judge is still speaking.

CK3's hunt uses `hunt_success_chance.gui` to read an activity variable and show a progress bar with a `GetScriptValueBreakdown` tooltip; `hunt.txt` exposes that widget in `activity_plugin_widgets_summary` and updates its value from `hunt_success_chance_value`. Use that as the UI pattern. The Bet Din's value and tooltip must reflect its own session score and tier thresholds. If a genuine final success probability is later calculated from the remaining docket, it can be added as a second, separately labeled estimate; do not present current score as probability.

## Build order and verification

1. Implement one representative two-party case and one case with a real third position, then migrate the shared event template and generator. Keep existing saves safe: an activity opened under the old flow should complete or fail gracefully rather than reading unset new variables.
2. Move citation selection behind argument selection and make its displayed final chance equal the actual roll. Reuse current work ranking, coverage and cherem mechanics where they serve this flow; change the library catalog generator for generated citation dispatch.
3. Add per-seat records, feedback, weighted panel resolution, and the activity log. Migrate all 100 current cases in reviewed groups; run a structural check that every case has 2–3 arguments, valid position IDs, a citation screen and a final result.
4. Add the activity-window progress bar using the hunt widget pattern. Check narrow layouts, long work titles, missing judges and the initial unscored state.

Run xTiger against the edited checkout before a live test. Source-check chance math, state cleanup, party effects, and the tie break. Use hidden debug events to force each stage, both fact states, a banned/unknown/rare source and each judge count. A Luna live test should then check real event order, visible percentages against the rolled result, stress previews, citation warnings, panel votes, log entries and progress bar updates. Record the session and `error.log` baseline. Until that happens, this document remains a proposal; the current 100-case flow is unchanged.
