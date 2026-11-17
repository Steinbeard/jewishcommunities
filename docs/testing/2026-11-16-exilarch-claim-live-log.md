**Status: Isolated 1066 direct transfer, save/reload, and actual decision UI passed 2026-11-16.**

# David's Exilarchate: first live check

Luna alone performed this test, following `AGENTS.md` and the isolated
CK3 guide. It inspected CK3 ownership first: no process was running. It
launched the new worktree with
`scripts/kehillah_isolated_ck3_test.ps1 -Visible`, confirmed its owned PID
33588 used `-userdir=C:/Users/Daniel/.codex/ck3-test/festival-observance`,
and did not touch any other game instance. The PID stayed alive through
content and bookmark database initialization. The isolated debug log
reported the `kehillah_exilarch_debug` namespace and two events loaded
from `events/kehillah_exilarch_debug_events.txt` (lines 2929 and 2931).

The xTiger CK3 MCP game tools were unavailable to the Luna tester. It did
not enter a campaign, take screenshots, send UI input, or fire the console
events. David's character links and friendship, Isaac's Dayyan post, the
three communities, the petition requirements, title transfer, government,
quarter, player continuation, and save/reload are therefore **unverified**.
The isolated `error.log` was not clean: it included duplicate localization
keys, GUI/custom localization errors such as `Unexpected token: always` in
`kehillah_crisis_action_advice_custom_loc.txt:18`, a missing activity
localization key, and BOM warnings. These were not attributed to the new
Exilarch files by the available log review; no claim of a clean live run is
made. A follow-up Luna run should compare against this boot's errors.

The tester rechecked PID ownership, stopped only PID 33588, and confirmed
that no CK3 processes remained. No screenshot was taken.

## Second session: fresh 1066 campaign and direct transfer probe

Luna relaunched an isolated game as PID 16508. In the 1066 selector it
identified the only David ben Hezekiah at Granada: historical ID 9001102,
internal ID 34176. It began a fresh campaign, switched to that character
with `play 34176`, and confirmed the root with a `whoami` run-file probe.
The hidden event `.1` logged the before state, and `.2` invoked the same
`kehillah_press_exilarch_claim_effect` as the decision. Afterward the
log probe confirmed:

- `d_kehillah_baghdad` belongs to David and is his primary title;
- `d_kehillah_exilarchate` also belongs to David;
- he has `kehillah_government` and no longer holds his House of Hezekiah camp title;
- Baghdad's court chaplain/Dayyan is Yitzhak Ibn Sakri, historical ID 9003160;
- Sura is still Sherira's and Pumbedita is still Natan's, separate from Baghdad.

The startup log exposed an invalid Dynasty_house scope in
`kehillah_roster_seat_effect`, called while placing Baghdad steward Ibn
Fadlan. His new record had no dynasty, although the roster effect sets
a household variable. The local code now gives him dynasty 9000102;
this fix and David's post-transfer domicile still need a fresh probe.
The general script analyzer added repeated non-feature diagnostics to
`error.log` on each event invocation; corrected feature probes added no
Exilarch-specific error. Two invalid-scope errors came from an initial
malformed manual probe and were not reproduced when it was corrected.
Luna stopped only its owned isolated PID 16508 and confirmed no CK3 process
remained.

## Third session: corrected startup, Quarter and save/reload

Luna launched the corrected worktree in a new isolated PID 4072. It again
mapped David's history ID 9001102 to internal ID 34176, switched to him
and fired the direct transfer probe. Post-transfer script checks confirmed
David held Baghdad as primary title and the Exilarchate, had
`kehillah_government`, no longer held his former camp title, and owned a
domicile with type `kehillah_quarter` (object ID 450). The startup
`error.log` contained no `kehillah_roster_seat_effect` or invalid
Dynasty_house error after Ibn Fadlan received a dynasty.

The tester saved `exilarch_final_luna.ck3` (about 104 MB) and reloaded it
through the game's Load Game panel. The save entry showed Exilarch David
II of the Kehillah of Baghdad. A post-load probe still found David as
the player/root with Baghdad primary, Kehillah government, his former
camp absent, and a `kehillah_quarter` domicile. The original decision
source loaded in this process had an unset `ai_check_interval` error;
source now sets it to 24, but that last edit was not loaded by this game
instance. The `.1`/`.2` debug events are deliberately console-only and
are expected to be reported orphaned.

Luna rechecked and stopped only its isolated PID 4072; no CK3 process
remained. This test proves the scripted transfer path and persistence,
but it bypassed the decision's travel, opinion, cost, and UI gates.

## Fourth session: actual decision UI and requirements

Luna booted a fresh isolated 1066 game under PID 3276, confirmed David's
history ID 9001102 and internal ID 34176, entered a disposable campaign,
and switched to David. David's camp
`court_position:kehillah_adventurer_dayyan_position` resolved to Isaac ibn
Sakri (history ID 9003160). Baghdad's caretaker Ezra had a different
court chaplain, Shaul Bar Sheshna.

`Press the Claim to the Exilarchate` appeared under Major Decisions.
David passed the adult, free, peace, adventurer and title requirements;
Baghdad's leader and the host ruler met both opinion thresholds, and David
had the required 100 gold and 150 prestige. The only initial failing
requirement was David's location outside `c_baghdad`. In this disposable
game, the tester set his location with
`set_location = { location = title:c_baghdad.title_province stick_to_location = yes }`.
The location gate then passed, the decision enabled, and its confirmation
modal showed the requirements checked. The tester confirmed the actual UI
decision; CK3 logged the transfer effect marker at 12:57:39.

After the click, a script probe found David held Baghdad and the separate
Exilarchate, Baghdad was primary, his government was Kehillah, his old camp
title was gone, and his Baghdad domicile was a `kehillah_quarter`. Isaac was
Baghdad's Dayyan. The UI top bar showed gold 256 → 156 and prestige
900 → 750, exactly the decision costs. The fresh boot did not reproduce
the earlier `ai_check_interval` or Ibn Fadlan Dynasty_house errors; the
decision created no new Exilarch-specific error. The log contained expected
orphaned console-only debug event warnings and one invalid manual probe
scope from a failed first location command, corrected before the decision.
Luna stopped only PID 3276 and confirmed it was gone.

The save/reload check in the third session used the identical scripted
effect through the debug event. The fourth session establishes that the
normal player-facing decision reaches that effect with its gates and costs.
