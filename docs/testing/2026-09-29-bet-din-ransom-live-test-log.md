# Bet Din ransom case live test — 2026-09-29

**Status: LIVE-PROBED.** Case 7's host-to-resolution path passed in CK3
1.19.0.6 on a disposable 1066 Worms run. The second judge was AI-controlled;
player-controlled dissent and the Silversmiths' revised response remain to be
probed separately.

## Method and result

- `ck3-tiger` on the mod descriptor after the edits: 0 fatal, 0 error,
  63 existing warnings, 17 tips.
- A fresh debug-mode boot reached a fully staffed Bet Din on 20 December
  1066. `event kehillah_rabbi_loop_debug.1` confirmed a convening title, an
  ordained Av Beit Din, and judge 2 and judge 3 in `debug.log`.
- After clearing the naturally drawn first case, console-only
  `event kehillah_rabbi_loop_debug.3` opened `A Captive's Ransom`. The host
  popup showed all three localized policy choices. The player chose the full
  communal collection. Judge 2 resolved under AI control.
- By 1 January, the resolution popup showed its public-collection paragraph.
  Its hover effects displayed a great ruling, +3 Rabbi Talmudics XP, +20
  piety, and the public-collection explanation. After selecting `Send the
  court's answer`, the activity advanced to a naturally drawn dowry case on
  3 January. The activity log panel itself was not opened.
- `error.log` grew from 600 to 605 lines between the probe and next case.
  All five new lines were the existing community-map GUI layout warning;
  there were no case 7 event, scope, script, or localization errors.

## Scope of the result

This confirms the host choice, AI continuation, direction-specific verdict,
reward display, and docket progression. It does not confirm a player-controlled
second judge successfully changing the policy or numeric pillar changes.
The same boot started while the new case 6 response-localization lines were
being edited, so its startup log contains stale missing-key errors for those
keys. They exist in the final UTF-8 BOM localization file and the final
`ck3-tiger` pass reports no missing keys from this change; a fresh boot is
still needed for a visual check of those revised responses.
