# Headship offices and tenet gates

**Status:** 2026-11-15. Part 1 (tenet gates) BUILT for the Sanhedrin, source- and xTiger-checked,
live test pending. Part 3 (Restore the Kohen Gadol) BUILT the same day, xTiger clean, live test
pending. Parts 2 and 4 are a PROPOSAL, not implemented; all three open questions are decided.
Depends on [V47, Gaon and the Seat of the Sanhedrin](v47-gaon-and-the-seat-of-the-sanhedrin.md),
[the messianic, prophetic and Temple tenets](2026-11-15-messianic-prophetic-and-temple-tenets.md)
and [their build record](../implementation/2026-11-15-revival-tenets-and-integration-audit.md).
Supersedes nothing yet; the Sanhedrin gate adds one requirement to V47's Restore the Sanhedrin.

## 1. Tenet gates (Daniel, 2026-11-15)

Each office that can head a Jewish faith is opened by the theology that wants it. A tenet counts
if the character's rite holds it **or** the character holds it as a personal tenet, the rule that
`kehillah_has_messianic_hope_trigger` already uses. **Any one** listed tenet is enough.

| Office | Gate (any one) | State |
|---|---|---|
| Sanhedrin | Iyyun ha-Talmud (`tenet_kehillah_scholarly_study`), Pesak (`tenet_kehillah_pesak`) | BUILT in Restore the Sanhedrin's `is_valid`, and both AI potentials in that file |
| Kohen Gadol | Messianic Hope, Temple Service, Sacred Homeland (`tenet_kehillah_avelei_tziyon`) | Trigger built (`kehillah_kohen_gadol_tenet_gate_trigger`); no decision yet |
| Mashiach | Messianic Hope | Existing mission already gated; declaration not built |

Triggers: `common/scripted_triggers/kehillah_headship_gate_triggers.txt`.

Starting coverage (checked 2026-11-15): Iyyun ha-Talmud starts on Ashkenaz and the Talmud Torah
rites; no rite starts with Pesak; Sacred Homeland starts only on Yerushalmi; Temple Service only
on the Samaritan faith. So none of the gates is near-universal; most rulers need a rite change, a
reform or a personal tenet. The gate is a requirement, not a visibility check, so the goal stays
visible and the tooltip says what is missing. AI rulers seldom pick personal tenets, so AI
restorations become rarer. That is intended.

## 2. Who heads the faith (proposal)

Daniel's idea: **the first office restored while the faith has no head becomes the head**, other
rites may resent it, and an office restored later either exists without headship or the faith
reforms to switch.

### How Christianity handles it

- **In CK3:** each faith has exactly one head-of-faith doctrine (spiritual head, temporal head, or
  none), fixed when the faith is created and changed only by reforming. There is one head title.
  Every other office (patriarchs, archbishops) is an ordinary title under it.
- **In history:** a rival office either submitted or broke the church apart. The Conciliar
  movement claimed a council stood above the pope; Constance (1414–18) ended the Western Schism,
  and the papacy then reasserted supremacy. The Investiture Controversy set emperor against pope.
  Orthodoxy kept several patriarchs, with Constantinople first among equals and the emperor
  convening councils. When rival claims could not be settled, the result was schism (1054) or
  antipopes.

So Daniel's model is CK3's own model with one addition (the backlash), not a convoluted one.

### Recommended shape

1. **Headship follows the first restoration.** Restoring an office while
   `NOT = { exists = faith.religious_head }` makes it the head.
   - Sanhedrin → as built in V47 (`temple_authority_rabbinic_doctrine` already fits).
   - Kohen Gadol → the faith takes vanilla `temple_authority_kohanim_doctrine`, which already
     limits the head's election to male Kohanim (`kehillah_high_priesthood_triggers.txt`). This
     reuses the existing doctrine instead of adding a parallel "headship" doctrine.
2. **A later office sits under the head.** A Kohen Gadol under a Sanhedrin heads Temple service
   only. A Sanhedrin under a Kohen Gadol is his court; in the Second Temple period the high priest
   at times presided over it. Neither is a head-of-faith title.
3. **Switching is a reform**, through the existing reform/synod machinery, not a free decision.
4. **Backlash:** rites that hold the losing office's gate tenets take an opinion penalty toward the
   head and gain schism pressure. Rabbinic rites with Pesak or Iyyun ha-Talmud resent a Kohen
   Gadol; Temple-minded rites resent a court of sages.
5. **The Mashiach is the exception.** A recognized Mashiach is above both offices for every rite
   that accepts him; no doctrine is needed. The backlash is rejection: rites that deny him treat
   his followers as a heretical movement (the Sabbatean pattern). The existing three-year
   reckoning decides most claims against him.

## 3. Restore the Kohen Gadol (BUILT 2026-11-15; xTiger clean, live test pending)

The second step after Restore Jerusalem's Temple Service. Files:
`common/decisions/kehillah_kohen_gadol_decisions.txt`,
`common/scripted_effects/kehillah_kohen_gadol_effects.txt`,
`common/on_action/kehillah_kohen_gadol_on_actions.txt`, triggers in
`kehillah_headship_gate_triggers.txt`, loc `kehillah_kohen_gadol_l_english.yml`, debug events
`events/kehillah_kohen_gadol_debug_events.txt`.

**Requirements.** Shown to a landed Jewish ruler (not Gerizim-tradition) once Jerusalem's
service is restored and no High Priesthood exists. Valid with the gate tenet, Jerusalem held with
a same-faith population, no war, piety level 4, and a way to seat a Kohen (below). Cost 1,000
Piety and 500 Prestige.

**Who takes the office.**
- A ruler who is a male Kohen takes it himself, as priest-king (the Hasmonean pattern).
- Otherwise a king (kingdom tier or higher) seats his most learned adult Kohen courtier. The
  courtier first receives a temple holding in Jerusalem county that the king holds directly and
  that is not the king's capital. That makes him a theocratic vassal, the way vanilla does it,
  and avoids making a courtier a landless ruler, which can trip the Game Over fuse. The king
  requirement exists because a landless duchy held by a count's vassal would outrank its liege.

**What it does.**
- Creates a landless dynamic duchy, the **High Priesthood**, seated at Jerusalem and marked
  `kehillah_kohen_gadol_title`. This follows vanilla's `d_samaritan` and V47's dynamic Sanhedrin
  title.
- Switches the restorer's rite to vanilla `temple_authority_kohanim_doctrine`. Vanilla's
  temple-authority hostility makes sage-authority rites regard it as astray. This is the first
  piece of the backlash (decision 3); the added opinion penalty and schism risk are not built yet.
- **Head of faith** only for Rabbinic Judaism with no head. It uses V47's proven order (rite head
  doctrine, `set_religious_head_title`, rite head doctrine again): temporal head for a
  priest-king, spiritual head for a theocrat. `kehillah_high_priesthood_faith_trigger` now also
  reads the title mark, so the clerical election picks only Kohanim.
- Otherwise the office sits under the existing head (Karaite, Kabarist and other faiths with
  heads, or a sitting Sanhedrin).

**Lapse (yearly).** If the holder is not a male Kohen of the office's faith (a non-Kohen heir, a
conversion, a lost title), the title is destroyed. If it headed the faith, the faith returns to no
head, the way V47's Sanhedrin lapses. The rite keeps the Kohanim doctrine, and the office can be
restored again.

**Known limits.**
- While the High Priesthood heads the faith, Restore the Sanhedrin stays hidden. It still
  requires no head, so "the Sanhedrin as his court" (section 2, point 2) is not built.
- A subordinate High Priesthood's succession is not forced to a Kohen; the lapse check is the
  backstop.

**Live-test checklist** (disposable save; `kehillah_kohen_gadol_debug.0001` reports state,
`.0002` restores without conditions, `.0003` runs the lapse check):
1. Priest-king: a Kohen ruler holding Jerusalem with the service restored takes the decision.
   Check the High Priesthood exists and he holds it, Rabbinic Judaism's head is him, his rite
   shows the Kohanim doctrine, and `error.log` is clean.
2. Courtier: a Jewish king with a temple holding in Jerusalem county and a Kohen courtier. Check
   the courtier holds the temple holding and the High Priesthood as a theocratic vassal and is
   head of faith.
3. Succession: kill the High Priest (`kill` in the console). Check the successor is a Kohen, or
   that `.0003` makes the office lapse and the faith has no head, with no crash.
4. With a Sanhedrin seated, restore the Kohen Gadol. Check the Nasi stays head and the High
   Priesthood exists under him.

## 4. Declare the Mashiach (proposal; revised by Daniel, 2026-11-15)

Supersedes this section's first draft (a rare success branch that required existing Davidic
descent). A Messianic Mission can **proclaim** someone Mashiach ben David. Proclaiming is easy;
convincing every rite is very hard. History supports this shape: Rabbi Akiva hailed Bar Kokhba,
and Nathan of Gaza proclaimed Sabbatai Zevi. In both cases the lineage was asserted, not
documented, and much of the people believed for a time.

### Proclamation

- During an active mission, the mission's leader proclaims a candidate: himself, or a male adult
  of the promised faith (a prophet hailing a king is the classic pairing).
- The candidate gets a **claim** of Davidic descent (a modifier and flag), not the `ben_david`
  trait yet. The trait is inherited forever, so giving it to every failed claimant would leave a
  Davidic house behind each one. Real `ben_david` descent becomes a strong recognition factor
  instead of a requirement.

### Convincing the rites

Each Jewish rite of the promised faith gives its own verdict before the mission's three-year
reckoning. The rite's head decides (V47 heads of rite); a rite with no head is judged by its
highest-tier ruler. A player in that seat chooses; the AI weighs factors. The weights are shown
through vanilla tooltip modifiers, not prose. The base chance is very low.

| Raises it | Lowers it |
|---|---|
| Candidate holds `c_jerusalem`, and more so `k_israel` | Rite holds Pesak or Iyyun ha-Talmud (Rambam's test: proof by deeds) |
| Candidate truly has `ben_david` | A failed messiah in this faith within living memory |
| Endorsed by a prophet with Prophetic Revelation | Candidate is Deceitful, Arrogant or Craven, or lost the holy-city war |
| A sitting Sanhedrin endorses him | Rite's head is Cynical |
| Rite holds Messianic Hope; many pledges | |

### The reckoning

- **Every rite accepts:** he is Mashiach. He gains `ben_david` and the head-of-faith title. Any
  Sanhedrin or Kohen Gadol continues under him (decision 1 below).
- **Some rites accept:** a messianic movement, the Sabbatean pattern. He is Mashiach to his
  followers only: no trait, no headship. Accepting and rejecting rites become hostile, and the
  backlash question below decides how far that goes. A movement can still win the holdouts by
  deeds. Following Rambam, restoring Temple Service while holding Jerusalem and `k_israel`
  re-runs the verdicts with a large bonus.
- **No rite accepts:** the existing failure (disillusion, stress, disappointed patrons).

## Open questions for Daniel

1. **DECIDED (Daniel, 2026-11-15): subordinate.** When a Mashiach is recognized, an existing
   Sanhedrin or Kohen Gadol loses the head-of-faith title and continues as an office under him
   (the Sanhedrin as his court, the Kohen Gadol over Temple service). The offices survive; only
   headship moves.
2. **REVISED (Daniel, 2026-11-15, later the same day): proclaimed, not pre-existing.** A mission
   can proclaim a candidate ben David, and full recognition grants the trait (section 4).
   Existing descent is a strong factor, not a requirement. The superseded decision follows.
   **Superseded: Davidic descent is required.** It uses the existing
   `ben_david` trait (`common/traits/kehillah_traits.txt`): inherited from the acknowledged
   father by sons and daughters, never randomly created, and available in the ruler designer.
   The claimant must be a male `ben_david`. At the 1066 start the trait sits on four historical
   characters, one in `baghdad_1066.txt` (the Exilarch's line) and three in
   `kehillah_historical_families_1066.txt`, so a Mashiach comes from a small set of houses, a
   designed ruler, or a line that marries in through a Davidic father. This is deliberately
   rare. The existing Messianic Mission stays open to anyone with Messianic Hope; only the
   declaration branch needs the lineage. A non-Davidic leader's mission can still succeed as a
   holy-city recovery without making him Mashiach.
3. **DECIDED (Daniel, 2026-11-15): opinion and schism risk.** Applies to a contested head
   (section 2, point 4) and to a partially recognized Mashiach (section 4).
   - **Opinion:** rulers of a rite that rejects the head (or the Mashiach) take an opinion
     penalty toward him and toward rulers of rites that accept him, and the reverse. Sized like
     vanilla's faith-hostility opinions, not stacking per verdict.
   - **Schism risk:** in a rejecting rite with enough believers (pledged patrons and rulers who
     hold Messianic Hope or the winning office's gate tenets), a yearly chance splits them into a
     new rite. Reuse the Machloket mechanism (`kehillah_machloket_effects.txt`): vanilla
     `create_dynamic_rite`, with Messianic Hope (or the office's gate tenet) as a core override.
     The chance rises with the believers' share and the years the dispute lasts.
   - **The split ends** when the dispute does: full recognition, or the Mashiach's death,
     conversion or disgrace (the Sabbatai Zevi ending). Existing split rites remain; opinion
     penalties expire.

## Risk

Changing who holds the head-of-faith title touches the title-history and succession code that has
crashed the game before ([implementation doc](../implementation/v1-kehillah-implementation.md)
sections 6 and 8; V47's seat transfer). Parts 2–4 need a live playtest before they count as done.
