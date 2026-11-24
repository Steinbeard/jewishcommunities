# Native Jewish culture seeding guard — isolated CK3 check, 2026-11-16

**Status:** targeted 1066 runtime, combined culture-map color, and 867 game-start checks passed. Other bounded script errors remain.

## Baseline and source

The 1066 pre-alpha screenshot run on the original checkout produced **7,074** `title_province trigger [ Failed context switch ]` lines at game start. They were distributed evenly across nine geography checks in `kehillah_jewish_culture_homeland_effects.txt`: **786** failures per check. The debug trace starts at `kehillah_on_game_start` and `kehillah_seed_native_jewish_cultures_effect`. Opening Domain and the community inspector did not increase the count. The local CK3 1.20.1.2 game scripts use `exists = title_province` before following the same link in several places.

The fix adds that guard to the initial `every_county` seed loop and the North Europe clearing loop. It leaves every county with a usable province link on the existing path. xTiger totals before and after: **0 fatal, 32 errors, 126 warnings, 37 untidy, 135 tips**.

## First live boot: bugfix branch alone

Luna alone controlled CK3 in the isolated `festival-observance` profile, after inspecting process ownership. The mounted descriptor pointed to the `jewishcommunities-culture-seeding-fix` worktree. A fresh 1066 Granada campaign reported **zero** `title_province trigger [ Failed context switch ]` matches, down from 7,074. This branch is based on `origin/master` and lacks the separate leadership-style guard in PR #71, so its log flooded instead with unset-style `var` comparisons. The tester did not proceed to UI checks on that run and stopped only the owned PID 3484. No CK3 process remained.

## Combined live boot

The same two-line province guard was applied to the shared checkout, which already contains the leadership-style guard. Luna verified the isolated mod mount and entered the 1066 Granada campaign. `error.log` rose from **5 lines at boot to 1,937 after game start** (1,684 kehillah-tagged), with **zero** province context-switch, invalid-style `var` comparison, or unset `var` scope signatures. Jewish Cultures painted Iberia magenta; Al-Lacant and Medellin hovers read **Sephardi**. The log stayed at 1,937 lines during the UI interactions. A public screenshot was not saved because clearing debug hover data moved the camera off-map. The tester stopped only PID 37084 and confirmed no CK3 process remained.

Other bounded script errors remained: 15 attempts to add a mikvah to a full Quarter, two `add_saint` errors for Hebron, two opinion-modifier duration errors, and one Bet Din `trigger_else_if` syntax error. These are separate from the culture-seeding fix.

## 867 pre-Ashkenaz game start

Luna launched a new isolated shared-checkout process, PID 10984, and entered **Age of the Geonim** as Amram Gaon on **1 January 867**. The post-entry log had **1,998 lines / 1,554 kehillah-tagged**. It contained zero `title_province` context-switch errors, zero leadership invalid-var or unset-var-scope errors, and no lines from `kehillah_jewish_culture_homeland_effects.txt`. This checks that the 867 pre-Ashkenaz call path does not reintroduce the flood. The Jewish Communities map showed colored patches and an uninhabited Kirkuk inspector, but debug ID/title-key tooltips prevented a public screenshot. The tester closed only the owned PID 10984.
