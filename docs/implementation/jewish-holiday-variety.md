# Holiday event variety — 2026-10-12

**Status:** Five events scripted and source checked on 2026-10-12. Live event rendering and seasonal delivery remain unverified.

This extends the one-step holiday pool described in [the implementation record](v1-kehillah-implementation.md) at Daniel's request for more variety and character involvement. The [writing guide](kehillah-writing-style.md) governs the new text. The events remain available to playable Jewish characters outside the Kehillah, so their effects are personal and do not require a community title or building.

| Event | Holiday | Situation |
| --- | --- | --- |
| `.0009` | Yom Kippur | A named Jewish courtier remembers a public rebuke; the player may apologize, defend the correction, or defer the conversation. |
| `.0010` | Yom Kippur | During the final prayers, the player may sing, rest, or help an older worshipper follow the book. |
| `.0011` | Sukkot | Rain enters through a loose branch in the sukkah roof; the player may repair it, eat inside, or wait. |
| `.0012` | Sukkot | A named Jewish courtier brings figs to the meal; the player may welcome the guest closely, share the blessing, or begin supper. |
| `.0013` | Shavuot | A borrowed book of commentary is open for study; the player may read with others, pay for a copy of the worn leaves, or return it. |

The two named-courtier events require an eligible adult Jewish courtier. The other event for each of those holidays has no courtier requirement. The yearly selection remains a quiet year more often than an event: 300 quiet weight against 260 combined event weight, with the existing 25% roll. The calendar pulse presents Yom Kippur and Sukkot in its broad late-year window and Shavuot in May–July; these windows approximate a moving Hebrew calendar on CK3's fixed months and quarterly pulse.

The existing Purim gift event's fallback no longer requires five gold. Its text now describes sharing food from the basket, matching the effect. The previously unlocalized awkward-memory modifier has an English name.

## Verification

- `git diff --check` passed for the holiday files.
- All five new event IDs have a queue entry, yearly weight, seasonal delivery and title/description/choice localization. No duplicate event IDs or localization keys were found.
- `ck3-tiger` 1.19.0 against installed CK3 1.20.0.4 found no new holiday-file findings. The four existing faith-reference errors in `jewish_holiday_scripted_triggers.txt` predate this change and reflect the version mismatch; the three prior missing-modifier warnings are fixed here.
- Live event rendering, choice effects, and natural seasonal delivery remain to be checked. CK3 was already running in the shared workspace when this change was made, so that session was left undisturbed. For direct rendering checks after a fresh load, use `event jewish_holidays.0009` through `.0013` on an eligible Jewish ruler; `.0009` and `.0012` also need an eligible Jewish courtier.
