# Jewish festival observance on vanilla feasts — 2026-10-13

**Status: First pilot, partly superseded by the [presentation pass](jewish-festival-feast-presentation.md); its live event behavior was not verified.** Implements the narrow pilot in [Mo'adim le-Simchah](../spec/jewish-festival-observance.md) on branch `codex/festival-observance-2026-10-13`. This addendum records the first implementation and its differences from the proposal. It does not change rite slots, rename the shared vanilla tenet, create a decision, or add a feast intent.

## Player-facing behavior

`feast_start_events` invokes `jewish_holiday_feast_start` for every attendee. Its trigger compares each attendee with `scope:activity.activity_host` and admits only the host of a **generic** vanilla Feast who is Jewish and whose rite has `tenet_ritual_celebrations`. The one-button `jewish_holiday_feast.0001` then supplies a meal scene. The host gains a minor Piety reward. Every attending close family member gains +5 opinion of the host. Murder, legendary, and Tsagaan Sar feast options do not qualify. The normal Feast activity and its own start events continue unchanged.

Five existing holiday events mark a 45-day recent observance on the character when they fire: Pesach (`.0003`, `.0004`), Sukkot (`.0011`, `.0012`), and Shavuot (`.0013`). The feast event uses these flags for a Seder, Sukkot meal, or Shavuot seudah. Without one it uses generic Jewish meal wording. No month alone names a holiday. A Shabbat seudah remains future flavor because the current calendar has no reliable weekday state.

This first version awards the bonus **at feast start**, rather than after successful completion. The existing start on_action permits a small additive hook without copying vanilla's large feast activity definition. Kehillah leaders cannot currently host vanilla Feast, so this pilot does not grant Stability; their holiday-event frequency benefit remains active. A later Kehillah-compatible feast route or completion hook can add Stability after it is independently validated.

## Source and test notes

`ck3-tiger` on CK3 1.20.1 found only three `unknown token rite` reports in touched files. The installed 1.20.1 vanilla Feast uses `rite = { rite_has_tenet = tenet_ritual_celebrations }`, so these are 1.19-linter mismatches. The isolated CK3 profile enabled this mod and reached history load and the main menu. Its `error.log` reported four orphan notices for console-only debug events, with no Feast script or localization parse errors. The debug events now declare `orphan = yes`; a repeat boot for that change is pending. Events `jewish_holiday_feast_debug.1` through `.4` report qualification or arm one of the recent-holiday flags for a planned host before starting a real Feast.

A live event check must use the isolated profile in [the setup note](../testing/2026-10-13-isolated-ck3-setup.md): verify a Samaritan generic Feast gets one scene and the Piety/family reward; verify a Jewish host without the tenet and a murder Feast do not; arm Pesach/Sukkot/Shavuot flags to verify each text variant and check `error.log` after each run. The hidden boot check can confirm files load but cannot establish these outcomes or visual wording.
