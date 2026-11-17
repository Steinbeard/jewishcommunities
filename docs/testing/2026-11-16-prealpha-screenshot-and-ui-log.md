# Pre-alpha screenshots and UI check — 2026-11-16

**Status:** three bookmark captures, Granada Quarter art, and Rashi Domain leadership/pillar views captured. The leadership-style error flood found on the first run was removed by an unset-variable guard and rechecked live. Other game-start script errors remain and need a separate fix before release.

## Method and images

A Luna tester alone controlled CK3, following the repository's live-test rule. They checked process ownership, launched the shared checkout in the isolated `festival-observance` profile, and stopped only their verified PID 32040 after the session. No CK3 process remained in the final check. The game reached the **1066 Age of the Rishonim** bookmark and entered a Granada campaign.

Three full-window 1936×1119 JPGs and one 1715×802 Quarter crop were visually reviewed and added for public docs:

- [`rashi-start.jpg`](../images/rashi-start.jpg): Shlomo Yitzhaki selected at Troyes.
- [`granada-start.jpg`](../images/granada-start.jpg): Joseph ibn Naghrilla selected as Granada's Nagid.
- [`david-start.jpg`](../images/david-start.jpg): David ben Hezekiah selected as an adventurer in Granada.
- [`granada-jewish-quarter.jpg`](../images/granada-jewish-quarter.jpg): the 1066 Granada Quarter art with named buildings and levels; used as the README's lead image.

A third isolated game session added two full-window **1936×1119** Rashi/Troyes Domain captures:

- [`rashi-domain-leadership.jpg`](../images/rashi-domain-leadership.jpg): Quarter card and the three illustrated leadership-style choices.
- [`rashi-domain-pillars.jpg`](../images/rashi-domain-pillars.jpg): leadership summary and all three pillar bars with numbers and standing.

PNG masters and an **internal-only** Granada character-panel image remain in the tester's temp capture folder. The latter contains debug-mode campaign UI and is not used as a public screenshot. The existing library and Bet Din images in the README are from earlier live play; their current UI has not yet been reshot. The new Quarter JPG is a deterministic crop from the full-resolution PNG master, removing the debug map-mode controls at the right and lower edge. It shows the current art and buildings but is not a release-build capture.

## Error found while capturing

The first boot's `error.log` had 1,560 lines, 55 with `kehillah` tags. Opening Granada's character panel raised it to 165,365 lines, 87,602 tagged `kehillah`. The repeated new errors start at `common/scripted_triggers/kehillah_leadership_style_triggers.txt` lines 17 and 22, via `common/script_values/kehillah_leadership_style_values.txt` lines 17–28: `Failed to fetch variable for 'kehillah_leadership_style' due to not being set`, followed by `Invalid left side during comparison 'var'`. Unconfigured seats intentionally have no style variable, but the Political and Commercial checks compared it without a guard.

The two checks now require `has_variable = kehillah_leadership_style` before their numeric comparison. xTiger after this edit reported **0 fatal, 32 errors, 126 warnings, 37 untidy, 135 tips**, with no new diagnostic on the changed lines. The existing seven-check leadership source suite passed six checks; its GUI styling assertion fails because the source expects the older color tiles while the current panel uses the later Camp Purpose art. That mismatch does not test the new guard.

The Luna tester then launched a fresh isolated CK3 process, PID 39392, and loaded Granada on **15 September 1066**. The post-boot baseline was 58 lines. After opening the character panel and Quarter view, the previous leadership-style signatures stayed at **zero**: no invalid `var` comparison, unset `var` scope, trigger line 22 or value line 28 error. The tester captured the Quarter image above, then stopped only PID 39392; no CK3 process remained.

The overall log still grew to **57,743 lines** after entering the campaign. Its repeated errors are different: `title_province trigger [ Failed context switch ]` arose 7,074 times from `common/scripted_effects/kehillah_jewish_culture_homeland_effects.txt:104` through game-start seeding. A separate `trigger_else_if with no trigger_else` at `common/activities/activity_types/kehillah_bet_din_conference.txt:262` appeared during boot. The screenshot pass did not diagnose or fix either issue, and it does not establish that the release copy is ready to upload. The staged pre-alpha still needs its own smoke-test boot.

In the third session, Luna loaded Rashi at Troyes and opened **My Realm → Domain**, then scrolled from the Quarter/style cards to the pillar bars. The campaign log stayed exactly **57,743 lines / 36,268 kehillah-tagged** before and after those UI actions. All four leadership-style error signatures stayed at zero. The tester stopped only the verified isolated PID 16932; no CK3 process remained. Domain panel rendering and the displayed pillar values passed visual inspection. Style selection, mandate expiry and succession effects were not exercised.

## Additional map and library pass

In a fourth isolated session, Luna played Joseph ibn Naghrilla in Granada on **15 September 1066** and opened the Jewish Communities map mode. The live [Córdoba inspector](../images/cordoba-community-inspector.jpg) showed Parnas Hasdai, a founding date of 756, healthy Prosperity and Stability, strained Greatness, host and Quarter links, and an annual danger value. Its public JPG is a 1240×780 crop of the full-window PNG master, with debug map buttons omitted. Opening the inspector added no new error lines beyond the 57,743-line game-start baseline. Only the owned PID 18460 was stopped.

The Córdoba library reported **13 works** across Parshanut, Talmudics and Machshavah, but its shelf appeared as empty wood. No library image from this pass was selected for public docs. Whether this is a book-card rendering bug or a navigation/state issue remains unverified. The xTiger console tool was unavailable and the console did not open, so the requested title-scope probe was not run.
