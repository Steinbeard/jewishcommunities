# The Bet Din overdue, no hosting in a crisis, and the Bet Din's Piety cost

**Status: Implemented 2026-11-08 at Daniel's request. xTiger-clean on every touched file; not live-tested.**
Adds to the Bet Din conference ([v5](v5-bet-din-conference.md)) and the Stability baseline
(`kehillah_stability_baseline_value`). Supersedes nothing.

## 1. A long gap without a Bet Din lowers Stability

- **Clock:** `var:kehillah_bet_din_last_year` on the community title. The conference's
  `on_complete` (host only) sets it to the current year. The quarterly
  `kehillah_bet_din_overdue_pulse` starts it at the current year for any community that has none,
  so a new game, an old save or a newly founded community gets the full grace period.
  Only the community's **own** sitting counts. Attending someone else's court does not reset it.
- **Penalty** (`kehillah_bd_bet_din_overdue_value`, a Stability baseline term): once 5 years have
  passed without a sitting, -20, then -10 for each further year, to at most -60. All numbers are in
  `common/script_values/kehillah_bet_din_overdue_values.txt`. The Stability tooltip shows it as
  "No Bet Din for N years".
- **Not applied** while a crisis is on (hosting is forbidden then, see section 2), while the
  region cannot seat a panel, or while the leader's own sitting is under way. A missing rabbi is
  **not** an excuse: finding one is the leader's job.
- Year granularity: the gap is counted in whole calendar years, so it can start up to a year early or late.

## 2. Notifications

- **Alert:** "The Bet Din Is Overdue" (`action_kehillah_bet_din_overdue`) shows while the penalty
  applies. A click opens the activity planner on the Bet Din. It replaces the ordinary "Cases
  Await the Bet Din" suggestion in that time.
- **Message:** once, when the penalty first applies (`msg_kehillah_bet_din_overdue`). It is sent
  again only after the penalty has lifted and returned.

## 3. No hosting during a crisis

`kehillah_no_crisis_blocks_hosting_trigger` (false while `kehillah_trouble_crisis_active_trigger`
holds on the title) now gates:

- the Bet Din conference (planner, Convene decision, suggestion, AI);
- the Yeshiva Visit (planner and the Library's plan button).

**Vanilla activities: called off, not blocked.** These include Hunt, Pilgrimage, University Visit
and others a Kehillah leader can see. CK3 has no shared "may host" hook and no "activity started"
on_action, so they cannot be refused at planning without overriding each vanilla file. Daniel
chose cancellation instead, like a coronation called off by vanilla's `is_valid`.

- A hidden weekly check runs on every Kehillah leader: `kehillah_crisis_hosting.0001`, in
  `events/kehillah_crisis_hosting_events.txt`. The quarterly
  `kehillah_bet_din_overdue_pulse` starts it, and starts it again for a new leader.
- While a crisis is on, the check calls off any activity the leader **hosts** that is not yet in
  its active phase, i.e. guests still gathering or the host still travelling. It uses
  `invalidate_activity`, so the activity's own `on_invalidated` runs. The player gets a "Plans
  Called Off" message.
- This applies to the mod's own Bet Din and Yeshiva Visit too, when a crisis begins after they were
  planned.
- A gathering already in its active phase is left to finish.
- Costs already paid, including the Bet Din's Piety, are not refunded. Vanilla does not refund either.
- A vanilla activity planned in a crisis can run for up to a week before it is called off.

## 4. Piety cost

Convening the Bet Din now costs 100 Piety (`kehillah_bet_din_host_piety_cost`, vanilla's
`medium_piety_value`), paid when the sitting is planned. A strong session pays back 250, an
adequate one 50, a failed one nothing. **Soak-test item:** AI leaders with less than 100 Piety
cannot convene. They will then sit less often and take the overdue penalty. Lower the cost for
AI if that shows up.

## Test checklist (live)

1. Boot to `bm_1066_kehillah_worms`, play `d_kehillah_worms`. The Stability tooltip has no Bet Din
   line, and there is no overdue alert.
2. Console: `effect title:d_kehillah_worms = { set_variable = { name = kehillah_bet_din_last_year value = 1060 } }`.
   Hover Stability. Expected: "No Bet Din for 6 years: -30". The alert "The Bet Din Is Overdue" is
   in the top bar, and the plain suggestion is gone.
3. Wait for the next quarter. The "Bet Din Is Overdue" message appears once and does not repeat
   next quarter.
4. Click the alert. The planner opens on the Bet Din, and the cost shows 100 Piety. With less than
   100 Piety, the planner refuses.
5. Hold a sitting to completion. The tooltip line and alert are gone, and
   `title:d_kehillah_worms.var:kehillah_bet_din_last_year` equals the current year.
6. Start a crisis (`event kehillah_crisis.<intro>` or the safety debug events), then open the
   planner. The Bet Din and Yeshiva Visit show "The community is not in crisis" as failed. The
   Convene decision is invalid, and the Library's travel button is disabled. With the clock set
   back as in step 2, no overdue line appears during the crisis.
7. Outside a crisis, plan a Hunt or Pilgrimage, then start a crisis before guests arrive. Within a
   week, a "Plans Called Off" message names the activity, and it is gone from the activity list.
   Check that the host is not left stranded, especially on a Pilgrimage cancelled mid-journey.
   Repeat with a Bet Din planned before the crisis.
8. Start a crisis while a Hunt is already in its active phase. The Hunt finishes normally.
9. After every UI step, check `error.log` for new lines naming `bet_din_overdue`.
