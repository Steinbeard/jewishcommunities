**Status:** done 2026-10-30. **Route A is ruled out.** The engine refuses every way of placing an
independent Kehillah leader in a host's council, court positions or diarchy. This is the
[Nagid spec](../spec/2026-10-30-the-nagid.md)'s Slice 0 (§14).

# Nagid engine spike: can a Kehillah leader serve on a host's council?

## Method

- **Tool:** xTiger's `ck3_script`, in Daniel's open game (PID 11932, launcher-started,
  `-debug_mode -develop`), at Daniel's instruction. Daniel was playing Joseph ibn Naghrilla of the
  Kehillah of Granada, 10 August 1067. No mouse or screenshot steps were needed.
- **Baseline:** `error.log` offset 242195 before the first probe.
- **Scope:** all probes were scripts of effects with `debug_log` read-backs. Targets were picked at
  run time and saved to temporary global variables: the Granada leader, and the top liege of his
  county as host.

## Results

| Probe | Effect | Engine answer | State changed |
|---|---|---|---|
| Council seat | Badis: `assign_councillor_type = { type = councillor_chancellor target = <Joseph> remove_existing_councillor = yes }` | **Refused:** "Badis … must be the liege of you to assign it as Councillor." `is_councillor_of`, `has_council_position` and `is_councillor` all false | No. Ra'is Issam of Guadix stayed chancellor |
| Court position | Badis: `appoint_court_position` with `court_physician_court_position`, then `court_poet_court_position` | **Refused, both:** "Employee doesn't have employer as liege" | No. The physician (Rahel) and Abu Ishaq kept their positions |
| Vizierate diarchy | Badis: `designate_diarch = <Joseph>` | **Refused:** "Can't designate diarch who is not a vassal or courtier of the liege causes diarchy invalidation" | No designated diarch before or after |
| Leader death while seated | Not run | Moot: nothing could be seated. Running it would also have killed Daniel's own character | n/a |

**Other facts read in the same game:**
- **Joseph:** `is_independent_ruler = yes` and `is_landed = no`, and his `liege` is himself. His
  `suzerain` is Badis, through the V15 charter. His own Kehillah council (five members) is intact.
- **Capitals (1067):**
  - Badis's capital is Granada, and his primary title is the Taifa of Granada.
  - al-Mustansir's capital is Cairo.
  - Tamim's capital is Mahdia.
- **Baghdad:** `d_sunni` is held by al-Qa'im, whose capital is Baghdad and whose top liege is Alp
  Arslan. The Baghdad community's top liege is also Alp Arslan. This confirms the spec's Exilarch
  rule (§12): an ordinary top-liege rule would seat Baghdad's office at the Seljuk court.
- **Incidental:** Badis's active diarch, holding the vizierate, is **Abu Ishaq of Elvira**, the
  staged anti-Jewish jurist. Historically Joseph was the vizier. Check the Granada staging and
  diarchy setup for this. It is not part of this spike.

## What this means

The engine checks the liege relationship itself, inside `assign_councillor_type`,
`appoint_court_position` and `designate_diarch`. Mod triggers can't loosen these checks. The only
characters a host can seat are his own courtiers and vassals. The mod deliberately keeps a Kehillah
leader neither: `cannot_be_vassal_or_liege`, and V32's reasons. Landless vassalage would also need
an administrative liege.

The remaining routes are design choices, for Daniel:
- **Route B, service in name (the spec's fallback):** the Nagid stays the community's leader. The
  host gets a skill-scaled modifier for the service chosen (Vizier, Treasurer, Physician, Envoy).
- **Route C, a delegate at court (new):** the Nagid sends a member of the community, a kinsman or a
  learned courtier, into the host's court. As the host's courtier he can hold real vanilla council
  seats and court positions. He leaves the Kehillah's court to do so.

## Errors and cleanup

- **New `error.log` lines:**
  - the three refusals above;
  - an effect-localization note for `assign_councillor_type`;
  - wrong syntax in one read-only `every_court_position_candidate` probe;
  - one "Variable … is set but is never used" block per console `run`. That block is the parser
    re-validating every script file on load, not a runtime error.

  Nothing else appeared in the window, and no mod files were edited while the game ran.
- **Cleanup:** the spike's global variables were removed, and the final probe confirmed Badis's
  council and court positions were unchanged.
