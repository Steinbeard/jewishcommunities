# County endowments and the community library

**Status:** Built 2026-11-15 in the shared checkout; five source regression checks pass. Live county-grant, save/reload and tooltip checks remain pending. Extends the county-endowment path in `kehillah_sanhedrin_effects.txt` and the [Sefer redesign](../spec/2026-11-08-sefer-system-redesign.md). Does not implement the proposed Jewish-conqueror choice event.

## Rule

Daniel requested that turning a community into a landed county preserve its library and house it in the temple. The existing county grant retains the communal title and government. Its library now gains a physical seat in a Jewish-held temple in that community's capital county, with the existing temple Beit Midrash building. Repeated refreshes keep the same temple. Existing building upgrades and temple collections are untouched.

The community title remains the canonical collection record. There is no copy, merge, re-seeding, deletion or re-registration of its shelves: this preserves language copies, loans, pending acquisitions, yeshiva state and ongoing study references. It also preserves direct community-title consumers of the book system. This is a relocation, not a second collection on the temple title. A separate library already registered on that temple remains a distinct collection.

The grant refreshes the seat after resolving ownership. The existing annual library pass applies the same relocation to older saves and retries if there was no suitable temple. If the holder does not own the community's county, is no longer landed/Jewish, or the temple ceases to be suitable, the library falls back to its Quarter (or selects another suitable temple when applicable). No county conversion or temple faith conversion is forced, and no castle/city is replaced.

The county's library card can link to this temple-seated community collection, and the Library/Yeshiva tooltips name its housing location. The card still shows one library per county, following the existing registry-order behavior where multiple collections coexist. The separate Communities-map temple paint remains limited to barony-owned libraries; the Libraries map reads the collection's updated physical seat.

This does not implement surrendering/destroying the communal title to become an ordinary hereditary feudal ruler. Such a future conversion must transfer the canonical collection record and retarget its consumers before deleting the community title; it must not invoke a fresh temple-library seed as a substitute.

## Verification

- `python scripts/test_kehillah_library_county.py`: five checks pass (no collection mutation; grant/yearly integration; seat priority/fallback; local Jewish temple constraints and stable selection; county-card physical seat).
- xTiger before edits: 0 fatal, 32 errors, 124 warnings. First run after relocation effects: unchanged. Later concurrent work changed repository-wide totals; final run reported 0 fatal, 35 errors, 132 warnings, with no diagnostics on this change's files (including after adding UTF-8 BOMs to the new script files). The concurrent revolt/leadership work changed unrelated diagnostics, so the aggregate delta is not attributed to this unit. No claim of runtime validation.
- Luna availability check: no xTiger CK3 tools exposed; CIM denied process-ownership inspection. No game launched or controlled.

## Manual checks (disposable save)

1. Before a county grant, record the exact shelves, language variants, outstanding loan/commission and an active study target. Use an acquired/authored work beyond the starter collection.
2. Grant the community county through its existing petition/debug grant path. Confirm the Quarter remains, all recorded data is unchanged, and the library seat is a Jewish-held temple in that county. Confirm its Beit Midrash building and location tooltip. Existing temple upgrades and any separate collection must survive.
3. Run `event kehillah_library_county_debug.1` twice. The log must report preserved shelf count; the temple identity must stay the same. Complete the previously started study, then save/reload and recheck shelves and location.
4. With no Jewish-held temple, repeat the grant: retain the Quarter library. Provide a suitable temple and run the annual Sefer pass (`event kehillah_sefer_v2_debug.3`); verify relocation without starter books being added.
5. Lose the county or change the temple's custodian to a non-Jew, then refresh. Confirm safe fallback and no shelf loss. Check a Karaite/Haymanot collection as well: no Rabbinic books should be introduced by relocation.

## Delivery

Git staging of only this unit's files failed creating `.git/index.lock` with Permission denied. Commit, push and PR creation remain blocked by read-only Git metadata. No branch switch or cleanup was attempted; unrelated shared-checkout edits remain intact.
