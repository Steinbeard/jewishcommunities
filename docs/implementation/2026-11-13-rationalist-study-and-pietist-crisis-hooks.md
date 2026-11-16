# Rationalist study and pietist crisis hooks

**Status: built 2026-11-13 in the shared main worktree; source and xTiger checked, live behavior pending.** Extends [the Sefer mechanics](../spec/2026-11-08-sefer-tenet-mechanics.md) and [the rite pass](2026-11-12-rabbinic-rite-tenet-pass.md). It does not change starting rite tenets or replace an existing tenet ID.

## Tenet choice

Vanilla `tenet_alexandrian_catechism` is the closest analogue to philosophical rationalism: outside Christianity its name is Islamic Rationalism, its description appeals to unaided reason, and it improves Learning lifestyle experience. `tenet_pursuit_of_knowledge` describes an interest in learning generally; it does not carry the same theological claim. Our `tenet_kehillah_hokhmah` already means Reasoned Theology (Hokhmah in Jewish rites) and is part of book arguments, reception, reviews and reform. Replacing that ID with the vanilla one would require an explicit migration of that catalog and saved statuses. Keep the existing ID for now; do not add a separate Philosophical Rationalism rite or another tenet.

## Implemented hooks

- A reader with either Hokhmah or Alexandrian Catechism as a rite or personal tenet gains **5 percentage points** when mastering a book in the Machshavah/Hashkafa genre. The bonus is counted once. Authored works use their selected genre at runtime. This is inside each book's actual mastery value, so the ledger breakdown, scheme chance and final roll agree. It is independent of the existing +10/-10 when a book argues for/against a personal tenet.
- A leader with Asceticism in their rite or personal tenets gains **5 weight** on the risky public fast during Agitation. Its Jewish presentation is Hasidut, but the check uses vanilla Asceticism. This rewards an ascetic approach in the crisis, rather than granting passive protection for holding a tenet.

The book system and crisis are Jewish mod systems, so a ruler of another government uses these hooks if they have access to the action. The tenets' ordinary character and personal modifiers continue to apply to any government. In CK3, a tenet's modifiers and vanilla parameters are consumed by game systems independently of government; a custom parameter only matters where a script reads it. The mod's book and crisis hooks are such explicit reads, and need not be built into each government definition.

## Follow-up audit

Compare custom Pesak to Legalism and Religious Legal Pronouncements, Pilpul to Scholasticism, and Ge'onut to Pentarchy. A replacement needs a migration of historical statuses, selected rites, authored work indexes, standing and personal tenet arguments. Ashkenaz retains vanilla Asceticism; Yordei Merkavah retains vanilla Esotericism. Decide a rationalist rite only if a distinct community, authority structure and doctrine can be demonstrated, not merely because a tenet exists.

## Verification

The catalog's targeted language-value generator ran after the change and Python compilation succeeded. xTiger reports its baseline `fatal: 0, error: 16, warning: 107, untidy: 38, tips: 44`. In a disposable game, inspect mastery chance for a Hashkafa book with and without Hokhmah or Alexandrian Catechism, including an authored work of that genre; check that other genres do not gain it. In an Agitation crisis, compare the risky fast's weights with and without Asceticism. Live checks are pending.
