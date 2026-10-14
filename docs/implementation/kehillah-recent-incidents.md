**Status:** V40 slice 1 built and source-checked, 2026-10-14. Live verification pending.

# Recent incidents in the host's faith

Implements [V40 §5.1 and slice 1](../spec/v40-living-crises-and-councils.md).
This dated addendum supersedes [V38 §1](../spec/v38-anti-jewish-pressure.md)'s
silent annual teaching changes and the annual route in
[V34 §3](../spec/v34-outlook-teachings-and-founding.md). The council debate
and the existing teaching step effects remain available.

The existing `kehillah_faith_pressure` variable and addition effect keep their
names for save compatibility. Players see **Recent incidents**, alongside
**Goodwill**, in the Your Host tooltip. The line names the host's faith;
missing counters read as zero, and one decimal place preserves the fractional
memory left by decay. Other religions omit the line. No council threshold is
advertised before the council actually exists.

Both counters fade by 20% annually, only on the faith's main rite pulse.
The annual wrapper now calls `kehillah_faith_incidents_yearly_effect`; it
cannot change a teaching or start a teaching cooldown. The old random
hardening and softening branches are removed together: this conservatively
keeps teaching changes visible through council events. **Until slice 2 lands,
the non-DLC Council/Caliph route does not exist.** Vanilla rite drift and the
existing DLC council debate are retained. The established head-of-faith
outlook shift at 10 incidents after decay is retained; it changes outlook,
not doctrine.

A completed V39 pogrom adds **4** to the county faith's incidents before
deaths or dissolution can remove the victim's domicile. Warnings, sieges and
ransom resolution do not repeat that addition. Existing attribution stays:
risings/violent accusations affect the county faith; court preaching and
disputations affect the instigating host's faith. These can differ when host
and county have different faiths. The HUD explicitly names the host's faith
and does not imply the two counters are the same. The 0–100 clamp remains.

The Learned Exchange tooltip no longer promises annual softening. It states
its existing -1 incident/+1 goodwill outcome and the yearly decay instead.
The bold disputation victory uses the same incidents terminology.

Console probes in `events/kehillah_incidents_debug_events.txt`:

- `.1`: reports host-faith HUD values.
- `.2`: seeds 10 incidents/5 goodwill, calls the main-rite yearly wrapper,
  expects 8/4, checks +4 addition and both clamps, checks absent HUD values,
  and restores the original counters, including their absence. Its decay
  seed stays below the head-mood threshold. It does not run an actual pogrom.

Verification and limitations are recorded in
[the dated test log](../testing/2026-10-14-recent-incidents-live-test-log.md).
Next: verify slice 1 on a fresh boot, then V40 slice 2, the Council and
Caliph's lobbying window and outcomes. The preserved running instance did
not register the new namespace; no live assertion or rendering PASS is claimed.
