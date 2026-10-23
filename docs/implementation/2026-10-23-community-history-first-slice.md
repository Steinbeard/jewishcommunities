# Community history: county record and portable summary

**Status:** First implementation slice built and partly live-verified 2026-10-23. Implements the summary tier of [V50](../spec/v50-community-founding-and-place-memory.md). It does not yet provide an unlimited chronological list of every loss and refounding.

The community title already had `kehillah_founded_year` for age and Greatness. Its destruction erases its variables. `kehillah_community_history_effects.txt` therefore stores the original year and the most recent loss/refounding on the **county title**. Historical title-year assignments seed county records at new-game start, including the vacant Kairouan site. The 1057 Banu Hilal sack seeds Kairouan's loss only in bookmarks after that date; Mahdia receives a separate 1057 refugee-arrival line rather than a false second founding.

The three runtime creation paths call `kehillah_history_record_founding_effect`: the adventurer decision, Send Out Settlers, and the Norman founding event. Existing county history causes a refounding and preserves the first year. A named founder is saved automatically. Settlers use their mother community's county as origin; exiles use the county they were driven from. No origin is invented for other adventurers or Norman founders. A new title mirrors the county's first year into `kehillah_founded_year`, so the existing age benefit survives a local refounding.

The common dissolution path calls `kehillah_history_record_loss_effect` before `destroy_title`. It classifies mob violence as destruction, and expulsion, forced conversion, or internal collapse as abandonment/dissolution. A mob leader is linked only when its existing title variable still identifies a character. The last loss and refounding fields are replaced on a subsequent cycle; the original year is never replaced. This is explicitly a **summary**, not a complete archival ledger. A full, save-safe iterable event representation remains the V50 engine spike.

`KehillahHistory*` county-context customizable localizations compose the original year and current age with optional founder, origin, loss, and refounding clauses. The age comes from a county-scoped script value, so it updates with the game year. Domain shows the summary for the player's community; the no-community map tooltip shows the same place memory for a vacant historical site. Character and county references use tooltip-capable names. The hidden `kehillah_history_debug.1` and `.2` events inspect Kairouan and the current community record through `debug.log`.

## Historical boundaries

The current Worms 960 and Baghdad 762 anchors are retained as approximate establishment dates, not exact foundation days. [Encyclopaedia Iranica](https://www.iranicaonline.org/articles/judeo-persian-communities-iii-parthian-and-sasanian-periods/) places Jewish deportations to Babylonia in the sixth century BCE; [its Baghdad entry](https://www.iranicaonline.org/articles/baghdad/baghdad-iranian-connection-i-pr-mongol/) dates the Abbasid city to 762 CE. Older Babylonian history does not become a Baghdad founding by changing the label. [ANU's Kairouan entry](https://dbs.anumuseum.org.il/skn/en/c6/e246606/Place/Kairouan) identifies the Banu Hilal sack in 1057. Sura's academy and Pumbedita's office are not treated as automatically destroyed town communities when their scholarly institutions end.

## Verification

- xTiger 1.20 fork, before and after: **0 fatal, 15 errors**; no new fatal/error. The 15 errors are in pre-existing files outside this change.
- `git diff --check`: clean.
- Isolated 1066 Worms boot and numeric debug comparisons: Worms county and title both 960; Kairouan founding 670 and loss 1057. Domain rendered “Established by 960” after using the custom localization's `ROOT.Title` county scope. No history-related errors arose on the fresh boot or Domain open. See [the dated live log](../testing/2026-10-23-community-history-live-test.md).
- Isolated 867 boot: Kairouan founding 670 was present and the 1057 loss was absent, as required by the date gate.
- Still required: the new age suffix in Domain, vacant Kairouan map render, save/reload, and a live founding → dissolution → refounding probe. Per `AGENTS.md`, live tests must be delegated to a Luna subagent.

## Known limits

- This seed runs at new-game start. Existing saves need a migration pass before the new historical county data will appear.
- The summary retains only the latest loss and latest refounding, plus the original year and Mahdia refugee arrival. It must not be presented as a complete chronology.
- Historical character-origin records have not been mass-authored: uncertain founder names remain omitted. The 35 existing founded-year anchors supply the dated base.
