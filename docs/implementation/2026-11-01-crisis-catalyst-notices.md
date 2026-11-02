**Status:** implemented, source checks pass, 2026-11-01; live rendering/timing unverified.
Follows Daniel's request for vanilla-style catalyst feedback and clearer Granada writing.
Extends [grouped catalysts](../spec/2026-11-01-crisis-catalyst-groups.md) and
[opening acknowledgment](2026-11-01-crisis-acknowledgment.md).

# Catalyst notices for the attack crisis

## Behavior

The native `msg_catalyst_triggered` notice is a Struggle message. Its installed localization uses
`STRUGGLE_NAME`, `CATALYST_INFO`, `STRUGGLE_PHASE` and `CATALYST_VALUE`, provided by that system.
The installed situation schema documents no corresponding catalyst-notification callback. The
mod therefore uses a separate message with the same vanilla `struggle` icon and neutral style,
its own mutable Message Settings filter, and situation-specific scopes.

The header reads **[county]: Catalyst Triggered**. A compact action/event notice names the
catalyst and gives **+N progress toward [future track]**. The track is selected before firing,
not inferred from the phase afterward. Points are read from the same script value as the native
binding and snapshotted before firing; a threshold crossing can immediately change phase and
clear/reseed counters. The notification itself never awards points.

The eleven grouped attack catalysts have fourteen phase/destination bindings. Each route is
explicit and source-tested against `kehillah_crisis_situation.txt`. The shared race helpers use
these routes, and explicit phase-transition signals remain compatible pass-throughs rather than
being misreported as ordinary point awards.

Recurring messages combine story and mechanics:

- The monthly agitator catalyst retains its four narrative variants, now followed by the
  actual catalyst name and its points toward Armed host. The initial single-catalyst notice is
  suppressed because the existing narrative report carries it.
- The armed host retains its every-second-four-day-tick report (approximately weekly). Its
  footer explicitly reports accumulated progress **since the last report**, not a fictitious
  single-tick award. Each underlying tick still fires its catalyst once.
- Other grouped actions, scene outcomes, preparations and protection receive compact individual
  notices. The independent special-driver notices keep their existing behavior.

No scoring values, thresholds, race timing, narrative pool weights, or no-repeat state changed.
The new presentation is for the attack situation; trial and decree scoring wrappers are untouched.
A pending introduction produces no new catalyst notice. AI characters receive no player message.

## Granada writing

The former underlined-line notice did not say what the mark meant and introduced a named courtier
without a role. It now describes the delivery to the study hall and identifies the underlined
passage as a call to kill the Jews. Abu Ishaq remains the poem's author even if another agitator
is leading the threat.

`kehillah_granada.0021` is the Armed phase's muster scene, not itself a new catalyst award. Its
new title is **The Sanhaja Mobilize**. The body identifies the commanders and recruits, explains
that they are preparing to act without the sovereign's permission, and identifies defense and
protection as the remaining responses. It uses the existing sovereign scope for name/pronouns
rather than assuming Badis remains alive. The option reads **We must prepare the quarter.**

## Validation

[The test record](../testing/2026-11-01-crisis-catalyst-notices.md) records the baseline comparison,
five new source contracts, existing lifecycle checks, console probe and unavailable Luna check.
A source pass cannot establish the native toast layout or that scope values render correctly;
those checks remain pending.
