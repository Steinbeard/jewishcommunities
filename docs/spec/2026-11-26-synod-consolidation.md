# Synod consolidation and native tenet proposals

**Status:** SOURCE BUILT 2026-11-26, at Daniel's request. Regression and validator results are recorded in [the test record](../testing/2026-11-26-synod-consolidation.md). Live checks are **UNRUN**. This supersedes the agenda, picker and law-menu design in [2026-11-25-dynamic-synod-agenda.md](2026-11-25-dynamic-synod-agenda.md), sections 3–7 and 9b–12a. It preserves the two ordinary cases followed by one synod proposal, the existing vote/quorum rules, and the current headship office. It does not change headship succession.

## Problem and decision

The previous interface mixed genuine engine changes with resolutions whose continuing consequences were unimplemented. Monogamy renewal could spend prestige to reapply an existing doctrine; the divorce-consent wording described a head-of-faith approval doctrine as the wife's consent. Ordinances mostly set unused flags and gave the host pillar rewards. The captive fund destroyed gold without keeping a fund or paying a ransom. These do not justify separate categories of communal government.

The agenda now has **three categories**, plus a free option to conclude without a proposal:

| Category | Maximum substantive choices on a page | Mechanical result |
|---|---:|---|
| Belief and tenets | Three known tenets; four possible actions at Sanhedrin level | Change the host's rite's actual core tenets, or Sanhedrin-only faith-wide tenet acceptance |
| Rite practice | Three alternatives | Change the host's rite's marriage, proselytism, or clergy-gender doctrine |
| Leadership and discipline | Two kinds; up to three nominees on the headship page | Grant the existing head-of-rite office, or apply existing Herem to a named eligible leader |

Pagination/back navigation adds at most two controls. Empty kinds and invalid substantive choices are hidden. The host may leave any unsubmitted choice without paying proposal prestige. The existing sitting cooldown still starts when the third phase opens.

## Comparison with installed vanilla

Sources read from the installed game at `E:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/`, not the empty D: Steam directory:

- `common/activities/activity_types/ecumenical_council.txt`, especially its `special_type` options and debate phases.
- `common/activities/activity_types/_activity_type.info`, `tenet_doctrine_based_activity` and its slot filters.
- `common/scripted_effects/pam_ecumenical_council_effects.txt`, including proposal enactment and branched-rite adoption.
- `common/scripted_triggers/pam_scripted_triggers.txt`, native rite-cap and exclusive-ascetic swap checks.
- `localization/english/dlc/pam/pam_ecumenical_council_events_l_english.yml`, tenet/doctrine object links and core replacement names.
- The installed game's script documentation dumps: `logs/triggers.log` and `logs/effects.log`, `any_character_tenet`, `ordered_character_tenet`, `knowledge_filter`, `knows_tenet`, `ordered_rite_tenet`, and `set_tenet_status`.

| Vanilla ecumenical council | Consolidated synod |
|---|---|
| Planner slots select two known-character tenets and one active-faith doctrine | Third-phase event pages enumerate actual known-character tenets, three at a time |
| Activity stores actual tenet/doctrine objects as debate topics | Activity stores actual topic, replacement, action and rite objects/flags |
| Native object names provide the tenet links/tooltips | Same `GetName(rite)` object links, with current standing beside each choice |
| Core replacement uses actual rite-tenet objects and native eligibility checks | Same underlying rite enumeration, cap and eligibility checks, including the native exclusive-ascetic swap exception |
| Faith-wide acceptance and Christian schism consequences | Acceptance changes reserved for the Sanhedrin; ordinary synods change their rite's cores only; no Christian schism code copied |
| Two tenet debates and a doctrine debate | Two ordinary Bet Din cases, then one confirmed proposal |

The native planner flag changes how the whole activity's options are presented, including ordinary Justice sittings. This rework therefore uses the documented engine iterator in the existing third-phase flow rather than making every Bet Din select council topics. It preserves the independently changing invitation/activity configuration. A separate Synod planner is a possible later design, not required to remove the hard-coded catalogue.

## Belief: data and scope

`ordered_character_tenet` with `knowledge_filter = known` supplies the catalogue. It is filtered through shared proposal-validity triggers. There is no list of tenet IDs or manually maintained theme taxonomy in picker generation. A known compatible tenet from vanilla or another mod can appear without adding a row to this mod.

Three objects are shown per page. A seen-object list prevents repeats; returning to the agenda and reopening Belief restarts browsing. A book controversy's queued tenet is preferred when known and actionable, followed by personal tenets. This is a priority hint, not a new active-debate mechanic. There is no claim that an unseen debate is currently running.

Names and native tooltips come from the objects, not copied English labels. The action page shows the selected tenet and its effective standing. A core change lists the rite's actual replaceable cores and presents a confirmation before spending prestige. An empty slot may be filled without dropping a core.

The native `set_tenet_status` effect is faith-scoped. Ordinary synods consequently cannot permit, prohibit or lift prohibitions for all Rabbinic Judaism. Those three actions require the Sanhedrin at selection and enactment. Lifting a prohibition returns the teaching to Known, not automatically Permitted. A tenet held as core by any rite cannot be prohibited.

Temple Service and Prophetic Revelation retain their host-specific institutional/calling requirements, in addition to engine `rite_can_choose_tenet` checks. A recorded vote is revalidated before either removing or adding a core. It cannot silently remove a core if the host changed rites or the selected replacement disappeared.

Book ceilings are recalculated through the existing standing system after a valid ruling. This does not grant mastery or automatically increase every book's standing. The central library's existing numeric tenet indices remain unchanged. A small compatibility bridge decodes queued book-contest ordinals into objects; that bridge does not determine what can appear in the picker.

## Rite practice

The bounded policy pairs are marriage (monogamy/polygamy), proselytism (discouraged/encouraged), and clergy gender (male/either). These are deliberate limits on supported policy, not a substitute catalogue of beliefs. Each offers only an engine-legal alternative to a doctrine currently held. Current and proposed doctrine names use native tooltip links. There is no paid reaffirmation of unchanged monogamy.

Divorce and funeral motions are withdrawn. In particular, `doctrine_divorce_approval` must not be presented as the wife's consent: the recorded engine meaning is head-of-faith approval. This pass does not invent an alternative consent system.

The existing controversy score affects votes and the host's Stability. The old “None/Minor/Major” preview remains, without inserting manual bullets inside another effect-list bullet. A proposal stores its old doctrine and original rite and rechecks both before enactment, so a stale vote cannot overwrite an intervening change. The Sanhedrin's practice proposals still affect its host's rite only.

## Authority and withdrawn resolutions

Headship lists at most three eligible attending academy heads, ranked using their **community title's** existing merit score (fame, Learning and devotion). It does not evaluate a title-scoped score in character scope. The vote still calls `kehillah_gaonate_grant_effect`; the single shared Gaonate title and its vacancy requirement remain explicit limitations. No new inheritance law or additional title is introduced.

Discipline names a real leader already in Niddui, selected through the existing Herem eligibility system, and revalidates that leader on enactment. It is not a general licence to excommunicate arbitrary characters.

Ordinances, captive funds, public fasts and academy levies are withdrawn from the agenda and cannot open a new sitting. Old event IDs redirect to the agenda; old enactment branches and title flags remain for compatibility. They are not offered as working policies. Reintroduce any of these only with an actual enforcement point, beneficiary or resource account.

## Build and runtime contract

- `scripts/kehillah_reform_build.py`: generic tenet triggers/effects/events, standing text and native object links.
- `scripts/kehillah_synod_agenda_build.py`: agenda/practice/authority pages and their matching gates/wording. It preserves unrelated synod events and the separately developed closing callback fix.
- The activity's closing callback snapshots the complete reform payload before its `involved_activity` link disappears. The closing event uses the captured scope, not that disappearing link. Valid enactment is marked; a lapsed new proposal does not get a success announcement or the Sanhedrin bonus.
- `event kehillah_synod_debug.13 <id>`: console-only known-tenet/pagination probe. Use outside an active proposal on an expendable test save; it clears selection scratch state. Existing `.11` replays a closing ruling; `.12` reports title and engine headship recognition.

Both generators must remain repeatable without changing their outputs on a second run. There is no vanilla file override or global configuration change in this rework.

### Vote and appointment feedback — Daniel's follow-up, 2026-11-26

Daniel reported that he could not see the other delegates' votes or find himself as head of rite after a carried motion. The old vote options incremented counters without preserving a visible named roll call. The grant ran only when acknowledging the final popup; the disappearing activity-link issue in [the earlier closing fix](../implementation/2026-11-26-synod-closing-ruling.md) was another plausible failure path, not a verified diagnosis of his save.

`scripts/kehillah_synod_vote_build.py` is now invoked automatically at the end of the agenda builder, after the reform output is ready:

- Each delegate can vote once. Their name and side are retained on the activity, shown in a host toast and entered in the activity log. The sponsor's counted supporting vote is also recorded. The activity stores the electorate asked to vote, so an unanswered ballot is distinguished from an opposing vote.
- Completion snapshots support, opposition, uncast ballots and the named lists onto the host. The final popup displays all three totals; its Record the ruling tooltip lists the voters under each side. The lists remain available after the activity link disappears.
- The ruling is enacted in the closing event's **immediate** block, before its result text is displayed. The acknowledgment button records the already-applied result and cannot grant the office a second time. This explicitly supersedes the earlier closing-fix document's acknowledgment-time enactment.
- A headship result is announced as confirmed only after the nominee both owns `d_kehillah_gaonate` and is returned by the rite's native `head_of_rite` scope. Distinct text handles an already-held headship, title ownership without native recognition, and a lapsed proposal. A vote which passed but could not enact is not described as an appointment.

No succession/title definition changes were needed. The new feedback and immediate timing still require live verification. The existing `.11` debug probe now enacts a passed proposal when it opens the ruling; do not use it on a valuable save expecting a harmless preview.

## Remaining verification and compatibility

Live enumeration, native tooltips, zero/three/many-candidate pages, empty core slots, enactment after activity completion, nominee changes and doctrine application remain unverified. Native eligibility checks use the head of rite as a reference character; explicitly include a **headless rite** in the live test. An empty menu must be investigated against actual known-tenet/status/eligibility data, not loosened by bypassing the engine's `can_pick` restrictions.

Reload the mod and start a fresh sitting for review. Existing book agenda ordinals and community ordinance flags are retained; an old in-progress tenet ballot without the new object payload is not migrated and should be treated as a lapsed proposal. This is source-built work, not a claim of saved-game or rendering verification.
