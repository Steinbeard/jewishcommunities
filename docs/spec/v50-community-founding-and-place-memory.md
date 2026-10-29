# V50: Community founding and place memory

**Status:** Design and source audit, 2026-10-23; not implemented or live-tested. Extends [V48](v48-world-kehillot-founded-legacy-and-pillar-ui.md)'s founded-year anchors and the [Domain overview](../implementation/kehillah-domain-overview.md). Supersedes no existing gameplay rule. This user-directed research unit was taken ahead of the standing Near-term TODO live passes; they remain open.

## 1. What exists

The mod already writes `kehillah_founded_year` on 35 authored community titles in `history/titles/kehillah_titles.txt` and `kehillah_world_titles.txt`. The ledger row and Standing tooltip display it, and V48's capped age calculation uses it for Greatness. Adventurer, settlers, and Norman founding paths also write `current_year`. Daughter communities keep `kehillah_mother_community`; exile and invitation paths save an origin or inviter for gameplay. There is no unified founder/origin/loss/refounding record.

`kehillah_dissolve_community_effect` calls `kehillah_departure_prepare_effect`, unregisters the title, then `destroy_title`. The departure code explicitly states that the destroyed title's variables go with it. A new runtime title at the same county therefore cannot recover the old founding date or cause of loss. A vacant authored title such as Kairouan retains scenario history data, but has no 1066 community UI.

## 2. Place-owned record

The county title should own the durable **place memory**. A current Kehillah title represents its playable institution; its existing `kehillah_founded_year` remains a compatibility and Greatness value, mirrored from the place. The original date is never reset by refounding. Each transition records a date, type (founded, destroyed, abandoned, refounded), and known references: origin county or mother community, optional leader, optional responsible character or title, and controlled cause key. Do not invent an attacker for internal collapse. A future migration rule must explicitly decide how the old and new places link; a domicile move alone does not prove migration.

Use a shared county-context localization key so Domain, map tooltip, and a later history view can show the same account. Linked character and title tokens must use tooltip-capable localization (`GetName`, `GetTitledFirstName`) rather than `NoTooltip`. Missing or invalid references omit that clause. Uncertain historical anchors should render as "by" or "around", never as an exact 1 January. The age derives from original year and current year. A vacant county needs a map/history entry point because the existing Domain body only appears for a living Kehillah leader.

The resulting text can say, according to available data: "Established by 960. Destroyed by [linked party] in 1057. Refounded by families from [linked origin] under [linked leader] in 1080." With no leader, omit "under..."; with no origin, say "founded in [year]" or "founded by [leader] in [year]". Chronological order and actual wording need a live render check.

## 3. Recording hooks

1. Seed source-backed founding facts on county titles. Retain existing title-year assignments until 867/1066/1178 checks show the mirror matches. Seed authored losses at their dates, including Kairouan in 1057. `holder = 0` alone is not evidence of destruction: some vacancies are bookmark staging.
2. Call one `kehillah_record_founding_effect` after title creation from the adventurer decision, settlers, and Norman founding chokepoints. Pass origin and founder before `move_to_pool_at` destroys origin context. If the county has an earlier founding, append a refounding without changing the original date. Mirror the original year to the new title.
3. Call one `kehillah_record_loss_effect` from common dissolution **before** `destroy_title`, with cause and responsible party supplied by each caller. Audit other title-destruction paths. Differentiate collapse, expulsion, mob violence, and voluntary abandonment.
4. Spike CK3 save/load and GUI data-model behavior before choosing an unbounded chronology representation. A first slice may store original founding plus latest loss/refounding, but must label that view a **summary** and not silently overwrite history while claiming a complete ledger. A full list requires an iterable, save-safe event representation.
5. Add a hidden console debug event that seeds founding, loss, and refounding and logs all fields. Check save/reload, multiple bookmarks, optional references, and linked text. The Domain render and vacant-place entry point require a Luna subagent live test under `AGENTS.md`.

## 4. Historical standard

V48's founding years are gameplay anchors, not exact certificates of institutional continuity. Distinguish an attested settlement, an organized Kehillah, a revived institution, and a traditional association. Named founders and origins are optional. Link a historical person only if an appropriate character exists at that date.

- **Worms:** the current title anchor is **960**. The Lucca-to-Rhineland Kalonymos migration is associated with **Mainz**, with an uncertain early tenth-century date. Do not assert that a named Kalonymus founded Worms in 890 without new evidence.
- **Baghdad:** its current title anchor is **762**, matching the Abbasid foundation and the Jewish community there. A 560 BCE exile from Jerusalem associated with Ezekiel is Babylonian regional history, not an attested founding of Baghdad's city community.
- **Kairouan:** the 1057 sack is attributed to the **Banu Hilal**; the Zirids retreated to Mahdia. The mod's 1066 vacant Kairouan and Mahdia refugee community provide the right scenario anchors. Avoid "destroyed by the Zirid Host".
- **Sura and Pumbedita:** academy history and town-community history are distinct. Sura's 1066 playable community is explicitly a gameplay revival. Pumbedita has a historical office roster, not a current playable Kehillah. Academy closure must not automatically mean total loss of the town's Jews.

Historical sources and existing editorial limits: [V48 bibliography](v48-world-kehillot-founded-legacy-and-pillar-ui.md#2-historical-standard-and-sources), [UNESCO SchUM dossier on Kalonymos chronology](https://whc.unesco.org/document/184456), [Encyclopaedia Judaica on Baghdad](https://jewishvirtuallibrary.org/jsource/judaica/ejud_0002_0003_0_01872.html), [ANU Museum of the Jewish People on Kairouan](https://dbs.anumuseum.org.il/skn/en/c6/e246606/Place/Kairouan), [V29's academy note](v29-yeshiva.md#6-sura-and-pumbedita-for-reference), and [the historical office roster](historical-jewish-leadership-roster.md).

## 5. Verification gates

- Audit all founding and title-destruction paths; compare xTiger against the baseline.
- Probe original-date preservation across destruction/refounding and optional fields with debug events.
- Test save/reload and 867/1066/1178 starts, including vacant Kairouan.
- Live-check linked text and layout in Domain and a vacant-place entry point through a Luna subagent.
