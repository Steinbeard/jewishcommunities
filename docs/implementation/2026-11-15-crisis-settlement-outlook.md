# Crisis settlement outlook — 2026-11-15

**Status:** BUILT 2026-11-15 at Daniel's request. Source checked and xTiger
validated against the feature branch; live check pending. This is a focused
settlement/outlook pass on the crisis response system described in
[crisis response and recovery](../spec/2026-11-06-crisis-response-and-recovery.md).

## Why

Daniel's Granada playthrough reached **Spared**, then received *A Seal from
the Court*: Emir Badis forbade disorder but declined to renew the quarter's
protection. The event had no lasting effect on his Outlook on the Jews, and an
outlook of +12 missed the prior event's sole favourable threshold at +15.
That made the answer feel arbitrary and left no visible political memory of a
court letting incitement pass unanswered.

## Ruler choice weights

`kehillah_crisis.0200` still makes an AI ruler choose among protection, paid
protection, a bare order against disorder, and (only for a cold or hostile
ruler without prior protection) expulsion. Its outlook weights now use every
existing band:

| Outlook band | Protection | Paid protection | Bare order | Expulsion |
| --- | ---: | ---: | ---: | ---: |
| Indifferent | +10 | — | — | unavailable |
| Well-disposed | +30 | — | — | unavailable |
| Protective | +50 | — | — | unavailable |
| Cold | — | +15 | +15 | +15 |
| Hostile | — | +25 | +25 | +35 |

The existing trait and prior-protection weights remain: Just favours renewed
protection, Greedy favours a price, Craven favours the bare order, Zealous
favours expulsion, and existing protection strongly favours reaffirming it.
This is still a weighted AI choice, not a dice check against the exact outlook
number; the bands make the political meaning legible and avoid treating an
Indifferent ruler exactly like a Cold one.

## Temporary aftermaths

Both effects are timed character modifiers on the host ruler, visible in the
character window and in the host-outlook HUD breakdown. A later incident
refreshes the relevant ten-year timer instead of stacking an unlimited penalty.

| Cause | Modifier | Outlook effect | Duration |
| --- | --- | ---: | --- |
| Spared or Quarter Held; ruler leaves protection unanswered (including a player declining a demanded payment) | **Unanswered Incitement** | −5 | 10 years |
| Quarter Struck | **Anti-Jewish Violence** | −15 | 10 years |

The first label deliberately does not call a bloodless outcome violence. A
breach uses the stronger label. Its timed modifier is applied directly at the
common `OUTCOME = 4` resolution point, so every breach shares the same visible
political consequence.

The player sees the smaller effect in the result option's tooltip. Both effects
also appear as named modifiers with their game-calculated expiry date (for
example, a December 1066 result ends in December 1076).

## Checks

1. Static audit: both normal refusal and declined paid protection resolve to
   response 3 before `kehillah_crisis_settlement_outlook_effect` runs.
2. Static audit: every Quarter Struck resolution passes through the same
   guarded `OUTCOME = 4` block, so it cannot be skipped by a particular attack
   scene.
3. xTiger: this branch reports no finding in any touched file. The full mod
   still has 17 existing validator errors elsewhere, so a new fatal/error in a
   touched script/localization file remains blocking.

## Live check still needed

Use a disposable crisis save. Reach Spared, force or wait for the bare-order
answer, and confirm the result option says −5 for ten years; the host character
and HUD breakdown should show **Unanswered Incitement**. Repeat after declining
a paid-protection answer. Reach Quarter Struck and confirm **Anti-Jewish
Violence** gives −15 with a ten-year expiry. Then inspect an Indifferent, Cold,
and Well-disposed AI ruler's choice distribution over repeated probes. For a
fast rendering-only check, console events `kehillah_crisis_debug.26` and `.27`
apply the two respective modifiers to the current host's top liege.
