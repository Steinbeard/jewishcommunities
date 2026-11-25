**Status:** BUILT 2026-11-25; xTiger clean, not live-tested. Adds a top-bar notice alongside the
library's foundation alert ([shelf and ledger](2026-11-08-library-shelf-and-ledger.md)).

# Missing Foundational Works notice

Daniel asked for a top-bar notice when a Kehillah leader's library is missing foundational works
and no sefer is being acquired.

**When it shows** (`action_kehillah_library_missing_foundations`,
`common/important_actions/kehillah_library_foundation_actions.txt`): a human Kehillah leader, adult
and free, whose primary title has `kehillah_lib_foundational_missing_count_value > 0` and no
`kehillah_library_commission_work` list. That count is the same one that already costs
Greatness (`kehillah_bd_foundational_works_value`): works that circulate by now and stand at
Foundational or higher in the leader's rite. The description gives the count.

**What a click does.** It opens the library window on the community's own shelf, where the
foundational centrepiece and its alert name the missing works and each can be sought. An
important action's effect cannot set GUI variables, and the library window opens only through
them. So the effect sets a one-day `var:kehillah_lib_open_request` on the player. A new
zero-size scripted widget, `gui/kehillah_library_opener.gui`, shows while that variable exists.
Its `_show` runs scripted GUI `kehillah_lib_open_request_consume`, which clears the request and
points `kehillah_lib_view_owner` and `kehillah_lib_view_title` at the player's library. It then
clears the window's selections, lays out the shelf, and opens the window, the same steps as the
Libraries map click. Clearing the variable hides the widget again, so the next click fires again.
Other script can reuse this to open the library.

**Live checks still needed** (the new widget needs a game restart to load):
- the notice appears for a leader missing a foundational work, with the right count;
- one click opens the library on the community's shelf, and a second click after closing it
  opens it again;
- the notice clears once a commission starts and stays away until it ends;
- `error.log` shows no new lines from the opener.
