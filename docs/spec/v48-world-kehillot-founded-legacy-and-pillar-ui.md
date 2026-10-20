# V48: World Kehillot, Founded Legacy, and Pillar Readability

**Status: BUILT, source-reviewed and `ck3-tiger` checked; live bookmark/UI verification deferred by Daniel on 2026-10-20.**
**Date: 2026-10-20.** Extends V20's dynamic-baseline start rule and V9's
community ledger. It does not change 1066 as the primary designed scenario.

## 1. Decision

The authored world roster now demonstrates three genuinely date-specific
snapshots rather than treating every title in the database as a 1066 title.
The registry includes only held community titles at the selected date, and
all shared initialization (library, charter, settlement network, pillars,
and ledger) runs over that held roster.

This is a first pass, not an assertion that the following lists are complete.
Named historical leaders remain limited to people whose office is supportable;
the new bookmark leaders are explicitly representative lowborn characters.

| Bookmark | Starting Kehillot | Intent |
|---|---:|---|
| 867 | 14 | Old Mediterranean, Andalusi, Babylonian, Persian, Central Asian, and Yemenite centers |
| 1066 | 32 | The existing 22-community designed roster plus ten world centers |
| 1178 | 27 | Continuing European centers, a later Mediterranean/eastern network, Fustat at its height, and post-Conquest London and York |

### 867 roster

Rome, Constantinople, Palermo, Bari, Kairouan, Alexandria, Damascus,
Isfahan, Balkh, Sana'a, Córdoba, Baghdad, Jerusalem, and Sura.

### 1066 additions

Rome, Constantinople, Palermo, Bari, Alexandria, Fustat, Damascus, Isfahan,
Balkh, and Sana'a. The original 22 starts remain unchanged in membership.
Kairouan is absent after its 1057 destruction; Mahdia remains the existing
1066 refugee-community start.

### 1178 roster

Worms, Speyer, Mainz, Troyes, Paris, Orléans, Rouen, Cologne, Prague, Vienna,
Narbonne, Béziers, Lunel, Rome, Constantinople, Palermo, Bari, Alexandria,
Fustat, Damascus, Isfahan, Balkh, Sana'a, Baghdad, Jerusalem, London, and
York. The disrupted Andalusi, Kairouanese, Mahdian, and Sura starts are
explicitly vacant rather than carrying their 1066 representatives forward.
London and York use 1178-only static title keys. They do not replace or
collide with V18's dynamic post-Conquest English founding path in a campaign
begun in 1066.

## 2. Historical standard and sources

A `kehillah_founded_year` is an editorial gameplay anchor: the earliest
secure presence used for this model, the foundation of a city whose Jewish
community is attested from its early centuries, or a documented medieval
institutional establishment. It is not a claim that a modern legal body
continued unchanged from that exact 1 January.

The broad roster is supported by:

- [Encyclopaedia Judaica's Byzantine survey](https://www.jewishvirtuallibrary.org/byzantine-rule-313-636-2), which describes Jewish communities throughout the empire from Constantinople's foundation;
- [the Rome community survey](https://www.jewishvirtuallibrary.org/rome-jewish-history-tour), which identifies Rome as Europe's oldest continuously attested Jewish community;
- [the Fustat/Cairo survey](https://jewishvirtuallibrary.org/jsource/vjw/Cairo.html), including the synagogue documented by 882 and the distinct Palestinian and Babylonian congregations;
- [Encyclopaedia Iranica on medieval Judeo-Persian communities](https://www.iranicaonline.org/articles/judeo-persian-communities-iv-medieval-to-late-18th-century/), which names Isfahan, Balkh and Bukhara among the wider documented network and notes the scale of Iranian Jewry;
- [Encyclopaedia Iranica's Bukharan-Jewish survey](https://www.iranicaonline.org/articles/bukhara-vii/), whose caution is why this pass uses ninth-century-attested Balkh rather than projecting the city of Bukhara back into 867;
- [the Palermo entry](https://www.jewishencyclopedia.com/articles/11865-palermo), which places its community in the Roman period;
- [the Bari entry](https://www.jewishencyclopedia.com/articles/2525-bari) and the [Oria entry](https://jewishvirtuallibrary.org/jsource/judaica/ejud_0002_0015_0_15190.html), which support the early medieval southern-Italian network;
- [Benjamin of Tudela context from the University of Washington](https://jewishstudies.washington.edu/jewish-history-and-thought/jews-medieval-iraq-kurdistan-benjamin-of-tudela/), used cautiously for the later Constantinople/Baghdad world rather than as exact population data.

Uncertain foundation dates are deliberately conservative and are recorded in
`history/titles/kehillah_world_titles.txt`. A later research pass may refine
an anchor without changing the mechanic.

## 3. Balance rule

V20 still governs: authored starts initialize to their visible dynamic
baselines. The new representative leaders receive the same playable floor
(community seed, succession pool, recorded Quarter, leader flavor, and 60
gold), not hidden pillar grants. Location development, host charter, nearby
network, leader skill, buildings, and institutional age produce the actual
differences.

Institutional age contributes to Greatness as:

```
max(0, min(50, (current year - founded year) / 20))
```

The cap prevents ancient communities from outweighing living institutions.
Runtime-founded communities write the current year and therefore begin with
zero age contribution. The player can see the founded year and contribution,
so this is not a hidden starting bonus.

## 4. UI rule

The ledger row and Standing tooltip display the founded year. Pillar
breakdowns aggregate all building-family contributions into one `Buildings`
line per pillar while retaining the individual script values as the source of
truth. Readable sections separate durable foundations, current or timed
conditions, leadership, ruler outlook, and seasonal changes.

Timed dispute, tzedakah, shaken-community, pogrom-memory, and Decrees entries
display their expiry date. Companion timed variables were added where the old
character modifiers did not expose a localization-readable date; legacy-save
fallback text remains available when the modifier exists without that timer.

## 5. Historical office links

Two already-authored library figures now receive office history without
changing any playable bookmark:

- Judah haNasi holds a history-only `Sanhedrin of Tiberias` title from 170 to
  217 and is styled **Nasi**.
- Ravina II holds the existing Sura community title from 475 to 499 and is
  styled **Gaon**.

The Tiberias title is history-only and is not V47's restorable Sanhedrin.
Sura's later playable history remains separate.

## 6. Required live checks

1. Boot 867, 1066, and 1178; run `event kehillah_debug.137`; verify registry
   counts 14, 32, and 27 with no holder/founded failures.
2. Advance each start three days; verify the provisional baseline reconciles
   and the ledger contains only that date's held titles.
3. Inspect one ledger row and the Domain pillar tooltips for building
   aggregation, section order, founded legacy, and real expiry dates.
4. Open the encyclopedia links for Judah haNasi and Ravina and verify their
   historical Nasi/Gaon title presentation.
5. Confirm the 1066 Norman English founding path still creates runtime titles
   and does not see the 1178-only London/York titles as occupied communities.
