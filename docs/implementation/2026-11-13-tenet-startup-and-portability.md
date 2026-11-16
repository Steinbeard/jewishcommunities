# Tenet status initialization and portable names

**Status: built 2026-11-13 in the shared main worktree; xTiger/source checked; fresh-start UI and runtime checks pending.** Extends [the rite pass](2026-11-12-rabbinic-rite-tenet-pass.md) and [the Sefer tenet mechanics](../spec/2026-11-08-sefer-tenet-mechanics.md). This is a compatibility and presentation pass, not the final decision on which custom tenets should be retired in favor of vanilla counterparts.

## Startup notification

The displayed "Rabbinic adopted Halakha as Known" refers to vanilla `tenet_religious_legal_pronouncements`, called Halakha for Jewish rites. The previous pass displaced it from the main Bavel rite, but the starting `rabbinic_faith` history had not explicitly marked it Known. It is now in the dated 867.1.2 `known` list. The fresh-game Sefer migration no longer calls `set_tenet_status` after the lobby. The one-time status migration remains available from the yearly pulse for old saves that predate the history entries.

Tenet statuses are **faith-level** in CK3 1.20, not independent lists on each rite. A core tenet belongs to its rite; known, permitted and prohibited choices are shared with the other rites under the faith. Rabbinic, Karaite and Kabarist statuses already had dated history entries. Haymanot and Samaritanism now also explicitly permit ancestral custom and prohibit the Oral Torah, Geonic authority and dialectical Rabbinic study. Their vanilla Known entries are repeated to preserve them in case mod history replaces a same-key entry. The more specialized book canon remains per rite in the Sefer system.

## Tenet presentation and baseline effects

The ten tenet IDs are retained because the book catalog, reviews, reform votes and events refer to them. They can now be selected outside Judaism, with generic names and descriptions for those rites and Hebrew names and Jewish descriptions for Jewish rites. The theological opposition pairs remain mutually exclusive. No save migration of IDs is required.

| Jewish name | General name | General effect adjusted here |
|---|---|---|
| Hokhmah | Reasoned Theology | Existing cross-faith opinion and Learning experience apply across governments. |
| Emunah Temimah | Inherited Faith | Existing Piety modifier applies across governments. |
| Pesak | Codified Law | Replaces generic Prestige with vassal opinion for core followers and Learning for personal followers; the Bet Din hook remains Jewish-specific. |
| Pilpul | Dialectical Study | Existing Learning modifier applies across governments. |
| Ge'onut | Scholarly Authority | Existing Learning modifier applies to core followers even during a vacant headship; academy acclamation remains Jewish-specific. |
| Minhag Avoteinu | Ancestral Custom | Existing same-faith opinion applies across governments. |
| Avelei Tziyon | Sacred Homeland | Adds a small Piety bonus to the existing spiritual-fulfillment bonus; Send Alms to Jerusalem remains explicitly Jewish. |
| Ba'alei ha-Miqra | Scriptural Primacy | Core followers gain Learning experience, matching the existing personal bonus; Karaite scriptural study stays Jewish-specific. |
| Talmud Torah | Received Tradition | Existing Learning experience applies across governments; Rabbinic rereading stays Jewish-specific. |
| Kiddush ha-Shem | Witness Through Sacrifice | Existing Piety and stress bonuses apply across governments; the pogrom response remains Jewish-specific. |

The Jewish-only parameter tooltip lines are labeled as such where needed, to avoid suggesting a non-Jewish ruler can send alms to Jerusalem or host a Jewish Bet Din. Images and full effect redesign still require review; keeping the IDs and icons avoids breaking book metadata while that design is settled. In particular, the current borrowed icons and some virtue weights remain provisional.

## Head of rite correction

Vanilla's Chalcedonian faith names `k_papal_state` as its `head_of_rite` and includes Roman and Carolingian rites. The mod's previous documentation inferred too much from a test of a Gaon in one rite. A single title holder could be recognized across several rites; this needs an engine probe in the Rabbinic setup. The cherem interaction now tests whether the actor is the **target's** `rite.head_of_rite`, rather than requiring both characters to follow the same rite. The annual Gaonate selection still offers only one title holder at a time.

## Verification to complete

- Start a fresh 1066 game: confirm no Halakha status toast, the faith's known/permitted/prohibited lists, and Jewish names in rite screens.
- In a disposable game, inspect `rite:rabbinism.head_of_rite`, `rite:minhag_ashkenaz.head_of_rite`, `rite:minhag_sepharad.head_of_rite` before and after granting `d_kehillah_gaonate` to a Bavli Gaon. Test cherem on two actual rite followers and check `error.log`.
- Inspect a non-Jewish custom rite's tenet picker and a landed follower's character modifiers for generic names and effects. The current CK3 process must be identified before any live control.
