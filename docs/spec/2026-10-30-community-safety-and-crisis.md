**Status:** built in the main worktree at Daniel's request, 2026-10-30;
source and xTiger checked. Runtime and visual checks remain **UNRUN**.

# Community Safety, warning preparations and political aftermath

Daniel approved a visible, slower crisis with preparation choices, varied
encounters and consequences after survival. His subsequent direction moves the
tracker from Intrigue into Military. This direct request takes priority over the
older live-test queue. It supersedes the fixed Granada outbreak in
[V39](v39-pogroms-and-the-popular-crusade.md), the mandatory encounter ladder in
[V41](v41-danger-incidents-and-the-pogrom-unfolding.md), the event-only entry point
in [V42](v42-the-crisis-as-a-place.md), and the absence of a political settlement
after a successful defense in [V43](v43-after-the-violence-and-granada.md).
The existing march, siege, losses, captivity, children and struck-community
recovery systems remain the foundation.

## Military as the entry point

For a Kehillah, opening **Military (F3)** defaults to **Community Safety**.
An **Armies** tab preserves access to the native troop and mercenary pages.
Other governments retain the native Military view. Intrigue no longer needs an
override. The revised vertical layout and native `scrollbox_content` override
from the earlier layout repair are carried forward.

The dashboard groups the current phase and general incident risk, the active
warning's escalation forecast, preparation choices, completed protection,
petitions, and the latest outcome and ruler response. Preparation choices appear
before the full readiness ledger. Their cost, duration and principal effect are
visible without hovering. The forecast includes a native progress bar.

The two percentages have different meanings: annual incident risk covers all
eligible threats, accusations and restrictions; escalation chance is a single
roll when the current warning ends. Neither is a daily massacre roll. The
warning's remaining time comes from the existing preacher story, not a second
independent timer. An already-formed host arriving from another community can
still enter the armed phase directly; this revision does not restart its march
as a local preaching warning.

## Warning and preparations

State belongs to the community title. Stages are warning (1), armed (2), waiting
for judgment (3), and recovering after judgment (4). An incrementing incident
epoch guards the new delayed settlement/recovery relays against a later crisis.
The next incident clears its preparations and response while retaining the last
outcome, prior opening family, and unexpired royal protection.

Agitation starts at 45, rises by 3 on each weekly warning update, and is clamped
to 5–95. At the end of the warning, the outbreak chance is agitation, minus
15 for condemnation, 15 for promised soldiers, 10 for arms, 5 for refuge, and
10 for renewed royal protection, clamped to 5–95. Existing protection effects
on casualties/severity also remain. No combination guarantees safety.

| Preparation | Gold | Time | Completion effect |
| --- | ---: | ---: | --- |
| Quarter watch | 20 | 14 days | Existing defended flag: severity −15 |
| Emergency provisions | 30 | 14 days | Severity −10 |
| Escape routes | 10 | 14 days | Existing scattering effects; prepared escape option |
| Answer accusations | 15 | 14 days | Agitation −20 |

Only one communal task can run at a time. The leader must be free, present,
able to pay, and in the warning phase. Completion uses weekly story updates;
an unresolved task is canceled when the crisis ends. Completed preparations
remain relevant after mobilization. Existing council visits, messengers,
petitions, negotiation and their timers remain accessible from the dashboard.
The regular warning acknowledgment no longer immediately opens that council.

There are at most three warning developments, spaced at least 28 days apart,
drawn without replacement from threats on a shutter, a market boycott,
neighbors speaking up, and watch wages. These are fictional cases, not claimed
historical transcripts. They supplement preparation rather than repeatedly
opening the navigation event.

## Granada and attack encounters

The day-30 circulating poem opens a 76-day local warning with a distinct
agitator, leaving the staged historical poet separate. The original day-106
event resolves the shared warning instead of declaring war unconditionally.
Earlier exposure can shorten the warning through the existing schedule.
Poem-response choices now affect agitation/preparation as appropriate. An old
save reaching the historical checkpoint without a recorded warning receives
a short grace period. The existing global history/news flags are still set
when an armed host actually rises.

An attack draws **at most two** encounters from six families: street, fire,
forced conversion, rescue, escape, and a fallen castle gate. A conversion
encounter may close the sequence early through its existing final choices.
Families do not repeat within the same attack, and the previous attack's first
family is excluded from the next opening. Context gates the street/castle and
children scenes. Existing choices still record the flags used to resolve
losses, conversion, captivity and the leader's fate. New rescue and escape
encounters give completed routes a direct use.

English player prose in the mob, pressure and realm-view families now uses
attack, massacre or unrest wording. The old `pogrom` namespaces, keys and save
variables remain compatible identifiers.

## Endings and the ruler's response

Prevention, successful defense, payment and a struck quarter all enter the new
settlement flow before old cleanup removes preparations or the agitator. A
one-day hidden relay reaches the current community holder, providing a closure
scene and stress relief; the actual ruling sovereign is asked six days later.
Granada has a specific survival description. The ruler may:

- Renew protection for two years and provide 20 gold if affordable.
- Demand 20 gold for that protection; the community can accept or refuse.
- Forbid further disorder while withholding additional aid.
- Issue a targeted residence edict against this community.

AI weights use outlook and relevant traits. Targeted expulsion requires outlook
below −15 and no castle/soldier promise from the actual current sovereign at
resolution. It uses the existing edict, appeal, ransom and departure system.
Accepting its appeal clears the local edict without raising realm settlement
law or clearing another community's edict. A local edict lapses when its living
issuer ceases to be the community's sovereign; a new host's realm ban may then
start its own ordinary edict. General policy repeal does not erase a valid
targeted edict automatically.

Spared communities receive a recovery choice about 45 days after acknowledgment
of the ruler's answer. Struck communities retain the existing burial, survivors,
rebuilding and remembrance chain. Recovery therefore also follows a successful
defense rather than ending at a single survival acknowledgment. Quarterly
retry covers a judgment relay that never reached a ruler; unusual succession
while a visible judgment is already open still needs runtime testing.

## Files and verification

New content uses the `kehillah_crisis_*` triggers, effects, values, scripted
GUIs, custom localization, quarterly on-action, events and debug events.
The interface is `gui/kehillah_crisis_military.gui`, mounted by a narrow set of
edits to the installed 1.20.1.2 `window_military.gui`. The earlier new Intrigue
override and panel were retired after backing up their repaired layout.
The full vanilla Military file is still a compatibility surface for other UI
mods and future game updates.

See the [test record](../testing/2026-10-30-community-safety-crisis-live-test.md)
for completed checks, the denied live attempt and the remaining probe matrix.
Hidden `kehillah_crisis_debug.1`–`.4` events provide warning setup, a synthetic
preparation tick, state logging and a successful-defense ending. They are
console-only probes for a disposable campaign.

The implementation is left in the requested main worktree. Publication remains
blocked by read-only Git metadata and the previously denied GitHub integration
write route. No commit was made directly on `master`, and no PR is claimed.

## 2026-10-31 addendum: one Military navigation row

**Status:** implemented, source check complete; live visual check pending.
This addendum supersedes the "Armies" parent-tab arrangement in "Military as the
entry point" above, following Daniel's review of the two-level layout. A
Kehillah player sees one row: Community Safety, Your Armies, Mercenaries.
Community Safety is selected when Military opens. The two army pages keep their
native content and controls. The window title remains Military on all three
pages. Non-Kehillah governments keep the original Military navigation.
