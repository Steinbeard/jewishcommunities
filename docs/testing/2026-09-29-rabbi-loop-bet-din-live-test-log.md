# Rabbi loop: Bet Din participant rewards — 2026-09-29

**Status: FOCUSED LIVE PASS, with guest-play caveat.** A real three-person
bench received the new per-case Rabbi XP. A fresh boot confirmed the repaired
session-close tier and displayed the attendee payout. This does not verify the
player experience of attending an AI-hosted Bet Din or exact attendee
before/after resource numbers.

## Method and baseline

- Fresh debug-mode Worms 1066 boot, advanced past day three. The player took
  the rabbinate so the existing preside gate allowed a Bet Din, and a real
  three-person panel assembled. `kehillah_rabbi_loop_debug.1` confirmed the
  convening title, Av Beit Din, judge 2, and judge 3 were all bound; the Av
  held the Rabbi trait.
- `ck3-tiger` before and after the script changes: **0 fatal, 0 error**.
  Existing warnings remain. `error.log` had pre-existing GUI layout and
  unrelated script errors; no new Bet Din reward-related line appeared during
  this probe.

## Per-case Rabbi XP — PASS for the first good ruling

Before the probe, `.1` did not log `AV TALMUDICS XP AT LEAST 1`. The
console-only `.2` effect awarded one good-ruling point to the actual bench;
afterward `.1` logged `AV TALMUDICS XP AT LEAST 1`. More importantly, the
subsequent **natural case ruling tooltip** showed **+1 Rabbi Talmudics XP**
for all three named judges: the player, Rav Shlomo, and Rav Isaac. This
confirms the positive-case call site, not merely the standalone effect.
Great rulings (+3), poor rulings (0), and non-rabbi judges remain source
checked but not live measured.

## Session close — FAIL found in older code; fix pending live regression

The `.2` probe also set a positive session score and queued the closing event.
The event appeared as generic “The Docket Is Closed,” while `.1` did **not**
log `SESSION SCORE POSITIVE`. Source inspection found the cause: the docket
writes `kehillah_bet_din_session_score` and
`kehillah_bet_din_cases_heard_count` on the activity, but both shared
closing-event triggers still read old `global_var:` paths. All four existing
tiered host payouts, and the new attendee payout, silently fell through.

Both triggers now read guarded `involved_activity.var:` paths. The linter
reports 0 fatal/0 error. The first boot could not test this correction because
CK3 loaded the old triggers at startup.

## Fresh-boot close regression — PASS for the positive path

The second CK3 process reached a fully staffed Bet Din and opened a real
case. After `.2`, `.1` now logged `SESSION SCORE POSITIVE` and Av XP ≥1. When
the queued `.0099` event opened, it showed the **adequate** close and its
existing host payout: Greatness +10, Stability +5, Piety +50. Hovering the
option showed named non-host attendees receiving **+10 Prestige, +10 Piety,
+15 Learning Lifestyle XP**, and an opinion gain. The close option was
clicked, the game stayed responsive, and `error.log` gained no Bet Din reward
error. This proves the positive tier was reached and the attendee effect was
shown and executed without a script error. A numeric before/after on an
attendee was not captured, so each exact resource delta remains unmeasured.

The opinion tooltip displayed the raw modifier key in parentheses. English
localization was added for the favor and disfavor modifiers afterward; its
rendering has not been checked in a subsequent boot.

## Still open

- An AI-hosted Bet Din with the player as a non-host attendee: invitation,
  meaningful choice during a case, visible personal reward notice, and
  before/after resource change.
- Great-ruling +3 XP, poor-ruling 0 XP, a non-Rabbi judge, and a docket that
  closes without any case. Their branches are source checked, not live
  measured in this pass.
