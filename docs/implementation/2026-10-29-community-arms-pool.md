# Curated coat of arms pool for runtime Kehillot

**Status: Implemented 2026-10-29; xTiger source check passed, live validation pending.**

The authored community titles retain their fixed arms in
`common/coat_of_arms/coat_of_arms/kehillah_title_coas.txt`. A title minted at
runtime by `create_adventurer_title` has no matching authored title key. Its
founding path now calls `kehillah_generate_community_coa_effect` exactly once,
after the title exists. That effect uses CK3's documented
`generate_coa = kehillah_community` effect. The custom template list selects
one of two high-contrast layouts; each draws one of eight vanilla charges:
menorah, key, scales, tower, pomegranate, tree, fish or grain. These are
editorial gameplay emblems, not claims of historical heraldry. No new art
assets or DLC-only charges are required.

The three creation paths are the adventurer decision
(`kehillah_found_community_effect`), Send Out Settlers
(`kehillah_found_with_founder_effect`) and the Norman founding finish effect.
The shared effect is not called on title gain, succession or a periodic pulse,
so an existing title's arms are not deliberately rerolled. The hidden
`kehillah_coa_debug.1` event rerolls the currently played Kehillah on a test
save to inspect several generated examples without repeated founding.

The installed game's `effects.log` documents `generate_coa` for landed titles
and accepts a named template list. Vanilla uses it on `scope:new_title` in
`common/casus_belli_types/00_religious_war.txt`, and the mod already uses it
for mob faction titles. The installed game's template and emblem list syntax
provided the patterns used here.

## Validation

- xTiger 1.6.10, aimed at this worktree: 15 errors, all in previously
  existing files; no findings in the new arms files or touched founding
  effects.
- The xTiger scripted launch was attempted without screenshots. It did not
  reach a validation result: an existing CK3 PID 22144 had no Codex ownership
  marker, and the short-lived xTiger MCP client stopped before its queued job
  completed. No other CK3 process was controlled or stopped.
- Pending when the CK3 test instance is free: boot this checkout at the Worms
  bookmark, confirm no new coat-of-arms load errors, found a runtime community,
  inspect several samples via `kehillah_coa_debug.1`, then save/reload and
  confirm the chosen arms persist. Verify at least one settlers or Norman
  founding as well.
