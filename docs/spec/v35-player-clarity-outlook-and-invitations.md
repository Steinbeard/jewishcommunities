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
- **Opinion (Daniel 2026-10-13: first "mostly it should mitigate the evil religion modifier, except
  for the lowest outlook tiers", then "have opinion of Jews run from -50 to +50 ... directly on
  opinion"):**
  - **The rule:** a lord's opinion of every Jewish character (vanilla ``judaism_religion_opinion``)
    equals his outlook on the Jews, capped at ±50.
  - **Steps:** a modifier holds a fixed number, so there are 21 modifiers in steps of 5
    (``kehillah_jews_opinion_m50`` .. ``p50``), truncated toward zero so each step's band name matches
    its band.
  - **How it reads:** the character window shows "Outlook on the Jews: <band>". The opinion
    breakdown shows the same line with its value.
  - **Effect:** typical lords (outlook +5 to +45) offset much of vanilla's faith-hostility penalty
    (astray -10, hostile -20, evil -30). Cold and hostile lords add to it.
  - **Knock-on:** a host's opinion of a community leader now carries his outlook. That feeds the
    host-attitude opinion tiers and the review's patron trigger.
  - **Superseded:** the first build's five-step version (+30, +20, +10, 0, -15).
