# V32 host arrest and exile: live test log, 2026-10-12

**Status: live-tested 2026-10-12; steps A-E PASS. One gap: the custom refusal-warning text
(`ImprisonCharacterDeclineSummary` override) could not be seen, because the vanilla Imprison popup
does not render it. Spec: [v32-host-arrest-and-exile.md](../spec/v32-host-arrest-and-exile.md).**

## Method

- Daniel's running game (PID 21408, Rav Pinchas, 7 Oct 1066) was saved first as
  `Rav_Pinchas_1066_10_07before_v32_test` (the typed name appended to the default field text; no
  existing save overwritten). CK3 was then killed and relaunched directly with
  `-debug_mode -develop`. `debug.log` `Mod:` line includes
  `Jewish Communities|mod/jewishcommunities.mod|Enabled`.
- Fresh start: Kehillah of Worms 1066 bookmark, Isaac ben Eliezer ha-Levi. `run whoami.txt` confirmed
  Root = Isaac HaLevi (internal 29176). Played to 18 Sept 1066 (pillars initialised, "A Charter Is
  Sealed" shown), then probed. Baseline `error.log` taken after boot and before the first probe.
- Step D used the saved game (Rav Pinchas of Worms, host Kaiser Heinrich again), loaded in the same
  process.

## Results

| Step | Expected | Actual | Result |
|---|---|---|---|
| A. `.1` | no reason, interaction not valid | "host holds NO imprisonment reason", "imprison interaction NOT valid", "HEIR EXISTS (refusal = exile)" | PASS |
| B. `.2` then `.1` | toast; reason held, interaction valid, heir | Toast "Grounds for Arrest: Kaiser Heinrich now holds a crime against you and may Imprison you." Then HOST HOLDS AN IMPRISONMENT REASON, IMPRISON INTERACTION VALID, HEIR EXISTS | PASS |
| C. `.3`, refuse | popup; exile not war | See below | PASS (text caveat) |
| D. accept | imprisoned by host | See below | PASS |
| E. error.log | no new feature lines | See below | PASS (one tooltip-time note) |

### C. Refusal

- Popup "Imprison": "To the miserable Rav Isaac, You are hereby under arrest for crimes against the
  Crown. Signed, Kaiser Heinrich of the Holy Roman Empire." Accept tab: -30 opinion, family -15,
  rivalry; "Imprisons you"; "You are a known Criminal (Defied an Expulsion Edict)".
- Decline tab (effect preview): "Loses 40 Opinion of Kaiser Heinrich IV for 15 years (Attempted
  Arrest); Crime - Rightful imprisonment; Ends the Christian Host Charter contract with Kaiser
  Heinrich IV; Adopts Adventurer Government; Adopts the Camp Succession Law"; below, "Iyov: Gains the
  Kehillah of Worms Title". No "rise up in rebellion" text anywhere.
- **Refusal-warning text not observed.** `imprison_decline_summary` is not shown in this popup (not on
  either tab, nothing on hovering Decline). It may only appear in the sender-side interaction UI,
  which the AI host path never opens. The override is nonetheless live: the later `error.log` stack
  shows `war_for_imprison_effect[...]` resolving to `kehillah_host_arrest_effects.txt` line 156 and
  calling `kehillah_arrest_refused_effect`.
- debug.log after clicking Decline:
  - `kehillah_arrest_refused_effect: begin`
  - `kehillah_step_down_effect: begin`
  - `kehillah_step_down_effect: handed the community to its appointment heir`
  - `kehillah_step_down_effect: end`
  - `kehillah_arrest_refused_effect: stepped down into exile`
  - `kehillah_arrest_refused_effect: end`
  - `kehillah_succession.0010: PASS a domicile exists after provisioning`, `PASS successor has Kehillah
    government`, `PASS the real community title is primary after cleanup`
  - `kehillah_departure_finish_effect: government is landless_adventurer`
- Toast "Tributary Invalidated" (host charter ended). Isaac's realm became `x_d_laamp_690`. New Heir:
  daughter Orpa HaLevi. **No war** declared (no war notification; no war lines in debug.log).
- One day later (19 Sept) event `kehillah_arrest.0010` "Into Exile": "Kaiser Heinrich sent men to take
  me. I would not go to his dungeon, so I have gone from the community instead. Others will keep the
  synagogue and the books; I take the road, and only what my wagons can carry, out of his lands."
  Option "Better a wanderer than a prisoner." Real text, no raw keys. debug.log: `kehillah_arrest.0010:
  the exile's camp is on the road out of the host's realm`. A dotted travel route westward is visible
  on the map; vanilla Wayfarers Camp events then fired ("Rank Gained", "Empty Bags and Empty Stomachs",
  "Do I See a Light?", "The Lutin Bridge", "Danger: Flawed Fare"; "Camp Moved to Chalons" 2 Nov).
- The game then ran from 18 Sept 1066 to 2 Feb 1067 (a stuck-Ctrl input slip by this tester let time
  run on; see below) with no crash and no Game Over. No new file in `crashes\`.

### D. Accept

Loaded `before_v32_test` (8 Oct 1066). `.2` then `.1`: reason held, interaction valid. `.3`, clicked
Accept. Event "Imprisoned! I have been captured and detained against my will by Kaiser Heinrich!" Probe
file after accepting: `root IS imprisoned`, `imprisoner exists`, `still kehillah gov`, `primary title
exists`. Ran to 30 June 1067 (prison art visible in events) with no crash.

### E. error.log

Searched for host_arrest, kehillah_arrest, imprison_decline, war_for_imprison,
basic_allowed_to_imprison, kehillah_crime.

- Boot lines: `Event kehillah_arrest_debug.1/.2/.3/.4 is orphaned` (expected for debug-only events).
- New-game run (refusal, exile, a month-plus of travel): the only new error was vanilla
  `ep3_laamps_provisions.1080` `abort_travel_plan` loc ("missing exact perspective 'third'"). Nothing
  from this feature.
- Loaded-save run (13:21:14, when the Imprison popup built its Decline preview): six tooltip-time
  errors, stack `imprison_interaction:on_decline` > `war_for_imprison_effect` >
  `kehillah_arrest_refused_effect` (host_arrest_effects line 126) > `kehillah_step_down_effect` (line
  293) > `kehillah_refresh_map_view_for_players_effect` > `kehillah_refresh_map_view_effect` (map_view
  line 317): `Failed to fetch variable for 'kehillah_map_view_registry_size' due to not being set`,
  `Event target link 'var' returned an unset scope`, `Invalid left side during comparison 'var'`.
  Interpretation: the old save predates the map-view registry variable; the new-game popup preview
  raised none of these. Preview-time only, not seen on a real refusal. Worth hardening the map-view
  refresh against an unset registry variable, but it is not a V32 defect.

## Bugs found vs known noise

- No V32 defects found.
- Possible follow-ups (judgment calls, not tested further): (1) the refusal-warning loc is invisible in
  the AI-sent popup, so the "no heir, arrest goes through" and "passes to your heir" warnings never
  reach the player there; (2) the exiled leader's camp starts nearly out of provisions (vanilla
  starvation events fire within a day or two of leaving), which is harsh but arguably thematic;
  (3) the map-view unset-variable preview error above.
- Known noise ignored: duplicate localization keys, `ai_check_interval`, bet-din rule and bookmark
  asset lines.
- Tester slip: a diagnostic script left Ctrl held down, so Esc opened the Windows Start menu and the
  game ran unpaused for a few extra in-game months. No effect on results.

## Daniel's original game

Saved before closing, as `Rav_Pinchas_1066_10_07before_v32_test.ck3` in `save games\`.
