**Status:** BUILT 2026-11-11 at Daniel's request; source checked and xTiger
baseline unchanged. Live validation is pending: this session cannot inspect
CK3 process ownership through CIM and has no exposed xTiger game tools.

# Communal departure, realm headship and teshuvah

This addendum supersedes the two-option leadership response and the separate-only
teshuvah entry in the [cherem build record](../spec/2026-11-11-reviews-and-cherem.md).
It also corrects office forfeiture in the [Nagid build](2026-10-30-nagid-build.md).
The existing appointment-succession and adventurer-creation mechanisms are unchanged.

## Realm headship follows communal leadership

Daniel reported that a leader who resigned under cherem became an adventurer but
remained the realm's Head of the Jews and its vizier. The eligibility rule already
required Kehillah government, but the quarterly on-action also required that
government, preventing the cleanup from ever running on the departed character.

- `kehillah_departure_prepare_effect` now invokes the existing
  `kehillah_nagid_step_down_effect` before transferring or destroying the community.
  This removes the headship modifier and rank, court relations, personal service
  modifiers, the patron link, the matching realm holder/service entries and the
  ruler's service bonuses. The institution remains vacant, ready for confirmation
  of the new seat leader; the appointment does not pass automatically to the heir.
- The same cleanup covers voluntary resignation, cherem, conversion, arrest and
  dissolution when they use the shared departure path.
- Engine-driven community-title losses schedule a guarded cleanup one day later,
  after the title transaction, through `on_title_lost` and `kehillah_nagid.0080`.
  The installed vanilla `title_on_actions.txt` documents root as the former holder
  and `scope:title` as the lost title.
- Quarterly checks now include anyone with the headship modifier or patron link,
  including adventurers from existing saves. Affected playable characters are
  repaired at their next quarterly pulse. Missing-title/domicile checks are guarded;
  an adventurer's camp is not recorded as the community in realm news.
- Departure clears the old leader's title-level defiance marker so the heir does
  not inherit the departing leader's unresolved discipline.

## Teshuvah before resignation

*The Ban Is Read* now offers **Let me do teshuvah and seek reconciliation** as
its first option, alongside resignation and defiance. An unavailable option stays
visible with its requirements.

- Uses the existing cost of **200 Piety**, stress and book-renunciation effects,
  **365 days** of penance and **five-year** retry cooldown.
- The event and the separate *Do Teshuvah* decision call one shared start effect.
  A shared character cooldown also prevents switching between the two doors to
  bypass the waiting period; the existing native decision cooldown is respected.
- A leader may retain communal leadership and an otherwise eligible realm headship
  while penance is pending. There is no immediate -20 Stability defiance penalty;
  the quarterly discipline cost is **-1 Stability**, rather than defiance's **-6**.
  These are the discipline effects alone; ordinary community changes still apply.
- A persistent pending marker lasts until the verdict, including a player judge
  who answers after the temporary penance modifier expires. It prevents duplicate
  applications and suppresses another leadership ultimatum during the penance.
- Acceptance removes the ban, score, stage modifiers, pending state, penance
  modifier and title's defiance marker. The retry cooldown remains.
- Refusal ends the grace period and schedules *The Ban Is Read* again for a leader
  still under cherem. The player chooses resignation or defiance; a failed roll
  does not abdicate on the player's behalf. The cooldown prevents an immediate retry.
- A queued cherem resignation rechecks that the character is still a banned leader
  before stepping down; if the ban has been lifted, it does nothing.

## Validation and repeatable checks

The pre-edit and final xTiger results are identical: 0 fatal, 16 errors,
108 warnings, 38 untidy and 44 tips. There are no new findings in the changed feature files. Existing unrelated
shared-worktree changes have been preserved. The Luna tester confirmed that live
tests are **UNRUN** because no xTiger tools are exposed and CIM process-ownership
inspection is blocked; no game was launched or controlled.

Git staging was attempted but failed because `.git/index.lock` cannot be created
(permission denied); these changes could not be committed, pushed or published
as a PR from this session. The repository-wide whitespace check also finds an
unrelated pre-existing trailing-whitespace line in `gui/window_domicile.gui:854`;
it was left untouched.

New console-only probes are in `events/kehillah_leadership_discipline_debug_events.txt`:

| Console event | Purpose |
| --- | --- |
| `event kehillah_leadership_discipline_debug.1` | Read-only leadership, headship links, court relations and penance report. |
| `event kehillah_leadership_discipline_debug.2` | Force refusal of an active penance. |
| `event kehillah_leadership_discipline_debug.3` | Force acceptance of an active penance. |
| `event kehillah_leadership_discipline_debug.4` | Run the guarded invalid-office repair on the current character. |
| `event kehillah_leadership_discipline_debug.5` | Apply one discipline quarter and log Stability before/after. |

Pending live checks, using a disposable Granada 1066 save after the day-five
Nagid setup and with sufficient Piety:

1. Fire `event kehillah_cherem_debug.3`. Choose teshuvah. Verify 200 Piety paid
   once, the same leader and headship remain, no immediate -20 Stability, and the
   separate decision is unavailable. Probe `.5` above should subtract 1 Stability.
2. Force acceptance with discipline debug `.3`: verify the trait, penance and pending
   marker are gone and another `.5` subtracts no discipline Stability. Separately
   let the full year elapse to verify the ordinary AI/court verdict path.
3. Reload, begin penance and force refusal with `.2`. Advance a day: the ban event
   returns, teshuvah is unavailable on cooldown, and there is no automatic resignation.
   Choose defiance and verify its immediate -20 and subsequent -6 quarterly penalty.
   Also verify a player head of rite can accept/refuse the scheduled judgment.
4. Reload and choose resignation. Confirm the heir holds the community, the former
   leader has a playable camp for at least 30 days, and neither the old leader nor
   Badis retains the headship/service modifiers or court relation. The office itself
   should remain. The new leader must be confirmed before holding it.
5. Load an affected adventurer save and run discipline debug `.4`, or wait for the
   next quarterly pulse. Confirm the stale appointment and service disappear. Test
   an engine-driven community-title loss separately to exercise the deferred hook.
   Check the owned test profile's error log against its boot baseline after UI use.
