# Succession console run book

**Status: ready to run.** Updated 2026-09-27 for the successor Jewish
Quarter provision fix (`7c45233`). This is a human-facing companion to
the [successor Quarter live-test log](2026-09-27-successor-quarter-live-test-log.md).

Use a fresh **1066 Kehillah of Worms** game launched with `-debug_mode`.
The commands below are entered in CK3's console (the `~` key). Save before
each route: both deliberately change the player character, and the death
route cannot be undone within the save.

The two files to inspect are:

- `C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\logs\debug.log`
- `C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\logs\error.log`

`debug.log` is buffered: wait a couple of seconds after advancing time before
looking for a line. Record the `error.log` line count before the test; a new
`Trying to set illegal government`, `change_government`, or
`kehillah_succession` error is a failure even if the UI appears normal.

## A. Production regression: ordinary appointment succession

This is the priority check. It exercises the actual death/appointment path,
not the voluntary departure shortcut.

1. After the Worms game has loaded, enter these commands as Isaac HaLevi:

   ```text
   event kehillah_debug.104
   event kehillah_debug.111
   ```

   `.104` arms a one-use title-gain trace. `.111` records the starting
   Quarter: synagogue level 5 plus all eight other Worms structures.

2. Right-click Isaac's portrait, then choose:

   ```text
   DEBUG: Main → Slay Character! → No Killer → confirm
   ```

   Do not use a `die` run-file effect: it is not a CK3 script effect.

3. Continue as the successor when CK3 offers the continuation. Unpause and
   let **three game days** pass, so the deferred handoff event can run.

4. As the new player character, enter:

   ```text
   event kehillah_debug.111
   event kehillah_debug.105
   ```

5. In `debug.log`, find the block beginning
   `kehillah_succession.0010:`. The required lines are:

   ```text
   created the temporary Kehillah scaffold
   PASS a domicile exists after provisioning
   PASS successor has Kehillah government after provisioning
   PASS the real community title is primary after cleanup
   restored the recorded Quarter and refreshed the host charter
   ```

   The two `.111` blocks should both say `SYNAGOGUE 5` and report each other
   Worms building as `PRESENT`. There must be no `.0010: FAIL` line and no
   new relevant line in `error.log`.

## B. Voluntary departure: community handoff regression

This repeats the route that has already passed once, but is a convenient
quick smoke test and confirms that the departing player gets an adventurer
camp while the community continues under the successor.

1. In a fresh Worms save, enter:

   ```text
   event kehillah_debug.112
   event kehillah_debug.111
   ```

2. Press **F8**, find **Step Down and Take to the Road**, and take the real
decision. Do not fire a succession event manually.

3. Unpause for three game days. You are now controlling the departing
adventurer. Enter:

   ```text
   event kehillah_debug.100
   event kehillah_debug.113
   ```

4. Read the log. `.100` should report only its six `PASS` states. `.113`
should report all of:

   ```text
   TITLE EXISTS
   HOLDER EXISTS
   HOLDER IS NOT ROOT
   HOLDER IS A KEHILLAH
   PASS the new holder has a domicile
   pillar variables still present on the title
   ```

   The same `.0010` success lines and clean `error.log` requirement from
route A apply here too.

## C. Check the successor's Quarter after voluntary departure

After step-down, the player is the departing adventurer, so `.111` would
inspect the camp rather than the successor's Quarter. Create this temporary
run file once, saved as **UTF-8 with BOM**:

`C:\Users\Daniel\Documents\Paradox Interactive\Crusader Kings III\run\kehillah_successor_buildings.txt`

```text
global_var:kehillah_debug_watched_community = {
    holder = {
        trigger_event = kehillah_debug.111
    }
}
```

Then, after step 3 of route B, enter:

```text
run kehillah_successor_buildings.txt
```

It fires the read-only building probe on the watched community's current
holder. Compare that `.111` block to the pre-step-down one. For the developed
Worms start, parity means synagogue 5 and the same eight `PRESENT` results.

For a community with custom later improvements, also open the Jewish Quarter
before and after the succession and compare every visible building tier. The
current probe is deliberately exact for the developed Worms synagogue and
presence/absence for the other eight tracks; it does not yet print every
possible tier on every track.

## What to report if it fails

Send the relevant `debug.log` block starting at either
`kehillah_titlegain_trace:` or `kehillah_succession.0010:`, plus the new
`error.log` lines. Include whether this was route A or B, how many days you
unpaused, and whether CK3 offered continuation as the successor.
