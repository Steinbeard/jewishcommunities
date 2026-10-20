# Auxerre Kehillah live test — 2026-10-18

**Status: Corrected rerun passed. A fresh isolated boot reached the 1066 selector, `kehillah_debug.135` returned all eight required PASS results, and the fresh error log contained neither the former Auxerre UTF-8 BOM warning nor another new Auxerre history/setup error. The earlier failed result is retained below as superseded evidence.**

## Method and isolation

- Tested branch `codex/auxerre-kehillah` in
  `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities`.
- An unrelated launcher-owned CK3 process was already running as PID `7748`. It had no isolated
  `-userdir` marker and was not focused, moved, sent input, or stopped.
- Launched `scripts/kehillah_isolated_ck3_test.ps1 -Visible`. The exact test process was PID
  `26572`, started at 22:50:39 with:

  ```text
  ck3.exe -debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance
  ```

- Moved and controlled only PID `26572` on non-primary `DISPLAY5` (`2560,0`, `2048x1152`).
  Navigation used PID-owned focus plus `SetCursorPos` on the VDD.
- Loaded a normal 1066 Kehillah start so game-start effects ran, then fired the hidden console-only
  probe `event kehillah_debug.135`.
- Stopped only PID `26572`. PID `7748` remained running with its original command line.

## Boot and bookmark

The isolated process remained responsive and `debug.log` reached:

```text
[22:51:15][D][history.cpp:1543]: End loading of history
```

The 1066 selector rendered normally, including `The Kehillah of Worms`. Screenshot SHA-256:
`CB203772BB8533615CA40C731FFE83AC28DFAF4CE22F9BA2AA0AC08733509AD2`.

## `kehillah_debug.135`

The first probe run at 22:53:11 reported:

```text
kehillah_debug.135: Auxerre start -- START
kehillah_debug.135: HOLDER PASS
kehillah_debug.135: YEHUDA PASS
kehillah_debug.135: REGISTRY PASS
kehillah_debug.135: WESTERN ASHKENAZ PASS
kehillah_debug.135: GOVERNMENT PASS
kehillah_debug.135: DOMICILE PASS
kehillah_debug.135: LOCATION PASS
kehillah_debug.135: HOST CHARTER FAIL
kehillah_debug.135: Auxerre start -- END
```

After switching play to Auxerre's holder, the same probe was fired again at 22:54:35. It returned
the same seven PASS results and the same `HOST CHARTER FAIL`, so the failure was reproducible and
not dependent on the original Worms player scope.

The required holder, historical character `9000225`, registry membership, Western Ashkenaz
minhag, Kehillah government, domicile, and `c_auxerre` location therefore pass. The required host
charter does not.

## Visual title and holder check

A title-holder scope dump resolved:

```text
Yehuda Frankfurter of d_kehillah_auxerre
(Internal ID: 34290 - Historical ID 9000225)
```

After switching to internal ID `34290`, the character panel visibly showed:

- `Rav Yehuda of Kehillah of Auxerre`;
- the localized title card `Kehillah of Auxerre`;
- Ashkenazi culture and Rabbinic rite; and
- a functioning **Rabbi** trait icon and full localized Rabbi tooltip.

Panel screenshot SHA-256:
`4D53949D421308EEB8567D067AFE111EB08F74E53DCC11E248D1AACE42F5A3A5`.
Rabbi-tooltip screenshot SHA-256:
`D0152BB624C3D669C443B07614CD12F3F805BE386374896B4E76914389221227`.

## Error-log comparison

The final fresh `error.log` contained two target-string matches:

```text
Event kehillah_debug.135 is orphaned
File 'history/characters/auxerre_1066.txt' should be in utf8-bom encoding
```

The orphan notice is the existing engine behavior for the entire console-only debug namespace in
this file: the same fresh log reports every `kehillah_debug` probe from `.1` through `.135` as
orphaned. It is not specific to Auxerre's implementation logic, though the new `.135` naturally
joins that baseline class.

The UTF-8 BOM notice is new and attributable to `auxerre_1066.txt`; the engine continued to read
the file, as the successful holder and visual checks demonstrate. No error-log line named
`9000225` or `kehillah_setup_auxerre_start_effect`, and no other line named Auxerre.

Final logs:

- `debug.log` SHA-256:
  `3FA87ED5E01E1AFDA1C2994F86506B2A8E8BF660532ABB482560CB790585B2D1`.
- `error.log`: 73,352 bytes / 455 lines; SHA-256
  `BBD51A25F9A654CA6BDBFA3376487E1392F824D176A328E73203967D77A5AEAA`.

## Initial-run verdict (superseded)

- Fresh boot / 1066 selector: **PASS**.
- Holder, Yehuda, registry, minhag, government, domicile, location: **PASS**.
- Host charter: **FAIL**, reproduced twice.
- Localized title, Yehuda, Rabbi presentation: **PASS**.
- Targeted error-log comparison: **FAIL** for the actionable Auxerre character-file encoding
  notice; `.135`'s orphan notice matches the pre-existing console-only debug baseline.

Initial result: **FAIL** pending the host-charter probe correction and UTF-8 BOM correction. This
result was superseded by the corrected rerun below. No commit was made.

## Corrected isolated rerun — 2026-10-19

The corrected branch was rerun from a fresh isolated launch after the probe was expanded to accept
all three supported host-charter groups and `history/characters/auxerre_1066.txt` was saved with an
`EF BB BF` UTF-8 BOM.

- Branch/worktree: `codex/auxerre-kehillah` at
  `C:\Users\Daniel\.codex\worktrees\jewish-festival-observance\jewishcommunities`.
- The pre-existing, non-isolated launcher process remained PID `7748`; its command line had no
  isolated `-userdir` marker. It was not focused, moved, sent input, or stopped.
- `scripts/kehillah_isolated_ck3_test.ps1 -Visible` launched only PID `10264` with:

  ```text
  ck3.exe -debug_mode -develop -gdpr-compliant -userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance
  ```

- Only PID `10264` was moved to and controlled on non-primary `DISPLAY5` (`2560,0`,
  `2048x1152`). After the check, only PID `10264` was stopped. PID `7748` was rechecked and
  remained alive with its original launcher command line.

### Corrected boot and probe evidence

The new `debug.log` reached the end of history loading at 01:23:48, and the 1066 selector rendered
normally. The selector screenshot SHA-256 is
`7450C87AB56CCB0FFD51A21A97CB14592280ADBE6BC4C8B215AE9E47532ACED3`.

After loading a normal 1066 Kehillah start, `event kehillah_debug.135` produced at 01:28:02:

```text
kehillah_debug.135: Auxerre start -- START
kehillah_debug.135: HOLDER PASS
kehillah_debug.135: YEHUDA PASS
kehillah_debug.135: REGISTRY PASS
kehillah_debug.135: WESTERN ASHKENAZ PASS
kehillah_debug.135: GOVERNMENT PASS
kehillah_debug.135: DOMICILE PASS
kehillah_debug.135: LOCATION PASS
kehillah_debug.135: HOST CHARTER PASS
kehillah_debug.135: Auxerre start -- END
```

Thus the holder, Yehuda `9000225`, registry, Western Ashkenaz minhag, Kehillah government,
domicile, `c_auxerre` location, and supported host charter all passed in the corrected run.

### Corrected error-log evidence

The fresh 64,169-byte / 413-line `error.log` contained no
`auxerre_1066.txt should be in utf8-bom encoding` warning (zero matches). A targeted search for
`auxerre`, `9000225`, `setup_auxerre`, `kehillah_debug.135`, and `debug.135` returned only:

```text
[01:23:43][E][jomini_eventmanager.cpp:368]: Event kehillah_debug.135 is orphaned
```

As established in the initial run, this is the common baseline notice for the console-only debug
namespace rather than an Auxerre history/setup failure. There were no matches naming `9000225`,
the Auxerre setup effect, or the Auxerre character-history file, and no other new relevant
Auxerre history error.

Final corrected-run artifacts:

- `debug.log`: 1,190,341 bytes / 10,146 lines; SHA-256
  `260C345EFF7C29383D0252C69A69E657FE36824A2F7459FBE0D9B9FA4DF4C5D7`.
- `error.log`: 64,169 bytes / 413 lines; SHA-256
  `277357A77DD118F1B648404D927D8FB36A487F73FEFB21CD55025639DCB5FBEF`.
- 1066 selector screenshot: 1,345,622 bytes; SHA-256
  `7450C87AB56CCB0FFD51A21A97CB14592280ADBE6BC4C8B215AE9E47532ACED3`.

## Final verdict

- Fresh isolated boot / 1066 selector: **PASS**.
- All eight `kehillah_debug.135` assertions: **PASS**.
- Auxerre UTF-8 BOM warning absent: **PASS**.
- Targeted fresh error-log comparison: **PASS**; only the established console-debug orphan
  baseline remained.
- Process isolation: **PASS**; exact test PID `10264` was stopped and unrelated PID `7748` was
  preserved.

Overall corrected result: **PASS**. No commit was made.
