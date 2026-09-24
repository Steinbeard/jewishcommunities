# V16 Spec: Jewish Settlement Policy, Host Charters, and Settlement Conditions

**Status: IN PROGRESS — the policy-to-fresh-charter and actual-charter-to-pillar
implementation slice is source-validated as of 2026-09-24; its first live
contract/default test is still required.** This document supersedes the *v1 charter-term model*
in [v15-host-charter.md](v15-host-charter.md) §2 only. V15's use of a real
tributary subject contract, host-resolution mechanism, inheritance behaviour,
and no-unilateral-exit rule all remain the foundation. It also adds the
previously-unscoped policy layer anticipated by
[v2-pillar-economy-and-lifecycle.md](v2-pillar-economy-and-lifecycle.md) §§3
and 5. No expulsion, migration, or resistance outcome is shipped by this
spec's first implementation slice.

## 1. Decision and goals

Every realm has one **Jewish Settlement Policy**, resolved from the primary
title of the community's host (the same `top_liege` already used by V15's Host
Charter). Its default is **Settlement Allowed**. The policy tells a player and
the AI whether a *new* Jewish community can plausibly be established in the
realm; it is not a duplicate, permanent pillar modifier alongside the
community's own charter.

The policy is deliberately universal. A Hindu, Buddhist, Christian, Muslim, or
other ruler can encourage, allow, discourage, or prohibit Jewish settlement.
That common question does **not** imply that all religious and regional legal
systems use the same charter dimensions. V16 defines the shared policy
envelope; later regional packages may supply appropriate contract language and
terms within it.

The design goals are:

1. Give potential founding and migration destinations an intelligible,
   non-random frontier signal.
2. Let a realm-wide political decision constrain all local Jewish charters
   without erasing meaningful local variation.
3. Make the forecasted benefit become the same kind of pillar benefit that a
   real, negotiated charter produces after settlement — never double-count it.
4. Give existing communities clear, actionable warning before a hostile policy
   becomes an expulsion or migration crisis.

## 2. The three layers (one direction of causality)

```
Realm policy -> permitted/default charter offer -> actual local charter -> pillar baselines
                               + local development/network -----------^
```

- **Realm policy** is an entitlement envelope. It sets the default offer for a
  newly made charter and the best/worst terms that may be negotiated while it
  remains in force.
- **Host Charter** records what a particular Kehillah actually obtained. A
  sympathetic patron, special grant, cost, or later negotiation may make it
  better or worse than the ordinary offer, as long as the policy permits it.
- **Settlement Conditions** are derived values. The ongoing pillar baseline
  reads the actual charter and local geography, never the policy's forecast.

Thus an Encouraged policy makes a prospective city attractive because it
projects a strong initial charter. Once founded, the same numeric right values
come from the contract's flags. If negotiations yield a lesser deal, the pillar
benefit is correspondingly lesser and the UI can honestly say why.

Policy changes do **not** silently rewrite existing contracts. They affect new
foundations and future negotiations immediately; existing communities are
grandfathered until an explicit warning/escalation event or renegotiation
changes the actual charter.

## 3. Jewish Settlement Policy

| Policy | New foundation | Default charter outlook | Existing communities |
|---|---|---|---|
| **Encouraged** | Legal and AI-favoured | Secure residence and an advantageous ordinary offer | No pressure |
| **Allowed** | Legal; normal baseline | Recognized ordinary residence and ordinary rights | No pressure |
| **Discouraged** | Exceptional, costly, or patron-backed only | Conditional/limited offer | Visible political concern; no automatic loss |
| **Banned** | Not lawfully possible | No charter may be created | Starts a warning/escalation path; never an instant deletion |

An absent stored policy resolves to Allowed. That avoids mutating every
top-level title at game start and makes the feature compatible with newly
created realms. A later policy-change system stores only deviations from
Allowed on the host's realm title.

**First implementation boundary.** V16 now uses the resolver for foundation
validity, fresh-charter default selection, and contract validity. It does not
yet choose policy changes for AI rulers. That requires a separate, transparent
political-event design; it must not be smuggled in as a quarterly random
modifier.

## 4. Charter dimensions

V15's `Right to Lend at Interest` and `Walled Quarter` were a workable
mechanical spike but are no longer the intended permanent model. The first
Christian package should instead have these dimensions:

1. **Residence and Protection** — tolerated -> recognized -> protected.
   Its main output is Stability.
2. **Economic Privileges** — restricted -> market access -> chartered
   privileges. Its main output is Prosperity. Moneylending can later be a
   historically specific consequence or option within this right, not the
   definition of Jewish communal life everywhere.
3. **Communal Jurisdiction** — host court -> mediated disputes -> recognized
   Bet Din. Its outputs are Stability and Greatness.

The walled-quarter concept becomes an optional building/permission consequence
of a strong protection right rather than a universal legal dimension.

**Regional fresh-charter packages, 2026-09-24.** Two loadable contract groups
now express this divergence. They are selected only when a *new* Christian or
Muslim host charter is made; an existing V15 charter remains untouched:

- **Christian:** Quarter Construction, Community Security, Jurisdiction over
  Jewish Subjects, and Talmudic Study. The last is a three-rung censorship
  regime (Unrestricted -> Licensed -> Talmud Proscribed), not a UI list of
  works. A future book-burning chain can record a small, inspectable list of
  proscribed library works underneath that regime, but such a list must never
  be represented as a contract row per book.
- **Muslim:** Quarter Construction, Community Security, Jurisdiction over
  Jewish Subjects, and Market Access. This intentionally does not declare a
  generic "Dhimma" row or assert a single Islamic legal experience; its
  regional language and consequences need historical research before shipping.

"Community Security" is deliberately narrower than a universal right to bear
arms. Its rungs model whether a community can maintain a licensed watch or
whether the host pledges protection. Similarly, Bet Din Discipline means civil
discipline and communal penalties, not autonomous criminal jurisdiction.

The armed-watch rung is also the natural gate for a very small **communal
retinue**: exactly one character-owned men-at-arms regiment, rather than levies
or a realm army. This makes the legal right matter in play and gives a leader
who later becomes an adventurer a credible force to take with them. It remains
a spike, however: the present Kehillah government deliberately suppresses MaA,
so the prototype offsets that only while the armed-watch right is active. A
fresh-game test must verify both recruitment and persistence across a real
Kehillah-to-adventurer transition before this becomes shipped gameplay.

The packages are live for fresh Christian/Muslim charters, but their initial
default selection and contract-window presentation remain a live-test gate.
V15 remains the fallback for every other host tradition and for all existing
V15 save contracts. The console-only V16 harness (`kehillah_debug.76` then,
after a tick, `.77` for a Christian host or `.78` for a Muslim host) remains
useful for an isolated fresh-save probe; `.79` then `.80`, again with a tick
between them, restores the V15 charter.

### 4.1 Policy envelope and ordinary defaults

`defaults_to_highest_valid_level = yes` makes the most generous permitted
rung the ordinary offer. Lower valid rungs deliberately remain legal, so a
specific liege or vassal can negotiate a less generous local charter without
changing the realm's shared policy. The policy must never silently rewrite an
already accepted charter.

| Policy | Christian ordinary offer | Muslim ordinary offer |
|---|---|---|
| Encouraged | Free construction; Recognized Watch; Bet Din; Unrestricted Study | Free construction; Host Protection; Bet Din; Chartered Trade |
| Allowed | Free construction; No Communal Watch; Royal Appeal; Unrestricted Study | Free construction; Unarmed Community; Communal Arbitration; Regional Trade |
| Discouraged | Permission Required; No Watch; Local Court; Licensed Study | Authorisation Required; Unarmed Community; Host Court; Local Market |
| Banned | New construction forbidden; no watch; local/host court; Talmud proscribed | New construction forbidden; unarmed; host court; local market |

The Banned row is an envelope edge case for an already-existing or debug
charter, rather than a way to create a new community: the founding decision is
disabled under Banned.

V16 does **not** remove the two V15 terms until the live-save/contract-default
spike in §8 passes. Removing a contract entry from an active contract group
without proving how CK3 handles saved obligations is unnecessarily risky.

## 5. Pillar and suitability accounting

Each right has its contribution defined exactly once in a mod-prefixed script
value. The live charter reads that value through its contract `flag`; the
pre-foundation outlook calls the same value for the policy's projected initial
rung. Component ownership is:

| Component | Forecast source | After founding | Pillars |
|---|---|---|---|
| Legal security | Policy's projected security right | Actual security right | Stability |
| Economic access | Policy's projected construction/market right | Actual construction/market right | Prosperity |
| Jurisdiction | Policy's projected jurisdiction | Actual jurisdiction right | Stability, Greatness |
| Urban opportunity | County development/capacity | Same county condition | Prosperity, modest Stability |
| Diaspora network | Nearby reachable Kehillot | Same live network | Stability, Greatness |

The forecast is a report, not a fourth score. Its top-line rating is the
weighted summary of these components. For ongoing communities, contributors
are capped so charter/location conditions matter greatly to a young Kehillah
but cannot outweigh buildings, officers, events, or player choice.

**Implemented accounting.** The pillar baseline reads only the flags on the
actual fresh charter: construction and Muslim market access contribute to
Prosperity; security, jurisdiction, and network contribute to Stability; and
jurisdiction and Christian text freedom contribute to Greatness. Policy itself
adds no pillar value. The intentionally visible first-pass values are:

| Actual term | Pillar contribution |
|---|---|
| Free construction / permission / forbidden | +15 / +5 / -10 Prosperity |
| Recognized or host protection / licensed watch | +25 / +10 Stability |
| Bet Din / intermediary jurisdiction | +22 Stability +20 Greatness / +12 or +10 Stability +4 Greatness |
| Unrestricted / licensed / proscribed study | +25 / +5 / -30 Greatness |
| Chartered / regional / local market access | +40 / +20 / +5 Prosperity |

The network cache is recomputed when the initial registry is built and when a
community is founded, never in the quarterly pillar pulse. It counts other
registered communities within vanilla's `squared_distance_medium` band:
zero is -5 Stability, one or two is +15, three or four is +7, and five or more
is 0. This is deliberately a Goldilocks mutual-aid result, not a linear
"more neighbours is always better" bonus. The distance scale and performance
with a large registry remain live-test questions.

## 6. Player information architecture

Do not expand `Take Stock`; it is a fallback/debug decision. The bespoke UI
is authoritative:

- **Own-community pillar strip/tooltips:** show Settlement Conditions as named
  baseline contributors under Prosperity, Stability, and Greatness.
- **Community map ledger:** show each community's host-policy badge and a
  tooltip with its actual charter, including a clear exceptional/grandfathered
  marker where applicable.
- **Founding/migration picker:** show the full Settlement Outlook at the
  candidate location before commitment. Until a destination-picker exists, the
  existing current-location founding decision shows that same tooltip for its
  current county.

The UI must identify whether a number is *projected* or *actual*. It must
never display an Encouraged policy as though it were a right a community
already holds.

**Implemented in the first slice:** the existing ledger row tooltip now shows
the cached host-realm name, policy badge, and a dynamic charter-status line.
It reports when a grandfathered charter contains rights that exceed a newly
restrictive policy, without revoking those rights. The pillar tooltip names
each actual charter and network contribution. A visual badge column and an
actual-charter/exemption summary wait on a dedicated contract-UI pass.

## 7. Policy deterioration and warning

`Banned` is a state of political danger, not a destruction effect. A later
escalation design should use a clearly announced sequence:

1. a host court considers a restrictive edict;
2. affected communities receive a warning and time window;
3. players may petition, mobilize the Shtadlan, seek a patron, pay a
   concession, build support through nearby communities, or prepare to move;
4. the policy stabilizes, a community is grandfathered, a charter is
   renegotiated, or an actual expulsion/migration chain begins.

The causes, pacing, and AI choices are intentionally out of scope until the
warning UI and the real exit mechanics are designed together.

## 8. Required spikes and live tests

The following are hypotheses, not assumptions. Each needs a narrow probe and an
entry in `docs/testing/` before it becomes load-bearing.

1. **Dynamic contract envelope.** A subject-contract obligation level's
   `is_valid` can read `scope:liege.primary_title` and the contract window
   correctly greys/rejects a rung prohibited by a realm-policy variable.
2. **Initial default selection.** `defaults_to_highest_valid_level = yes`
   chooses the projected policy-default rung when `start_tributary` creates a
   new contract. Test on a freshly founded community, not an existing charter,
   and verify the write after the known deferred contract tick.
3. **Saved-charter migration.** A save containing V15's two terms safely loads
   after a group adds/replaces terms, and a controlled migration effect can
   change a charter's rungs without same-tick reads.
4. **Realm-title persistence.** A policy stored on the host realm title
   survives a ruler's death and reads as the same value from every Kehillah
   under that top liege. Test both host succession and a county changing realm
   by conquest.
5. **Pillar source of truth.** Change one actual charter rung, allow the
   deferred contract write to settle, then verify exactly one matching named
   contributor changes in the bespoke pillar tooltip and the quarterly
   baseline. The policy forecast must not add a second copy.
6. **Development and distance primitives.** County development is available
   at the founder's current `location.county.development_level`, and is now a
   modest AI founding weight. Confirm the band implied by
   `squared_distance_medium` and measure the one-shot registry scan with many
   communities. Do not put an all-world nearest-community scan in the
   quarterly baseline.
7. **Warning visibility.** Before any AI policy-change event ships, live-test
   that a proposed policy and countdown are visible in the pillar/ledger UI to
   every affected player community.
8. **Armed-watch retinue.** On each regional prototype, select the armed-watch
   rung and verify it exposes exactly one character MaA slot (not title MaA or
   levies). Recruit a regiment, revoke the right to learn CK3's disposition
   rule, then repeat through a real Kehillah-to-adventurer transition and
   confirm the regiment and its upkeep behavior. Do not promise retention in
   the player-facing text until this is observed. Use the debug harness noted
   in §4 on a fresh save and restore V15 immediately afterward.

## 9. First build slice and non-goals

The first build slice is deliberately bounded:

1. policy resolver with implicit Allowed;
2. policy-selected fresh Christian/Muslim charter groups and actual-charter
   contributor infrastructure in the existing pillar breakdowns;
3. debug-only policy setters/reporting for repeatable contract probes;
4. cached Goldilocks network conditions and the first foundation weight;
5. live spikes 1–4 and 8 above before any V15 migration or player-facing MaA
   promise.

This slice does not implement policy-changing AI, bans, expulsions, migration,
the final founding picker, Indian-specific terms, or an unbounded geographic
network calculation.
