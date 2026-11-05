**Status:** revised in the main worktree, 2026-11-05; xTiger checked, live choice and presentation verification pending. This is a shortcut to the options in [Three standing actions](../spec/2026-11-01-three-standing-actions.md), not a separate pool of crisis actions.

# Suggested crisis actions

The small **Suggested Actions** button beside the situation's Actions heading opens the elders' counsel in Agitation or Armed Host. The dayyan appears when the community has one. The counsel lists at most three courses. Choosing a course goes directly to its action scene: a public answer opens the learning contest, a plea during Armed Host opens the lord's answer, and an appeal in Agitation opens the local lord's approach scene with that patron already selected. The latter still lets the player go personally or send a messenger, and a personal audience retains its 2-4 day travel delay. No gold or race points are granted merely by choosing advice.

The seven simpler measures use the shared effects in `common/scripted_effects/kehillah_crisis_recommendation_effects.txt`. The elders' counsel opens a short confirmation event for each measure; confirming rechecks eligibility and then calls the shared effect. The three standing menus apply that same effect directly when an option is chosen. This keeps those familiar menus responsive and avoids a second event that could fail to appear after the player has already made a choice. The Military buttons also call the shared effects directly. The standing menu tooltips describe the immediate costs and results.

| Phase | Suggested course | Canonical option and scene | Cost and selection gate |
| --- | --- | --- | --- |
| Agitation | Communal fast | Proclaim a Fast, Prepare the Quarter | Free; direct in standing menu, confirmation in counsel |
| Agitation | Ask the local lord | Go to the Powerful, Seek Protection | Local lord not yet asked; opens his approach scene |
| Agitation | Public answer | Answer Him in Public, Make Our Case | Free; opens the Learning contest |
| Agitation | Campaign of answers | Answer the Accusations, Make Our Case | 15 gold; direct in standing menu, confirmation in counsel |
| Agitation | Post a watch | Post a Watch, Prepare the Quarter | 20 gold; direct in standing menu, confirmation in counsel |
| Agitation | Seek the town | Win the Town, Seek Protection | 40 gold; direct in standing menu, confirmation in counsel |
| Armed Host | Plead with the lord | Beg the Lord to Send His Men, Seek Protection | Free; opens the lord's answer scene |
| Armed Host | Bar the streets | Bar the Quarter, Prepare the Quarter | Stress; direct in standing menu, confirmation in counsel |
| Armed Host | Shelter families | Shelter in the Stone Houses, Prepare the Quarter | Prosperity; direct in standing menu, confirmation in counsel |
| Armed Host | Send silver | Send Silver, Make Our Case | 50 gold; direct in standing menu, confirmation in counsel |

The shortlist calls the same per-crisis gates used by the canonical options. Paid courses must also leave at least four fifths of current gold in the treasury: `common/script_values/kehillah_crisis_recommendation_values.txt` derives each threshold from the original action cost. Thus a leader with 97 gold may hear about a 15-gold campaign, but the 20-gold watch and 40-gold town gifts are left to the full menus. The action event, rather than the advice option, spends resources and records the action.

In Agitation the selection order is fast, lord, public answer, campaign, watch, town. At 70 Armed points, the fourteen-day campaign and watch are omitted because they may not finish before the next phase. In Armed Host it is lord, barricades, shelter, silver. A course is absent if its existing eligibility or the additional spending threshold fails. The source still keeps `kehillah_crisis_recommendation_effects.txt` for effects shared between canonical scenes and Military buttons; the counsel event no longer calls those effects.

The scripted GUI sets a one-day fallback flag as soon as the button is pressed, so repeated clicks while the event is opening cannot queue duplicates. The event's `after` block normally clears the flag and temporary shortlist when it closes. Console probes `kehillah_crisis_debug.11` and `.12` open the Agitation and Armed counsel for inspection. A fresh game check should verify the button lock, advisor portrait, direct action routing (especially the emir), tooltip values, AI confirmation, and that a course disappears after its canonical action is taken. AI decision weights are unchanged.

