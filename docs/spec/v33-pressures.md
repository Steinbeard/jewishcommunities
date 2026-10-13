**Status:** agreed with Daniel 2026-10-12 (items 1–3 of the pressure proposal); being built. This
amends the pillar baselines of [v2](v2-pillar-economy-and-lifecycle.md). It complements, and does
not replace, the v31 host-relationship design. The v31 "Teaching on the Jews" doctrines are read
directly, as the host's official position. The religious-tension term remains as the local
population's view.

# V33: Pressures, so Stability and Prosperity move

## Why

The 2026-10-12 soak test ([report](../testing/2026-10-12-balance-soak-test.md)) found that every
AI community settled at Stability ~200 and Prosperity ~190 within ten years, and stayed there for
sixty. None reached Healthy and none fell into Crisis.

The cause is structural. Each quarter a pillar moves 5% of the way toward a baseline. That
baseline was a sum of nearly static contributors: buildings, officers, charter terms, households.
Nothing in it reacted to the world.

Daniel's direction: host pressure should feel more aggressive. Stability should start higher and
change mostly through negative feedback, from the host, the charter, war through the county, and
religious tension.

## 1. Stability rests at Healthy

`kehillah_stability_baseline_floor_value` rises from 200 to **500**. A community under a tolerant
host, at peace, sits in Healthy (≥400). Its institutions are bonuses on top.

## 2. Falls fast, recovers slowly

Stability and Prosperity move **15%** of the gap per quarter toward a *lower* target
(`kehillah_convergence_rate_down_value`), and 5% toward a higher one. A bad year bites at once;
recovery takes years. Greatness is unchanged.

## 3. Live pressures

These are breakdown values, `kehillah_pressure_values.txt`, with scope a Kehillah leader. They are
read every quarter and added to the pillar baselines, and each appears as its own line in the
pillar tooltip. "Host" means the top liege of the county the quarter stands in.

| Term | Stability | Prosperity |
|---|---|---|
| Host's attitude: opinion of the leader | ≥40 +50, ≥10 +20, ≤−10 −60, ≤−40 −150 | — |
| Host's traits | zealous: +20 under a protective teaching, −120 under an exclusionary one, −60 otherwise (v31: "a zealous Witness bishop protects"); sadistic −40, greedy −30, paranoid −30, compassionate +30, just +20, cynical +20 | — |
| Realm's Jewish Settlement Policy | Encouraged +40, Discouraged −100, Banned −250 | +40 / −60 / −150 |
| War in the county | occupied −200, raided −120, host at war −40 | −150 / −100 / −25 |
| A holy war preached: the county's or host's faith has a great holy war in any stage | −150 | — |
| Religious tension: the county's faith regards Judaism as evil / hostile / astray (the local view; light, because every county reads "evil" at start) | −30 / −20 / −10 | — |
| The county's economy | — | development × 4; −50 if county control is under 50 |
| The host's Teaching on the Jews (v31 doctrines, on the host's rite) | protective +30, strict −80, exclusionary −200 | strict −40, exclusionary −100 |

Ranges are deliberate. Under a neutral host at peace, Stability is ~500 (Healthy). A zealous host
who dislikes the leader brings it to Strained. War or a crusade pushes it toward Crisis. A ban plus
defiance means Crisis.

## Not in this slice

- **Host demands** (proposal item 4): tallage, forced loans, confiscation, quartering. These are
  the aggressive events and the gold sink the soak found missing.
- **Shock events** (item 5): blood libel, riots, fire.
- **The doctrines** (v31 Slice A) landed on 2026-10-12. They are read by the teaching term
  above, and they scale the host's zeal.

## Verification

Run ck3-tiger, then a live probe that reads each term for Worms. The real test is a repeat soak:
communities should spread across the bands, and the bands should move with wars, crusades and host
changes.

## Addendum, 2026-10-12: overcrowding is a population limit, not a Stability cost

The live probe ([log](../testing/2026-10-12-v33-pressures-probe.md)) found two problems.

**Overcrowding.** Worms has 33 courtiers and 8 places. The flat −8 a quarter outweighed the slow
5% recovery, so Stability could never climb back. Daniel decided that the player has little
control over population, so a full quarter should be a soft limit rather than a Stability cost.

- **The Stability drain is removed.** The mild crowded-quarter modifier (−5 courtier opinion)
  stays.
- **Capacity:** the base goes from 4 to 20, plus the existing Prosperity bonuses.
- **Arrivals:** a full quarter turns newcomers away. Arrival sources check
  `kehillah_quarter_has_room_trigger`; the yeshiva's travelling students are the first.
- **Capacity from buildings** (Daniel chose this over a separate housing building): each building
  tier the community has built adds +2 places (`kehillah_courtier_capacity_buildings_value`). A
  fully built quarter adds about +50.

**Religious tension.** It read −120 ("evil") in every community. It is now light: −30, −20 or −10
by the local faith's view. The teaching carries the ideology.

## Addendum 2026-10-13: a Prosperity floor

**Status:** built 2026-10-13 (autonomous session, V34 follow-up); live check pending.

- **The problem:** the 51-year soak ([2026-10-13-v33-pressures-soak.md](../testing/2026-10-13-v33-pressures-soak.md))
  found 21 of 23 communities pinned in Strained or Crisis for the whole game. Troyes sat at 77-124
  for 50 years, and only Toledo ever reached Healthy. Prosperity-gated play (Send Out Settlers needs
  Strained) was shut for good in much of the diaspora.
- **The change:** `kehillah_prosperity_baseline_floor_value = 150`, at the Strained line. It is
  added to the Prosperity baseline the way Stability's 500 and Greatness's 60 are, and shown as
  "Every community's footing" in the breakdown tooltip.
  - A peaceful community with nothing built rests just above Strained, plus its county's economy.
  - War, a hostile policy or teaching, and occupation can still push it into Crisis.
- **Not chosen:** the soak's alternative (development x8), and a larger floor of 250. The smaller
  floor is the more reversible step. Revisit after the next soak.

## Addendum 2026-10-13: the county's economy weighs more

**Status:** built 2026-10-13; live check pending.

Daniel asked for county development to matter more to Prosperity, without building ahead of the
upcoming trade DLC.

- **Was:** a flat 4 per development level. Worms (about 12) got +48 against the 250-point gap from
  Strained to Healthy.
- **Now** (``kehillah_bd_local_economy_value``): 8 per level up to level 20, then 4 per level beyond.
  Worms gets about +96. A development-40 city gets +240 (flat 8 would give +320). Daniel: big cities
  should be richer, which is realistic, so the knee is a soft compromise (first built at 2 beyond 20).
- **Why the knee:**
  - The old great cities (Baghdad, Constantinople, Cordoba, at 30-50 in 1066) would otherwise run far
    ahead of Ashkenaz (8-15).
  - Development roughly doubles by 1300, which would otherwise inflate every community toward
    Flourishing.
  - Development is not a community's own lever, so it should not dominate the pillar.
- **The trade DLC:** this value is the single hook for the county's economy. When the DLC lands,
  its market and trade-route data belongs here, beside or instead of development. Nothing
  trade-like is built ahead of it.
