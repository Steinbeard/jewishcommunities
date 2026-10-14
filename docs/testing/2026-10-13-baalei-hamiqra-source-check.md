# Ba'alei ha-Miqra source check — 2026-10-13

**Status: Source checked; live boot and gameplay pending.** This log covers the [Ba'alei ha-Miqra addendum](../spec/jewish-baalei-hamiqra-tenet.md) on `codex/festival-observance-2026-10-13` in the separate development worktree.

## Checks

- Compared the new tenet, Karaism Rite override, study scheme, Religious Scholar XP, faith-status effects, and Spiritual Fulfillment effect with the installed CK3 1.20.1 definitions. Vanilla uses `rite:` and `faith:` identifiers, `set_tenet_status`, `has_tenet_status`, and `change_spiritual_fulfillment`. Its Study Scripture event uses Religious Scholar XP. The custom study scheme uses a separate curriculum and never calls the rabbinic library or Rabbi trait.
- Guarded both new Spiritual Fulfillment paths with `is_playable_character = yes`, matching a vanilla interaction's explicit warning that the effect errors for non-playable characters. New mastery gives +3, successful rereading +1, and successful Examine Scripture +3; failures give none.
- Ran `ck3-tiger` 1.19.0 against `descriptor.mod` after the changes. It exited successfully, reported no new missing localization or malformed script, and still reported older-model unknown tokens for the installed 1.20.1 religion and fulfillment APIs. Those findings were checked against the installed vanilla source rather than patched around. `git diff --check` passed.

## Live-test status

An existing `ck3.exe` process (PID 9328, started 20:27:34 with `-debug_mode -develop`) was active in the shared desktop. The delegated read-only check did not launch, focus, send input to, or close it. The shared `error.log` had no Ba'alei/Miqra/Examine/Literalism/tenet-status lines, but that log does **not** validate this worktree. A fresh boot, decision/scheme run, three-course trait award, faith-status display, and Fulfillment change remain to be tested when a separate CK3 instance is available.
