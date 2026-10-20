# V45: Rabbinic synods and Minhag Ashkenaz

**Status:** Daniel's request and decisions, 2026-10-18. Built: the rite, the 1066 synod and the
Second Wife fix. The synod tiers were revised on 2026-10-19 (§8): they are now Synod and
Sanhedrin intents of the Bet Din, replacing §3's separate activity. Nothing here is live-tested
yet (§7).

**Answers, and so closes,** [v25](v25-by-god-alone-adaptation-proposals.md) §12 questions 6-8 (rite
compat level, synod binding unit, the herem no-op). **Supersedes** the doctrine effect of
[v5](v5-bet-din-conference.md) §8's case 3, "The Second Wife" (§4 below). Builds on v25 §6-7 (P8,
P7). Their research on how 1.20 rites work still stands. Leaves v5's ordinary Bet Din unchanged
otherwise.

## Decisions (Daniel, 2026-10-18)

1. **The synod founds Ashkenaz.** Vanilla `rabbinism` stays the general Rabbinic rite (Sepharad,
   Bavel, Italki, Romaniote and so on). It permits polygamy again in a 1066 start. A new rite,
   **Minhag Ashkenaz**, is founded by the synod and is monogamous.
2. **The 1066 event is a renewal, not Gershom's own synod.** The herem dates to around 1000 at
   Mainz, and Gershom died in 1028. In 1066 his students' successors ratify his ordinances.
3. **Marriage is the only real doctrine a synod changes.** Every other takkanah is
   community-level: title variables and pillar effects.

## History the design rests on

- Rabbenu Gershom's takkanot, traditionally c. 1000-1030, Mainz: no second wife; no divorce
  against the wife's will; no reading another's letters. They bound **Ashkenaz**. Sephardi,
  Yemenite and Babylonian communities did not adopt the ban. Sephardi ketubbot often added a
  clause in which the husband swore not to take a second wife: a contract, not a herem.
- In 1066, Isaac ben Judah heads Mainz's school and Isaac ben Eliezer ha-Levi heads Worms's. Both
  were Rashi's teachers, and both are in our character history.
- Later synods give the Regional Synod its takkanot. Troyes, c. 1150 under Rabbenu Tam: no
  appeal to gentile courts, and a ban on informers. *Herem ha-yishuv* limited new settlers.
  *Takkanot Shum*, 1220s.

## 1. Rites (engine)

- `minhag_ashkenaz` (`common/religion/rite_types/kehillah_minhag_ashkenaz_rites.txt`):
  `faith = rabbinic_faith`, `create = no`. Its tenets match our Rabbinism override (Legalism,
  Halakha, Talmud Torah), plus `doctrine_monogamy`. Vanilla precedent for a `create = no` rite
  founded in play: Daoxue and the PAM heresy rites (`create_rite_from_type`, then `rite:key`).
- **Game start, for starts on or after 1000.1.1.** Vanilla's `on_game_start` applies the herem to
  the main rite (`game_start.txt` l.32-48). Our `on_game_start_after_lobby` runs later. It sets
  `rite:rabbinism` back to `doctrine_polygamy`, and sets both of vanilla's
  `rabbinicism_accepted/rejected_monogamy` variables on the rite. The yearly check in
  `yearly_on_actions.txt` l.370-433 reads those variables, so it never fires
  `jewish_events.0001`. Pre-1000 starts (vanilla's 867) keep vanilla's own event untouched. The
  mod ships no such bookmark.
- **Founding** (`kehillah_found_minhag_ashkenaz_effect`, run on the founder):
  1. Create the rite, then move `culture:ashkenazi` from Rabbinism to it.
  2. Move every living Rabbinic character into it who either is Ashkenazi by culture, or is a
     Kehillah leader in an Ashkenazi region, or belongs to such a leader's court.
  3. Move Ashkenazi Rabbinic counties too.
  4. Set `global_var:kehillah_minhag_ashkenaz_founded`.
- **Later characters.** Two places create Ashkenazi Jews with a hard-coded `rite:rabbinism`: the
  Norman-conquest founders and the pool repopulation patch. They now call
  `kehillah_apply_ashkenaz_rite_effect`. Ordinary births inherit their parents' rite.
- **Ashkenazi region** (`kehillah_in_ashkenazi_region_trigger`): minhag flag `western_ashkenaz`
  or `eastern_ashkenaz`, or a capital in `e_britannia`. This matches how
  `kehillah_shares_minhag_region_trigger` already treats England.

## 2. The 1066 Rhineland synod (`kehillah_synod.0001`)

- **When and who.** It fires 30 days after the 1066 start for the leader of Worms. Mainz is the
  fallback.
- **Portraits.** The Worms and Mainz leaders.
- **Options:**
  - **Renew both ordinances.** Founds Minhag Ashkenaz and records the divorce ordinance on the
    three Rhineland communities. Stability and Greatness go up. This is the AI default.
  - **Renew the ban on a second wife alone.** Founds the rite. Greatness goes up.
  - **Leave each community to its custom.** Nothing is founded, and
    `global_var:kehillah_gershom_deferred` is set. The Regional Synod can take the herem up
    later. Greatness goes down.
- **News.** Founding notifies other Kehillah players in range through
  `kehillah_notify_region_players_effect`.

## 3. The Regional Synod (`activity_kehillah_regional_synod`)

> **Superseded 2026-10-19 by §8.** The separate activity was removed at Daniel's request. A synod
> is now an intent of the Sitting of the Bet Din, and a Sanhedrin tier sits above it. The
> takkanot table and the vote below still apply. The planner option, the activity's own phase and
> its cooldown do not.

This is a higher tier above the Sitting of the Bet Din. It is a sibling activity, not an option
on the conference, because it needs a different phase and a quorum. It also must not touch the
conference's docket machinery (v5 §11).

- **Who may call it.**
  - A Kehillah leader with a rabbi in post (as the conference requires), who is the
    highest-Greatness leader of their minhag region (`kehillah_is_regional_greatness_leader_trigger`).
  - At least one other community leader of the region (the quorum).
  - At least one takkanah still open to them.
  - A long personal cooldown.
- **Who attends.** The conference's invite rules. The *delegates* are the attending Kehillah
  leaders who share the host's minhag region.
- **The takkanah** is the planner's `kehillah_synod_takkanah` option category, one per sitting:

| Option | Shown when | Binds | Effect |
|---|---|---|---|
| Herem against a second wife | Ashkenazi region, Minhag Ashkenaz not yet founded | the rite | founds Minhag Ashkenaz (engine) |
| Monogamy clause in the ketubbah | host's rite permits polygamy | region's communities | Stability, Greatness |
| No appeal to gentile courts | always | region's communities | Stability |
| Ban on informers | always | region's communities | Stability |
| Herem ha-yishuv | always | region's communities | Prosperity, Stability; Greatness down |
| No reading another's letters | always | region's communities | Stability, Greatness |

  An option a region has already enacted on the host's community is not valid again.
- **Flow.**
  1. **Opening** (`kehillah_synod.0101`, host). The host argues the takkanah with a learning or
     diplomacy `duel`, whose odds the tooltip shows. Success sets a persuasion mark.
  2. **Votes** (`kehillah_synod.0102`), sent two days later to every delegate. AI weights:
     opinion of the host, the persuasion mark, and one personality trait for each takkanah. A
     player delegate chooses.
  3. **Resolution** (`kehillah_synod.0103`), from the activity's `on_complete` after
     `kehillah_synod_debate_days`. There is no self-chaining, so it cannot hang (v5 §11's lesson).
     The host's vote counts. Votes for must exceed votes against. With fewer than the quorum
     present, the synod rises without a ruling.
- **Enacting** (`kehillah_synod_enact_takkanah_effect`) writes the takkanah variable to every
  registered community in the host's region, then applies the pillar effects to the host's
  community through `kehillah_change_pillar_effect`, so the numbers come from script.

## 4. The Second Wife (v5 case 3), corrected

- **Draw.** The case is drawn when the convening leader's **rite** permits polygamy, not the
  faith, and the community has no ketubbah clause yet. It used to need a polygamous *faith*.
  Since 1066 no faith is polygamous, so the case could never be drawn.
- **Effect.** A great "forbid" ruling writes the ketubbah clause to the convening community. It
  no longer edits the faith. Editing the faith now would make every non-Ashkenazi Jew monogamous.
- **Where it fires.** In practice this is Sephardi and other non-Ashkenazi communities, which is
  historically where the question remained live.

## 5. Compatibility

- Every non-Ashkenazi Rabbinic character, landed or not, can again take more than one wife in a
  1066 start. This is a deliberate change to vanilla, and historically correct.
- Other mods that test `rite:rabbinism` will not see Ashkenazi characters once the rite is
  founded.
- Nothing edits faith-level tenet status.

## 6. Not in this pass

- **A lasting pillar term for each takkanah.** That needs a breakdown line in
  `kehillah_breakdown_l_english.yml`, which another session currently has uncommitted edits in.
  Takkanot pay out once, on enactment, for now. The variables are in place for a later baseline
  term.
- **Gameplay hooks for each takkanah.** Examples: herem ha-yishuv against new settlers in
  founding and immigration; the gentile-courts ban in host disputes; the informer ban in
  accusations. All belong in the backlog.
- **Divorce at rite level.** Daniel chose marriage only.
- **The tradition that the herem lapsed in 5000 AM (1240).** A later synod reaffirming it would
  be a good follow-on.

## 7. Verification

See the dated entry in [ROADMAP.md](../../ROADMAP.md) and the test log it links.

## 8. Revision, 2026-10-19: Synod and Sanhedrin as Bet Din intents (Daniel)

Daniel: not a new activity, but "a gated activity intent for the Beit din", and "a Sanhedrin
level above that where you need to be the head of the Sanhedrin to choose it."

- **Three host intents for `activity_kehillah_bet_din_conference`.**
  - **Justice:** the ordinary sitting, unchanged.
  - **Synod** (`kehillah_bet_din_synod_intent`). Shown to everyone except the head of the
    Sanhedrin. It is valid for the highest-Greatness leader of a minhag region with a regional
    quorum.
  - **Sanhedrin** (`kehillah_bet_din_sanhedrin_intent`). Shown only to the head of the Sanhedrin,
    and valid with a quorum anywhere.
  - Both also need an open takkanah, no motion in the last `kehillah_synod_cooldown_years`, and
    prestige for the motion.
  - The requirements are waived once the session opens (`kehillah_synod_in_session`). Otherwise
    the session's own cooldown would invalidate the intent and fire vanilla's "intent lost" event.
- **Superseded 2026-10-19 by [v46](v46-the-sanhedrin.md):** the head of the Sanhedrin is now
  the holder of a restorable head-of-faith title, and nobody holds it at game start. The
  Jerusalem seat described next was removed.
- **The head of the Sanhedrin** leads the community whose title carries
  `kehillah_sanhedrin_seat`. That is Jerusalem at game start: Elijah ha-Kohen's Yeshiva of the Land
  of Israel, which saw itself as the Great Sanhedrin's successor. It is a variable, so a later
  event can carry the seat with the academy to Tyre (c. 1073) and Fustat. That move is not built
  yet.
- **Flow within the sitting.**
  1. Once the docket opens (phase 1, quorum met), `kehillah_synod_open_session_effect` seeds the
     votes, records the level, and starts the cooldown.
  2. A day later the host chooses the motion. It is offered on two pages, so no event has more
     than four choices: marriage (`kehillah_synod.0100`) and communal order (`.0105`). Choosing
     it pays the prestige.
  3. The host argues the motion (`.0101`), and delegates vote (`.0102`) while the cases are
     heard.
  4. The conference's `on_complete` fires the ruling (`.0103`) beside the docket's own close
     (`kehillah_bet_din.0099`). The ruling settles its outcome in `immediate`, while the activity
     still exists.
- **Delegates and binding.** At a Synod, the delegates are the region's community leaders and a
  takkanah binds the region. At a Sanhedrin, any community leader present is a delegate, the
  quorum is `kehillah_sanhedrin_quorum`, a takkanah binds every registered community, and
  passing it adds extra Greatness.
- **Sanhedrin attendance.** The head may seat any community leader
  (`kehillah_bet_din_eligible_judge_trigger`). A new invite rule asks every community leader. The
  planner fixes invitations before the intent is chosen, so this applies to every sitting the
  head convenes.
- **The Sanhedrin's own takkanah, still marriage only.** It is the herem against a second wife
  for all Israel. `change_rite_doctrine = doctrine_monogamy` on the general Rabbinic rite carries
  Gershom's ban beyond Ashkenaz, which history never did.
- **Removed:** `activity_kehillah_regional_synod`, its planner options and icons.
