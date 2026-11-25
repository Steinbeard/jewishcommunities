# Samaritan priestly succession and Jewish cleric names

**Status: BUILT 2026-11-25, xTiger-clean on the new files, NOT live-tested.** Daniel's
request, from a 1066 screenshot. Succession code has crashed this mod before
([v1 implementation](v1-kehillah-implementation.md) §6, §8), so this is not done until the
live checklist below passes.

## The problem

Vanilla's Samaritan High Priest (`d_samaritan`, Simeon I in 1066) is a landless head of
faith, so he gets the vanilla theocracy government. His title followed the default
theocratic succession: the heir in 1066 was Matityahu, a Romaniote court cleric with no
priestly descent.

The Kohen-only filter built 2026-11-15 (`kehillah_high_priesthood_candidate_ok_trigger`
in the copied `theocratic_elective`) never applied. Vanilla gives that election only to
faiths with `special_doctrine_has_clerical_electors`, and the Samaritan faith has none.

Turning that doctrine on was rejected. It would make the office elected by the faith's
clergy. The Samaritan high priesthood was hereditary within the priestly family.

## What was built

- **`kehillah_priestly_succession_law`** (`common/laws/kehillah_priestly_succession_laws.txt`).
  A title law, modeled on the live-proven `kehillah_sanhedrin_succession_law`. It is valid
  on any title marked `kehillah_priestly_succession_title`; only `d_samaritan` is marked
  today.
- **`kehillah_priestly_elective`** (`common/succession_election/`). The holder is the only
  elector, so it works like a designated heir.
  - Candidates are male Kohanim of the holder's faith (`kehillah_priestly_heir_candidate_trigger`),
    drawn from his kin, his council and his faith's clergy.
  - Scoring ranks sons, then brothers, grandsons, nephews and other kin, and prefers the
    eldest adult. Learning breaks ties.
- **Game start** (`kehillah_samaritan_priesthood_setup_effect`):
  - adds the law;
  - makes the High Priest a Kohen;
  - makes every male cleric of his faith at his court a Kohen. A Levite among them loses
    the Levite trait.

  Vanilla's High Priests are lowborn with no recorded family, so this is the seeded
  "priestly family". Their sons inherit the trait.
- **Yearly** (`kehillah_samaritan_priesthood_yearly_effect`):
  - re-adds the law if missing;
  - guarantees an heir the election can reach. If no kinsman or councillor is a Kohen,
    the most learned adult Kohen courtier is made court chaplain. If there is none, a new
    lowborn Kohen cleric is created and made chaplain.

  This matters because `d_samaritan` is `destroy_if_invalid_heir`: with no valid heir,
  the office would end.
- **Cleric trait names** (`common/traits/kehillah_cleric_trait_override.txt`). A copy of
  vanilla's `cleric` trait from 1.21.0.3, with per-faith Jewish branches added before
  vanilla's "Hazzan":

  | Faith | Name | Note |
  | --- | --- | --- |
  | Samaritan | Priestly Elder | |
  | Rabbinic | Talmid Hakham | |
  | Karaite | Maskil | the Karaite sages' own term |
  | Haymanot | Debtera | |
  | Kabarist, Malabar, any reformed faith | Hazzan | unchanged |

  These names are proposals for Daniel to review. Refresh the copy if vanilla changes the
  trait.
- **Debug probe** (`events/kehillah_samaritan_priesthood_debug_events.txt`):
  - `.1` reports the law, the High Priest, his primary heir, and whether each is a Kohen;
  - `.2` runs the yearly effect;
  - `.3` kills the High Priest.

## Assumptions and open risks

- **The seeded clergy are made Kohanim.** This gives Simeon a priestly line from day one.
  The alternative was creating sons he never had in the history files.
- **`same_faith_clergy` coverage is unverified.** Which courtiers count as "clergy rulers
  and clergy councillors" is unknown, so the heir guarantee counts only kin and
  councillors. xTiger 1.6.10 rejects `same_faith_clergy` as an unknown set. That report
  is a false positive: vanilla 1.21's `_succession_election.info` lists the set, and the
  live-proven Sanhedrin election uses it and gets the same report.
- **A fallback can replace the chaplain.** It replaces the court chaplain only when no
  Kohen is among the holder's kin or council.
- **The law may not take effect.** A theocracy might override a title law. The Sanhedrin
  law works on a landed seat; on a landless theocratic head of faith it is untested.

## Live checklist

1. New 1066 game. Run `event kehillah_samaritan_priesthood_debug.1`. Expect: law PRESENT,
   High Priest is a Kohen, a Kohen kinsman or councillor exists, heir PASS.
2. In the Samaritan High Priest's character window, check that his primary heir is a
   Kohen. The succession tab should show "Priestly Succession". The clergy should show
   "Priestly Elder", not "Hazzan".
3. Run `event kehillah_samaritan_priesthood_debug.3`, wait a day, then run `.1`. Expect the
   office held by a Kohen, with no Game Over and no `error.log` flood.
4. Check a Rabbinic court cleric shows "Talmid Hakham", and its tooltip text renders.
