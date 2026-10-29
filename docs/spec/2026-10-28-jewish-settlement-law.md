**Status:** built 2026-10-28 at Daniel's request ("Let's convert it to a law!"); xTiger clean, **not
live-tested**. Supersedes the *storage* of [V16](v16-jewish-settlement-policy-and-charters.md) §3 (the
title variable) and the S9a raise/lower **decisions**. The rules V16/V17 set for the policy (four
rungs, one rung at a time, a five-year review, its consequences) are unchanged.

# Jewish Settlement Policy as a realm law

## Why

Daniel expected the policy to be a realm law and to find it among the laws. It was a title variable
changed by two decisions, so no laws screen showed it. A law group flagged `realm_law` is listed
in vanilla's laws tab automatically (`window_my_realm.gui` reads `MyRealmWindow.GetRealmLaws`).
That gives the player the standard law UI, with names, descriptions, costs and the reasons a law
is unavailable, without any custom GUI.

## What it is

- **Law group** `kehillah_jewish_settlement` (`common/law_groups/`), flagged `realm_law` and
  `realm_law_no_number`. Its default is Allowed.
- **Who holds it:** an independent ruler who isn't Jewish and doesn't have Kehillah government
  (`kehillah_can_hold_settlement_law_trigger`). This is the same ruler V15/V16 resolve as a
  community's host. Anyone else holds no law, which reads as Allowed, the old "no variable"
  default.
- **Four laws** (`common/laws/`): `_banned`, `_discouraged`, `_allowed`, `_encouraged`.
  - Each law can only be passed from a neighbouring rung.
  - Changes share the five-year review cooldown with the AI's review.
  - Raising costs piety (the decision's old price, as a `pass_cost`).
  - `ai_will_do = 0`: the AI changes the policy only through its event-led review, as before.

## How script reads and changes it

- **Reading is unchanged.** The four band triggers
  (`kehillah_jewish_settlement_policy_*_trigger`, title scope) are still the only way to read
  the policy. They now read the law on the title's holder. "Allowed" still means Allowed *or*
  Encouraged.
- **Changing goes through the law.** `kehillah_raise/lower_jewish_settlement_policy_effect`
  call `add_realm_law` with the neighbouring rung. Every caller (AI review, open-door
  invitations, the Shtadlan council task, expulsion counterplay, debug) is unchanged.
- **One place for the consequences.** Each law's `on_pass` records the old rung, and its
  `on_after_pass` runs `kehillah_settlement_policy_changed_effect`. That effect handles:
  - clergy opinion, or piety for lowering;
  - the cooldown;
  - re-applying charters and notifying the communities;
  - the invitation;
  - edicts of expulsion, or lifting them.

  So a change behaves the same whether it comes from the laws tab or from script.
- **Setting a rung exactly** (the Norman Conquest's welcome, the debug probes 72–75, and the
  outlook and expulsion probes) uses `kehillah_set_settlement_law_effect`, which skips those
  consequences. For a ruler who can't hold the law, it writes the old variable instead, so
  those calls behave exactly as before.

## Old saves

A save from before this change keeps the title variable. While the variable exists, the
triggers read it first, so nothing reads wrongly in between. A yearly pulse
(`kehillah_settlement_law_on_actions.txt`) converts it to the matching law and removes it. A
ruler who passes a settlement law sooner converts at once.

## Removed

`common/decisions/kehillah_settlement_policy_decisions.txt` and its strings. The laws tab
replaces both decisions.

## Live checks owed

1. The group appears in the laws tab for an independent Christian or Muslim ruler with the
   four named laws, and not for a vassal or a Jewish ruler.
2. Passing one rung works, and the neighbour and cooldown rules grey out the others with
   their reasons.
3. Raising charges piety; lowering grants it.
4. The changed effect fires once: one notice per community, and an edict on Banned.
5. In an old save, a title with the variable shows the right rung before and after the yearly
   conversion.
6. The realm view's policy fact opens this laws tab.

## Fixes after Daniel's first live look (2026-10-29)

- **Every realm read as Banned.** Loading a save from before the law, the engine gave every
  existing ruler the group's *first* law (Banned, index 0); the group's default is only for
  new rulers. Fixed with a global flag, `kehillah_settlement_laws_ready`:
  - Until the flag is set, the band triggers ignore the law and read the old variable
    (absent means Allowed).
  - `kehillah_settlement_laws_normalize_effect` then sets every eligible ruler's law from
    their old variable (or Allowed), removes the variables, and sets the flag.
  - It runs at game start, on the first yearly pulse after a load (within days), and
    before anything changes or shows the policy: the raise, lower and set effects, the
    realm view, and the policy map.
  - Passing a settlement law in the laws tab is refused until the flag is set, so the pass
    can't overwrite a law the player has just chosen.
  - This replaces the yearly per-ruler migration.
- **Kehillah leaders saw the law.** The group's `can_have_group` alone didn't keep it off
  their laws tab, so every law now also has `potential`, `can_have` and `can_keep`.
- **Who holds it, revised by Daniel:** Christian and Muslim rulers, or a ruler of any other
  faith with a Jewish community already in their realm. It must also be independent, landed,
  not Jewish, and not a Kehillah (`kehillah_can_hold_settlement_law_trigger`).
- **Icons:** the laws had none, since law icons are looked up as
  `gfx/interface/icons/laws/<law>.dds`. Vanilla's four Church Authority icons stand in as
  placeholders for Banned through Encouraged.
- **Other realms' laws:** vanilla has no window for them; My Realm's laws tab shows only the
  player's own. The realm view's policy fact goes back to the policy map mode, which compares
  every realm at once.
