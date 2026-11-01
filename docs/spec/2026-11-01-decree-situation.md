**Status:** design 2026-11-01, being built. Daniel: "continue polishing and building features! Maybe some more non-violent crises?" This is the second non-violent crisis family after the [Talmud trial](2026-11-01-talmud-trial-situation.md), built on the same pattern: a race in the crisis window, actions as scenes, an opening announcement, monthly toasts. It replaces two one-event incidents of [V41 step 4b](v41-danger-incidents-and-the-pogrom-unfolding.md): the badge (`kehillah_incident.0010`, the ghiyar under Islam) and the servants' decree (`kehillah_incident.0040`).

# A decree against the Jews, as a situation

## History it shows

A decree was proclaimed, then argued over, often for years, and its enforcement was patchy:
- Lateran IV (1215) ordered distinctive dress.
  - England enforced the badge from 1218.
  - In Castile in 1219, the Jews threatened to leave for Muslim lands, and the Crown suspended the decree.
  - Aragon and France enforced it unevenly, and towns sold exemptions.
- Under Islam, the ghiyar of the Pact of Umar was old law, enforced in waves: al-Hakim in 1009, the Almohads after 1147.
- The servants' decree (Gregory VII to Alfonso VI, 1081; councils from 1078) was repeated so often because it was so often ignored.

So the outcome that matters is not only "decreed or not". It is also whether it is enforced, laid aside for a price, or withdrawn.

## The situation: `kehillah_decree`

**Kinds**, held as a variable on the situation:
- **badge:** the badge under a Christian lord, the ghiyar under a Muslim one;
- **servants:** the servants' decree.

The kind changes the text and the enforced effect; the mechanics are the same. The display name is "The Badge Decreed in X", "The Ghiyar Decreed in X" or "The Servants' Decree in X".

**Start.** The incident director's badge and servants picks are unchanged in weight, dates and cooldowns. They now start the situation instead of firing the incident events. A community runs one crisis at a time: no decree while an attack, a trial or another decree runs. A decree laid aside for a price counts as a cooldown: the same kind is not decreed again while the suspension lasts.

**Participants:** the community's leader, and the sovereign who issued the decree.

**Phases:**

| Phase | Ends | Next |
| --- | --- | --- |
| **Proclaimed** | A three-way race to 100. A hidden 120-day backstop takes the leader. | **Enforced**, **Laid aside**, or **Withdrawn** |
| **A verdict** | 30 days | Closed: the situation ends |

**Proclaimed.**
- **Enforced** is pushed every month by the lord's clerks. The push is larger under a hostile or cold lord, or a strict or exclusionary teaching, and smaller under a protective one. Answers that fail add to it too.
- **Laid aside** is pushed by payment, and by a successful threat to leave the realm (Castile 1219).
- **Withdrawn** is pushed by a petition that persuades, and by a common petition with the realm's other communities.

## Actions

One situation decision, **Answer the Decree**, opens a scene. The opening scene, the crier in the market, offers the same answers first. Each counts once per decree:
- **Petition the lord:** the Shtadlan, or the leader. Persuaded: Withdrawn; refused: a little toward Enforced.
- **Pay to have it laid aside:** gold to the lord, a sure push toward Laid aside.
- **Threaten to leave the realm:** the lord weighs what he would lose. Believed: a large push toward Laid aside. Called a bluff: a push toward Enforced, and the lord's outlook falls.
- **Join with the realm's other communities:** shown only when another Kehillah lives under the same sovereign. A common petition, a push toward Withdrawn.
- **Accept it**, in the opening scene only: the decree is enforced at once, with no anger spent.

## Verdicts

- **Enforced:**
  - The badge: the existing `kehillah_badge_decree_effect` and the leader's badge modifier. A player then answers how the community will wear it:
    - with pride, as their fathers wore their names (zealous or stubborn leaders: piety, a minor Stability bonus);
    - or simply.
  - The servants' decree: the existing `kehillah_servants_decree_effect`.
- **Laid aside:** nothing changes for now. A suspension variable keeps the same kind from being decreed again for ten years.
- **Withdrawn:** a minor Stability bonus.

## Window and toasts

- The window's pressure line: "The lord's clerks next month: +N toward Enforced".
- A monthly toast: "The Clerks Go House to House" (the badge), "The Reeve Counts the Servants" (the servants' decree).

## Not built

- Communities' collective threat with real emigration if it fails.
- The badge's later forms (the Judenhut, the rouelle's colours) as variants.

## Console

- `event kehillah_decree_debug.1`: decree the badge (or the ghiyar).
- `kehillah_decree_debug.2`: the servants' decree.
- `kehillah_decree_debug.3`: log the decree's state.
