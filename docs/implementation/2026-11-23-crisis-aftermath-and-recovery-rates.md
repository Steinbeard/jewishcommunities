**Status:** built 2026-11-23 from Daniel's playtest feedback; xTiger clean (no new reports). Not live-tested. Adds to [2026-11-06 crisis response and recovery](../spec/2026-11-06-crisis-response-and-recovery.md) and supersedes its implied flat Recovery rates.

# Crisis aftermath and Recovery rates

## What Daniel saw

1. After Quarter held, the window showed no progress, and "Returning to Ordinary Life" came months later.
2. After the Danger let him take several of its options.
3. "A Charter Revised" improved his charter without saying why.
4. Fustat collapsed after a Contained attack in which one person died.

## What changed

**The wait after Spared or Quarter held** (commit 02788ae). The window now says "Awaiting the ruler's judgement" until `kehillah_crisis.0202`, then "Ordinary life returns within N months". The wait is a month count on the title (`kehillah_crisis_return_months`, 2), ticked by the situation's `on_monthly` (`kehillah_crisis_return_monthly_effect`). It was a fixed 45-day event. CK3 cannot show a timed variable's days left in GUI text, so the count is in months. A crisis with no live situation keeps the 45-day event.

**After the Danger: one choice per crisis.** Every option of `kehillah_crisis_act.0010` sets `kehillah_crisis_aftermath_done`, which closes `kehillah_crisis_aftermath_open_trigger`.

**Charter reasons** (84854f5). Script that changes a charter term calls `kehillah_charter_change_reason_effect`. The toast appends the reason (`KehillahCharterChangeReason`). The player's own toast is good for a granted term, bad for a taken one, and neutral for the lord's own renegotiation. The next charter read clears the reason.

**Recovery dropped every Endure push** (fda4593). `kehillah_crisis_recovery_progress_effect` and `_setback_effect` compared the title with `root`. Called from an event, root is a character, so the check failed and the push was lost. Relief, the reckoning, captives and every mutual-aid gift gave Recovery nothing. Fustat lost four gifts this way. Both now compare against a saved title scope. The situation sync had the same comparison and was fixed too.

**Recovery's base rates follow the threat grade.** The grade is the final one, after preparations lowered it at the breach. The loss and lord modifiers in `kehillah_crisis_recovery_start_effect` still add on top.

| Final grade | Endure / month | Collapse / month (base) |
| --- | --- | --- |
| Contained | 20 | 3 |
| Serious | 15 | 7 |
| Grave | 12 | 10 (the old flat rates) |
| Catastrophic | 10 | 14 |

Fustat's case, with low Stability, one death and damaged buildings, is Collapse 3 + 8 + 4 + 3 = 18 against Endure 20. It endures even if the community does nothing. A Contained crisis can still collapse when everything else is bad (a cold lord, captives, low Stability), and Recovery actions can still save it.

## Still to check live

- The window lines in Spared, Quarter held and Recovery.
- A struck quarter's Recovery bars move when relief or a mutual-aid gift lands, with no "different types" lines in `error.log`.
- The charter toast's reason and colour.
