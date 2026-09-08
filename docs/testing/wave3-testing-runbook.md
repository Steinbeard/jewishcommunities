# Wave 3 testing runbook

Status: **ready to run.** Companion to
[events/kehillah_debug_events.txt](../../events/kehillah_debug_events.txt), a set of hidden,
console-only events written 2026-09-07 specifically to support this runbook. They do nothing on
their own -- no on_action, no pulse, no trigger hooks them up -- the only way to reach one is
typing `event kehillah_debug.<number>` in the debug console while playing the Kehillah leader
(requires launching with `-debug_mode`).

Two logs matter here and they are not the same file: **error.log** (script/loc errors -- what the
2026-09-07 localization patch pass was cleaning up) and **debug.log** (where the `debug_log`
effect below writes its output). Both live in the same CK3 logs folder. Don't check one for the
other.

---

## Setup

- Launch fresh: `-debug_mode -develop`, Worms 1066 bookmark. A brand-new file (like the debug
  events file itself) is only picked up on launch -- if you add more `kehillah_debug.N` events
  later, you'll need to relaunch before they're reachable, the same way the given-names loc file
  needed a relaunch this session.
- Console cheat for Gold if you need it for anything: `money <amount>`.
- Check `error.log` for `kehillah` once at boot, before touching anything, so you have a clean
  baseline to diff later test-induced errors against.

---

## 1. Sfarim tiers (Compose a Commentary)

For each band, jump there and take the decision:

| Band | Command |
|---|---|
| Crisis | `event kehillah_debug.1` |
| Strained | `event kehillah_debug.2` |
| Healthy | `event kehillah_debug.3` |
| Flourishing | `event kehillah_debug.4` |
| Legendary | `event kehillah_debug.5` |

At each: open **Compose a Commentary**, confirm the option text/tooltip matches the band (private
note / commentary / responsum / chronicle), take it, confirm the resulting artifact's rarity
(masterwork / famed / illustrious at Healthy / Flourishing / Legendary respectively). Specifically
sanity-check the **Healthy tier** -- it was remapped from the old flat `illustrious` down to
`masterwork` because vanilla's rarity scale has nothing above illustrious, and that's the one
judgment call worth a gut-check in play.

## 2. Band-gated building tiers

Use the same five jump commands. At each band, open the Jewish Quarter domicile UI and check the
7 gated buildings (Synagogue, Beit Midrash, Countinghouse, Market Stalls, Workshops, Hekdesh,
Sofer's Workshop):

- Below the gate: confirm the padlock's tooltip actually renders the `kehillah_requires_*_tt`
  reason text, not a blank or garbled tooltip -- this `can_construct` + `custom_tooltip`
  combination has no vanilla precedent, so this is the one part of Wave 3 with no prior art to
  lean on.
- At/above the gate: confirm it's actually constructible now (`money` for the Gold if needed).
- Confirm Mikvah and Slaughterhouse are **not** gated at all, at any band.

Then run the isolation tests, which pin two pillars at Crisis and one at Legendary -- these catch
a gate accidentally checking the wrong pillar, a real risk since all 12 gates were built by
copying the same trigger block with a different `PILLAR` param:

| Isolates | Command | Should unlock | Should NOT unlock |
|---|---|---|---|
| Greatness only | `event kehillah_debug.11` | Synagogue/Beit Midrash/Sofer's Workshop tiers | Countinghouse/Market/Workshops/Hekdesh tiers |
| Prosperity only | `event kehillah_debug.12` | Countinghouse/Market Stalls/Workshops tiers | Synagogue/Beit Midrash/Hekdesh/Sofer's Workshop tiers |
| Stability only | `event kehillah_debug.13` | Hekdesh's Strained tier | everything else |

If, say, `kehillah_debug.12` unlocks a Greatness-gated tier, that tier's gate is reading the wrong
variable -- exactly the bug this test exists to catch.

## 3. Courtier quality/cap/retention

- **Quality**: compare a courtier who joins at `kehillah_debug.1` (Crisis) vs one who joins at
  `kehillah_debug.5` (Legendary) -- Learning/Stewardship should be visibly higher at Legendary.
- **Cap pressure**: invite guests until headcount exceeds the current band's capacity (Crisis = 4,
  +4 Strained, +6 Healthy, +8 Flourishing, +10 Legendary -- so e.g. 5+ at Crisis should trip it),
  then run `event kehillah_debug.30` and check `debug.log` for `courtier count EXCEEDS capacity`.
  Confirm the character modifier and Stability drain both actually show up in the UI, not just in
  the log.
- **Retention**: get to Crisis Stability (`event kehillah_debug.1`, or naturally) and advance
  several quarterly ticks. Watch for a non-dynasty courtier leaving for the local county holder's
  court. This is probabilistic -- if nothing happens in a few ticks, that's inconclusive, not a
  fail; give it more ticks before calling it broken.

## 4. Loan contracts

1. Get to Prosperity ≥ Healthy (`event kehillah_debug.3` or higher) so **Extend a Loan** is
   available, then take it.
2. Run `event kehillah_debug.30`, check `debug.log` for `local county holder HAS an outstanding
   Kehillah loan`.
3. Confirm the county holder actually received the gold (150) and that **Repay a Loan** is
   available from their side; take it, confirm the debt clears (`kehillah_debug.30` again should
   now report no outstanding loan) and Prosperity/Greatness get the repayment reward.
4. **Default path**, instead of repaying: run `event kehillah_debug.40` (needs an outstanding loan
   from step 1) to fast-forward to 5.9 of the loan's 6-year term, then advance one quarterly tick.
   Confirm the loan clears itself via default and Prosperity drops by the default penalty (60)
   rather than the repayment reward.
5. **Succession while a loan is outstanding**: take a loan, then use the debug right-click ->
   `DEBUG: Main` -> `Slay Character!` -> `No Killer` on the player. After succession, run
   `event kehillah_debug.30` again as the new leader and confirm the loan (which lives on the
   *title*, per the lender-is-the-title design) survived the handover. This is genuinely untested
   territory -- flagged as the one loan scenario most likely to reveal an orphaned-state bug.

---

## Cross-cutting, throughout

- Re-check `error.log` for new `kehillah`-tagged entries after each section, not just at the end.
- The two known **pre-existing** bugs below are not Wave 3 regressions -- don't mistake them for
  new findings if you see them again:
  - The benign "illegal government" error on every succession (harmless in practice, root cause
    still open).
  - `has_domicile_building_or_higher` wrong-scope error from `kehillah_prosperity_baseline_value`,
    and `Unknown trigger: is_child` in the holiday events -- both flagged in the 2026-09-07
    localization patch pass, neither fixed yet.

Report back whatever breaks and I'll fix it against the live files.
