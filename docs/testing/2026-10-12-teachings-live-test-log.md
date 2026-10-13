# V31 Slice A (Teaching on the Jews) live test - 2026-10-12

**Status:** live-tested against commit 1d70a5c (branch autonomous/shabbat-2026-10). Observations only; nothing fixed. Fresh `ck3.exe -debug_mode -develop` boot (PID 29360); `debug.log` showed `Jewish Communities|mod/jewishcommunities.mod|Enabled`. error.log baseline at main menu: 237 lines. Played "The Kehillah of Worms" as Isaac (internal id 29176; host Heinrich Salian, e_hre, internal id 38688).

## Key finding
`change_rite_doctrine` DOES accept the mod doctrine group, and the rite screen DOES show it. Every rite probe held its assigned teaching.

## 1. Start, ~5 days, assignment fired - PASS
Ran 15 Sep to 18 Sep 1066 (the Charter event paused the game; accepted). debug.log:
`kehillah_assign_teachings_effect: Christian and Muslim rites given their teaching on the Jews` (21:32:19, game start). error.log has no `kehillah_teaching` / `change_rite_doctrine` lines except the five expected "Event kehillah_teaching_debug.N is orphaned" lines (hidden debug events, in baseline).

## 2. `kehillah_teaching_debug.1` - PASS
```
roman_rite HOLDS Witness
byzantine_rite HOLDS Imperial Law
maliki HOLDS Dhimma
host rite HOLDS a teaching doctrine
band PROTECTIVE
ceiling FORBIDS Banned
forced conversion FORBIDDEN
```
Probe variables (zeal / clergy / protective / net / ban_threshold): NOT READABLE. The probe sets them on the host, dumps scopes, and removes them; the `debug_log_scopes` dump lists only saved event targets (leader, patron/prosperous/grievance host), not variables. So none of the values were observed. (Tester note: the dump format cannot show them; the probe would need `debug_log` with a value-formatted string.)

## 3. Rendering - PASS
Clicked the Emperor's portrait on the map, then the "Roman Rite" box in his character panel; the Roman Rite window opened. Under "Main Doctrines" there is a doctrine tile labelled "Witness" with an icon (document/scroll with figure icon). Hover tooltip: title "Witness", tag "Doctrine", text: "Jews are to be preserved, subordinate, as witnesses to Scripture: not killed, not baptized by force. Zeal under this teaching presses them as much as it presses them. A realm's Jewish Settlement Policy can fall no lower than Discouraged through ordinary review." No raw keys, no blanks (read from a 1024px downscale; the tooltip text was legible). The group name "Teaching on the Jews" was not visible as a heading on this tile or tooltip (the tile sits in the generic Main Doctrines grid); not checked in Faith Details.

## 4. `.3` (Exclusion), `.1`, conversion_debug.4 - PASS
```
kehillah_teaching_debug.3: host rite set to Exclusion
band EXCLUSIONARY / ceiling PERMITS Banned / forced conversion PERMITTED
kehillah_conversion_debug.4: PLAYER DEMAND VALID, host sends it
```
"Demand Conversion" popup from Kaiser Heinrich arrived (realm was not Banned); Declined. Ban threshold 4 not observable (see step 2). Side note: after `.3`, `.1` reports "roman_rite does NOT hold Witness" - expected, since the host's rite is the Roman rite and Exclusion replaced it (one doctrine per group).

## 5. `.2` (Separation and Mission), `.1`, conversion_debug.4 - PASS
```
kehillah_teaching_debug.2: host rite set to Separation and Mission
band STRICT / ceiling PERMITS Banned / forced conversion FORBIDDEN
kehillah_conversion_debug.4: player demand NOT valid (is the realm Banned?)
```
The step 4 cooldown did not interfere.

## 6. Discouraged + three reviews - PASS (runs clean, no change)
`kehillah_debug.74: host realm policy set to Discouraged`. Reviews at 18 Sep, 28 Sep and 7 Oct 1066 (separated by ~10 game days each) all logged:
```
kehillah_policy_ai_review_effect: reviewing this ruler's Jewish Settlement Policy
kehillah_policy_ai_review_effect: no pressure strong enough -- policy unchanged
```
No errors.

## 7. Back to Witness + review - PASS (ceiling not exercised)
`.4: host rite set back to Witness`; `.1` then reads band PROTECTIVE, FORBIDS Banned, forced conversion FORBIDDEN, all rites HOLD. Review: "no pressure strong enough -- policy unchanged". The "teaching on the Jews forbids it" line did NOT appear (the policy was Discouraged, so there was no downward pressure to cap). The ceiling was therefore not seen working live in this run.

## 8. ~60 more days - PASS
Ran 7 Oct 1066 to 3 Jan 1067 (~88 days). ck3.exe alive and responding, no Game Over. Consequence of my declining the conversion in step 4 (known from the earlier log): an Imprison demand arrived about 8 Nov (declined), then "Into Exile" - Isaac left for the road as a wayfarer, Shaul leading Worms. error.log 237 -> 361 lines. Lines added mentioning teaching, doctrine, rite, policy, conversion or expulsion: none from this mod. The only hit is a vanilla `hold_court_8180_grant_contract_effect` error ("Sunni does not have the Jizya Doctrine", `religious_rights_protected` for a Gandhara vassal), plus other vanilla hold_court / legend_events / missing-loc lines.

## Surprising
- Probe variables cannot be read through `debug_log_scopes`.
- The "Teaching on the Jews" group heading is not shown on the doctrine tile.
- Declining the step 4 demand cascaded into arrest demand and exile within ~50 days (expected per the 10.3 log, but it ends the Kehillah leadership for Isaac).
- Clicking through wayfarer popups to reach 60 days took several pauses.
CK3 closed by PID after the test.
