**Status:** first integration and custom window built in the main worktree, 2026-10-31; source/xTiger checked, new window live verification pending. Daniel's Warning screenshot confirms a situation exists before violence. The dated presentation revision below supersedes this document's original Military-first presentation in sections 1 and 4. See the [implementation note](../implementation/2026-10-31-crisis-situation-integration.md). Extends the [Community Safety specification](2026-10-30-community-safety-and-crisis.md) and the [situation source spike](https://github.com/Steinbeard/jewishcommunities/pull/59). Its warning, attack, settlement, and recovery mechanics remain in force.

# Community crises as situations

## 1. Purpose and boundary

An active threat to a Kehillah should appear as a CK3 **situation** tied to that community's place. The player can find it in the Situations list and on the map, see its stage and principal people, and return to Community Safety to act. A crisis remains local: a preacher at Worms does not turn all Ashkenaz into one shared situation. Two communities can face independent crises at once, even under one sovereign.

Community Safety in **Military (F3)** remains the main action surface. It holds preparations, petitions, the annual incident risk, the current warning's one-time escalation chance, the readiness ledger, and the latest outcome. The situation window summarizes the active crisis and links to that surface; it does not create a second copy of preparation buttons or a second probability calculation. The Armies tab and the ordinary Military view for other governments remain as specified on 2026-10-30.

This change does not turn annual incident risk into a persistent situation. A situation begins when a particular warning starts or an already-armed host targets a community. Quiet periods show no crisis situation. It does not replace the preacher and mob story cycles, battle, siege, encounters, ruler judgment, or existing recovery content.

## 2. Identity, place, and ownership

Use a **non-unique situation type** with one runtime instance per community's active crisis. The instance has one sub-region containing the community's domicile county and a center at that domicile's province. Its displayed name includes the community title, not merely the county. An attack moving between counties does not move the pin away from the threatened quarter; the march route remains in the Military dashboard and events.

The community **title** owns the incident epoch, numeric stage, agitation, preparations, promises, outcome, and delayed-relay guards. It stores a reference to its current situation instance. The situation stores the community title and the epoch it represents. Every update checks the reciprocal references and epoch before changing either object. Never use `situation:<type>` to find a crisis: that lookup is for unique types, and several communities may be in danger. The same title must not have two live crisis situations.

The existing title stage values map to these visible phases:

| Title stage | Situation phase | Meaning |
| --- | --- | --- |
| 1 | Warning | Agitation, protection requests, and communal preparations are underway. |
| 2 | Armed | A host has risen or arrived; march, siege, defense, and attack encounters use existing systems. |
| 3 | Judgment | Violence was prevented, paid off, defended against, or suffered; the sovereign's answer is pending. |
| 4 | Recovery | The sovereign has answered; the community faces its recovery or departure follow-up. |

The situation phase **mirrors** the title stage. No situation duration or catalyst independently decides whether violence begins. The preacher story remains the warning clock, including Granada's 76-day warning and any shortened warning. The mob story remains the four-day march/siege clock. If the engine cannot advance a situation phase promptly and reliably when the title stage changes, the integration must wait; the UI must not display a stale phase as fact.

## 3. Lifecycle

1. **Creation.** The shared warning-entry effect creates one instance after the title has a new epoch. An incoming armed host with no local warning creates it directly in Armed. Granada's poem warning uses the same path. Repeated calls during one epoch reuse the stored instance.
2. **Warning to Armed or Judgment.** The existing outbreak and prevention effects change the title stage and then synchronize the same instance. A failed warning can go directly to Judgment without fabricating an armed phase. Preparations already completed keep their existing effects.
3. **Armed to Judgment.** Existing victory, payment, dispersal, and struck-quarter resolution effects synchronize after they record the outcome. The one-day closure relay and six-day sovereign response remain title/epoch guarded.
4. **Judgment to Recovery.** The actual sovereign's answer moves the title and situation to Recovery. A targeted edict remains this community's consequence; it does not change another crisis's situation.
5. **End.** Close the situation after the first recovery choice or the struck-community chain's initial recovery/leave decision has resolved. Longer building, captivity, conversion, remembrance, or edict consequences continue under their existing systems without keeping a permanent crisis pin. If the community dissolves, close its instance immediately. End only the instance stored on that title and only when its epoch matches.

When a new incident starts before an old delayed relay arrives, the incremented epoch invalidates the old relay. It must not change, end, or recreate the newer situation. If a saved reference points to an ended or wrong instance, clear that reference and report the inconsistency in debug logging; do not end another community's situation.

## 4. People and presentation

The situation identifies the current community leader, the current actual sovereign, and the agitator or armed host leader when one exists. Leadership and sovereignty can change mid-crisis, so participation must be refreshed from the title and current host relationship, not frozen at creation. A dead or missing agitator leaves the display without a broken portrait. The situation must not grant a character war status, court office, or realm authority merely to make them a participant.

Use a modest crisis entry in the native Situations list and a pin at the threatened community. The icon and text distinguish Warning, Armed, Judgment, and Recovery. The situation window shows the place, stage, people, and a short consequence/next-step summary. It includes a working route to **Military → Community Safety** for the player's own Kehillah; for an outside observer it can show a read-only summary. Do not present the warning's escalation percentage as a daily risk or use the generic phase progress bar as the outbreak chance. If a truthful clock cannot be supplied to the situation window, omit that progress display and point to Community Safety.

Multiple simultaneous situations, including nearby counties and two communities in one realm, must remain individually named and navigable. The UI must not fill the HUD with repeated notices or show the generic situation window's irrelevant future-phase/catalyst controls. A custom window is appropriate if the generic one cannot meet these requirements. The Military tab must remain fully usable without opening Situations.

## 5. Save compatibility and failure behavior

An older save with active title/story crisis state but no situation continues to resolve normally. A one-time, bounded reconciliation may create a missing situation from an active title stage if the title, domicile, and epoch are valid; it must not restart the warning, reset preparation, or fire an extra encounter. Quiet titles get no situation. An orphan situation whose title or epoch is invalid is ended by a bounded cleanup pass. Reconciliation must be idempotent across quarterly pulses, save/reload, and title succession.

If situation creation or phase synchronization fails, existing crisis logic continues from title state; Community Safety and debug logs expose the true state. The player must never be forced to click a situation in order to progress the crisis. No global scan should end all instances of the type as a shortcut.

## 6. Implementation gates

**Gate A — isolated engine spike.** Define the non-unique situation type and console-only events in a disposable branch. Create crises for two different community titles, save/reload, and verify distinct persistent instances, title/epoch links, county centers, and independent deletion. Test two communities in one realm and, if possible, the same county. Verify the player, host, and agitator can be represented without unintended game effects. Use xTiger first; a Luna tester performs the live run. If this fails, stop before wiring normal gameplay.

**Gate B — lifecycle mirror.** Connect creation, phase synchronization, and ending to the existing central effects. Exercise direct Armed entry, warning prevention, outbreak, payment, successful defense, struck quarter, ruler response, targeted edict, leader death/succession, host change, dissolution, and an old relay after a new epoch. Check save/reload at each stage. A situation must never change the outcome or its timing by itself.

**Gate C — player UI.** Verify Military/Armies behavior first, then the situation pin, list, window, and navigation on a fresh 1066 start and with concurrent crises. Confirm localized text, no misleading percentage or phase progress, and no tooltip-only error flood. If a custom situation window requires a broad vanilla GUI override, record that compatibility cost before accepting it.

Only after all three gates pass should the situation become part of the ordinary crisis build. The [2026-10-30 live-test matrix](../testing/2026-10-30-community-safety-crisis-live-test.md) still applies to the underlying crisis mechanics. The research spike establishes that CK3 has the needed APIs in its installed files; it does **not** establish the runtime or UI behavior for this mod.

## 7. Presentation revision — 2026-10-31

Daniel's live Warning screenshot establishes that the situation exists during preparation, but the generic window shows an impossible phase end date, irrelevant future phase and catalyst controls, and a raw catalyst key. The Military warning page also repeats four actions and their explanatory text, crowding the overview. This section supersedes the Military-first action placement in sections 1 and 4.

The custom crisis window is the primary home for warning preparations. It shows the actual current phase, warning forecast, pending preparation, four existing preparation actions, and a council action. It omits the generic situation's phase date, takeover points, and catalyst display; these do not govern the crisis clock. The existing scripted GUIs continue to own costs, eligibility, and effects, so there is one action implementation.

Military Community Safety retains the annual incident risk, current situation, warning forecast, readiness, and outcome. A direct button opens the active crisis situation. During Warning, the preparation block is collapsed by default when a situation exists; the player can expand it there, and it appears automatically if the situation reference is absent. The crisis window offers a route back to Military. This preserves a usable fallback for save repair and GUI failure without making the overview the main action list.
