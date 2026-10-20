# Jewish lineage traits live test — 2026-10-18

**Status: Corrected rerun passed fresh boot, both historical-character assignments, the Ben David icon/tooltip check, and the targeted clean-log check. The initial run below found three defects which were fixed before the successful rerun.**

## Scope and isolation

- Tested branch `codex/jewish-lineage-traits` in
  `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities`.
- An unrelated launcher-owned CK3 process was already running as PID `7748`. It had no isolated
  `-userdir` marker and was not focused, moved, sent input, or stopped.
- Launched the worktree with `scripts/kehillah_isolated_ck3_test.ps1 -Visible`. The exact test
  process was PID `5252`, started at 22:26:51 with:

  ```text
  ck3.exe -debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance
  ```

- Moved only PID `5252` to non-primary `DISPLAY5` (`2560,0`, `2048x1152`) and targeted all input
  by that PID. The existing `winkeys.py` virtual-desktop mouse path was avoided; navigation used
  PID-owned focus plus `SetCursorPos` on the VDD.
- Stopped only PID `5252`. PID `7748` remained running with its original command line.

## Boot and targeted log check

The process remained responsive and `debug.log` reached:

```text
[22:27:37][D][history.cpp:1543]: End loading of history
```

The 1066 bookmark selector rendered, including `The Kehillah of Worms` (screenshot SHA-256
`96C42F00C77DF252BFF908F7DE2663FDA72704793338A038E5067ECE63616AE8`).

At that point `error.log` contained no line naming the changed trait, name-list, succession,
history, debug-event, or localization files. It also contained no `ben_david`, historical-ID,
name-list, or succession-score error. It did contain these two new definition errors:

```text
[22:27:25][E][trait.cpp:401]: Trait kohen is both set as genetic and has an inheritance chance
[22:27:25][E][trait.cpp:401]: Trait levite is both set as genetic and has an inheritance chance
```

There was no error attributable to the altered Israelite name lists or the Ben David succession
score. The two trait errors are blocking for the requested clean-log criterion.

## David and Elijah

There is no direct Baghdad bookmark. A normal 1066 Kehillah start was loaded, then the hidden
`kehillah_patronym_debug.1` probe was fired in the Baghdad and Jerusalem title-holder scopes.
The log proved the intended historical characters and runtime traits:

```text
kehillah_patronym_debug.1: BEN/BAT DAVID
Root: David of the House of David of d_kehillah_baghdad
      (Internal ID: 31919 - Historical ID 9000222)

kehillah_patronym_debug.1: KOHEN
Root: Elijah ha-Kohen of d_kehillah_jerusalem
      (Internal ID: 29853 - Historical ID 9000220)
```

The test then switched play by those exact internal IDs and opened each character panel:

- David's trait tooltip visibly read **Ben David**, including the localized description and
  Jewish-opinion/inheritance lines. Screenshot SHA-256:
  `2CA004C630D647132042198A406DA22090378E291900BAC4FCC5EF3384E877AD`.
- Elijah's trait tooltip visibly read **Kohen**, used the intended custom icon, and displayed the
  localized description. Screenshot SHA-256:
  `6A7DFC9F32CFCECDED193611E070B6FE1066DCD898E5F48D6CD7BEB19F6E0E38`.

David's Ben David icon itself rendered as the engine's `?` fallback. Opening that tooltip produced
9,950 copies of this attributable error before the isolated process was stopped:

```text
[E][pdx_data_localize.cpp:146]: Data error in loc string 'sayyid.dds'
```

The same tooltip evaluation also produced repeated vanilla activity-custom localization errors;
those are not attributed to this feature. The direct `sayyid.dds` error and visible fallback icon
are attributable to the new `icon = sayyid.dds` line and independently fail the UI/log check.

## Evidence and verdict

- Final `debug.log`: 1,193,637 bytes; SHA-256
  `3ACF8A9CE9BCF76B199E8761FDEA10C105963C07A7DD3D54895BF1BE61EC06EA`.
- Final `error.log`: 11,545,566 bytes / 100,002 lines; SHA-256
  `56C246625D7D10E54A65ECAFCFA344B1A73E53197D5BF713D998144AE04243FA`.
- Crash/bookmark: **pass**.
- David `9000222` has Ben David: **pass**, log and visible tooltip.
- Elijah `9000220` has Kohen: **pass**, log and visible tooltip.
- Name-list and succession-score errors: **none observed**.
- Clean error log and Ben David icon: **fail**.

No repository file other than this test log was added or changed by the live-test session, and no
commit was made.

## Corrected rerun — 22:40

After removing the conflicting `genetic` declarations and adding the dedicated
`gfx/interface/icons/traits/ben_david.dds` asset, the same focused test was repeated from a fresh
isolated process.

### Isolation and boot

- PID `7748`, the unrelated launcher-owned CK3 instance, was present before and after the run with
  the same command line. It was not focused, moved, sent input, or stopped.
- The exact isolated process was PID `18284`, started at 22:39:58 with
  `-debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`.
- Only PID `18284` was moved to non-primary `DISPLAY5` and controlled.
- `debug.log` reached `End loading of history` at 22:40:57, the process remained responsive, and
  the 1066 selector rendered normally, including `The Kehillah of Worms`.
- Bookmark screenshot SHA-256:
  `550858A48CBEF47EA02C3C95BBE8EF47E6B42306FA5EB937747E9EBC6662336D`.

### Trait checks

The hidden holder-scope probes again resolved the expected runtime characters and traits:

```text
kehillah_patronym_debug.1: BEN/BAT DAVID
Root: David of the House of David of d_kehillah_baghdad
      (Internal ID: 31919 - Historical ID 9000222)

kehillah_patronym_debug.1: KOHEN
Root: Elijah ha-Kohen of d_kehillah_jerusalem
      (Internal ID: 29853 - Historical ID 9000220)
```

David's character panel showed a proper colored Ben David icon rather than the earlier `?`
fallback. Hovering it displayed the localized **Ben David** tooltip, and the error-log line count
was 499 both immediately before and after the hover: zero delta. Screenshot SHA-256:
`7ABEC2E8E73BF162842354B06310E5A45E47190D12EB1D247345A6D24C6923C2`.

Elijah's character panel again displayed the **Kohen** tooltip and icon. Screenshot SHA-256:
`A7C4E63831C7F4A23ED756AA6DD6DBFB8529C4E9E4327907F5CB295F8D5D75BA`.

### Corrected log result

Targeted searches of the final fresh `error.log` returned zero matches for:

- `sayyid.dds` or `ben_david.dds` localization/data errors;
- `ben_david` trait errors;
- `Trait kohen is both set as genetic and has an inheritance chance`;
- `Trait levite is both set as genetic and has an inheritance chance`;
- the changed trait, name-list, or succession-score files/tokens.

One unrelated Baghdad start-setup `set_employer` report names David's historical ID `9000222`
because it attempts to place Natan in David's court when he is already there. It does not mention
or evaluate the lineage traits and is outside this correction's targeted errors.

Final evidence:

- `debug.log`: SHA-256
  `083F7B51D05F5DB095A002FF665FEF773C75A23055DB9707DA839937AA8F7A21`.
- `error.log`: 82,707 bytes / 499 lines; SHA-256
  `9B27AB33D0C52B7A85B398C8674A35FD1B6571362497F7784D69FA4C61A6D628`.
- Stopped only PID `18284`; PID `7748` remained running.

The corrected rerun passes all four requested checks. No commit was made.
