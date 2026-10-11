**Status:** Live probe session, 2026-10-10 ~23:30 (interactive, not a heartbeat). Fix shipped as
`kehillah_laicize_character_effect` / `kehillah_laicize_court_effect`. The probes ran against the
game already open, which still had the old script loaded. They proved the mechanism. The shipped
effect itself has not yet run in a fresh boot.

# Lay Kehillah courtiers showing as "Jewish Clergy"

## Report

Daniel, playing: many characters show as "Jewish Clergy" who shouldn't — Parnasim, and female
courtiers of Kehillot. "Jewish Clergy" is vanilla's faith-organization name
(`FAITH_ORGANIZATION_NAME`, `organizations_l_english.yml`). For a non-ruler, `is_clergy` reads
organization membership.

## Who is clergy, and why

Engine sources of clergy status: theocratic rulers (`mechanic_type = theocracy`, "Should rulers be
considered clergy"), `clergy = yes` traits (vanilla: `devoted`, `cleric`; mod: `kehillah_rabbi_trait`),
and `is_clergy_position` council seats (the Kehillah's Dayyan seat, `councillor_court_chaplain`).

Probe 1 (`run/clergy_probe.txt`): every living Jewish clergy character, classified.

| Class | Count |
|---|---|
| Kehillah rulers | 15 |
| Non-ruler, Dayyan seat | 16 |
| Non-ruler, devoted | 1 |
| Non-ruler, **no clerical role** | 81 (55 male, 26 female), all courtiers, 76 in Kehillah courts |

Probe 2/3: in Kehillah courts, 91 of 266 courtiers are clergy. Under **vanilla** theocratic rulers
it is 881 of 1,055, including 28 consorts. All of them are organization members. Unmarried adults
appear on both sides, so no simple court rule explains the split. The likeliest reading is that the
engine generates characters for a theocratic court as organization members, the way a bishop's
court fills with priests. The Kehillah inherited this when H1 (2026-10-09) gave it
`mechanic_type = theocracy`.

## Can it be undone?

Probe 4: `leave_organization` on the 76 unexplained Kehillah courtiers → **76/76 lay
immediately**. Probe 5, after unpausing ~25 s real time (game days passed — engine log activity
resumed): **76/76 still lay**, and **no new** unexplained clergy courtiers. So unlike a ruler, the
engine does not re-sync a courtier back into the organization.

## Fix

`kehillah_laicize_character_effect` (`common/scripted_effects/kehillah_scripted_effects.txt`)
does `leave_organization` on any non-ruler that has no clerical role (Rabbi trait, `devoted`,
`cleric`, or the Dayyan seat). It is called from two places:

- `kehillah_on_join_court`, on each arrival;
- `kehillah_quarterly_pulse`, via `kehillah_laicize_court_effect`, as a backstop sweep that also
  cleans every court at game start (the pulse first fires 1066.9.16).

## Not changed: Parnasim

A lay Parnas leader is still clergy. That is H1's player-heir continuation: without organization
membership a dying leader whose appointee is from another dynasty gives Game Over. Removing it
needs a different continuation mechanism. Recorded in ROADMAP as an open design question.

## Still to verify

After a fresh boot with this build, run one quarter and re-run `clergy_probe.txt`. Expected: the
"UNEXPLAINED" lines are gone from Kehillah courts, and the Dayyan, rabbi and ruler counts are
unchanged. Also confirm H1 still holds (`kehillah_household_debug.8` on the leader).
