# Bet Din AI hosting experiments

Status: **experiment in progress** — 2026-10-17.

## Experiment 01 — renamed vanilla Camp Party baseline

- **Baseline:** installed CK3 1.20.1.1 `common/activities/activity_types/camp_party.txt` (885 lines).
- **Why:** it is the closest vanilla activity to a non-landed Kehillah: landless-adventurer host gate, domicile venue, and vanilla AI scoring/location selection. It also has no custom annual `ai_attempt_to_host_activity` hook, so it tests the activity system's autonomous scheduler itself.
- **Change:** copied the complete definition to `common/activities/activity_types/kehillah_ai_probe.txt`; changed only the activity identifier `activity_camp_party` to `activity_kehillah_ai_probe` (definition and cooldown reference). All host/location/phase/AI fields and existing camp-party behavior remain unchanged.
- **PASS criterion:** an AI landless adventurer starts `activity_kehillah_ai_probe` during normal unpaused simulation without a console command, player start, or directly fired opening event. Confirm through the live activity state/log.
- **Result:** pending live test. This is the known-good source baseline, not yet proven in the mod build.

### Source observations

- Camp Party uses `is_shown`/`can_start_showing_failures_only` for landless adventurer eligibility, `domicile_domain` for both player and AI venue filters, `ai_will_do = 50` plus general modifiers, and `ai_check_interval = 60`.
- Its vanilla definition contains no `ai_attempt_to_host_activity` call in `yearly_on_actions.txt`; it therefore provides the best test of autonomous activity scheduling rather than an explicit forced-start route.
- First mutation after the renamed baseline passes: change only the host-eligibility gates toward Kehillah actors. Do not change AI score or venue until a later isolated experiment.

## Sync note — 2026-10-17

Merged `origin/autonomous/shabbat-2026-10` (latest observed development branch, commit `dfa1db2`) into the Codex worktree as merge commit `75220a3`. The merge added a dedicated Bet Din Justice intent and its AI-weight update. The probe remains isolated and unchanged in behavior. Its header background intentionally reuses the vanilla Camp Party texture so the identifier-only experiment does not introduce a missing asset.

**Live test status at merge time:** not yet run; see the later dated live observer run below. Experiment 01 remains unproven, and no Bet Din-specific mutation has been made.

### Baseline source map

- **Definition and availability / host eligibility / AI schedule / location / participants / phases:** installed `game/common/activities/activity_types/camp_party.txt`, copied to `common/activities/activity_types/kehillah_ai_probe.txt`. The copy retains the vanilla landless-adventurer + EP3 availability gate, cooldown, `domicile_domain` player/AI venue filter, one phase, standard guest rules, and vanilla event/pulse references.
- **AI scheduling:** Camp Party's definition uses `ai_will_do = 50`, `ai_check_interval = 60`, and `ai_will_select_province = 10`. A source search found no Camp Party `ai_attempt_to_host_activity` call in `yearly_on_actions.txt`; vanilla's explicit annual override route in that file is used for tournament, feast, and imperial examination instead.
- **Creation/start:** there is no mod-style activity creation effect in this vanilla definition; normal AI scheduling is delegated to CK3's activity system. The test must therefore observe a real autonomously scheduled instance.
- **Location and phase:** `province_filter` and `ai_province_filter` are both `domicile_domain`; the predefined camp-party phase runs vanilla EP3 Camp Party events after start.
- **Mod comparison:** `common/activities/activity_types/kehillah_bet_din_conference.txt` contains its own availability and validity gates, domicile filters, open-invite guest rules, three case phases and AI scoring/venue selection. `common/on_action/kehillah_bet_din_ai_on_actions.txt` adds a separate yearly override/attempt route. The live question remains whether the generic scheduler can host the vanilla-derived copy before mutating those fields toward Kehillah actors.

### Static check

After the branch merge and texture-reference correction, `ck3-tiger` reports **0 fatal**, **976 errors**, and **137 warnings** for the entire worktree. The 1.19.0 Tiger vs. installed 1.20.1.1 version mismatch remains; the repo-wide static findings are not attributable to this probe. `git diff --check` passes.

### Live-test setup attempt — 2026-10-17

- Launched `scripts/kehillah_isolated_ck3_test.ps1 -Visible` with no other `ck3.exe` process present. The Codex instance was PID 27408 with `-userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`; it reached the main menu and was placed at `{X=2560,Y=0,Width=2048,Height=1152}` on DISPLAY5. The primary checkout/process was untouched.
- A click inside the loading screen released the known initialization stall; `Responding` became true and `debug.log` advanced. The mod loaded to the main menu.
- **No game was started and no autonomous-hosting result was observed.** The available CUA inventory exposed no native app/window. The prescribed `winkeys.py` mouse helper also misroutes extended-desktop clicks: its `_absolute()` normalizes across the virtual desktop but `mouse_move`/`mouse_click` omit `MOUSEEVENTF_VIRTUALDESK`. A direct shim-based workaround moved the cursor onto the correct second-screen point, and `WindowFromPoint` identified PID 27408 there, but repeated clicks did not activate New Game. This is an input/UI blocker, not a feature PASS or FAIL.

### Live observer run — 2026-10-17 (continued)

- Used the Computer Use window API to reach the running isolated CK3 instance on DISPLAY5; used the repository-authorized `winkeys.py` helper for the layout-independent console command `observe` after character selection. The process was PID 27676 with `-userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`. No primary-checkout files or game process were touched.
- Started the 1066 **A Rabbi on the Road** bookmark, then observed normal unpaused simulation through **1072.6.3** (about 5.7 in-game years). Saved an observer snapshot outside the repo at `C:/Users/Daniel/.codex/ck3-test/festival-observance/save games/KBD_AI_PROBE_1072.ck3`.
- The saved world has 25 active activity records (including vanilla pilgrimage, roaming, survey, hunt, feast, coronation, and other types), and 116 characters with `landless_adventurer_government` plus 75 camp domiciles. The save has **zero** `activity_kehillah_ai_probe` and **zero** `activity_camp_party` references. With `aiwatch` enabled, debug.log contains no probe/camp-party creation attempt; the AI errors are for unrelated coronation/hunt validation.
- **Result: inconclusive, not PASS and not a demonstrated clone failure.** The renamed copy loaded without an activity-type registration error, but the unmodified vanilla Camp Party itself also did not start, so this run does not establish that the vanilla control is being scheduled in this campaign. No Bet Din-specific field has been changed.
- **Next step:** keep the probe unchanged while checking the vanilla Camp Party AI's complete cost/provisions and host-candidate gates against the saved candidates, or select a better empirically active vanilla activity with a compatible landless host scope. Do not interpret the absence of both Camp Party types as evidence against the rename-only mutation.

### Experiment 02 — AI weight stress probe

- **Baseline:** Experiment 01 rename-only Camp Party copy, loaded in the same isolated observer save.
- **Single change:** raised only the copied activity's `ai_will_do` base from 50 to 5000. Host gates, costs, location, phases, guest logic, and events remained unchanged. `aiwatch` was enabled and confirmed by detailed vanilla invalid-activity diagnostics.
- **Run/evidence:** resumed at 1081.5.30 and ran unpaused at fastest speed to the 1086.1.1 autosave. The save contains 24 active activity records; it contains neither Camp Party ID. The log records normal AI attempts for other activity types, with no probe/Camp Party creation attempt or invalid-creation diagnostic.
- **Result: FAIL to meet autonomous-start criterion; causal result is unresolved.** A 5000 base score did not produce an attempt or activity within the observed 5.6 in-game years. This shows the score alone does not make the copy start in this campaign; it does not identify whether the scheduler is considering the copy or rejecting all candidates before creation.
- **Crash note:** the process exited at 1086.1.1 with `pdx_assert.cpp:619` (`GetOriginalIDHash collision`) while the 1086.1.1 autosave was being processed. No probe/Camp Party record is present in that autosave. The log does not establish that this assertion was caused by the probe, so treat it as a separate unresolved live-test risk and inspect crash details before another long run.
- **Reversion:** restored the probe score to 50 after the run; no failing mutation remains in the probe.
- **Next experiment:** inspect the exact vanilla `ai_attempt_to_host_activity` call sites and active vanilla host scopes to find a more empirically reliable control, then test the existing clone's scheduler path without changing unrelated Bet Din fields. Camp Party remains the closest structural comparison but is not yet a known-good autonomous baseline.

### Experiment 03 — targeted positive control (instrumentation attempt) — 2026-10-17

- **Candidate:** Olaf, character ID 38393, appears as the host of a vanilla `activity_roaming` in the saved 1072 observer campaign. He is an adult in that snapshot. This makes him a candidate for the landless-adventurer control, but the diagnostic did not verify his current AI/government predicates.
- **Instrumentation:** a one-off `run` file tried to target `character:38393` and check `is_ai`, landless-adventurer government, and `can_host_activity = activity_kehillah_ai_probe`. It did not call `ai_attempt_to_host_activity` and had no scheduler hook.
- **Result:** **invalid diagnostic; no eligibility result.** It ran against the already-advanced live observer state, not the 1072 snapshot, and `error.log` reported `Referencing non-existent character in script link character:38393`; the conditions did not evaluate on a character. No explicit host attempt or generic scheduler test was made.
- **Cleanup:** restored the probe's `ai_will_do` base to 50, removed the temporary on-action file, and paused the isolated CK3 process. The instrumentation script was removed. No feature conclusion is drawn from this run.
- **Correction:** `event <id> <character>` does not retarget a character; use a scoped `run` effect instead. A later bounded check is recorded below. The 1072 save was not used for that check, and this invalid Olaf attempt remains an invalid diagnostic.

### Experiment 04 — one-shot explicit host attempt (2026-10-17)

- **Scope:** gate 2 only. No `ai_will_do` change, on-action, Bet Din mutation, or generic scheduler test.
- **Test state:** one isolated Codex CK3 boot, loaded from `autosave_exit` at 2 June 1126. The pre-attempt save had no `activity_kehillah_ai_probe` records.
- **Targeting:** a temporary `run` file iterated living characters without randomness, selected the first AI character whose `can_host_activity = activity_kehillah_ai_probe` passed, logged its scopes, and guarded the explicit call with a global one-shot flag. It selected Virdyan Lowborn (runtime ID 105724). This was not the preferred previously observed vanilla activity host: the narrower roaming-host selector found no eligible candidate in this loaded state and made no attempt.
- **Gate 1:** **PASS** for Virdyan in this run (`is_ai = yes` and `can_host_activity` both passed immediately before the call). Earlier `KBD_PASS` logs also established the host gate on multiple AI roots; the failed Experiment 03 character-link attempt does not invalidate those results.
- **Gate 2:** **FAIL for immediate activity creation.** The run log records exactly one `ai_attempt_to_host_activity = activity_kehillah_ai_probe` call, followed by an immediate `every_activity` check; no matching activity hosted by Virdyan existed. The engine emitted a dynamic effect-localization error for `ai_attempt_to_host_activity_global` at the call site, then continued through the postcondition and reported the failure. This is a bounded result for this candidate, not proof about all eligible characters.
- **Gate 3:** **not tested**; the generic autonomous scheduler was not allowed to run as an experiment.
- **Cleanup:** removed the temporary event and run file. `ai_will_do` remains 50; no on-action or production Bet Din content was changed. The game was not advanced to wait for a later scheduler check.
