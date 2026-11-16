**Status: Partial isolated boot 2026-11-16; 1066 play and claim transfer unrun.**

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

## Next probe

With xTiger CK3 tools available, start the 1066 bookmark as David, log
`kehillah_exilarch_debug.1`, travel to Baghdad and satisfy the two opinion
gates, take the actual decision, then log `.1` again. In an isolated test
save, `.2` may bypass the gates to test the engine transfer directly.
Confirm David holds `d_kehillah_baghdad` and `d_kehillah_exilarchate` with
`kehillah_government`, has a Quarter and no old camp, and has Isaac in the
Dayyan council position. Check the old Baghdad caretaker and both separate
Sura/Pumbedita titles. Compare `error.log` with this boot, save, reload,
and confirm the title and government persist.
