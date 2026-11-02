**Status:** built 2026-11-01, not live-tested. Changes how the attack crisis's race is shown in its window, not how it is scored: every push keeps its points. Builds on [2026-11-01-the-attack-as-a-race.md](2026-11-01-the-attack-as-a-race.md) and [2026-11-01-crisis-variety-and-consistency.md](2026-11-01-crisis-variety-and-consistency.md).

# The crisis window's catalysts, grouped

## Why

Daniel, looking at the window's "Catalysts towards Armed host" list: *"I don't think these should all be broken up into their own types of events here. Could we have lots of different flavorizations, but still group them into a set of logic actions? ... I think the current view I'm sharing is unimmersive."*

The window lists every catalyst registered for a phase. The attack crisis had 43 toward the Armed host and 50 toward Spared, one for each scene's answer, so the list read like a ledger of one-off events, most of them at x0. The specific story already lives where it belongs: in the events, the banners and the monthly pressure notices.

## The groups

Each group is one catalyst. Its points vary by what triggered it; the scene's own number is kept.

**Agitation → Armed host**

| Catalyst | Kind | Folded in |
| --- | --- | --- |
| An angry town | once | the opening, each named opening, an accusation in Holy Week |
| The agitator | monthly | the preaching, the agitator's following |
| Hard times | monthly | a cold or hostile lord, a great holy war, Holy Week |
| The town turns | scenes | every warning-event answer that helps the agitator, Granada's court scenes, the lord's refusal in the accusation |
| Our missteps | actions | a failed answer, an exposed effort, questions about the witness that were caught |
| A host gathers | decided | unchanged |

**Agitation → Spared**

| Catalyst | Kind | Folded in |
| --- | --- | --- |
| Our protectors | monthly, and as won | the lord's protection, his goodwill, each protection first won, the lord's protection in the accusation |
| The town softens | scenes | every warning-event answer that calms the town, Granada's court scenes |
| Our own efforts | actions | the watch, the stores, the ways out, advocacy; the standing actions' successes; the lie exposed; the gates barred |
| The danger passes | decided | unchanged |

**Armed host → Quarter held:** What we prepared (once, as the host forms: the sum of everything prepared before), Our own efforts (silver, shelter, bars, the gate scene, the plea, prayer), Our protectors (the lord's men), and the decided catalyst.

**Armed host → Quarter struck:** The host closes in (muster, march and siege ticks), Abandoned (the hand-over, the lord's refusal), Our missteps (the gate scene and the plea going wrong), and the decided catalyst.

## How

- One catalyst per group, defined in `common/situation/catalysts/kehillah_crisis_catalysts.txt`.
- Each group's points are a script value, `<catalyst>_points_value`. It reads a variable on the situation, `<catalyst>_pts`, which is set just before the catalyst fires. This is the same pattern the preaching catalyst already used with `kehillah_crisis_push`.
- `kehillah_crisis_race_add_effect` and `kehillah_crisis_armed_race_add_effect` take a `POINTS` argument. Each call passes the value the old catalyst had, so no push changed. `kehillah_crisis_struck_tick_effect` already took one.
- The monthly drivers sum into one firing per group.
- The window's number beside a group shows its last push.

## Not changed

- The trial (about six catalysts per phase) and the decree (fewer) were already short enough.
- The points, the thresholds and the order of the race.
- The pressure and driver notices: they still name the specific cause.
