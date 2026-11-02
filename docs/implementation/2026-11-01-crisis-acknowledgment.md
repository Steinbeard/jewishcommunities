**Status:** implemented and source-verified, 2026-11-01; CK3 runtime/UI verification pending.
Daniel explicitly requested the current primary worktree and branch for this unit. Existing
uncommitted Nagid work is outside its scope.

# A crisis starts when its trigger event is acknowledged

Supersedes opening announcements in [Community crisis situations](2026-10-31-crisis-situation-integration.md),
[the attack race](../spec/2026-11-01-the-attack-as-a-race.md),
[the Talmud trial](../spec/2026-11-01-talmud-trial-situation.md), and
[the decree](../spec/2026-11-01-decree-situation.md). Their active mechanics remain in force.
Expulsion keeps its original grace counter; this does not implement its proposed situation conversion.

## Sequence and implementation

1. The narrative trigger event opens. No new active situation, race, war, or expulsion grace
   clock exists yet. Context such as an accuser, preacher, or drafted decree may exist.
2. The player selects a response. The option previews its existing effects and records the
   selection. Its `after` block initializes the crisis, then applies the response once. AI
   communities use the same events and their existing AI weights.
3. A persistent native important-action alert opens the situation. Expulsion links to Answer
   the Edict instead. Pending introductions do not show either alert. Existing Situations and
   Military navigation remain available.

Startup paths no longer send duplicate opening banners. Legacy opening messages default to the
feed, and their attack descriptions are shortened. Ruler, phase and outcome notices retain their
existing behavior.

| Opening | Trigger event | Start after acknowledgment |
|---|---|---|
| Granada poem | `kehillah_granada.0018` | Preaching and attack situation, then selected catalyst |
| Accusation | `kehillah_accusation.0001` | Agitation, then accusation response |
| Generic/local/crusade preaching | `kehillah_mob.0004` | Agitation, then AI answers if applicable |
| Debts / Holy Week | `kehillah_crisis_race.0300` / `.0310` | Agitation |
| Sudden host / rising | `kehillah_crisis_intro.0001` | War and Armed situation |
| Existing host's next community | `kehillah_crisis_intro.0001` | Same host, new war and Armed situation |
| Talmud denunciation | `kehillah_talmud_trial.0001` | Denunciation, then selected response |
| Badge / ghiyar / servants decree | `kehillah_decree.0001` | Proclaimed, then selected response |
| Expulsion | `kehillah_expulsion.0001` | Existing grace counter, then selected response |

A player lord still decides whether to proclaim a proposed decree before its recipient sees the
opening. Granada's later scenes are scheduled 35 and 76 days after the poem is acknowledged,
retaining their previous spacing without spending the preparation interval while it is unread.

## Pending state, identity, and saves

`kehillah_crisis_intro_pending` reserves the community title. Shared admission excludes pending
introductions, active attacks, trials, decrees and expulsion clocks. The reservation stores its
recipient, county, sovereign and an increasing introduction epoch. Saved events carry the title
and epoch; activation checks both and the expected family. A stale event cannot acknowledge a
newer incident, including another of the same family.

While pending, the preacher's weekly following growth, movement, countdown and notices stop.
An existing retargeted host's scripted march also stops. Situation reconciliation refuses to
create a situation from pending state. A dead pending preacher cannot initialize an unseen crisis
through the existing resolution fallback. Each new opening discards the prior resolved incident's
opening before selecting its catalyst.

Quarterly reconciliation reoffers a pending event to a changed holder, including an AI successor;
it does not resend to the same holder. County/sovereign changes cancel pending context. Cancelling
a retargeted host ends that host through its existing cleanup path. Realm-wide expulsion can
supersede a pending lesser incident; its fresh epoch rejects the older event. Existing active
save events use compatibility gates and do not restart their clocks.

Trials and decrees roll their cast and terms on the pending title. The opening reads that
snapshot; activation copies it into the situation without rerolling. Later scenes read the live
situation as before.

## Tooltip and verification boundaries

Initialization is in event `after`, outside option tooltip evaluation. Original response effects
are inline scripted effects: `show_as_tooltip` previews them, and the selected response executes
after successful activation. A token comparison found all 22 nonempty helpers identical to the
pre-change options' gameplay effects. Two acknowledgment-only options remain without direct
response effects.

`python scripts/test_kehillah_crisis_intro.py` checks source contracts, not CK3 runtime behavior.
Console probes and remaining checks are in [the test record](../testing/2026-11-01-crisis-acknowledgment.md).
