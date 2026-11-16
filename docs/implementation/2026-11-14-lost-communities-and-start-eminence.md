# Lost communities on the map and in the ledger; starting buildings and libraries by eminence

**Status: BUILT 2026-11-14 at Daniel's request. xTiger reports nothing new. Not live-tested; the
checklist is at the end.** It extends
[V50 place memory](../spec/v50-community-founding-and-place-memory.md) and
[its first slice](2026-10-23-community-history-first-slice.md),
[V52's world ledger](../spec/v52-world-ledger-and-standing-rank.md), the
[Jewish Communities map](2026-11-08-jewish-map-category.md), and
[Shas-first library seeding](../spec/2026-11-08-sefer-system-redesign.md) §5.2. The research
behind it is in
[the Ibn Daud / Benjamin spike](../research/2026-11-14-sefer-haqabbalah-and-benjamin-community-spike.md)
§9.

## What Daniel asked for

1. A record of destroyed communities in the tracking systems.
2. Destruction and abandonment in the community history and on the Jewish map mode: where Jews
   once lived, when the community ended, and its peak standing, in words rather than numbers.
3. A note about Benjamin of Tudela and Petahiah of Regensburg as bookmark characters.
4. More or fewer starting sefarim and buildings for each community, according to its historical
   greatness in 1066 and 1178.

## 1. Tracking

[`docs/data/kehillah-lost-communities.csv`](../data/kehillah-lost-communities.csv) lists every
lost community this research found:
- the place, county and title;
- the year and cause;
- its peak;
- any re-establishment;
- whether it is seeded in game;
- the source.

Rows that are not seeded (Bari 1156, Seville, Oria 925, Thebes 1147, Sana'a 1172, and the end of
the Sura academy) record why not.

## 2. Place memory: historical losses and the peak

New **county** variables, next to V50's:

| Variable | Meaning |
|---|---|
| `kehillah_history_peak` | The highest the place ever stood, from 1 to 5. In words: always a struggling congregation; a modest congregation; an established community; a major center; one of the great lights of the diaspora. |
| `kehillah_history_last_refounded_approx` | The refounding year is approximate, so the history reads "Re-established by around …". |
| global list `kehillah_former_sites` | Every county with a lost community that has not been refounded. |

The new cause flags are `kehillah_history_almohad` (forced conversion or flight) and
`kehillah_history_crusade` (destroyed).

**How the peak is set:**
- **At the start**, a living authored community's county gets one step above its eminence tier
  (§4); a historical loss gets an editorial peak.
- **Every quarter**, the rank pass (`kehillah_rank_communities_effect`) raises the peak to the
  community's current Standing band. The peak never falls.
- **When a community is lost**, `kehillah_history_record_loss_effect` takes a final peak reading
  and lists the county as a former site.
- **When a community is refounded**, `kehillah_history_record_founding_effect` removes the county
  from the former-site list. The refounding then has an exact year.

**Historical losses seeded at game start** (`kehillah_history_seed_authored_roster_effect`).
Each is gated on its own date, so 1066 shows only Kairouan:

| County | Loss | Cause | Peak | Afterwards |
|---|---|---|---|---|
| Kairouan | 1057 | Banu Hilal | 5 | (already seeded; now listed as a former site) |
| Fez | 1145 | Almohads | 4 | lost |
| Córdoba, Lucena (`c_cabra`), Granada | 1148 | Almohads | 5 | lost |
| Mahdia | 1160 | Almohads | 3 | lost |
| Mainz, Worms | 1096 | crusade | 5 | re-established by around 1100 |
| Cologne, Rouen | 1096 | crusade | 3 | re-established by around 1100 |
| Jerusalem | 1099 | crusade | 4 | re-established by around 1160 |

The summary keeps V50's limit: one loss and one refounding per place. Granada in 1178 therefore
shows its 1148 end, not the massacre of 1066. In a 1066 game the massacre happens in play.

## 3. Where the player sees it

- **Jewish Communities map:** each former site is painted ash (`d_kehillah_mapcolor_former`, darker
  than the no-community base). The painted barony is the one the community last held, otherwise
  the county capital. The hover card (`KEHILLAH_MAP_MODE_TOOLTIP_FORMER`) shows the place, the
  community history line (founding, loss, refounding) and the height it once reached. A living
  community is painted afterwards, so it always wins its barony.
- **Community history and the vacant-site card** read the two new causes. The ledger, map and
  domain summaries use the same custom localization.
- **World ledger:** a new "Lost communities" section under the ranking lists each former site,
  greatest first: *Córdoba — Ended under the Almohads, 1148; once a great light of the
  diaspora*. The full history is in its tooltip. The ranking area was cut from 580 to 430 pixels
  high to make room.

## 4. Starting eminence: buildings and libraries

`common/scripted_effects/kehillah_start_eminence_effects.txt`. Each authored community gets
`kehillah_start_eminence` for the 1066 and 1178 bookmarks. 867 and runtime-founded communities are
unchanged.

**The 1066 table:**

| Tier | Communities |
|---|---|
| 4 great | Baghdad, Fustat, Granada, Lucena, Mainz, Worms |
| 3 major | Toledo, Córdoba, Narbonne, Troyes, Rome, Jerusalem, Constantinople, Sura, Fez, Alexandria, Damascus, Palermo, Bari, Isfahan |
| 2 established | Cologne, Rouen, Paris, Orléans, Prague, Béziers, Lunel, Mahdia, Balkh, Sana'a |
| 1 modest | Speyer (founded 1084), Vienna (no Jews attested before about 1194), Auxerre |

**The 1178 table:**

| Tier | Communities |
|---|---|
| 4 great | Baghdad, Fustat, Constantinople, Toledo, Narbonne, Lunel, Troyes |
| 3 major | Worms, Mainz, Speyer, Cologne, Paris, Posquières, Rome, Palermo, Damascus, Alexandria, Isfahan, Béziers |
| 2 established | Rouen, Orléans, Prague, Jerusalem, Bari, Balkh, Sana'a, London |
| 1 modest | Vienna, York |

**Buildings.** Every add is guarded, so Worms' developed start is never reduced. Each tier adds
to the one below:

| Tier | Buildings added |
|---|---|
| 1 | Synagogue and Beit Midrash |
| 2 | Mikvah, hekdesh and market stalls |
| 3 | Synagogue tiers 2–3, countinghouse, sofer's workshop, slaughterhouse, workshops |
| 4 | Synagogue tier 4, House of Debate (Beit Midrash 2), countinghouse 2, market stalls 2 |

The upper tiers are gated on pillar bands, and add_domicile_building honours those gates. So, as
Worms does, each pillar is lifted for the grant and then put back exactly as it was. Day three's
V20 snapshot then computes the opening pillars from the new buildings. A greater Quarter therefore
opens higher through the visible baseline, not through a hidden grant.

**Libraries.** `kehillah_seed_starting_library_effect` reads the tier. A yeshiva seat (Beit
Midrash 3) still gets the whole Shas.

| Tier | Talmud orders | Other works |
|---|---|---|
| 4 | the whole Shas (6 orders) | 3 |
| 3 | 4–5 | 2 |
| 2 | 2–3 | 1–2 |
| 1 | 1 | 1 |

## 5. Noted for later: traveller bookmark cards

Benjamin of Tudela (journey about 1165–73, back in Spain by 1173) and Petahiah of Regensburg (on
the road about 1175–80) are candidate **1178 adventurer cards**, like Eldad ha-Dani in 867. Not
built. Recorded in ROADMAP's backlog and in the spike §7.

## Choices made without asking

- The tables are editorial, from the spike and general history. Speyer and Vienna are
  deliberately modest in 1066.
- Sura's academy and Oria's 925 sack are not seeded as losses. Both places kept Jewish life, and
  the 1066 roster still seats Sura.
- Bari's 1156 razing is recorded in the CSV only. Whether to move the 1178 seat to Taranto is still
  Daniel's decision.

## 2026-11-15 revision (Daniel's screenshot review)

This section supersedes the text described in §3.

**The map hover is one sentence**, built from parts that any loss fills, historical or in play
(`KehillahFormerSiteSummary`). For example: *"A great Jewish community was destroyed here in
1057, after standing for about 387 years."*
- The adjective comes from the peak: great, major, established, modest or small.
- The verb comes from the loss:
  - destroyed (status 2);
  - came to an end (Almohads, forced conversion);
  - was driven out (expulsion);
  - was abandoned (otherwise).
- The span is counted from the last refounding, otherwise from the first record. It reads "about"
  when that year is approximate, and is left out when unknown
  (`kehillah_history_years_stood_value`, `kehillah_history_has_span_trigger`).

**The county inspector's "Community history"** shows, in this order:
1. The same sentence.
2. The barony the quarter stood in, when recorded.
3. A plain account of what happened, one per cause (`KehillahHistoryCauseDetail`). The causes are
   Banu Hilal, Almohads, crusade, mob (named leader if known), expulsion (named ruler if known),
   forced conversion, no successor, and dwindling.
4. The last leader and the ruler at the time, when recorded in play.
5. Underneath, in weak text: when Jews are first recorded there, and how high the community once
   stood.

The ledger tooltip uses the same account. Two fixes from the screenshot:
- A lost community no longer shows an age ("396 years old"); it says "Jews are first recorded
  here in 670."
- The awkward "Jews previously lived in Sheikhdom of Kairwan" heading is gone.

**Dynamic capture:**
- `kehillah_history_record_loss_effect` (every dissolution: mob, expulsion, forced conversion,
  collapse, crisis collapse, exile) now also stores `kehillah_history_last_leader` and
  `kehillah_history_last_host` (the ruler at the time) on the county.
- **Heirless deaths** were the one gap. The engine ends such a title without passing through
  dissolution. Now `on_death` notes the leader, title, year and ruler on the county
  (`kehillah_community_history_on_actions.txt`). The yearly pulse records the loss
  (`flag:kehillah_history_no_successor`) if the seat is still empty, and clears the note if a
  successor took it.

**Ibn Ghiyyat and the five Isaacs** (`history/characters/kehillah_five_isaacs_1066.txt`, tracker
HC338–HC340):
- Isaac ibn Ghiyyat's father **Judah** is now a history-only character. He is attested only by the
  patronymic, his dates are estimated, and he dies before 1066.
- The five Isaacs are now all present. **Isaac ben Moses ibn Sakni** (new dynasty 9000098) is a
  young scholar at Lucena in 1066. His city, his dates and his later eastern office are not
  established; that placement is an inference. The other three were already in the mod:
  - Isaac ibn Albalia (9002019);
  - Isaac b. Reuben al-Bargeloni (9002085);
  - Alfasi (9002023).
- Isaac ibn Ghiyyat (born 1038) was elected to lead Lucena only after Joseph ha-Nagid's death on
  30 December 1066 (Jewish Encyclopedia), at 28. The 1066.9.15 start places him there about three
  months early. That was already recorded as a caveat (HC027) and is left as it is.

## Live checklist (Daniel)

1. **1066:** start as Worms and check `error.log` for `failed to meet triggered requirements` or
   `Cannot construct an upgrade`. Open Granada's or Baghdad's Quarter: it should show synagogue
   tier 4, a House of Debate, a countinghouse 2 and market stalls 2. Open Auxerre's: only the
   synagogue and Beit Midrash. Baghdad's library should hold all six Bavli orders.
2. **1066, Jewish Communities map:** Kairouan's barony is ash. Its hover shows the 1057 sack and
   "one of the great lights of the diaspora".
3. **1178, map:** Córdoba, Lucena (Cabra), Granada, Fez, Mahdia and Kairouan are ash. Mainz,
   Worms, Cologne, Rouen and Jerusalem are not, and their Domain history reads "Destroyed by
   crusaders in 1096 … Re-established by around 1100".
4. **1178, ledger:** the "Lost communities" section lists the six, greatest first, with readable
   tooltips. The ranking above still scrolls.
5. **Day 3 or later:** greater communities open with higher Greatness and Prosperity than modest
   ones, and no pillar is stuck at Legendary.
6. **2026-11-15 text:** hover Kairouan. It reads "A great Jewish community was destroyed here in
   1057, after standing for about 387 years." The county inspector adds the Banu Hilal account and
   "Jews are first recorded here in 670", with no "years old".
7. **Heirless death:** with the console, kill a small community's leader who has no successor
   candidates. Within a year (or after `yearly_global_pulse`) the site turns ash and reads "was
   abandoned here … Its last leader, X, died with no one to take up the office".
