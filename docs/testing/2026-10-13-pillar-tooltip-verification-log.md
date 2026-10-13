# Pillar tooltip source audit and deferred UI check — 2026-10-13

**Status:** source review passed; nested tooltip rendering remains untested. Live
control was deferred after 30 minutes of another agent's CK3 activity.

This run selected the first item in [ROADMAP.md](../../ROADMAP.md), **Pillar band
effects in tooltips**, following [implementation note §18](../implementation/v1-kehillah-implementation.md#18-pillar-band-effects-in-the-community-roster-tooltips-2026-10-12).
It did not move on to a later feature or change gameplay.

## Checkout and ownership

- Used the existing checkout and `autonomous/shabbat-2026-10`, starting at
  `73c9116`. No branch or worktree was created, switched, or merged.
- Other listed Codex chats were idle. Claude Code session
  `b0186a7c-f855-44cc-bcd8-422829ed0748` had an active tester,
  `agent-a4feaf910d19ffb7b`, with CK3 input, screenshot and soak helpers.
- Preserved the five pre-existing tracked edits: `kehillah_traits.txt`,
  `kehillah_settlement_conditions_events.txt`,
  `kehillah_host_charter_prototype_l_english.yml`, `make_trait_icons.py`, and
  `trait_icon_prompts.json`. Untracked trait icons and their source images were
  also left alone. This run's only repository change is this log.

## Source verification

Ran `ck3-tiger.exe descriptor.mod --no-color` before script inspection. Baseline:
**0 fatal, 756 error, 136 warning**. The repository is not globally linter-clean.
No diagnostics named `kehillah_breakdown_custom_loc.txt`,
`kehillah_breakdown_l_english.yml`, or `kehillah_community_map_view.gui`.
Full output is retained in the automation directory as
`tiger-2026-10-13-baseline.log`; no script/localization/GUI file was edited.

Read the band custom localization, gap script values, modifier definitions and
the HUD/roster tooltip bindings. Findings:

- Thresholds are 150 / 400 / 700 / 950. The hover-detail ranges match them.
- Current, next and lower band selections check the highest threshold first.
  Crisis has no lower band; Legendary has no higher band.
- All 15 detail keys exist. Prosperity describes income; Stability describes
  stress gain and courtier/guest opinion; Greatness describes prestige and,
  in its upper two bands, Learning. Values and signs match the modifiers.
- Healthy has no band modifier. The HUD and roster use the same assembled
  breakdown keys with a title data context.

These checks establish source consistency, not whether a nested link is
reachable or renders correctly in CK3.

## Passive observations; no live probe

Ownership checks began at **2026-10-12 23:58 America/New_York** and continued
until **2026-10-13 00:28**, with process, log, checkout and downscaled screen
observations roughly every 2.5 minutes. The automation directory retains the
timestamped observations and 1024-pixel captures.

The screen showed the main menu at 00:00, a running Worms game in 1099 at
00:07, and 1102 at 00:10. Cursor positions changed, logs grew and Claude's
tester issued fresh input/soak commands. At 00:27 the screen had advanced
again and a character panel was open; Claude still had an outstanding test
command. This was active testing, not merely an open Claude app or a static
paused game. The automation did not send input, run debug events, load a save,
relaunch, or stop CK3.

The observed game's error log was changing under the other tester. No
before/after error delta from this run can be attributed to the pillar UI.

## First task for the next run

Retry this same first TODO after rechecking agent and CK3 ownership. Use a
throwaway test state while preserving the existing game/save. Record the
error-log baseline immediately before the probe, then:

1. Lock each pillar breakdown and hover its next/lower labels in the HUD and
   community roster. Report the exact nested text and whether the pointer can
   reach it without closing the parent tooltip.
2. At Flourishing (750), expect Healthy below and Legendary above, with a
   200-point gap. Check all three pillars' distinct modifier effects.
3. Check Crisis and Legendary endpoints, then the 150 / 400 / 700 / 950
   boundaries. Existing `kehillah_debug.1`–`.5` set representative bands;
   `.11`–`.13` isolate one pillar. When checking applied modifiers after
   changing variables, also run `kehillah_update_all_pillar_bands_effect` on
   the leader: the variable-setting probes alone do not refresh modifiers.
4. Compare error-log line count and new content after each hover. Confirm
   there are no missing keys, wrong neighboring bands or repeated UI errors.

Do not mark ROADMAP's live rendering check complete until those observations
exist. No later TODO was substituted for it during this run.
