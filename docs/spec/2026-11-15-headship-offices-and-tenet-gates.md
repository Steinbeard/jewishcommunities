# Headship offices and tenet gates

**Status:** 2026-11-15. Part 1 (tenet gates) BUILT for the Sanhedrin, source- and xTiger-checked,
live test pending. Parts 2–4 are a PROPOSAL, not implemented, with open questions for Daniel.
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

## 3. Restore the Kohen Gadol (proposal)

The second step after Restore Temple Service (which already grants Temple Service): a ruler of
Jerusalem with the restored service, a Kohen, and the Kohen Gadol gate. It sets the Kohanim
doctrine; if the faith has no head, the high priest's title becomes the head (section 2).

## 4. Declare the Mashiach (proposal)

A rare success branch of the existing Messianic Mission reckoning, not a separate decision. It
needs Jerusalem and the kingship of Israel; false messiahs stay the usual outcome. On success the
Mashiach heads the faith for accepting rites (section 2, point 5).

## Open questions for Daniel

1. With a Mashiach reigning, does an existing Sanhedrin or Kohen Gadol lose its head-of-faith title
   or keep it as a subordinate office?
2. Should the Mashiach need Davidic descent, and if so how is it represented?
3. Backlash size: opinion only, or a real schism risk?

## Risk

Changing who holds the head-of-faith title touches the title-history and succession code that has
crashed the game before ([implementation doc](../implementation/v1-kehillah-implementation.md)
sections 6 and 8; V47's seat transfer). Parts 2–4 need a live playtest before they count as done.
