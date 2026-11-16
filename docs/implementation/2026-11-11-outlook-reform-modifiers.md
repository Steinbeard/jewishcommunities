**Status: implemented, source-verified; live test pending.**

# Reform modifiers in the ruler's outlook

## Decision

The 1066 Almoravid exception is no longer inferred from `house_almoravid` by
the outlook calculation. Maliki rulers continue to receive the ordinary
Dhimma teaching value. At game start, the independent Almoravid ruler instead
receives the visible `kehillah_almoravid_reform_movement_modifier`, which adds
`-65` through its own displayed outlook line. This preserves his former total:
the replaced house exception had stood in place of the ordinary `+15` Dhimma
line, whereas the modifier now appears beside it.

This makes the difference political and historical rather than hereditary or
doctrinal. It also leaves a reusable `kehillah_reformist_enforcement_modifier`
(`-30`) for future events or systems. Neither modifier contains vanilla stat
effects; their gameplay effect is deliberately limited to the Kehillah outlook
calculation and the systems that already use it.

## Rationale

Maliki Dhimma is shared by the Almoravids and their taifa contemporaries. The
early Almoravid movement's reformist political programme is therefore shown as
a character modifier, not a new rite or a permanent dynasty rule. It ends
with the ruler unless a future event deliberately grants it to another ruler.
