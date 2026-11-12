# Standing on one scale: twelve tiers, no bands, no Class

**Status: BUILT 2026-11-11, xTiger-clean, not live-tested.** Daniel's decision of 2026-11-11.
Supersedes, in content, [2026-11-08-sefer-system-redesign.md](2026-11-08-sefer-system-redesign.md)
§3.1 (canon tiers), §3.2 (the ten-tier ladder), §3.4's gate table, and the bands and Class added
on 2026-11-10 (`KEHILLAH_STANDING_BAND_*`, `KEHILLAH_SEFARIM_CLASS_TT`). Everything else in §3
(reception, ceilings by tenet status, floors, per-rite storage) stands.

## Why

Daniel, 2026-11-10/11: the tiers were "not so intuitive". There were three scales on one book:
a fixed **Class** (Foundational … Obscure), a per-rite **Standing** of fourteen levels, and six
**bands** grouping them, with "Obscure" on two of them. The system should also read as general
enough to hold non-Jewish and secular works, and Muslim or Christian libraries, one day.
Daniel's own list of tiers, below, replaces all three; "the simplicity of just one scale is worth"
dropping the bands.

## The scale

One number per work per rite, `var:kehillah_standing_<work>` on the rite, read through
`kehillah_lib_standing_<work>` (the viewer's rite) and `kehillah_lib_rite_standing_<work>`.

| # | Tier | Meaning | How a work gets here |
|---|---|---|---|
| 11 | **Divine** | God's own words (the Torah; for Islam the Quran) | doctrine only |
| 10 | **Prophetic** | the Prophets and Writings (for Islam, the hadith) | doctrine only |
| 9 | **Foundational** | not prophetic, but canonical and essential to the rite's practice (Mishnah, the Talmuds) | doctrine only |
| 8 | **Authoritative** | not the main text, but a serious authority owed deference (Onkelos, the Halakhot Gedolot) | earned; the top of the climb |
| 7 | **Esteemed** | respected everywhere, though parts may be disputed (Midrash Rabbah, the Tosefta) | earned |
| 6 | **Celebrated** | praised and possibly authoritative; the consensus is still out | earned |
| 5 | **Popular** | read and known, without the praise | earned |
| 4 | **Obscure** | little known or studied; where most new books start | — |
| 3 | **Contested** | some find parts of it problematic or offensive | points fall |
| 2 | **Rejected** | judged too riddled with errors to be of value; reading it is not forbidden | points fall |
| 1 | **Banned** | its ideas are deeply problematic; reading it draws suspicion | points fall |
| 0 | **Anathema** | a danger to the faith, cut off by a formal act | an act only |

Mapping from the old scale: 1–7 keep their numbers (Banned, Suspect → Rejected, Contested,
Obscure, Circulating → Popular, Respected → Celebrated, Esteemed). Old 8–10 (Classic,
Authoritative, Venerated) become 8 Authoritative; old canon 11–13 become 9–11. The old computed
0 ("Rejected Tradition", outside a rite's canon) becomes **2 Rejected**: the Talmud for a Karaite,
the Prophets for a Samaritan. Old saves are remapped once
(`kehillah_standing_one_scale_rite_effect`, from `kehillah_sefer_migrate_save_effect`).

Colours group neighbouring tiers without naming the groups: purple for 9–11, gold for 7–8, green
for 5–6, grey for 4, light red for 2–3, red for 0–1.

### Assumptions recorded (conservative choices, reversible)

- **Canon is still by tradition, not yet by rite.** Daniel's idea that the Yerushalmi is
  Foundational for a Minhag Yerushalmi rite but Authoritative elsewhere, and that Anan's works
  are Foundational for Karaites, needs canon per rite. The Yerushalmi stays Foundational for every
  Rabbinic rite and Anan stays at Authoritative for now.
- **No climb into Foundational yet.** A synod, Sanhedrin or rite reform that makes a work
  Foundational for its rite (the Zohar's path) is proposed, not built.
- **Anathema.** Only a Machloket the critics overwhelmingly win pronounces it (today's
  "overwhelmed, it is banned" outcome). It holds for `kehillah_anathema_years` (30), whatever
  its points or floor; then the work may rise to Banned like any other.
- **Ceilings by tenet status**, shifted onto the shorter top: prohibited 3 Contested, unknown 5
  Popular, known 6 Celebrated, permitted 7 Esteemed, core 8 Authoritative. Arguing against a core
  tenet still takes two off. A book in its author's vernacular: no royal court 6, a court 7, a
  great court 8.
- **Class is gone from the UI.** The catalog's `rank_name` still orders the shelf and decides
  which works every rite knows; it is no longer shown.

## Gates (reworked from §3.4)

*Superseded the same day by [2026-11-11-rulings-sermons-and-gates.md](2026-11-11-rulings-sermons-and-gates.md)
§1 (built): Popular and Celebrated from points alone, Esteemed by masters, Authoritative by genre.
The table below is the first version, kept for the record.*

A work's **points** (reception, 0–100) set the tier it is heading for: points ÷ 10 + 1, between
its floor and ceiling. Once a year it moves one tier toward that target. **Falling** needs only
five straight years below target. **Rising** past Obscure also needs that tier's **gate**: a
fact about the world that points alone cannot buy.

| To rise to | Gate |
|---|---|
| Banned (from Anathema) | 30 years since the anathema |
| Rejected, Contested, Obscure | none |
| Popular | copies in 2 libraries |
| Celebrated | mastered by 3 scholars, or an approbation |
| Esteemed | taught at yeshivot twice; copies in a third of the libraries; 10 years old |
| Authoritative | cited in 3 rulings; endorsed; a commentary written on it; 30 years old; its author dead |

Each gate is the meaning of its tier: Popular is *read*, Celebrated is *praised*, Esteemed is
*taught*, Authoritative is *relied on*.

**Proposed, not built:** the work card shows the next gate as a checklist (✓/✗ per condition),
with a bar for points toward the target and the ceiling's cause. See ROADMAP.

## Addendum, later 2026-11-11 (Daniel)

- **Other traditions are Obscure, not banned, to a Jewish faith of neither tradition.** The Beta
  Israel and the Samaritans now start every Rabbanite or Karaite work at 4 Obscure (was its lower
  baseline less one, often Banned), and the Oral Torah reads Obscure to them (Rejected stays for
  Karaites). Older saves are repaired once (`kehillah_standing_other_faiths_obscure_rite_effect`).
- **The library's Greatness follows its books' standing** (`kehillah_bd_library_works_value`, a
  Greatness breakdown row):

  | Standing | Greatness per book |
  |---|---|
  | canon | +2 |
  | Authoritative | +5 |
  | Esteemed | +4 |
  | Celebrated | +3 |
  | Popular | +2 |
  | Obscure | +1 |
  | Rejected, Contested | 0 |
  | Banned | −4 |
  | Anathema | −8 |

  The total is held between −40 and +80. To make room, the Greatness floor drops from 60 to 30.
