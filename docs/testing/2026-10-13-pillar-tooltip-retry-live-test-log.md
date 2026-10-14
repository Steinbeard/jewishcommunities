# Pillar tooltip retry — 2026-10-13, 09:30 Eastern

**Status:** PASS for the remaining roster nested links, Crisis/Legendary endpoint
spot-checks and exact threshold HUD labels. The final controlled probe also verified
all three Legendary leader modifiers at 950 with zero new runtime script errors.

This closes the remaining checks in [ROADMAP.md](../../ROADMAP.md) and the
[morning playtest](2026-10-13-pillar-tooltip-live-playtest-log.md). It is a paused-game
rendering check with artificial pillar scores, not an economy or succession soak.

## Ownership and setup

Started after Daniel's 09:30 testing hold. Other Codex chats were idle; Claude had
finished its latest recorded work at 09:15, with no CK3 or live-input helper running.
Used the same `autonomous/shabbat-2026-10` checkout, initially `1175400`. Preserved
the five existing tracked edits and untracked trait assets. A Luna subagent owned
input; the parent made no repository writes until the live work finished.

Launched CK3 PID **10004** at 09:32 into fresh, paused Worms 1066. No existing save
was loaded or manual save made. The corrected identity probe logged Isaac HaLevi,
internal ID **29176**, historical ID **9000002**, primary title `d_kehillah_worms`.
Action Lock used actual middle-button SendInput events; the shim's `button="middle"`
alias sends a right-click and had to be replaced in the temporary helper.

`ck3-tiger` ran before testing: **0 fatal / 795 error / 128 warning / 1 untidy / 22 tips**
overall. No diagnostics named the pillar breakdown custom localization, English
localization or community-map GUI files. This is a targeted result, not global linter
cleanliness. No script, localization, GUI, threshold or modifier file changed here.

**Ownership limitation:** a later checkout review found Claude's `f501ce4` settlers
commit at 09:43 during this pass. Its four changed files concern natural founding
and the v34 spec; the tested pillar GUI, localization, values, modifiers and effects
were unchanged. Roster completion and final endpoint/boundary/assertion checks ran
after that commit. The parent missed this activity while the tester was running;
process checks alone were insufficient. The guide now requires branch/status and
recent transcript checks before probes. The other session had finished its latest
reply by the final review. This was not a wholly frozen-checkout test.

## Observed UI results

At **750**, all three debug reports were Flourishing. The two previously unfinished
roster pairs passed using a locked parent and reachable nested links:

| Roster pillar | Current effect | Legendary child (950+) | Healthy child (400–699) |
| --- | --- | --- | --- |
| Stability | −10% stress gain; +5 courtier/guest opinion | −20% stress gain; +10 courtier/guest opinion | No stress or courtier/guest opinion modifier |
| Greatness | +10% monthly prestige; +1 Learning | +20% monthly prestige; +2 Learning | No prestige modifier |

Both parents gave **200 more to Legendary** and named Healthy as the lower band.
Their exact nested titles read “Stability — Legendary”, “Stability — Healthy”,
“Greatness — Legendary” and “Greatness — Healthy”, with the ranges above.

At **50**, all three parents showed Crisis, **100 more to Strained**, and
“Crisis is the lowest.” Current effects were −20% income, +20% stress gain/−10
courtier/guest opinion, and −20% prestige respectively. The reachable Prosperity
Strained child showed range 150–399 and −10% monthly income. The tester corrected
an initial reporting typo about Greatness's sign against its existing capture;
the rendered Crisis value was negative, as source requires.

At **975**, all three parents showed Legendary, no higher band, and Flourishing
below. Current effects were +20% income, −20% stress gain/+10 courtier/guest
opinion, and +20% prestige/+2 Learning. The reachable Prosperity Flourishing
child showed range 700–949 and +10% monthly income.

Four targeted run files set all three title scores to exactly **150 / 400 / 700 /
950**. HUD captures and `kehillah_debug.30` agreed on **Strained / Healthy /
Flourishing / Legendary**, respectively, for every pillar. This did not exhaustively
rehover every neighboring link at every boundary; nested coverage comes from the
750 roster/HUD checks and representative endpoint children.

## Actual modifiers and controlled replay

The paused day-one game had no historical initialization marker, so
`kehillah_pillars_are_live_trigger` was false. The public refresh wrapper had
therefore not applied modifiers merely because the score probes ran. At final
value **950**, three direct band-update calls applied all three Legendary modifiers,
confirmed by `.102`, but the console emitted errors while building their descriptions.

A controlled replay cleared only the six `kehillah_band_now_*` / `kehillah_band_prev_*`
cache variables on the test title, then ran the same updates inside `hidden_effect`.
The log recorded three “seeded a band” results. `.102` confirmed all three recorded
bands and all three **LEGENDARY** modifiers again. No new tooltip-build or runtime
script-system error followed. This isolates the preceding 36 errors to console
effect-description construction before the transient variables existed.

## Error-log accounting

| Observation | Total lines | Kehillah-tagged lines |
| --- | ---: | ---: |
| Post-load baseline | 315 | 252 |
| After roster, before endpoints | 763 | 514 |
| After boundaries and unhidden direct-update probe | 1,054 | 663 |
| After controlled hidden replay | 1,069 | 676 |

- The first **448** additional lines comprised 171 repeated known roster layout
  messages plus their 171 context lines, 105 unused/set-variable validation notices,
  and one failed identity-helper parse. That helper initially contained literal
  PowerShell newline escapes; rewriting it with real newlines produced the correct
  identity log. The five layout locations remained GUI lines 754/774/856/881/913.
- The next **291** lines comprised 75 repeated validation notices and 36 console
  description-building errors with their context. Those errors referenced the four
  modifier comparisons at effect lines 161/165/169/173, for each pillar's unset
  `kehillah_band_now_*` variable. The direct effects still executed successfully.
- The hidden replay added **15** known unused/set-variable validation notices,
  **zero** description-building errors and **zero** other runtime script errors.
  No missing pillar key, new pillar UI scope error or wrong neighboring band was found.

Existing layout and validation messages remain; this pass did not fix them.

## Evidence and next step

Evidence, temporary helpers, baseline/final error logs and four boundary captures are
retained in `C:\Users\Daniel\.codex\automations\retry-kehillah-pillar-ui-check\live-0930`.
The parent independently read the identity, band and modifier verdicts and log counts.

CK3 **10004** was left responsive and paused in the fresh test game at **950 / 950 /
950**, with all three Legendary modifiers. Recheck ownership before future input.
The first roadmap verification item is closed. The next item is the Kehillah
death-screen wording and feudal control check. Disable this temporary retry heartbeat;
keep the regular overnight schedule unchanged.
