**Status:** decided with Daniel 2026-11-01, being built on `codex/crisis-situation-spec-20261031`. Supersedes the action list and the "window and flow" section of [The attack as a race](2026-11-01-the-attack-as-a-race.md), and adds a rule to [Crisis situations as the mechanic](2026-11-01-crisis-situations-as-the-mechanic.md) that every crisis family follows. Prompted by [the UX play-through](../testing/2026-11-01-attack-race-ux-test.md) and Daniel's Granada play-through the same day.

# Three standing actions

## Why

**The window had too many rows.** It showed 18 crisis actions as separate full-art rows. They pushed the list of what drives the danger off the window, and hid the last actions entirely.

**Old and new overlapped.** Old event chains offered the same tools as the new actions under other names, so the player met the same thing twice. In Granada:
- The poem arrived three times: "A Copy of the Verses", "The Verses Reach the Street" and "Verses in the Souk".
- "The Verses Reach the Street" offered guards (Post a Watch), a refuge in Almería (Prepare a Way Out) and the emir's ban (Seek Protection).
- "The Emir's Confidence" offered horses for Lucena (Prepare a Way Out again).
- The gate scene offered silver (Send Silver) and barred doors (Bar the Quarter), with rolls that ignored the race.

## The rule

**Actions are the player's tools; events are what happens to them.** A crisis has three standing actions, the same in every phase and every crisis family:

| Action | What it stands for |
|---|---|
| **Prepare the Quarter** | What the community does for itself: watch, stores, a way out, prayer, shelter, barricades. |
| **Seek Protection** | Who might shield it: the lord, his overlord, the Church or the qadi, the town council, the ruler or head of the faith by letter. |
| **Make Our Case** | How it changes minds: answering the accuser, a campaign of answers, the accuser's past, going to him, the neighbours, forgiving debts, silver to the host's leaders. |

**Each action opens a scene,** and its options are the sub-actions:
- The scene's text depends on the phase and on how the crisis began. Granada has its own.
- A sub-option that doesn't belong to this phase or opening is hidden.
- A sub-option that belongs but is blocked (a task already running, once per crisis, not enough gold) is shown greyed out, with the reason.
- Every scene ends with "Not now".

**An event never offers one of these tools again.** Event options are reactions to that development: pay, endure, take a risk. Each moves one of the bars.

Later crisis families (a Talmud trial, a libel, an expulsion) add their own sub-options to these three scenes instead of adding rows to the window.

## The attack's sub-options

| Action | Agitation | The host armed |
|---|---|---|
| Prepare the Quarter | Post a Watch · Lay In Provisions · Prepare a Way Out (Granada: a discreet refuge in Almería, which risks feeding the plot charge) · Proclaim a Fast | Shelter in the Stone Houses · Bar the Quarter |
| Seek Protection | Go to the Powerful (the lord, his overlord, the Church; players only) · Win the Town · Appeal to the Emperor or the Head of the Faith | Beg the Lord to Send His Men |
| Make Our Case | Answer Him in Public · Answer the Accusations · Discredit Him · Go to His Camp (players only) · Ask the Neighbours to Speak (once they have offered) · Forgive the Debts (debts opening only) | Send Silver to the Host |

Costs, odds and race points are unchanged from the attack-race spec. Each sub-option's tooltip shows them through the game's own tooltips.

## What changes elsewhere

- **The Elders' hub (`kehillah_mob.0100`) does not open while the community has a crisis window.** Its pages' "back" options then simply close, leaving the player at the window. The Gather the Elders action is gone.
- **Granada:**
  - "A Copy of the Verses" is the opening; its option no longer leads to "The Verses Reach the Street", which stops firing.
  - "The Emir's Confidence" keeps its three answers as reactions that move the race: swear loyalty (a roll: Spared, or Armed), remind him of Samuel's service, stand on the office. Its horses-for-Lucena option is gone, since the way out is under Prepare the Quarter.
  - "The Preaching" and "Verses in the Souk" are skipped there.
- **The gate scene,** while the Armed race runs:
  - Standing at the gate, opening the gates to plead, and barring the synagogue add Quarter-held or Quarter-struck points instead of acting on their own.
  - Its silver option is hidden, since Send Silver is the action for that.
  - The personal answers (Granada's flight, the craven's cellar, the cemetery gate) stay as they are.
- **AI communities** take the same three actions, then pick a sub-option by weight, as the old decisions did.

## Not settled here

- **Balance.** Daniel found the Granada options unbalanced; this pass removes the duplicates first. A balance pass needs a natural, unforced race played through.
- **Held needs more sources** later in the Armed race (polish item 5 of the UX record).
