# V46: The Sanhedrin

**Status:** Daniel's request, 2026-10-19. Built and checked with `ck3-tiger`. **Not live-tested.**
This is title and succession code, the highest-risk area in this mod, so it is not done until a
live pass (§7) succeeds. **Supersedes** [v45](v45-rabbinic-synods-and-minhag-ashkenaz.md) §8's
"head of the Sanhedrin" (a seat variable on Jerusalem at game start). That is removed.

## Daniel's requirements

1. The Sanhedrin is a potential Rabbinic **head of faith**, restored only through a very
   difficult **decision**.
2. To restore it you must be a **master of all three rabbinic tracks** and at the **top piety
   level**.
3. It is **its own title**, with an **election like the College of Cardinals**, the electors
   being sitting rabbis.
4. It does **not exist at any game start**.
5. The Sanhedrin intent is **shown to everyone** and explains that you must be its head. Early
   players should see that this end-game content exists.
6. The Synod intent may show for the head, but **should not be selectable** by them.

## 1. The title

- **`d_kehillah_sanhedrin`** (`common/landed_titles/kehillah_sanhedrin_landed_titles.txt`).
  - A landless duchy, the same tier as every Kehillah, with its capital at Tiberias.
  - No history, so it is never created at game start.
  - `destroy_if_invalid_heir`, so it lapses if no member can succeed.
- **The holder, the *Nasi*, keeps his community as primary title.** Pillars, domicile and
  succession all read `primary_title`. This uses:
  - the PAM cardinal never-primary score (`ai_primary_priority -1000`);
  - `set_primary_title_to` after every grant;
  - `kehillah_sanhedrin_on_title_gain`, which does the same for an elected successor and
    removes his own seat.

**Where it sits (Daniel, 2026-10-19, same day):** the Sanhedrin can be restored anywhere, for
example by "a really influential rabbi in Toledo", and it can move.
`kehillah_sanhedrin_sit_with_nasi_effect` sets the title's capital to the Nasi's community. That
is the community title's capital county, falling back to the Nasi's own capital county, then to
his location. The effect runs at restoration and on every new Nasi's `on_title_gain`, so the
court moves to wherever the new Nasi leads, as it historically moved from Yavne to Usha to
Tiberias. New seats take the same capital. Tiberias is only the title's placeholder capital.
There is no separate "move the court" action: the court moves when its Nasi changes.

**The Nasi's style (Daniel asked, 2026-10-19):** Daniel would like the Nasi's primary title to
be the Sanhedrin. That is deliberately **not** done.
- **Why not.** The mod reads `primary_title` about 1,300 times across 167 files, and pillars,
  the domicile, appointment succession and player continuation all assume it is the community.
  Swapping it would be a large refactor in the mod's highest crash-risk area.
- **What was done instead.** The Nasi is styled **"Nasi"**: `kehillah_nasi_male/female`
  flavorization at priority 310, above Rav, Rabbenu, Gaon and Exilarch, driven by
  `kehillah_nasi_flag` in `kehillah_update_leader_flavor_effect`. The flag is refreshed at
  restoration, on a new Nasi's title gain, and by the existing pulses.
- **Revisit** only if "Nasi <name>" alongside his community proves not to be enough. A real
  swap would first need an audit of every primary-title reader.

## 2. Restoring it

`kehillah_restore_sanhedrin_decision`, a major decision.

- **Shown** to every Rabbinic Kehillah leader while no Sanhedrin exists, so the goal is visible
  early.
- **Valid** when all of these hold:
  - you have mastered all three Rabbi trait tracks: Parshanut, Talmudics and Hashkafa, at 100
    each;
  - `piety_level >= 5`;
  - at least `kehillah_sanhedrin_founding_members` other rabbis lead communities;
  - the faith has no head.
- **Cost:** piety and prestige.
- **Effect** (`kehillah_restore_sanhedrin_effect`):
  1. Create the title for the founder and restore his primary title.
  2. Add `kehillah_sanhedrin_succession_law`.
  3. Set the main rite to `doctrine_spiritual_head`. The head-of-faith doctrine group is
     `main_rite = yes`, so this applies faith-wide, Minhag Ashkenaz included.
  4. `set_religious_head_title`.
  5. Grant Greatness, seat the members, and announce it to every player.

## 3. The members (the College)

This is vanilla's cardinalate pattern (`11_dlc_pam_scripted_effects.txt`).

- **A seat** is a dynamic landless duchy, "Sanhedrin Seat of <name>". It is destroyed on
  succession and marked `add_clerical_elector = faith:rabbinic_faith`.
- **Who is seated:** rabbis (`kehillah_rabbi_trait`) who **lead a community**. The engine allows
  only rulers to be electors, and giving a courtier a title would make them a landless ruler, a
  structural change this design avoids. Seating is automatic at restoration and refreshed
  yearly, up to 70 seats, after the Great Sanhedrin of seventy-one.
- **Two vanilla hazards, both handled:**
  - **The strip.** PAM strips an elector title from any ruler who is not a theocracy or holy
    order. It does this on title gain, on every government change and in the yearly pulse, with
    no faith check. `kehillah_pam_strip_cardinalate_override.txt` overrides the effect verbatim
    and adds a Kehillah exemption. This is the only vanilla override in this feature.
  - **The cardinal flag.** On `on_title_gain`, vanilla treats a gained elector title as a
    cardinalate: it sets the cardinal flag and enrols the holder in the Christian Church
    situation. A seat is therefore marked as an elector only *after* the transfer resolves.
- **Lost seats.** Vanilla destroys an elector title when its holder changes rite, for example
  when Minhag Ashkenaz is founded after the Sanhedrin. The yearly refresh re-seats them.
- **Not added:** the `special_doctrine_has_clerical_electors` doctrine. It switches on PAM's
  vacancy-filling and seed-cardinal logic, which is Catholic-shaped.

## 4. The election

- **`kehillah_sanhedrin_succession_law`**, a title law: election, `faith = same_faith`.
- **`kehillah_sanhedrin_elective`**: electors and candidates are both
  `same_faith_clerical_electors` (the seat holders). Candidates must also be adult, capable
  rabbis.
- **AI scoring:**
  - a self-vote;
  - Learning, weighted three to one;
  - piety level;
  - Theologian;
  - Talmud mastery;
  - the same minhag region;
  - opinion;
  - the dying Nasi's preferred successor.

## 5. Lapse

The title is `destroy_if_invalid_heir`. When no successor is valid, the yearly
`kehillah_sanhedrin_lapse_check_effect` resets the main rite to `doctrine_no_head`, destroys the
seats, and tells Rabbinic players. The decision can then be taken again.

## 6. The intents (revises v45 §8)

- **Sanhedrin intent.** Shown to every Kehillah leader. Valid only for the Nasi; the tooltip says
  you must be Nasi and that the Sanhedrin can be restored. Its other requirements are unchanged.
- **Synod intent.** Shown to everyone, but unselectable by the Nasi ("you convene the Sanhedrin
  instead").
- **Delegates, binding and the herem for all Israel** are as in v45 §8.

## 7. Live pass needed (not yet run)

Run on a fresh 1066 boot, as Worms.

1. **Nothing exists at start.** `kehillah_synod_debug.5` should report no Sanhedrin and no
   faith head. The Bet Din planner shows the Sanhedrin intent greyed with its tooltip, and the
   decision is visible but invalid.
2. **Restore it.** Run `kehillah_synod_debug.4` on the Worms leader. Ensure at least four other
   community leaders are rabbis (add the trait in the console if needed), then take the
   decision.
3. **Check after restoring**, with `.5` and the UI:
   - the Sanhedrin exists and the faith has a head;
   - seats exist;
   - **the Worms leader's primary title is still the community**;
   - the Faith window shows the head;
   - no seat holder has `cardinal_flag` or is in the Christian Church situation.
4. **Seats survive a year.** Advance past 1 January: they are still there (the override).
5. **Succession.** Kill the Nasi. An election by members should give the title to a member,
   whose own seat is removed and whose primary title is still his community. Player
   continuation at Worms should be unaffected.
6. **`error.log`** shows no new kehillah lines.

**If electors come back empty:** the fallback is to make the members claimants of the title
(the `title_claimants` set) instead of clerical electors. Record it in a dated addendum.

## 9-10. Head of faith and government: what the live tests settled (2026-10-19)

Full record: [the live test log](../testing/2026-10-19-synod-sanhedrin-live-test-log.md).

- **The engine rule.** CK3 forces a **landless head of faith** onto the faith's theocracy
  government (vanilla `theocracy_government` for Rabbinic Judaism). This happens whether the head
  is spiritual or temporal, with theocratic or lay clergy, and whatever the title's landless flag.
  The Kehillah government is then refused as illegal. The domicile is lost, and the player gets
  Game Over. The community's succession also breaks: titles were left vacant.
- **Shipped (73ce2de, live PASS).** `kehillah_sanhedrin_apply_head_link_effect` decides per Nasi:
  - **a landless Nasi (a community rabbi):** no engine head, `doctrine_no_head`, the Kehillah
    government kept. Title, election, seats, the Nasi style, intents and takkanot all work;
  - **a landed Nasi (a king):** the Sanhedrin is a temporal head of faith with lay clergy, on the
    Caliph's model. This path is untested.
- **`kehillah_nasi_government` is defined but unused** (reconcile rule 1 is behind
  `always = no`). The diagnostic showed the engine ignored the **faith-level**
  `theocracy_government_type`; vanilla sets it only at **religion level**. A religion-level
  setting is the one untried route to making a rabbi-Nasi a true head of faith. It would also
  reach Karaite, Samaritan and other Jewish theocracies, so it needs its own design (for example
  widening the Nasi government's `can_get_government`, or per-faith handling) and a live test.
- **Tried and ruled out:** temple land for Kehillah leaders. Holding a barony destroyed the
  community title (`require_landless`), forced theocracy, and made the leader the Kaiser's vassal.
