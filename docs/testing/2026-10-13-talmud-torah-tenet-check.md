# Talmud Torah tenet check — 2026-10-13

**Status: Source and linter checks complete; live boot and gameplay pending.** Worktree: `codex/festival-observance-2026-10-13` in the separate Codex copy.

The Rabbinism rite override was compared with installed CK3 1.20.1 `00_rite_types.txt`: its third tenet is the only behavioral change. Source inspection followed the Learn Torah decision, scheme gate, shared work-resolution effect, and completion event. The new eligibility trigger admits readers with the tenet while retaining the prior rabbi/ordination route. The mastery reward runs after the result is set, pays only for results 1 and 2, and leaves Rabbi trait XP behind its existing trait check. `git diff --check` passed.

`ck3-tiger` 1.19.0 produced no touched-file findings except `unknown token rite`. The 51 reported instances include repeated expansions of the shared work effect; installed CK3 1.20.1 vanilla uses the same `rite = { rite_has_tenet = ... }` shape, so these are version-mismatch leads rather than syntax changes to make on the linter's say-so.

An isolated CK3 boot was requested, but another `ck3.exe` process (PID 6804) was already active. The test did not launch a second process, send UI input, or change display topology. Tenet display, Learn Torah visibility for a lay reader, the console probes (`kehillah_talmud_torah_debug.1` and `.2` in a disposable save), and actual Piety/XP resolution remain unverified in live play.
