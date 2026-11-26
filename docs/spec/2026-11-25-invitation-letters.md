**Status:** 2026-11-26. Slices 1 and 1b built; the personal-lead path of slice 4 is source-built,
**not live-tested**. Slices 2-3 remain proposals. Revises the invitation letter of [V34 section 7](v34-outlook-teachings-and-founding.md),
[V35](v35-player-clarity-outlook-and-invitations.md) and V44, and the decision in
[the Nagid spec, section 6](2026-10-30-the-nagid.md). The Send Out Settlers decision (V34 section 1)
stays as the route for an overcrowded quarter.

# Invitation letters: a named place, an answer in the letter

## Why

Daniel, 2026-11-25: the invitation "feels a little weak" next to the newer systems. The letter
only pointed at a decision. The player had to find the decision, meet its requirements, guess its
costs and click it. The decision's motive (an overcrowded quarter) was also not the letter's motive
(a lord asking for settlers). Decisions (Daniel):

- The answer belongs in the letter itself.
- The letter should read as the ruler's own: his reason, his promises.
- It should name one place, a county in his own domain, and say how suitable it is.
- "Welcome news" and "write to thank him" are one option.
- To keep many communities from answering at once, a call goes to a few nearby communities.

## Slice 1 (built 2026-11-25)

**The call.** When a ruler issues an invitation (`kehillah_invitation_issue_effect`: the open-door
review, the Invite Jewish Settlers decision, the Norman invitation), he also names a county.
That county is the best founding site in his own domain (`kehillah_invitation_site_score_value`:
prosperity, his capital, a city). It falls back to the rest of his realm if his domain has none.
The county is stored on his realm title as `kehillah_invitation_county`, for
`kehillah_invitation_call_years`. The realm-wide 20-year `kehillah_invitation_open` is unchanged:
exiles, adventurers and the old decision still read it.

**Who hears it.** The three communities nearest the named county (within `squared_distance_large`)
are called by name. A player community gets the letter as an event. An AI community decides in a
hidden event 1-8 months later, so a player always has time to answer first. Other Kehillah players
in diplomatic range get the feed news, as before. The old once-in-ten-years letter limit is gone:
only the nearest three get the letter now.

**First answer founds it.** The call closes when a community is founded in that county by any route
(`kehillah_invitation_answered_effect`). A later answer is refused because the site is taken. A
letter's send options stay visible but greyed, with the reason, once the call has closed.

**The letter** (`kehillah_invitation.0001`) is built from parts:

- the opening;
- his reason (`kehillah_policy_reason`: credit, towns, justice, a Shtadlan's petition, a plea, a
  decree; refugees from a neighbour's expulsion);
- his promises, which depend on his outlook and character (a protector, a greedy ruler, a zealous
  one, or the plain charter);
- the place: the county's prosperity, whether it is a market town, a castle town or rural, and how
  far it is from the quarter;
- whether our own quarter is crowded or has room;
- his outlook band.

The Norman letter keeps its own opening.

**The options:**

1. **[X] volunteers to lead families to [County]**: one option naming the strongest eligible
   courtier by Stewardship and Learning (revised 2026-11-26; Send Out Settlers retains its
   separate leader choices). Costs:
   `medium_gold_value` gold, and the party leaves the quarter. The party is the leader's household
   and others, at least `kehillah_invitation_party_min` people, or the whole overflow if more. Gains:
   Greatness (major), prestige (medium) and the inviter's opinion. The new community starts with the
   invitation's privileges (unchanged). The founding runs in a hidden event (`kehillah_invitation.0021`),
   never inside the option, because the tooltip dry-run crash of 2026-10-13 applies here too.
2. **"Welcome news. Write to thank [him]."**: the old thank-you, merged with "let them consider it."

## Slice 1b: adventurers and merchants (built 2026-11-25)

Daniel: "Can we have the ruler send invites to adventurers and merchants too?" The same call also
reaches the 2 nearest Jewish adventurers and the 2 nearest Jewish merchant companies (vanilla
`merchant_government`), within `squared_distance_large` of the county. They get the same letter,
with their own opening and a line about their band or house.

- **An adventurer** who could found a community (a rabbinic leader, the Found a Jewish Community
  rules) gets **"Take the band to [County]."** It earns the lord's opinion and minor prestige. The
  band travels there. On arrival a player gets `kehillah_invitation.0011`: found the community now
  for **half** the decision's cost (the lord's promise), or wait and use the decision later at full
  cost. The founding is the decision's own `kehillah_found_community_here_effect`, run from a hidden
  event (`.0012`). That keeps the adventurer-scaffold path the decision already uses, and no
  `change_government`. An AI adventurer travels with the old V44 arrival event (`.0010`), whose
  flag makes his founding decision weigh +100. The call is remembered as
  `kehillah_invited_to_county` for `kehillah_invitation_call_years`.
- **A merchant** gets **"Send [factor] with families of our house to [County]."** It costs the same
  gold as a community's answer and gives prestige and the lord's opinion, with no Greatness: a
  merchant company has no pillars. The merchant stays a merchant. His best Jewish courtier founds the
  community, with his household and up to 4 Jewish families of the company
  (`kehillah_invitation_merchant_go_effect`, through the same `kehillah_found_with_founder_effect`).
  No mother community is recorded: that effect now skips `kehillah_mother_community` when there is
  no mother title.
- AI chances when their turn comes: adventurer 50%, merchant 30%
  (`kehillah_invitation_ai_band_chance`, `kehillah_invitation_ai_merchant_chance`). The first founding
  still closes the call, by whatever route.

Not built: a merchant answering with trade instead of settlers (a factor's house or trade post in
the county). That needs the 1.21 trade hooks and is a slice of its own.

## Live checklist (slice 1)

Fire `event kehillah_outlook_debug.18` as a Kehillah player (Worms 1066). The nearest independent
duke or greater outside your host's realm issues an invitation; his realm is raised to Allowed if
needed. Check `debug.log` for the named county and whether you were among the three nearest.

1. The letter shows: the opening, the reason ("towns" from the debug event), the promises, the
   named county with its description, the distance, the quarter line, and the outlook band. No
   blank `[...]` and no missing text.
2. The volunteer option names the county and the leader. The tooltip shows the gold, the party size (at
   least 4), Greatness: Major bonus, prestige and the lord's opinion. Options are greyed with a
   reason when gold, Affluence or the cooldown fail.
3. Take a send option. A new community appears in that county, the leader and the party leave the
   quarter, and the invitation news reports it answered. `error.log` stays clean, with no
   null-title flood (the tooltip-dry-run crash of 2026-10-13).
4. Fire `.18` again with the same lord: the call closed when the community was founded, so a new
   call names a different county.
5. Thank option: the lord's opinion and prestige.
6. AI: after a few months in game, check `debug.log` for `kehillah_invitation.0020` lines and that
   only one community was founded per call.
7. As a Jewish rabbinic adventurer near the lord (or with `.18` fired from one): the letter shows the
   band opening and the **Take the band** option. Taking it starts the journey. On arrival `.0011`
   shows; the found option lists the half cost and the ten-followers rule. Founding gives a working
   Quarter, and the camp is not lost (watch for the "lost all titles" Game Over 15-25 days later).
8. As a Jewish merchant: the merchant opening and the **Send [factor]** option. After it, the factor
   holds a new community in the county, and the merchant company is unchanged.

## Proposed next slices (not built)

- **Slice 2, pledges and joint foundings.** Answers become pledges that set a gathering date. Every
  called community that pledges before it adds families. The founder comes from the largest party,
  and each contributor gets a share of the Greatness.
- **Slice 3, the inviter's side.** A player ruler picks the county (a picker, not the automatic
  best), sees which communities the call reaches, and gets an event when settlers come, with a
  choice of charter terms. If the call lapses unanswered, he is told. **Local lords** (vassals) may
  issue a smaller call for their own counties when the top liege's Status of the Jews is at least
  Allowed.
- **Slice 4, "I will lead them myself" (source-built 2026-11-26; live probe pending).** The
  player leaves the old Kehillah to its appointed Jewish successor and personally founds the
  new one with close household members. The same invitation cost, Greatness, prestige and
  ruler opinion apply. The old title transfer uses the existing `change_title_holder` pattern;
  the founding uses `kehillah_found_with_founder_effect` from a hidden event so tooltip
  evaluation cannot create a title. This is a high-risk title/domicile transition: verify both
  domiciles, player assignment, primary titles, registry and error.log on a disposable save
  before treating it as live-safe. The isolated tester could not verify CK3 process ownership
  in the 2026-11-26 session, so no live result is claimed.

**2026-11-26 letter edit.** The opening, motives, promises, site, distance and closing were
condensed, then given a little more voice after Daniel's screenshot showed spare room in the text
pane. A live visual check at 1440p is still needed to confirm it does not scroll for the longest
realm and ruler names. The option tooltips retain the detailed mechanical consequences.
