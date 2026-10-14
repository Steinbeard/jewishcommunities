**Status:** built 2026-10-13 (Daniel: "make sure the mechanics you've implemented are clear to
players -- events with characters shown, notifications informing about the world"); live check
pending. It builds on [v34](v34-outlook-teachings-and-founding.md) (outlook, invitations, settlers,
exiles) and [v30](v30-community-news.md) (Community News).

# V35: Making outlook and invitations visible

## The audit

V34's systems already reach the player in these ways:
- **News:** invitations, foundings, the invitation answered, exiles on the road and settled, teaching
  changes, risings.
- **Events with portraits:** Send Out Settlers (where and who) and councils.
- **Seek an Invitation:** its tooltip and feed messages.

The gaps:
1. **Outlook on the Jews was invisible.** It drives the host's attitude (Stability), the policy
   review, invitations and the Shtadlan's choice of lord, but nothing showed it or its changes.
2. **An invitation the player could answer** came only as a feed line.
3. **Settlers' destinations** did not say why a county drew them.
4. **The graduate recommended to the lord** did not say the lord's outlook warms.

## What was built

- **Outlook bands** (``KehillahOutlookBand``, any character; ``KehillahHostOutlookBand``, a leader's
  host). Each reads as a word and a number, such as "Well-disposed (+25)":
  - Hostile: -40 or lower.
  - Cold: -39 to -15.
  - Indifferent: -14 to 14.
  - Well-disposed: 15 to 39.
  - Protective: 40 or higher.
- **Where the outlook shows:**
  - The Stability breakdown's host line: "The host's attitude (outlook on the Jews: Well-disposed
    (+25)): +38".
  - The invitation news.
  - "The Shtadlan Sets Out".
  - The invitation event.
- **The lord's mood** (``kehillah_host_outlook_watch_effect``, quarterly, players only): when the
  host's outlook moves to another band, a feed notice reads "The Lord Grows Warmer" or "The Lord
  Grows Colder". It names the new band and lists what moves an outlook. A new host is recorded
  silently, since a new lord has his own news.
- **The invitation event** (``kehillah_invitation.0001``):
  - **Who gets it:** a player community with an invited county within its settlers' reach. It shows
    the lord's portrait and the leader's, and says what answering brings.
  - **Everyone else** in diplomatic range still gets the feed line.
- **Settlers' destinations** in "Where to Settle" carry a note: "(invited by its lord)" or "(Jewish
  settlement encouraged)".
- **The graduate option** shows "<lord>'s outlook on the Jews warms (+10)".

## UI (added 2026-10-13)

Daniel asked to read a character's outlook on the character view, "alongside their opinion". This
repo's GUI spikes found that a vanilla ``.gui`` cannot be extended piece by piece
([gui-spike-community-list.md](gui-spike-community-list.md)). Showing anything inside the vanilla
character window means a permanent fork of that file. So:

- **On the character window: an "Outlook on the Jews: <band>" character modifier.**
  - **What it is:** five display-only modifiers (``common/modifiers/kehillah_outlook_modifiers.txt``),
    using the vanilla letter icon (positive, mixed or negative). The tooltip says what the band means
    and what moves an outlook.
  - **Who carries one:** every landed Christian or Muslim ruler (non-Jewish). Others are left out,
    since the teachings that shape an outlook are Christian and Muslim (live: a duke of Wuxi read
    "Cold"). Set at game start, refreshed yearly, and
    quarterly for a player's host.
  - **Effect:** none, so no gameplay change.
- **On the community's own strip (under the top bar): a "Your Host" block.**
  - **Shows:** the host lord's name, his band and number, and "invited" when a lord within the
    settlers' reach has an open invitation.
  - **Its tooltip adds:** the realm's Jewish settlement policy, the invitation line, and what moves an
    outlook.
  - **Data:** mirrored quarterly onto the player (``kehillah_host_ref``, ``kehillah_invited_in_reach``)
    by ``kehillah_host_outlook_watch_effect``.
- **Opinion (Daniel 2026-10-13: "have opinion of Jews run from -50 to +50 ... directly on
  opinion"):**
  - **The rule:** a lord's opinion of a Jewish leader carries his outlook on the Jews, capped at
    ±50. It is an opinion modifier (``kehillah_outlook_opinion``), shown in the opinion breakdown as
    "Outlook on the Jews: +25".
  - **Which lords:** for every community, its host and the lord of its county. For a player's
    community, also every Christian or Muslim duke or greater within diplomatic range.
  - **Refresh:** yearly, at game start, and quarterly for a player's host. The old modifier is
    removed and the current value added.
  - **Effect:** typical lords (+5 to +45) offset much of vanilla's faith-hostility penalty (astray
    -10, hostile -20, evil -30). Cold and hostile ones add to it.
  - **Knock-on:** it feeds the host-attitude opinion tiers, the review's patron trigger, and the
    Shtadlan's choice of lord.
  - **Two first builds that did not work** (2026-10-13): five steps, then 21 steps of vanilla's
    ``judaism_religion_opinion``. That modifier is how *Jews* view the holder (the Bells of Santiago
    use ``islam_religion_opinion``), so the lord's opinion never moved. There is no "opinion of
    religion X" character modifier, hence one modifier per pair of lord and leader.
  - **The character-window band marker** stays display-only.

## The outlook's breakdown (added 2026-10-13)

Daniel: "It would be good to be able to see what's contributing to a character's Jewish outlook."

- **Why not in the opinion breakdown:** a vanilla opinion breakdown lists each modifier as one
  "Name: value" line, with no hover or sub-bullets. Splitting the outlook into one opinion modifier
  per source would add up to nine lines to every lord's opinion of every Jewish leader. So the
  opinion keeps one "Outlook on the Jews" line, and the breakdown is shown where the mod writes
  the text.
- **The sources** are now separate values (``kehillah_outlook_<source>_value``), summed by
  ``kehillah_outlook_on_jews_value`` with the same numbers as before: teaching, zeal, character,
  learning, Jews in their service, debts, Jewish friends and rivals, crusade, and history (personal
  shifts and sermons).
- **Bullets** (``KehillahOutlookBd<Source>``, one per non-zero source, green or red) appear in:
  - the "Your Host" tooltip on the community strip;
  - "The Lord Grows Warmer" and "The Lord Grows Colder" notices.
