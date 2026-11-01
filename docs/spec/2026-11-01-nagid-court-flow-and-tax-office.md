**Status:** PROPOSAL, 2026-11-01, written at Daniel's request ("Yes, write it up"). **Nothing here is
built.** It is an addendum to [the Nagid spec](2026-10-30-the-nagid.md). It **revises** §7 (how the
office is founded and abolished), §8 (the confirmation) and §9 (choosing the service), as built in
slices 4 and 5 ([build note](../implementation/2026-10-30-nagid-build.md)). It **adds** the
duplicate-family cleanup and a tax-office service. Decisions marked *Daniel* are his. The rest is
Claude's proposal, open to revision (§7).

# The Nagid at court: a smoother office, one Joseph, and the tax office

## 1. What Daniel asked for

Daniel live-tested slices 1–5 and the visibility pass on 2026-11-01. He asked three things:

- **The decisions:** "The decisions for appointing the head of the jews, selecting his position, and
  removing him feel kind of underbaked to me right, any ideas how to make it feel smoother?"
- **The tax collector:** "I just realized that there's a Yosef HaNagid in vanilla who's the tax
  collector of granada! ... Can we incorporate the tax collector position at all?"
- **The layout:** the realm view's line under the ruler (*Daniel*, built the same day, not part of
  this proposal).

## 2. What is wrong with the flow today

Today one appointment takes five separate pieces, each with its own timing:

| Step | Today | Problem |
|---|---|---|
| Founding | Decision **Establish a Head of the Jews** (ruler) or **Ask for a Head of the Jews** (seat leader) | The founding names the leader without the ruler ever "meeting" them. |
| Confirmation | Event `kehillah_nagid.0001`: confirm (fee) or not yet | The ruler confirms first and chooses the service separately. |
| The service | Event `kehillah_nagid.0003`, **the next day** | It is a second event for the same moment, and it arrives a day late. |
| Changing it | Decision **Assign the Head of the Jews**, yearly | It sits in the decisions list, away from the person. |
| Removing him | Only **Abolish the Head of the Jews**, at outlook Cold or worse | A ruler cannot dismiss a man without abolishing the office. |

The Kehillah side only receives notices: "Named Nagid", "Named Vizier", "Confirmation Withheld".

## 3. The proposal: one audience, then the person in the character menu

### 3.1 The audience (replaces `.0001` and `.0003` as one event)

When a ruler confirms a head of the Jews, they get **one event: an audience**.

- **Who appears:** the ruler and the candidate face each other on a court background, as vanilla's
  court events show two portraits.
- **The text:** names the community and the office (`KehillahNagidOfficeName`). It also gives the
  fee where one is asked.
- **The options are the decision itself:**
  - "Confirm him, and make him my vizier" (only under the Dhimma);
  - "Confirm him, and give him my treasury";
  - "Confirm him as my physician";
  - "Confirm him, and send him as my envoy";
  - "Confirm him, without a place at court";
  - "Not yet": withhold, as today.

  Each confirming option's tooltip shows the fee and the service's modifier, which the current
  `.0003` tooltips already compute.
- **The AI** keeps today's rule: it confirms by `ai_chance`, and its service options weight as
  `kehillah_nagid_service_ai_pick_effect` does now.
- **Founding leads into it:** Establish and Ask still found the office, then open the audience
  instead of naming the leader on the spot. Founding and confirmation become one moment.
- **The 1066 seed** skips the audience. Joseph is already Badis's Vizier.

`kehillah_nagid.0003` goes away. The day-later event goes with it.

### 3.2 The person, in the character menu (replaces the Assign decision)

Two **character interactions** for a ruler, on his own Nagid:

- **"Change his place at court":**
  - the same choices as the audience, as an interaction with a small event or option list;
  - once a year, as the Assign decision is now;
  - it replaces **Assign the Head of the Jews**.
- **"Dismiss the Nagid":** removes the man, not the office.
  - The office stands vacant, and the community's next leader may be confirmed after a year (the
    existing `kehillah_nagid_withheld` timer).
  - Costs: the community loses Stability; the Nagid gets a negative opinion of the ruler; there is
    a Realm News entry.
  - No outlook gate: any ruler may dismiss his own man, as any ruler may fire a councillor.

For a **Kehillah leader**, one interaction on the realm's ruler:

- **"Ask for a head of the Jews":** the same gates and effect as today's decision, opened from the
  ruler's portrait, where a petition belongs.
- The decision stays as well, so the realm view's empty frame still has somewhere to open.

### 3.3 Abolishing stays a decision, with weight

**Abolish the Head of the Jews** stays in the decisions list: it is a matter of the realm, not of
one man. It gains:

- a confirmation event that names who is hurt (every community in the realm) and what the clergy
  think;
- the Realm News entry that already exists.

The Cold-or-worse gate stays. Dismissing the Nagid (§3.2) is now the ordinary way to be rid of a man.

### 3.4 The Kehillah side gets events, not just notices

A Kehillah player who is confirmed, given a new place, dismissed or refused gets a short event
instead of a notice:

- **Confirmed:** the seal of office, a feast at the synagogue. A small choice of tone, for example
  thanking the ruler publicly (prestige) or quietly (piety, Stability).
- **Dismissed, or confirmation withheld:** the community's reaction, with the existing costs.
- **AI Kehillah leaders** keep the silent path.

## 4. One Joseph, not two

Vanilla already has the family, so a 1066 game has two Josephs. This was recorded as "found, not
fixed" in [V51](v51-bookmark-rosters.md).

| Person | Vanilla (`history/characters/sephardi.txt`) | This mod (`history/characters/granada_1066.txt`) |
|---|---|---|
| Samuel ha-Nagid | 3220 "Shmuel", dies 1055 | 9000230, dies 1056, nickname "ha-Nagid" |
| Joseph | 3221 "Yosef", Badis's courtier since 1045 and his tax collector in 1066, dies 1066.12.30 | 9000216, leader of the Kehillah of Granada, the Nagid |
| Joseph's wife | sephardi_0004 Rahel, daughter of Nissim, married 1049 | 9000233 Hannah (name not recorded), daughter of Nissim |
| Nissim ben Jacob | sephardi_0003 (with father Yaakov, sephardi_0002) | 9000232 (with father 9002025) |
| Azariah | sephardi_0005, born 1060 | 9000234 |
| Elyasaf | — | 9000231 |
| Qasmuna, the poet | sephardi_0001, born 1044, in vanilla's family by hypothesis | — |

**Proposal:** keep the mod's family, since the Granada storyline is built on it, and **retire
vanilla's living duplicates at game start**: Yosef 3221, Rahel (sephardi_0004) and Azariah
(sephardi_0005). Vanilla's Shmuel, Nissim and Yaakov are already dead by 1066.

The retirement is silent: a hidden death in the first moment of the game, so no player sees a
notice. CK3 cannot delete a character. Vanilla's alternative, overriding all of
`history/characters/sephardi.txt`, would break other mods' edits to that file.

- **Badis's tax collector slot** then opens, and §5 can fill it.
- **Qasmuna** is a real poet and only vanilla has her. **Open question for Daniel (§7):** leave her
  as she is (still linked to vanilla's dynasty), or recreate her as the mod's Samuel's daughter and
  retire vanilla's copy too.

The 867 and 1178 starts have no Naghrela, so this is a 1066 change only.

## 5. The tax office: the Nagid's man as tax collector

**What the engine allows** (checked 2026-11-01 in `common/tax_slots/types/00_tax_slot_types.txt`):

- A tax collector must have the ruler as his liege (`is_valid_tax_collector`: `liege ?=
  scope:liege`).
- The Nagid leads an independent community, so he can never be one. This is the same wall as the
  council (§14 of the spec).
- **Script cannot hire a collector:** there is `fire_tax_collector`, but no effect to hire one. The
  ruler hires through vanilla's tax window, or the AI fills its slots itself.

**So the man at the tax office is not the Nagid but someone he sends.** This fits the history:
Jewish tax farmers and collectors served Muslim and Christian rulers throughout the period. Their
unpopularity was one of the dangers of the office.

- **Who:** a courtier of the seat's Kehillah leader with Stewardship of 10 or more. Elyasaf in 1066,
  if his skills allow.
- **How:** a Nagid's interaction on the ruler, "Offer a man for the tax office". The man moves to the
  ruler's court as a courtier and carries a modifier ("Sent by the Jews of the realm"). From then on
  he is an ordinary candidate in vanilla's tax window. A player ruler hires him there; an AI ruler
  weighs him by his aptitude like anyone else. Nothing is forced.
- **While he collects** (`is_tax_collector_of` the ruler), checked each quarter:
  - the seat community gains Prosperity (the tax farm's profits and protection);
  - the danger term grows (a Jewish tax collector is resented by the taxed);
  - the Nagid gains standing with the ruler.
  
  Both terms show in the pillar and danger tooltips, by name and number.
- **The Treasurer service stays** (§9 of the spec). It is the Nagid at the ruler's side. The tax
  collector is the community's man in the provinces. A realm can have both.
- **Vanilla's jizya obligation** (`jizya_special_rights_tax_collector`) is worth a look when this is
  built: a collector of the poll tax on the protected peoples, drawn from them, is an irony the
  period knew.

## 6. Slices

1. **The duplicate family** (§4): a hidden game-start cleanup, and Qasmuna per Daniel's answer.
   Small; do first, since §5 depends on the free slot.
2. **The audience** (§3.1): fold `.0001` and `.0003` into one event, and lead founding into it.
3. **Character interactions** (§3.2): change place, dismiss, ask. Retire the Assign decision.
4. **Abolish's confirmation event, and the Kehillah-side events** (§3.3–3.4).
5. **The tax office** (§5).

Each slice keeps the debug probes current (`kehillah_nagid_debug.*`) and ends with a live check of
the event or window it touches.

## 7. Open questions for Daniel

1. **Qasmuna** (§4): leave her in vanilla's dynasty, or bring her into the mod's family?
2. **Dismissal** (§3.2): no outlook gate, as proposed? Or should a ruler who favours the Jews pay
   more to dismiss their head (prestige, opinion of the Jews)?
3. **The tax office** (§5): is the community's gain worth the danger? Should a tax collector's
   presence also feed slice 6's envy at court?
4. **The Kehillah-side events** (§3.4): a small choice of tone, as proposed, or plain events?
