# Roadmap

Working title: **Kehillah** (working name for the mod overall is still TBD — "Jewish Communities" is the folder/descriptor name for now).

Two playable tracks, per the project vision:

- **Track A — Diaspora Communities (the differentiator).** A new non-landed
  government type representing a Jewish community inside a host realm. This
  is the mod's signature feature and the main line of this roadmap.
- **Track B — Landed Realms.** Playable Jewish-majority landed polities
  (Khazaria, Himyar, Semien/Beta Israel, etc.), built mostly from vanilla
  culture/religion/government systems, reflavored. Lower priority; picked up
  once Track A's baseline is proven.

Phases are sequential within a track unless noted. This is the plan,
subject to revision after each phase.

## Near-term TODO
### Crisis situations research — 2026-10-30, Daniel's request

[Source spike](docs/research/2026-10-30-crises-as-situations.md): CK3 1.20.1.2 supports
multiple runtime situation instances with dynamically assigned county sub-regions.
This makes one native situation per active community crisis plausible, with a
map pin, Situations-list entry and phases. The current Community Safety build is
still uncommitted in the main checkout, so no situation code was grafted onto it.
Its Military dashboard and title-owned epoch remain the proposed action and
compatibility surface while a two-community identity/save/UI spike is tested.
No situation runtime or visual result is claimed. This user-directed research
unit was taken ahead of the older live-test queue below.

### The Nagid — 2026-10-30, Daniel's request — design agreed, nothing built

[Spec](docs/spec/2026-10-30-the-nagid.md), revised the same day with Daniel's second-round
decisions. The pieces:
- **Status of the Jews:** the Settlement law is renamed; its rungs become Banned / Restricted /
  Tolerated / Favored.
- **Favored:** always "beyond the teaching", with a cost scaled by the rite's Teaching on the Jews.
  It unlocks an Invite Jewish Settlers decision.
- **Culture:** an outlook line for African Tolerance and the other tolerance traditions.
- **The seat of the realm's Jews:** the capital's community, with tier-scaled pillars and more danger.
- **The office:** founded only at Favored, by a Protector, when the seat is Flourishing. It is held
  by the seat's leader and confirmed for a fee. It survives cold rulers down to Tolerated.
- **The Exilarch:** the same office with the caliph as host.

**Build order is the spec's §15.** Slice 0, the engine spike, **ran 2026-10-30** in Daniel's open
game through xTiger ([log](docs/testing/2026-10-30-nagid-engine-spike.md)). **A real seat is
impossible.** The engine refuses `assign_councillor_type`, `appoint_court_position` and
`designate_diarch` unless the host is the character's liege. Two routes remain:
- **Route B:** service in name, a skill-scaled host modifier;
- **Route C:** a delegate from the community serving as the host's courtier.

**Daniel chose Route B on 2026-10-30.** Progress is recorded in the
[build note](docs/implementation/2026-10-30-nagid-build.md):
- **Slice 1** (Status of the Jews, Invite Jewish Settlers): built and xTiger-checked, not
  live-tested.
- **Slice 2** (the culture outlook line, the cost of Favored beyond the teaching): built and
  xTiger-checked, not live-tested.

### English conquest invitation revision — 2026-10-29, Daniel's request

The Norman Conquest now opens a one-time decision for England's new ruler. William's AI is strongly weighted to choose it. The decision passes the Encouraged Jewish Settlement law, which sends the existing 20-year invitation with a special English letter. Ordinary settlers get a year to answer; a hidden review then fills a shortfall to three English communities in vacant named sites, retaining the player-adventurer London offer. Source review and xTiger pass against the unchanged 15-error baseline. An [isolated live check](docs/testing/2026-10-29-english-conquest-invitation-live-test.md) passed the decision, law invitation, ruler event and scripted London/York/Lincoln shortfall without new feature errors. The community-side letter rendering, natural one-year timer, player-adventurer path and AI pick rate remain pending. The wider recently-conquered, low-control realm rule is a separate design unit. See the [dated revision](docs/spec/2026-10-29-conquest-invitation-revision.md).
### Curated arms for newly founded Kehillot — 2026-10-29, Daniel's request

Runtime communities now roll one coat of arms from a curated eight-charge pool,
with two high-contrast color layouts. Adventurer, settlers and Norman founding
paths share the same one-time generation effect. Authored communities retain their
fixed arms. xTiger reports no new errors against the 15-error baseline. A launch
check was attempted through xTiger but did not complete while another CK3 process
was running; a live founding, save/reload and visual check remain pending. See
[the implementation note](docs/implementation/2026-10-29-community-arms-pool.md).

### Charter as a letter from the ruler — 2026-10-29, Daniel's request

`kehillah_settlement_conditions.0004` ("A Charter Is Sealed" / "The Charter Renewed") is now a
`letter_event` sent by the host ruler instead of a two-portrait scene. The ruler's outlook band
(`kehillah_outlook_band_value`, frozen when the event fires) sets the voice: salutation, a
paragraph in the ruler's voice, a closing sanction and the button text. Each band has Christian and
Muslim wording. The letter states why it was written (new charter, renewal for a new leader, or a
new ruler) and keeps the cached charter terms as its clauses. A footer outside the letter names the
outlook the voice came from, and for a new ruler it keeps the posture reading. The voice is flavour
only: the terms still come from realm policy. This replaces the three random renewal scenes from
2026-10-15, which were told from the community's side and don't fit the ruler's voice.
xTiger-clean (16-error baseline, none in the touched files). **Not yet live-checked** that the
letter window renders the opening, sender and full text.

### Community inspector on the Jewish Communities map — 2026-10-25, Daniel's request

The holding/county view now has a Kehillah inspector when any holding in a community’s county is selected, plus a vacant-site assessment in the Jewish Communities map mode. Daniel’s 2026-10-28 Granada review produced a community-first heading, corrected background bounds, 28-pixel side gutters, a lower card, separated holding/map controls, a unified three-column footer with annual risk, a host-character link and the Quarter action. Standing is removed from the card; its subtitle now selects one of 125 pillar combinations (Daniel’s definitive 125-cell matrix), and it shows the existing annual incident-risk percentage. Pillar text and metallic rims use the approved emerald/gold/slate palette; fills independently progress from red to green by tier using CK3’s native progress textures. Exact scores remain on hover. The vacant card now shares the same frame and gutters, with a place heading, compact settlement status, four aligned site-fact rows, conditional recorded history and a host-character link; detailed founding blockers are on hover. Source/exhaustive description checks and xTiger pass against the unchanged 15-error baseline; Daniel approved the active card’s appearance; the latest interactions and redesigned vacant-site card still need dedicated live checks. See [the implementation note](docs/implementation/2026-10-25-community-map-inspector.md), [palette](docs/spec/2026-10-28-community-ui-palette.md), and [test record](docs/testing/2026-10-28-granada-card-layout-check.md). This direct request was taken ahead of the older live-test TODOs below.

### Realm view: Jewish communities in a realm — 2026-10-28, Daniel's request

**Built, source and xTiger checked; live UI verification pending.** A menorah chip in the
character window opens "Jewish Communities in [realm]" for a ruler with communities or a Kehillah
leader. The view shows settlement policy, the faith's teaching, the ruler's outlook, the greatest
danger, community rows ordered by danger, and a 10-year news feed. A vassal sees communities in
their own lands and can open the full realm view. The top liege's primary title holds the 15-slot
news ring buffer; existing negative-incident hooks feed it. Later layout passes made the header
tiles and Charter/Quarter actions clickable, fixed the window background and news-panel height,
and added descriptors and a named regent. The realm view carries a CK3 1.20 character-window
override. See [the build record and remaining live checks](docs/spec/2026-10-28-realm-jewish-communities-view.md#10-implementation-record).

### Jewish Settlement Policy as a realm law — 2026-10-28, Daniel's request

**Built, source and xTiger checked; live verification pending.** The four policy rungs now live in
the realm-law group: Encouraged, Allowed, Discouraged and Banned. The old raise/lower decisions
are removed. A ruler sees the law and its costs and blockers in the ordinary laws tab; existing
charter and settlement consequences still read the policy. Later corrections fixed the
Encouraged piety cost and the policy map's display. See [the law specification and test
plan](docs/spec/2026-10-28-jewish-settlement-law.md).

### Jewish map ledger controls — 2026-10-25, Daniel's request

The Jewish Communities ledger now has a minimize control with a compact
restorable header. Closing the ledger leaves its map mode selected, and the
selected map button reopens it. A one-time reactive tip points Jewish player
characters with a populated community roster to that map. This user-directed
UI pass sits alongside the inspector work above. The source changes pass
xTiger against the pre-change baseline (0 fatal, 15 existing errors);
live UI verification is pending. See the dated [Faith map navigation
addendum](docs/spec/2026-10-13-faith-map-navigation-and-nusach.md#ledger-controls-and-jewish-character-tip--2026-10-25)
and the [attempt log](docs/testing/2026-10-25-jewish-map-ledger-live-test.md).

### V51 Bookmark rosters for 867, 1066 and 1178 — 2026-10-21, Daniel's request

**Built 2026-10-22; `ck3-tiger` clean; NOT live-tested.** Three Kehillah bookmarks:
- **1066** (five cards): Worms, Troyes, Granada, the Rif in Fez, and David ben Hezekiah as an adventurer.
- **867** "Age of the Geonim": Amram Gaon, Moshe ben Asher, Shefatiah of Oria, a Kalonymide of Lucca,
  Kairouan, and Eldad ha-Dani as an adventurer.
- **1178** "The Paths of Torah": Maimonides, Samuel ben Eli, the Ri, Judah he-Hasid, the Raavad of
  Posquières, and Joseph ibn Shoshan of Toledo.

New seats: Fez, Oria, Lucca, Tiberias, Posquières, plus two adventurer companies. Karaite and
Radhanite cards are recorded for later. The choices made while building, and the first-boot
checklist, are in [V51](docs/spec/v51-bookmark-rosters.md) section 0. **Next:** boot each bookmark,
press Play on a community card and an adventurer card, and calibrate portrait positions.

### Community rite and realm Jewish-policy map modes — 2026-10-23, Daniel's request

Two additional views are built beside the existing community map: **Community Rites** colours each
Kehillah's occupied barony by its leader's current rite, and **Jewish Settlement Policy** colours
each realm by its top liege's current policy. Source review, `git diff --check` and xTiger completed
without new errors in the changed files. The live UI check is pending: a separate CK3 process was
already running, so it was left untouched. See the [map-mode design note](docs/spec/2026-10-23-community-rite-and-realm-policy-maps.md).

**2026-10-29, Daniel's request:** all three Jewish map modes are now fixed buttons in a Jewish
group beside the vanilla Faith strip. They no longer appear only after the community button is
clicked, and they no longer shift around. Their names show under the banner's "Showing:". The mod
now carries a fenced copy of `gui/shared/mapmodes.gui` for this. The rites map gained a hover, and
the policy hover and both button tooltips were rewritten. xTiger-checked; live visual check
pending. See the [map-mode strip note](docs/implementation/2026-10-29-map-mode-strip.md).

### Ben David dynasty presentation — 2026-10-22, Daniel's historical-family request

**Implemented; source and xTiger checked; live UI verification pending.** The
Baghdad exilarch's dynasty now displays as Ben David, with symbolic lion arms
and a Genesis 49:10 motto. The arms are an artistic gameplay choice rather
than attested eleventh-century heraldry. See the [dated implementation note](docs/implementation/2026-10-22-ben-david-dynasty-presentation.md).

### Historical family roster research spike — 2026-10-22, Daniel's request

**Status: research complete; implementation on a stacked feature branch, live test pending.** The [dated spike](docs/research/2026-10-22-historical-character-roster-spike.md), [CSV tracker](docs/data/historical-character-tracker.csv), and [implementation note](docs/implementation/2026-10-23-historical-families-and-seeding.md) cover 110 tracked people, including 99 new history entries. Rashi has a young widower household with three daughters; Bodo lives in 867 Zaragoza; Sousse remains within Mahdia. Named families occupy appropriate 1066 courts before vacant seats receive random households. The former adult-child fallback is removed, and generated children have age-safe bounds. Source and xTiger checks passed; an isolated live-game check remains necessary. This user-directed work does not mark V50's pending live checks as passed.

### Hostile Christian rite names — 2026-10-22, Daniel's request

New Exclusion rites founded by mob preachers or popular rising leaders draw from
Agobardism, Amulonianism, Sisebutianism and Chrysostomianism according to the
founder's region. An existing suitable rite in the same faith remains the first
choice. Each historical label is used once per game. The decision and the
English-candidate limit are recorded in [the implementation note](docs/implementation/2026-10-22-hostile-christian-rite-names.md).
Source and xTiger checks found no new changed-file errors. An [isolated boot](docs/testing/2026-10-22-hostile-christian-rite-name-check.md)
reached the main menu, but the input fallback could not enter a campaign; rite
behavior and display remain pending.
This Daniel-directed naming unit does not close the older items below.

### V50 Community founding and place memory — 2026-10-23, Daniel's request

[V50](docs/spec/v50-community-founding-and-place-memory.md) records the source and architecture audit. The [first implementation slice](docs/implementation/2026-10-23-community-history-first-slice.md) now has a county-owned original year, last loss/refounding, optional founder/origin, and portable Domain/map summary. Source and xTiger checks pass against the existing baseline. The 1066 Domain year and 867 Kairouan date gate passed live checks; the age suffix and dynamic founding cycle still await Daniel-approved live tests. An unlimited chronological list, save migration, and historically sourced named-founder authoring remain future units. This user-directed work was taken ahead of the older live-test queue below; it does not close or reorder it.

### Pogrom warning and neighbouring news — 2026-10-21, Daniel's playthrough review

Built on a feature branch, **partly live-tested**: the [dated addendum](docs/spec/2026-10-21-pogrom-warning-and-news.md) records a 90–180 day warning, use of the elders' hub before local accusation mobs form, minimum post-declaration mustering, attack and outcome news, a dissolution notice, and hostile-rite reuse within the attacker’s faith (superseding fixed mob rites). This user-directed review takes priority over the standing TODO order. Source and xTiger checks found no changed-file findings. An [isolated boot](docs/testing/2026-10-21-pogrom-warning-live-test.md) loaded the mob events, and a subsequent scripted live check verified hostile-rite creation, same-faith reuse, and Shia isolation. Warning timing, rite UI display, siege timing, and notification rendering still require live verification.

### V49 Yeshiva Visit from the Library — 2026-10-20, Daniel's request

**Built; live-tested 2026-10-21 through the xTiger MCP server**
([log](docs/testing/2026-10-21-v49-yeshiva-visit-live-test.md)). The flow passed end to end. A
tooltip error flood and two presentation issues found in that test are fixed and re-tested in game
the same day. Not yet clicked in game: the "Plan a Yeshiva Visit" decision and the browse path. A book's page in the Library lists every
other community holding it. **Travel to study** opens the Yeshiva Visit planner with that
community as the only destination. A new **Plan a Yeshiva Visit** decision suggests books by
event, through the same plan. On arrival the traveller can take up the planned book directly. If
home lacks the work, they can copy it themselves (cheap, a long stay) or hire the host's scribes
(dearer, needs their Sofer's Workshop) and bring it back as a title-owned V48 acquisition that
survives succession. Design, assumptions and the live-test gate are in
[V49](docs/spec/v49-yeshiva-visit-from-the-library.md). The probe is `event kehillah_sefer_debug.6`.

### 1066 start screen — 2026-10-20, Daniel's request

**Status: built; source-checked, not yet seen in-game (textures need a CK3 restart).** The 1066
bookmark now offers three characters: Rashi (Troyes), Isaac ha-Levi (Worms) and Joseph ibn
Naghrilla, the Nagid of Granada. Joseph replaces Yosef ben Menahem, whose character and Norman
start are unchanged but who has no card on this screen. The bookmark is retitled "The Kehillot of
1066". Art is generated by scripts/render_bookmark_art.py from the game's heightmap and river
map (map, per-character highlight, two start-screen buttons). Portraits are copies of vanilla DNA in
period dress, not likenesses; no contemporary image of any of the three exists. To check on the next
boot: portrait position values (calibrated from one screenshot), highlight alignment, button art.

### V48 world Kehillot, founded legacy, and pillar readability — 2026-10-20, Daniel's request

**Built and `ck3-tiger` checked; live verification deferred by Daniel on 2026-10-20.** The held-title registry now supports distinct 867, 1066,
and 1178 community snapshots (14 / 32 / 27 starts), while 1066 remains the primary scenario.
Historical and runtime-founded communities record a visible founded year; institutional age adds
a capped Greatness baseline contribution. The ledger and Standing tooltip show the date, pillar
tooltips aggregate building effects and group durable/current/leadership/outlook terms, and timed
effects show their expiry dates. Judah haNasi and Ravina II now carry history-only Nasi/Gaon office
links. Design, roster, sources, editorial limits, and the required three-bookmark live test are in
[V48](docs/spec/v48-world-kehillot-founded-legacy-and-pillar-ui.md).

### Rouen and Orléans Kehillot — 2026-10-19, Daniel's request

Both northern French communities now exist as titular Kehillot at the 1066 start, with title
history, startup/registry wiring and representative lowborn leaders. Orléans begins under the
rabbinic scholar Yitzhak; Rouen begins under the lay parnas Yaakov and remains explicitly separate
from Yosef of Rodom's existing adventurer company. Historical basis, editorial limits and the
future console probe are recorded in [the implementation note](docs/implementation/2026-10-19-rouen-orleans-kehillot.md).
Per Daniel's instruction, this unit receives source review and `ck3-tiger` only, with no live boot.
### Auxerre Kehillah — 2026-10-18, Daniel's request

Auxerre is added as a 1066 Western Ashkenaz community in response to the documented correspondence between Rashi and the sages of Auxerre. The start uses the vanilla `c_auxerre` host geography and an explicitly representative rabbinic leader because the evidence establishes an eleventh-century scholarly community but does not securely identify its 1066 officeholder. Implementation and sources are recorded in [the Auxerre implementation note](docs/implementation/2026-10-18-auxerre-kehillah.md). This user-directed unit was taken alongside the V42/V41 queue and does not close those items.

### Historical Jewish leadership roster — 2026-10-18, Daniel's implementation seed

The researched Davidic/exilarchal, Sura, Pumbedita, Sanhedrin/patriarchal and Palestinian-Gaonate roster is now integrated as a staged, CK3-shaped source map with allocated IDs, proposed localized names, and institutional title-history assignments. The map reuses Saadia Gaon, Ravina II, Judah haNasi and the live 1066 Elijah ben Solomon; Hezekiah I/Gaon and Mar Zutra III each have one ID across their overlapping office lists; Pahda remains outside the Davidic dynasty. Every staged character is assigned to a relevant office sequence or explicitly marked as genealogy rather than title history. A fresh boot proved that undated records cannot live quietly in `history/characters` (one engine error per missing birth), so the 244 undated figures and proposed title histories remain under `docs/data` until defensible lifespans are sourced. Office years were not converted into invented lifespans, and the historical offices are not conflated with the current Baghdad, Sura, or Jerusalem community titles. No live title history or 1066 holder changed. See [the roster data note](docs/spec/historical-jewish-leadership-roster.md). This user-directed history-data seed was taken alongside the V42/V41 queue and does not close those items.

### V46 The Sanhedrin — 2026-10-19, Daniel's request

Spec: [v46](docs/spec/v46-the-sanhedrin.md).

**Built:**
- **The Sanhedrin** is a restorable Rabbinic head-of-faith title (`d_kehillah_sanhedrin`). It does
  not exist at any start.
- **Restoring it** is a major decision that needs mastery of all three Rabbi tracks, the top
  piety level, and enough rabbi-led communities.
- **The College:** members hold cardinal-style seats, which are clerical elector titles given to
  rabbis who lead communities. A title law makes them elect the next Nasi.
- **One vanilla override:** PAM's elector-title strip, which would otherwise destroy the seats.
- **Intents:** the Sanhedrin intent is now shown to everyone and selectable only by the Nasi; the
  Synod intent is unselectable for the Nasi.

**Status correction, 2026-10-19: live-tested.** After eight live cycles, the shipped build
(73ce2de) passes:
- restoring the Sanhedrin gives no Game Over;
- the Nasi keeps the Kehillah government, Quarter and buildings;
- seats survive 1 January;
- on the Nasi's death, play continues as the Worms successor, and the members elect Rashi of
  Troyes.

**The engine rule found.** CK3 forces a **landless** head of faith onto vanilla theocracy and
refuses the Kehillah government. So:
- a community-rabbi Nasi is **not** an engine head of faith;
- a landed Nasi (a king) is a temporal head of faith, an untested path.

Ruled out:
- the faith-level `theocracy_government_type`, which the engine ignores;
- the religion-level setting, which would also reach Karaite, Samaritan and other heads;
- the Nasi government (`kehillah_nasi_government`), kept but disabled;
- temple baronies for Kehillah leaders.

Full record: [the live test log](docs/testing/2026-10-19-synod-sanhedrin-live-test-log.md).
Spec v46 §9-10.

### V47 Heads of rite, the Gaon and the seat of the Sanhedrin — 2026-10-19, design agreed

Spec: [v47](docs/spec/v47-gaon-and-the-seat-of-the-sanhedrin.md).
- **Agreed:**
  - no heads of rite in 1066;
  - merit-based lifetime heads of rite at any time (Rabbenu for Ashkenaz, Gaon for Rabbinism);
  - "Establish the Office of the Gaon" for a merit head who leads Sura;
  - Baghdad as the Exilarchate (strong Ben David preference);
  - the Sanhedrin only in the Land of Israel, on a landed seat with a College election.
- **Live-proven building blocks:** a Kehillah head of rite through `head_of_rite`; a landed Nasi
  as head of faith. The spike code is in `docs/spikes/2026-10-19-landed-nasi-and-gaonate.patch`.
- **Phase A BUILT and live-tested, 2026-10-19 (8fd8737, 57fe3d8).**
  - Heads of rite come from the **Recognition of the Sages** doctrine (Rabbinic faith and Minhag
    Ashkenaz). A yearly acclamation event, "The Voice of the Generation", lets the most eminent
    qualifying rabbi accept the headship for life, or decline it. He is styled Rabbenu in
    Ashkenaz, Gaon otherwise.
  - The **Office of the Gaon** decision, for Sura or Baghdad, makes the headship inherited with
    the academy. A lay successor loses it.
  - Live PASS: the doctrine in the faith window; a player accepting (Rabbenu); an AI accepting
    (Gaon); the office passing through two rabbi successors; a lay lapse.
  - Fixed afterwards and not yet re-run: a lay heir kept the Gaon style.
- **Phase B BUILT, 2026-10-19 (f75070a, then restructured the same day in 487dd08 and a0538e7;
  see the v47 spec's "Phase B restructure" addendum).**
  - **Restore the Sanhedrin** is a decision shown to every Rabbinic ruler while no Sanhedrin sits,
    as a visible goal. Its requirements:
    - holding a county in the Land (the de jure Kingdom of Jerusalem);
    - all three rabbi tracks mastered;
    - top piety;
    - enough rabbi-led communities;
    - no head of faith.

    Kings, lords and community leaders can all take it. The seat is that county.
  - **Petition for Land in Eretz Yisrael** is a separate, rare decision and one way to get that
    county. A landless community leader in the Land asks his liege for his community's county,
    when the liege holds it directly and not as his capital. The odds follow the vanilla model
    (a Jewish liege, land to spare, a modest county, opinion). A player liege answers by event. A
    refusal bars asking again for 5 years.
  - **Kehillot may hold land** (Daniel). `require_landless` is removed from every community
    title, and the Nasi government is renamed to **`kehillah_landed_government`** ("Kehillah of
    the Land"), the government of any community leader who holds land. A grant switches the
    government first, because the engine refuses land to a leader on `kehillah_government`.
  - Earlier live-test findings fixed in this pass:
    - the election's self-opinion error flood;
    - a `min` on an unmodified `random_list` branch;
    - an overlong decision description.
- **Restructured Phase B live PASS, 2026-10-19 (a0538e7;
  docs/testing/2026-10-19-synod-sanhedrin-live-test-log.md).** The checks that passed:
  - Worms plays with its leader present;
  - a community leader granted his county in the Land moves to the landed government and keeps
    his Quarter;
  - the Sanhedrin can be restored on that county;
  - the election installs a community leader as Nasi, and his old community passes to its heir;
  - there is no error flood.
- **Still to check:**
  - the Petition for Land decision itself (its odds and the player-liege event 0006), since the
    test used the debug grant;
  - whether the Quarter's buildings survive a grant;
  - a king elected Nasi (v47 addendum, "Still open");
  - the Phase A lay-heir style fix.

### Open design: landed Jewish polities and other Jewish faiths (Daniel, 2026-10-19) — DANIEL-REVIEW

Raised while testing the Sanhedrin. These are design questions to settle with Daniel before any
build. Do not build them unattended.
1. **A landed Kehillah or Sanhedrin government.** The same community logic, but landed and a
   *vassal* of the host instead of an independent tributary. This would let a Nasi be a real head
   of faith, and would give Track B's landed Jewish realms a home. It needs:
   - a vassal-contract replacement for every host-charter mechanic (protection, dues,
     expulsion, settlement policy);
   - a decision on whether the Quarter survives as a domicile on a landed ruler;
   - adapting everything that reads the Kehillah government.

   The 2026-10-19 spike showed a Kehillah leader cannot simply be given a barony
   (`cannot_be_vassal_or_liege`). Independent baronies are not a CK3 concept.

   **Daniel's direction, 2026-10-19:** a fully empowered Sanhedrin needs a **county**, granted by
   the host. It should be very hard in the diaspora, through a demanding petition to one's
   liege, after the Roman grant of the Patriarchate at Tiberias and the caliphs' recognition of
   the Exilarch. That makes the Nasi a landed vassal, which the engine allows to be a head of
   faith (as the Caliph is). It would also introduce a **Sanhedrin government**:
   - landed, held as a vassal;
   - built from Kehillah components (council and officers, pillars, the Bet Din, appointment
     succession);
   - parts reusable for Jewish kingdoms that should not be plain feudal or nomadic.

   Open points:
   - Does the Nasi leave his Kehillah for the county (the Pope leaving his diocese), or does the
     community move with him?
   - Is there a landless "Sanhedrin in exile" stage before the land is granted? Today's build is
     effectively that stage.
   - What does the petition cost, and how does it depend on the host's faith and teaching?
   - Does the government need the theocracy mechanic?

   **First step before any build:** a one-cycle spike. Does a console-made landed Rabbinic
   count, holding the Sanhedrin as a spiritual head of faith, keep a non-theocratic government
   and stay playable?

   **Daniel's decisions, 2026-10-19 (same day):**
   - **The grant.**
     - It starts simple: the liege grants **the county your Kehillah is in**, if it is a
       **non-capital county in his own domain** and he is agreeable.
     - Later, a liege who is willing but whose county is ineligible may offer an **obscure
       county** instead.
     - Purchase, pledges and exchanges are not planned for now.
   - **Resistance.**
     - A liege with **less land** resists more.
     - A **more valuable** county is harder to obtain.
   - **The Nasi government *replaces* the Kehillah government for the Nasi.**
     - It is **landed** and **can be independent**.
     - It has **no pillars**.
     - It keeps the **domicile** and the **beit midrash**.
     - Under a **non-Jewish liege** it still suffers the dangers, expulsion and Jewish-policy
       effects that a Kehillah does.
   - **Order:**
     1. the spike;
     2. the simple domain-county grant plus the Nasi government;
     3. the Jewish-liege variant.
2. **Kehillot under a Jewish government.** Is a community under a Jewish ruler (Khazaria, a
   restored Israel) still a separate tributary body, part of the realm, or something between?
3. **Other Jewish faiths.**
   - **Today's systems are Rabbinic-specific:** beit midrash and yeshiva, semicha, the rabbi
     tracks, the Bet Din, the library.
   - **Karaites and Samaritans fit badly.** Karaites reject rabbinic authority; Samaritans are a
     separate tradition.
   - **Working assumption:** Kehillot stay Rabbinic (Rabbinism and Minhag Ashkenaz) for now.
     Karaite communities (their own sages, the Karaite nasi line in Egypt) and Samaritan ones
     would be separate institutions, designed later.

### V45 Rabbinic synods and Minhag Ashkenaz — 2026-10-18, Daniel's request

Spec: [v45](docs/spec/v45-rabbinic-synods-and-minhag-ashkenaz.md). It answers v25 §12 questions
6-8, with Daniel's three decisions:
- the synod founds Minhag Ashkenaz;
- the 1066 event renews Gershom's ordinances rather than issuing them;
- marriage is the only real doctrine a synod can change.

**Built:**
- **The `minhag_ashkenaz` rite** (`create = no`), seeded during 1066 setup so Ashkenazi
  characters and Kehillot begin play Ashkenazi.
- **Polygamy restored to the general Rabbinic rite** in starts after 1000. Vanilla's yearly event
  is suppressed so it can't undo this.
- **The automatic 1066 event was removed on 2026-10-19 at Daniel's request.** There is no
  conversion toast. Minhag Ashkenaz begins historically monogamous; the real Synod intent lets
  the assembled Kehillot renew and ratify Gershom's existing herem.
- **The synod tiers.** Revised 2026-10-19, per Daniel: no separate activity. The Sitting of the
  Bet Din has two gated host intents.
  - **Synod:** for the region's leading community. Every Kehillah leader is invited to debate
    and vote; its takkanot retain their defined regional or rite-level jurisdiction.
  - **Sanhedrin:** only for the head of the Sanhedrin, the seat being Jerusalem in 1066; its
    takkanot bind every community, and it alone may extend the herem to all Israel.
  - Revised 2026-10-19: a Synod hears two ordinary cases, then reserves its third phase for a
    rite-doctrine proposal and delegate vote. The doctrine ruling is presented before the
    docket's leave-taking. Ordinary Justice sittings retain all three cases (spec §10).
  - The Synod menu now contains only rite-doctrine proposals, modeled on vanilla's Ecumenical
    Council doctrine debate; community-level takkanot are no longer mixed into this intent.
- **The Second Wife case** now checks the host's rite and writes a ketubbah clause instead of
  editing the faith. It could not be drawn at all in a 1066 start before this.

**Original live pass:** the superseded event flow and the Synod/Sanhedrin mechanics passed on
2026-10-19; see `docs/testing/2026-10-19-synod-sanhedrin-live-test-log.md`.

**Revised-flow verification:** source and `ck3-tiger` checks are required, followed by a fresh
1066 boot confirming Minhag Ashkenaz exists at start, no day-30 event fires, all Kehillah leaders
are offered invitations, and the herem motion renews the existing Ashkenazi rule without changing
general Rabbinism.

**Follow-ups:**
- A lasting baseline term and breakdown line for each takkanah.
- Gameplay hooks for the community takkanot (spec §6).

### Jewish lineage traits — 2026-10-18, Daniel's request

Ben/Bat David is implemented as a paternal lineage trait modeled on Sayyid. Representative David of Baghdad starts with it, and Kehillah appointment scoring gives it a meaningful but non-dominating +15. The Kohen and Levite generated-character rates were corrected from accidental 0.05%/0.04% values to the intended 5%/4%; Elijah ha-Kohen now explicitly has the Kohen trait. Because CK3 name lists cannot condition a dynasty-name draw on a trait, HaLevi, Segal, Cohen and Cohen Tzedek were removed from random dynasty pools while authored matching families remain. Source/Tiger and live-probe status are recorded in [the implementation note](docs/implementation/2026-10-18-jewish-lineage-traits.md). This user-directed unit was taken alongside the V42/V41 queue and does not close those items.

### V42 The crisis as a place — 2026-10-14, Daniel's review of the mob preparation

Spec: [v42](docs/spec/v42-the-crisis-as-a-place.md).
- **The elders' hub** shows where things stand: secured, refused, on the road, and the harm if the
  host struck today.
- **At most four choices** an event, with "something else..." for more.
- **The leader goes, or sends a messenger** (in parallel).
- **Each person asked answers in a scene.**
- **Protective lords generally help.**
- **More warning time.**
- **Odds are shown the vanilla way:** percentages and skill-challenge duels, with no factor or
  number text.

**Status correction, 2026-10-15:** the V42 spec's dated 2026-10-14 addendum
records the navigation, messenger, answer scenes, Church letter, preacher duels
and own defence as live-tested, including fixes. The preceding "not yet
live-tested" claim here was stale. Slices 1-2 are covered by that report.
**Next:**
1. slice 3, vanilla-only odds across the V41 events (in small increments);
2. slice 4, cleanup of numbers in older text.

**Localization cleanup, 2026-10-18:** a user-directed pass completed the
older-text cleanup across Bet Din cases, council tasks, pillar notices, the
library and several event families. Player-facing prose no longer uses em
dashes or double hyphens. Static skill thresholds, tally formulas, band tables
and fixed-duration explanations were replaced with concise descriptions of
the actual tradeoffs; live script-value percentages remain where they tell the
player the current result rather than restating an implementation formula.
This was a localization-only pass. Source review and `ck3-tiger` completed
without a new fatal or error against the existing 1.19/1.20 baseline; no live
rendering pass was required for the shorter replacement text.

### V42 Sefer collection and scholarship — 2026-10-14, Daniel's request

**Named acquisition, 2026-10-20:** [V48](docs/spec/v48-sefarim-acquisition.md) replaces the Library's placeholder with a named-work acquisition catalog. Unreleased works are absent rather than shown locked. After choosing a known source, a community may buy a surplus manuscript, employ the source's Scriptorium or copy a borrowed exemplar locally; facilities gate methods rather than the catalog itself. A distant-network fallback remains when no source is known. Pending work is title-owned and survives succession. The player-facing random acquisition decision is retired while its AI route uses the same flow. The 1066 source/method UI and a clean active-profile error log are live-verified; the full purchase/external-copy/completion/succession matrix remains follow-up verification rather than a blocker for the first playable slice.

The first Books/Yeshiva panel split, clickable work descriptions, true mastery
checklist, and tier-aware starting-library seed are scripted in the Codex
worktree. **Fresh-boot seed verification passed** for Worms (tier 3, six
distinct works) and Mainz (tier 1, three distinct works). Window-relative
input later opened the Library and book detail; a primary-display check passed
the revised own-quarter panel, detail containment, and Books/Yeshiva tabs.
The standalone community-switch reset and personal mastery foldout still need
a recheck. The 2026-10-15 selected-book slice added a rabbi-only Learn Torah
starter for each held work, genre filters and badges, static Rabbinic tier
badges, attribution and representative game composition dates, and a recorded
living-master roster. A live click on Mekhilta opened its named study event and
spent 10 Piety. A fresh client showed localized metadata, a packed genre list,
and both empty and populated reader states; a portrait opens the character panel.
See the [selected-study live check](docs/testing/2026-10-15-sefer-selected-study-ui-check.md).
The corpus-card rework and its attached domicile tab are now live-verified in a fresh isolated 1.20.1 client. The repair fixed a full-width layout expansion, blocked clicks and tooltips from leaking to the quarter below, and replaced a dynamic corpus localization lookup that flooded the log after losing its `Title` context. The compact shelf, Jerusalem Talmud corpus, held-order list, Nezikin detail, progress count, and back navigation passed without a new `kehillah_lib` log entry. See the [corpus panel check](docs/testing/2026-10-15-sefer-corpus-panel-live-check.md).
The larger artifact inventory,
named acquisition, scholar demand, exceptional authorship, rewards, and canon
mechanics are staged in [V42](docs/spec/v42-sefarim-and-the-library.md).
Daniel's follow-up on composition dates, corpus/tractate grouping, and evolving
work standing is recorded in V42's dated addenda. The latest addendum adopts
exact in-game composition and circulation dates, optional historical author
links, and doctrine-based protected Torah/Tanakh and Rabbinic Bavli tiers.
Existing 933/1080/1140 acquisition gates are a partial chronology. The new
display catalog uses representative dates; a single authoritative acquisition
date table, broader historical author links, dynamic standing, and save-safe tractate
migration remain future work.
This user-directed slice was taken ahead of V41's soak and eastern-host tasks;
those remain open in their current order. The next V42 gate is the focused UI
check of those remaining states and natural-completion reader indexing before widening
the catalog or replacing title flags. See the [seed check](docs/testing/2026-10-14-sefer-seed-live-check.md)
and [primary UI check](docs/testing/2026-10-14-sefer-primary-ui-check.md).

### V41 The danger of violence, the incidents, the pogrom unfolding — 2026-10-14, Daniel's request

Spec: [v41](docs/spec/v41-danger-incidents-and-the-pogrom-unfolding.md).

**The plan:**
- **Character-driven checks,** and options unique to each leader.
- **The pogrom unfolds** in scenes, with the leader's own fate at stake. A leader baptized by force
  steps down; the player continues as the successor or as the convert. Forced converts take an
  anusim rite.
- **The crusade's preaching phase.**
- **A danger-of-violence score** (Greatness, incidents, hard times, the teaching, the lord): hard
  to reverse, possible to escape.
- **One incident director** with new incidents: host desecration, the Talmud trial, sumptuary
  laws, Holy Week humiliation, debt riots, uprisings.

**Division:** the director and the incident catalogue are Claude's; V40's Firebrand (Codex) drives
incidents through it.

**Status, 2026-10-14:**
- **Live-tested:** steps 1a, 1b, 2, 3 and 4a.
- **Built:** step 4b, the Talmud trial, the badge, Holy Week, the bonds, host desecration (an
  accusation variant), and risings that raise a mob.
- **Step 4b** passed its live test.
- **Two soak tests:** pogroms fell from 37 to 9 in 30 years after the balance fixes.
- **Refugees** are built and live-tested.
- **AI communities** now ask their lord to ride out.
- **Next:**
  1. a soak to see how often the lord's men save an AI community;
  2. a second eastern host.

### V40 Living crises and councils — 2026-10-13, Daniel's request

Spec: [v40](docs/spec/v40-living-crises-and-councils.md). Daniel wants crises to be character-driven
event chains with variety, not pop-ups fired by statistics.

**The plan:**
- **The Firebrand:** a named, recurring instigator whose acts escalate: preaching, then a
  disputation, an accusation and a mob.
- **Named allies.**
- **"Recent incidents" in a faith** (V38's pressure, made visible) call a **Council** (Christian) or
  a petition to the **Caliph** (Muslim). The communities lobby there, with pooled petitions. The
  outcome is a stricter teaching with a named decree, or protection reaffirmed.
- **What it replaces:** V38's silent yearly hardening. Vanilla's council needs the By God Alone
  DLC; this chain does not.

**Slices:**
1. The incidents counter.
2. The Council and the Caliph.
3. The Firebrand.
4. Allies.
5. Variants for the V36 events.

**Slice 1, 2026-10-14:** built and source/Tiger-checked; live verification pending.
Your Host now shows its faith's Recent incidents and Goodwill, retaining the existing
save variables and yearly fifth-decay. A completed pogrom adds 4 incidents to its county
faith. The silent annual teaching rolls are removed, including their softening mirror;
the Learned Exchange tooltip no longer promises annual softening. The existing DLC
council debate remains. The non-DLC Council/Caliph route is slice 2, not yet built;
no council threshold is advertised until it exists. See
[the implementation addendum](docs/implementation/kehillah-recent-incidents.md).
The existing running game did not register the new debug-event namespace; no counter
or tooltip assertion passed. It was left paused with its save untouched. First next
step is a fresh-boot slice-1 check, then slice 2 (Council/Caliph); see
[the actual test log](docs/testing/2026-10-14-recent-incidents-live-test-log.md).
No lower TODO item was selected for this run.

### V39 Pogroms and the popular crusade — 2026-10-13, Daniel's request

Spec: [v39](docs/spec/v39-pogroms-and-the-popular-crusade.md). It answers V22 feature 4 and closes
S11's open question: the popular bands are a mod-side peasant army.

**The plan:**
- **The Mob:** a general pogrom mechanic. A preacher's real army besieges communities one by one.
- **Its users:** the Popular Crusade, hooked on a Catholic Great Holy War, and Granada 1066.
- **The aftermath:** trauma, *Kiddush ha-Shem* and asceticism as tenets, forced converts' return,
  and refugees.

**Slices:** 0, the engine spike (eight questions, §10), then 1 the Mob, 2 the Crusade, 3 the
aftermath, and 4 Granada. **Status 2026-10-14: slices 0-5 built and live-tested** (details
and test results in the spec):
- **The Mob, against one community:**
  - the elders' hub, with visits that take travel time and show their odds;
  - the scripted march, the siege of the quarter, and the lord's men;
  - the pogrom outcome, the ransom, and pressure lines in the tooltips.
- **The Popular Crusade:**
  - a Catholic crusade call starts it, and it chains from town to town;
  - allies do not answer a call to arms on their own.
- **The aftermath:**
  - Kiddush ha-Shem, a new tenet, and personal tenets;
  - the Year of the Decrees and the Memorbuch;
  - the forced converts' return (petition or quiet return; the Bet Din's ruling).
- **Granada, 30 December 1066.**
- **Game rules:** popular crusades, and historical crises at game start.
- **Accusations** raise a real mob.

**Open:**
- refugees (via the exiles system);
- a second, eastern host;
- early answers during the months of preaching;
- the V36 rising, still abstract;
- a soak to tune how often and how hard.

V40 (councils, the Firebrand) is Codex's.

### Pillar band effects in tooltips — 2026-10-12, Daniel's request

Each Prosperity, Stability and Greatness breakdown now states the current level's applied
leader modifier. The next and previous bands are shown as hoverable labels with their ranges and
effects. **Verification complete, 2026-10-13:** the 09:30 retry finished Stability and Greatness
roster nesting at 750, Crisis/Legendary endpoint spot-checks, and rendered all three HUD bands
at exactly 150/400/700/950. This closes the remaining checks from the morning pass.
Action Lock requires a real middle-click; the input shim's `button="middle"` sends a right-click.
The final hidden probe confirmed all three Legendary leader modifiers at 950 without new runtime
script errors. Four roster score labels received the earlier live-checked layout fix; the five
other pre-existing row layout warnings remain. See [implementation note §18](docs/implementation/v1-kehillah-implementation.md),
[the morning test](docs/testing/2026-10-13-pillar-tooltip-live-playtest-log.md), and
[the retry log](docs/testing/2026-10-13-pillar-tooltip-retry-live-test-log.md) for coverage and
probe/ownership caveats. **This verification item is closed; the death-screen wording check is next.**

### Kehillah death-screen wording — 2026-10-12, Daniel's request

The vanilla death screen described Kehillah leaders and their appointed successors
as feudal rulers, speaking of thrones, vassals, peasants, armies, and dynastic
heirs. Selected epitaph and successor lines now use communal language for
characters marked as Kehillah leaders. The same vanilla lines remain intact for
other characters. This is a localization change only; succession and player
continuation are untouched. Source and `ck3-tiger` checks passed. Fresh-game
death-screen rendering and a feudal control case remain to be checked live.
On 2026-10-12, Daniel spotted the remaining short heir line, "ascends to the throne."
It now says the appointed Kehillah leader "takes office as the community's appointed
leader," while other successors retain vanilla's motion text. Source and targeted
`ck3-tiger` checks passed; live rendering remains open while CK3 is in use by
another agent.

### Dynasty succession warning and holiday modifier colors — 2026-10-12

Vanilla's "Primary Heir of the wrong Dynasty" warning is inaccurate for Kehillah rulers:
leadership passes by appointment, and a non-dynastic successor does not end the player's game.
The theocracy mechanic used to suppress the warning was removed because it made lay leaders
clergy. Both vanilla primary-heir dynasty alerts are now overridden to exempt the Kehillah
government flag while retaining their vanilla behavior for other governments. Source checked
against CK3 1.20.0.4; fresh-game UI confirmation remains open. The holiday modifier icons also
used the opposite positive/negative suffixes, which colored their names backwards in event
outcome previews. Their icon suffixes now match the effects.

Written 2026-09-07. Roughly priority order. Items 1-3 (the original correctness/verification work
this note referred to) are long since resolved and removed; numbering otherwise kept stable rather
than renumbered, since later items and other docs cross-reference these numbers by hand (e.g.
`kehillah_breakdown_custom_loc.txt`'s own header cites "ROADMAP item 4").

### Holiday event variety — 2026-10-12, Daniel's request

Five one-step events for Yom Kippur, Sukkot and Shavuot are scripted. Two use named Jewish courtiers; the others remain available without them. The Purim gift event now always has an affordable choice. Source checks passed; live rendering and seasonal delivery are pending. See [the implementation note](docs/implementation/jewish-holiday-variety.md).

**Festival-observance refinement, 2026-10-13:** Daniel chose a Jewish flavor overlay for vanilla feasts instead of a separate Sukkot decision or new feast intent. The earlier three-choice decision prototype was removed. A source-checked hook modestly raises holiday-event frequency for Jewish rites with vanilla Ritual Celebrations. The original Feast proposal, calendar limits, and Kehillah hosting limits are recorded in [Mo'adim le-Simchah](docs/spec/jewish-festival-observance.md); the pilot implementation follows below. This user-requested tenet work ran in parallel with the higher-priority live-test TODOs above; it does not close them.

**Feast overlay pilot, 2026-10-13:** A generic vanilla Feast hosted by a Jewish character with Ritual Celebrations now receives one Jewish meal scene, minor Piety, and +5 opinion from attending close family. Recent Pesach, Sukkot, or Shavuot events select the matching meal text; otherwise it stays generic. Source checks passed; live event behavior is pending. The first implementation is recorded in [the feast overlay note](docs/implementation/jewish-festival-feast-overlay.md). Kehillah hosting and Stability rewards remain future work.

**Feast immersion audit, 2026-10-13:** The one-scene pilot does not yet make the whole vanilla activity read as Jewish. Vanilla food-name pickers still allow some non-kosher choices for Jewish hosts, and a Pesach-themed scene can be followed by ordinary bread text. See [the source audit](docs/iteration/2026-10-13-jewish-feast-immersion-audit.md) before extending Feast flavor or modifying food localization.

**Feast presentation pass, 2026-10-13:** Jewish generic Feast hosts now receive the scene without the tenet; Ritual Celebrations adds its Piety and family opinion. A household invitation and host ending frame the vanilla activity, and scoped English food wording avoids the clear non-kosher picker results found by the audit. Holiday theme flags are narrowed to 8/8/2 days, with Pesach bread phrasing guarded where identified. Source checks and an isolated boot passed; live gameplay remains pending. See [the presentation note](docs/implementation/jewish-festival-feast-presentation.md). The Kehillah government still cannot host vanilla Feasts.

**Talmud Torah tenet, 2026-10-13, Daniel's request:** A new Jewish tenet replaces Rabbinism's generic Pursuit of Knowledge slot. It grants modest Scholar lifestyle growth, opens the existing Learn Torah scheme to eligible lay readers, and adds Piety and Learning XP for mastering library works without relying on the Scholar or Rabbi trait. Source and `ck3-tiger` checks passed apart from the known 1.19-linter/1.20-game `rite` mismatch; live display and reward probes remain pending. See [the tenet spec](docs/spec/jewish-talmud-torah-tenet.md). This user-requested feature runs in parallel with the higher-priority live-test TODOs above; it does not close them.

**Talmud Torah Rabbi synergy, 2026-10-13, Daniel's follow-up:** Successful library study adds modest Rabbi track XP for actual trait holders, and the tenet lowers the work-mastery Learning floor from 10 to the existing semicha-entry floor of 8. The two-work/two-field curriculum and study-hall requirement remain. An isolated CK3 boot passed after correcting a pre-existing Learn Torah description-key error; gameplay probes remain pending. See [the dated addendum](docs/spec/jewish-talmud-torah-tenet.md#rabbi-and-semicha-synergy--2026-10-13-addendum) and [test log](docs/testing/2026-10-13-talmud-torah-tenet-check.md).

**2026-10-15 tenet presentation correction:** A live faith tooltip showed the Talmud Torah mastery rules but exposed the wrong passive modifier: Religious Scholar trait XP rather than Learning lifestyle XP. The script now uses the vanilla Learning-lifestyle modifier key, and a fresh live tooltip confirmed the correction. Ritual Celebrations retains its shared vanilla ID and effects, with a Jewish-specific Mo'adim le-Simchah subtitle, description, and existing holiday/feast hooks; a Samaritan live tooltip confirmed the name and text. Halakha retains its shared vanilla ID and existing Jewish tooltip subtitle. CK3's faith cards use generic base names; changing those labels would require a substantial vanilla GUI fork. See [the Talmud Torah correction](docs/spec/jewish-talmud-torah-tenet.md#live-tooltip-correction--2026-10-15-addendum) and [the festival addendum](docs/spec/jewish-festival-observance.md#named-jewish-tenet--2026-10-15-addendum). This user-requested correction runs alongside V42 and does not close earlier TODOs.

**Ba'alei ha-Miqra and study fulfillment, 2026-10-13, Daniel's follow-up:** The separate branch now gives Karaism a scriptural-authority tenet in Literalism's slot and a continuing Examine Scripture course that progresses Religious Scholar instead of Rabbi. Rabbinic book mastery and successful Karaite scripture courses now grant small Spiritual Fulfillment gains for playable readers. Faith-level starting statuses prohibit the opposing authority tenet in Rabbinism and Karaism while leaving generic Torah study available. Source review and `ck3-tiger` checks passed with known 1.19/1.20 syntax-model mismatches. **2026-10-13 evening correction:** a separate CK3 instance mounted this worktree and reached the main menu on the extended virtual display; live gameplay and status display remain pending. See [the new addendum](docs/spec/jewish-baalei-hamiqra-tenet.md) and [source/boot log](docs/testing/2026-10-13-baalei-hamiqra-source-check.md). This user-requested pass continues in parallel with the older live-test TODOs above.

**2026-10-14 live correction for the separate branch:** A fresh Worms game on the virtual display confirmed Talmud Torah on Rabbinism, reader eligibility and the lower mastery floor. A forced Mishnah course reached first mastery and appeared in the library. The same game confirmed that Rabbinism prohibits Ba'alei ha-Miqra and Karaism prohibits Rabbinic Halakha. The Karaite course, precise Piety/Rabbi XP/Spiritual Fulfillment deltas, and feast presentation remain open. The community map now sits in the Faith-family button row; its roster, region paint, barony highlights, locate action, and both map hover branches were checked live. See [the live log](docs/testing/2026-10-14-faith-map-navigation-live-test.md) and [the map addendum](docs/spec/2026-10-13-faith-map-navigation-and-nusach.md). This map request was handled ahead of the older TODOs at Daniel's direction.

**2026-10-14 map visibility pass, Daniel's follow-up:** The separate branch has brighter, more distinguishable customary-region colours and matching colour swatches in the community roster. Live Worms testing confirmed the Rhineland tint, host-barony highlights, swatches, and “Customary region” hover wording. An attempted province GUI pin rendered in Details mode but not in the custom map at the tested paper-map zooms; its vanilla GUI override was removed. A proven dynamic on-map pin and actual community Nusach remain open. See [the visibility log](docs/testing/2026-10-14-map-visibility-live-test.md). This user-requested map pass also ran ahead of the older live-test TODOs.

**2026-10-14 Domain overview, Daniel's follow-up:** A Kehillah-only summary now sits below the Jewish Quarter card in My Realm > Domain. It shows Standing, pillar bands and trends, host ruler, and recorded charter terms; the redundant top-left score strip is retired. The Faith-family map button still opens the cross-community roster. This requires a full `window_my_realm.gui` override and will need review after game updates. See [the implementation note](docs/implementation/kehillah-domain-overview.md) and [the live test](docs/testing/2026-10-14-kehillah-domain-live-test.md). This user-requested UI pass ran ahead of the older live-test TODOs.

**2026-10-14 main integration, Daniel's request:** Main's V35 Your Host tile and V40 recent-incidents hover were reconciled with the Domain overview. The host outlook and invitation cue now appear in Domain when the quarterly host mirror exists; its hover retains the full outlook, goodwill, and incidents breakdown. The separate Faith-family map and roster remain available. See [the integration note](docs/implementation/kehillah-domain-overview.md) and [merged live check](docs/testing/2026-10-14-domain-main-merge-check.md).

**2026-10-14 Domain visual polish, Daniel's follow-up:** The overview now has a compact icon/name/Standing header, three shaded pillar cards, and dividers before the host and charter details. A separate CK3 instance confirmed the fresh and populated charter states, the pillar and host tooltips, and no clipping or new GUI/localization errors. See [the visual check](docs/testing/2026-10-14-domain-visual-polish-live-test.md). This user-requested UI polish ran ahead of the older live-test TODOs.

### Exceptional sefarim — 2026-10-12, Daniel's request

The `kehillah_book.0007` arrival event was misleading: it only granted Piety and
Learning lifestyle XP, without adding a library work. The ordinary-book chain
now chooses one of 14 stable named subjects at completion, including two
subjects drawn from a remembered Bet Din case. The author's completion event,
personal artifact, and delayed news event use the same title and description.
The recipient event reports scholarly discussion without claiming a library
copy or dwelling on its absence. Source checks passed; live rendering and
save/reload confirmation remain open. See
[the implementation note](docs/implementation/kehillah-ordinary-book-identities.md).
**The larger system is a proposal, not built:**
[v32](docs/spec/v32-exceptional-sefarim.md) describes rare
named works created by qualifying scholars during play, with visible progress
and real library copies. First next step is a one-work data/GUI spike, then an
end-to-end vertical slice. This user-requested correction and design review
precede the older v30 live-test TODO; they do not mark that test complete.

### Expulsion and the householders (v30) — 2026-10-12, interactive

Daniel asked for expulsion and for the householder system to be rebuilt ("very tacked on ...
without clear connection to the rest of the kehillah mechanics"). Design and decisions:
[v30](docs/spec/v30-expulsion-and-householders.md).
**Built and `ck3-tiger`-checked, NOT yet live-tested**; v30 §3 is the test plan.

- **Expulsion (S9b): built.**
  - **Edict:** a realm going Banned issues an edict to every community in it, with a year's
    grace.
  - **Counterplay:** plead through the Shtadlan, offer a ransom (a deceitful host may keep it),
    leave in good order, or wait.
  - **Enforcement:** leave (the crown seizes half the leader's gold and voids the community's
    debts) or stay in hiding (a heavy Stability drag, and driven out a year later).
  - **The ending** is the existing dissolution teardown. Daniel chose this over relocating the
    Quarter.
  - Probes: `events/kehillah_expulsion_debug_events.txt`.
- **AI policy review (V17 Slice B, first pass): built.**
  - AI rulers move the policy one rung per review, with a 10% yearly chance per host and the
    five-year cooldown.
  - Named pressures only: zeal, a zealous chaplain, debts to Jews, grievance, temper, against
    justice, compassion, a patron or a prosperous community.
  - Banned needs Discouraged first and two distinct pressures.
  - The reason prints in the policy notices.
  - The host decision now reaches Banned.
- **Householders reworked: built**, then stripped back the same night at Daniel's direction.
  - It runs in the background with side notifications. The register decision and the
    arrival/departure events are removed.
  - The register is observed from the court.
  - A head carries a "Ba'al Bayit" character modifier: flavour, +0.5 gold a month, and a target
    for future events.
  - Each family adds a flat 25 to its trade's pillar, capped at 100.
  - The next family is found in this order: a councillor, then an established, skilled or
    wealthy courtier (dynasty prestige first; lowborn men found a family name), then a family
    from another community, then a newcomer.
  - **Household standing is removed**, along with its succession term and its debug probes
    .11–.13. Dynasty prestige already covers it.
  - No opinion effects.
  - AI leaders fill empty lay council seats from householders.
  - **2026-10-12 notification correction:** passive removal from the observed register is
    silent; the report showed an empty, overly prominent "A Household Is No Longer Counted"
    notice. Actual family moves still notify the player. See v30 §2.
  - **2026-10-12 presentation correction:** the remaining household messages use a dedicated
    sidebar feed filter with full descriptions, instead of Court Grandeur's large banners.
    This awaits a fresh-game UI check.
- **Next:** the live test in v30 §3. It is also the first live run of S1's collapse path
  (criterion 2).

### The host relationship (v31) — 2026-10-12, interactive

Daniel wants the host relationship to be the core challenge: dynamic, tied into vanilla, and
driven by personality, economics and ideology. Design:
[v31](docs/spec/v31-host-teachings-stances-and-factions.md). **PROPOSAL, nothing built.** This
is the S11 "friendliness" design review; the Crusades chain stays separate and builds on it.

- A "Teaching on the Jews" doctrine on each rite. Latin: Witness → Separation and Mission →
  Exclusion. Byzantine: Imperial Law. Muslim: Dhimma → Strict Pact → Abolition, on top of
  vanilla's jizya. Councils and reform movements change it.
- Zeal is scaled by the teaching. A zealous Witness bishop protects.
- Personal ruler stances: Protector, Convinced, Predator, Pragmatist.
- An anti-Jewish vassal faction: debt relief, then restriction, then expulsion.
- A tribute term: jizya, or tallage plus a confirmation fee.
- **Forced conversion, built and LIVE-TESTED 2026-10-12** (v31 §10.2, [log](docs/testing/2026-10-12-forced-conversion-live-test-log.md)). A host may demand an
  AI Kehillah leader's conversion only when his realm bans Jewish settlement. This is a
  stand-in until the teachings exist. Any leader who leaves Judaism steps down within a quarter
  and becomes a playable wayfarer; the community dissolves if he has no successor. Succession
  scoring no longer favours the convert's co-converts. Probes: `kehillah_conversion_debug.1`–`.3`.
  The live run found two bugs, both fixed and re-tested: a charter leaking onto the wayfarer,
  and the successor styled "Duke".
- **Forced conversion, part 2, built and live-tested 2026-10-12** (v31 §10.3; the AI host's own demand is inconclusive: the test's debug ban skipped the review cooldown, so re-test with `kehillah_expulsion_debug.2`). Hosts can reach
  player-led communities through a copied vanilla interaction. AI hosts demand "convert or leave"
  while an expulsion edict stands. A player convert may carry on as the heir. Probe:
  `kehillah_conversion_debug.4`.
- **Slice A, the teachings, built and LIVE-TESTED 2026-10-12** (v31 §4–5, [log](docs/testing/2026-10-12-teachings-live-test-log.md)). Every Christian and
  Muslim rite gets a "Teaching on the Jews" at game start: Witness, Imperial Law (Eastern) or
  Dhimma. The AI policy review scales zeal by the teaching and refuses Banned under a protective
  teaching. Forced conversion now follows the teaching: the Strict Pact, Exclusion or Abolition
  allow it; a non-Abrahamic host still needs Banned. **In 1066 every host is protective**, so
  this adds variety but no pressure until rites move (Slice E, councils and reform) or the
  faction and incidents exist (Slices D and G). Probes: `kehillah_teaching_debug.1`–`.5`.
- **Balance finding, 2026-10-12 soak (session 0f):** across about 58 logged years, the AI policy
  review ran about 35 times and moved a policy 3 times (1 down, 2 up). Nothing reached Banned and
  no edict was issued. Expulsion and forced conversion therefore never happen in ordinary play.
  The host relationship needs pressure that builds over time (v31 incidents, the vassal faction).
- **Decided 2026-10-12:** tribute starts at 20% of income; every convert steps down. Still open
  (v31 §14, §16): secret Jews after conversion, non-rabbinic Jewish faiths, reaching a
  player-led community with forced conversion (answered: v31 §10.3).
- **Tribute, part 1: BUILT 2026-10-30, not live-tested** ([addendum](docs/implementation/2026-10-30-host-tribute.md)). Every charter has a Tribute term: None, Customary (20%, the default) or Heavy (30%). It is paid each quarter by script and shown as "Paid to host" on the Domain tab. This sidesteps the engine-tax spike (§11.2) rather than answering it. The levy, the confirmation fee and the regional names are not built.
- **Next:** live-test v30. Then v31 §11's spikes (doctrine group on rites, tributary
  tax on a Kehillah, custom faction), then the slices in §12. Open questions for Daniel: §14.

### Shabbat autonomous queue — 2026-10-09 evening to 2026-10-11 morning (works ABOVE everything below)

Daniel is offline for Shabbat. The `JewishCommunities-ShabbatHeartbeat` task runs every 5 hours on
branch `autonomous/shabbat-2026-10`. Same rules as Sukkot: BUILD means implement and live-test;
make small design choices and note them; no long specs. CK3 runs on a **virtual display**
(VirtualDrivers VDD, duplicating the 2560×1440 screen), so the physical monitor may be off; see
the shim guide. Current state is in the
[clerical succession log](docs/testing/2026-10-09-clerical-succession-live-test-log.md).

- **Interfaith marriage and Jewish descent — corrected 2026-10-11 (interactive,
  Daniel's request):** all existing Jewish faiths default to Forbidden outside
  Judaism and Matrilineal descent. The corrected marriage trigger was verified
  live with an eligible Jewish/Jewish pass and Jewish/Christian denial. The
  rite-creation UI showed Forbidden/Permitted and all three descent choices.
  The Find Spouse list for a Jewish courtier returned 0/125 with the Religion
  filter set to Not Judaism, confirming no non-Jewish candidate appeared.
  Completed rite creation and mixed-parent birth checks are still open; see
  [v27](docs/spec/v27-interfaith-marriage-and-descent.md) and the
  [live test](docs/testing/2026-10-11-interfaith-marriage-live-test-log.md).

- **Patronyms and priestly lines — BUILT 2026-10-11, not live-tested** (interactive, Daniel's request;
  [v28](docs/spec/v28-patronyms-and-priestly-lines.md)). Israelite cultures now print "ben"/"bat"
  patronyms; `kohen`/`levite` are seeded on generated Jewish characters and inherited father to son; 26
  random `dynn_Ben_*` names were pruned. Live check: `event kehillah_patronym_debug.1` and look at a
  named character with a defined father. Exilarch "Ben David" guidance is in the spec.

- **Lay courtiers as "Jewish Clergy" — FIXED 2026-10-10 (interactive, Daniel's report), mechanism
  verified live, shipped effect awaits a fresh boot**
  ([log](docs/testing/2026-10-10-lay-courtier-clergy-live-test-log.md)). A side effect of H1's
  `mechanic_type = theocracy`: the engine generates a theocratic ruler's courtiers as
  faith-organization members, so Kehillah courts filled with clergy wives and townsfolk (76
  courtiers with no clerical role, live). `kehillah_laicize_character_effect` strips the
  membership on court arrival and in a quarterly sweep, keeping it for the Rabbi trait,
  `devoted`/`cleric` and the Dayyan seat. A probe showed `leave_organization` sticks.
  - **Superseded 2026-10-11 (Daniel's call): Parnasim are no longer clergy, and vanilla's death
    screen still works.** H1's `mechanic_type = theocracy` was removed. CK3 gives a non-dynastic
    "Continue as" only when **both** the dying ruler and his successor are faith-organization members,
    measured live. So `kehillah_on_death_player_continuation` enrols a dying lay Parnas and his
    successor just in time, and the new leader leaves the organization on taking office. **Verified
    live:** a lay Parnas died and vanilla's screen offered "Continue as Parnas Amos". Amos was lay
    afterwards. No trait was added, and rabbis stay clergy through their trait. See implementation doc
    section 15.
  - **Done 2026-10-11 (implementation doc section 16):**
    - Leaders are named "Rav" only when they have the Rabbi trait, otherwise "Parnas".
    - "Rabbenu" is earned at piety level 4 and kept once earned.
    - The Dayyan must be a rabbi, and is styled "Rav <name>".
    - The rabbinic organization is named "Hakhamim".
    - The Chief Rabbi court position and its toggle decisions are removed. The community rabbi is the
      leader if he is a Rav, otherwise the Dayyan. "Seek a Rabbi" seats its find as Dayyan.
    - **Verified live:** the names, Rabbenu, Hakhamim, the Catholic fallback, and the Dayyan's "Rav"
      styling.
    - **The Chief Rabbi refactor, verified live (fresh boot):**
      - All 15 Dayyan seats were filled by rabbis at game start, with no seating errors.
      - `kehillah_debug.118` bound Isaac as the community rabbi while he was a Rav, and the Dayyan once
        his trait was removed.
      - Only "Seek a Rabbi" remains among the rabbi decisions.
      - A full search, from an empty seat to a candidate chosen, seated Rav Gad as Dayyan, and the
        Greatness term rose from 43.2 to 55.2.
      - No new errors and no missing localization.
  - **Follow-ups, all done 2026-10-11 and verified live:**
    - **The Dayyan can be fired and reassigned in a Kehillah.** Two vanilla locks were exempted in
      the council override: the clerical-doctrine `can_fire`/`can_reassign` rule and
      `can_change_once`. Firing him through the UI empties the seat, at a -20 opinion cost, and
      Seek a Rabbi becomes available.
    - **"New Realm Priest" now reads "New Dayyan"** with "Your Dayyan, X, takes his seat on the Bet
      Din with your blessing", through custom localization on the engine message. Other realms keep
      vanilla's text.
    - **Removing the Rabbi trait now also removes organization membership** via
      `kehillah_remove_rabbi_trait_effect`. Only debug events remove the trait; debug event .9 now
      yields a truly lay leader.
    - **The Bet Din's "rabbi to sit as Av Beit Din" requirement line** shows in red when unmet and
      disappears when met.
    - **Bonus: header art.** The Bet Din and Yeshiva Visit activities had no header image, which left
      a blank planner header, about 16,000 "Missing on demand texture" lines and a boot "missing
      Header Background texture" error. They now use vanilla's Adult Education study hall
      (`header_background` field plus the list icons). The header renders and the boot error is
      gone. The new list icons have not yet been looked at in the UI.
  - **Pre-existing activity errors noticed, not touched:**
    - Learn Torah journey: "no default guest intent" and "max_guests below 0".
    - The Bet Din's four default invite rules are "already an entry in the valid invite rules".

- **PROPOSAL: cross-pillar building gates (Daniel's question, 2026-10-11; not decided).** Every
  building line is gated today on the pillar it feeds:
  - Synagogue, Beit Midrash and Sofer's Workshop are gated on Greatness and feed it.
  - Countinghouse, Market Stalls and Workshops are gated on Prosperity and feed it.
  - Hekdesh is gated on Stability and feeds it.

  So a strong pillar snowballs and a weak one stays weak. The idea is that each line's upper tiers are
  gated on a different pillar:
  - learning on Stability;
  - communal institutions on Prosperity;
  - commerce on Stability or Greatness.

  This affects every building and the balance. Decide after V29's Stability-gated Yeshiva has been
  seen in play.

- **V33 PRESSURES and V34 OUTLOOK: built 2026-10-12/13; V34 live test pending** ([v33](docs/spec/v33-pressures.md), [v34](docs/spec/v34-outlook-teachings-and-founding.md)).
  - **V33:** Stability rests at Healthy and is pulled down by the host, policy, war, holy war, tension and teaching. It falls fast and recovers slowly. Prosperity follows the county. Overcrowding is a soft population limit. Soak: [2026-10-13](docs/testing/2026-10-13-v33-pressures-soak.md); Prosperity is still too flat.
  - **V34:** an outlook on the Jews for every character. Teachings change by a head of faith's outlook (yearly, and at councils) and by vanilla rite drift. Masmudi (the Almohads) teaches Abolition. Popular risings found Exclusion rites. The policy review reads outlook, and a policy change revises existing charters. Natural founding: about one community every 5 years.
  - **V34 section 7, invitations (2026-10-13):** a yearly open-door review lets a ruler with no Jews raise their policy by outlook, and Encouraged sends invitations: news, plus a pull on settlers and exiles.
  - **Live-tested 2026-10-13.** An invitation answered gives +60 Prosperity / +30 Stability and +5 outlook for the lord. More outlook sources: Jewish friends and rivals, crusade pledges. The Shtadlan's **Seek an Invitation** council task courts lords abroad. A **Prosperity floor** of 150 (no community starts in Crisis). The AI's settlers weight was raised: the gates probe found 5 of 23 communities eligible, but the AI chance was 1-11%. A 25-year soak of the AI founding rate is pending.
  - **V35 player clarity (2026-10-13)** ([v35](docs/spec/v35-player-clarity-outlook-and-invitations.md)): outlook bands in the host-attitude line, the invitation news and the Shtadlan's messages. "The Lord Grows Warmer/Colder" notices. An invitation event with the lord shown, for communities that can answer it. Settlers' destinations say why they draw.
  - **V36 host levers and crises (2026-10-13)** ([v36](docs/spec/v36-host-relationship-levers-and-crises.md)): violence scaled by the lord's protection (his outlook and the charter's security term). "The Lord's Demands", in which a Cold or Hostile lord demands a levy or forces a worse charter, answered by paying, the Shtadlan, an appeal to the head of the faith, or refusal. Levers: Present a Gift, Forgive the Debt, and generous loan terms.
  - **V36b/c and V37 (2026-10-13):**
    - The Lord's Favour.
    - Outlook traits.
    - A colder world: outlook "prejudice", Christian -15, Muslim -10.
    - Accusations ([v37](docs/spec/v37-accusations.md)): the blood libel or blasphemy, answered by the Shtadlan, paying for protection, an appeal, or barring the gates. The outcome is scaled by the lord's protection.
  - **Next:** a V34 live probe, then a soak. Prosperity tuning (development x8 or a floor). More outlook sources. The anti-Jewish faction.

- **V30, COMMUNITY NEWS: built and verified live 2026-10-12** ([spec](docs/spec/v30-community-news.md); test log run 20).
  - Quiet feed notices under a 'Community News' filter: your host lord dies; and, in your minhag region, a charter ends, new leadership, a pillar in Crisis, a new or Renowned+ yeshiva, a Bet Din concludes.
  - V29 §12 also added 'Yeshiva News' (newcomers, chavrutot, works and subjects mastered), and fixed every mod message's blank body.
  - Open: the 'minhag practice' line in the Bet Din notice is waiting for takkanot (v25 P7).

- **V29 §11, THE LEADER'S YESHIVA: built and verified live 2026-10-12** (test log runs 16-17; the
  "send to a community with no rabbi" option is not yet exercised)
  ([spec §11](docs/spec/v29-yeshiva.md)).
  - Yearly ordination with "The Graduating Class" choice (keep / send / recommend to the lord).
  - The head's depth in the focus sets study XP and whether renown holds.
  - The 1066 heads are seeded as masters.
  - Teaching-focus buttons in the library panel.
  - Also removed 2026-10-12: Take Stock decision, View Kehillah Communities interaction.

- **V29 §10, THE LIVING YESHIVA: built and verified live 2026-10-11** (test log runs 12-13;
  open: the arrival event `.0301` was not reached live, and only some students got a rebbe link)
  - **Cleanup 2026-10-11:**
    - Removed the zman system and Seek Semicha (decision plus ceremony event `kehillah_semicha.0001`).
    - Kept the childhood guardian-endorsement path (`.0002`/`.0003`).
    - Checked with ck3-tiger and a scan for dangling references; not booted live.
  ([spec §10](docs/spec/v29-yeshiva.md)).
  - **Enrolment:** continuous, for unordained rabbinic Jewish men aged 16+ with Learning above 8.
    Courtiers enrol automatically, travelling students arrive over time, and rabbinic players of any
    government travel there and enrol.
  - **On enrolment:** the Rabbi trait, but no offices until ordination.
  - **Study:** counts only while the student is present (no activity a war can cancel).
  - **Graduation:** a quarterly check (two years present), then ordination by the Rosh Yeshiva.
  - **The yeshiva's specialization** gives a study bonus.
  - **Relations:** rebbe/talmid (shown in the court list as "Rav X's Talmid") and chavruta.
  - **Display:** a student list in the panel.
  - **Replaces** Hold a Zman, Seek Semicha and the journey's zman option.
  - **Later:** upkeep per student; richer events.

- **V29 THE YESHIVA: FIRST IMPLEMENTATION PASS BUILT AND VERIFIED LIVE 2026-10-11**
  ([log](docs/testing/2026-10-11-yeshiva-live-test-log.md)).
  - **Verified live:** the Worms seed; the great map building (spike 1 passed); the Rosh Yeshiva
    position; the scholar event; founding at Mainz; and the Greatness fame row.
  - **Verified live in a third run:** the quarterly fame pulse; the zman, ordained (+10 track XP,
    +2 fame) and unordained (credit, then ordained on the spot).
  - **Not covered:** traveller events.
  - **Section 9, the Worms gameplay loop: BUILT AND VERIFIED LIVE 2026-10-11** (test log runs 6-10).
    - Hold a Zman, with events during the term.
    - Ordinations by the Rosh Yeshiva, with two terms needed for semicha.
    - Alumni seated as Dayyanim elsewhere.
    - Fame tiers and their notices, and the Great Yeshiva.
    - The Yeshiva section of the library panel.
  - **New communities and seeds (2026-10-11):**
    - Lucena, Jerusalem, Mahdia (with the ruined Kairouan hall) and Sura.
    - Baghdad is now the Exilarch's seat with the Yeshiva of Pumbedita.
    - Narbonne is seeded.
  - **Decided 2026-10-11:** players see the yeshiva's **renown** as tiers only (Modest, Respected,
    Renowned, Illustrious, with "growing toward" or "nearly" the next). The number stays behind the
    scenes.
  - **Not built yet:**
    - V29 section 4, where the tracks affect the Bet Din, responsa and charters;
    - Seek Semicha's retirement (kept for now);
    - the host's "Jewish attractiveness" benefit (needs V16/V18 hooks);
    - the Yeshiva panel in the domicile window;
    - the map-view marker.
  The design, agreed with Daniel 2026-10-11:
  ([spec](docs/spec/v29-yeshiva.md)).
  - **Founding:** a rare "Found a Yeshiva" decision, aiming for 10–25% of communities. It needs
    Stability Healthy, Greatness Strained, the House of Debate, a qualified Rav (high Learning, a
    track at 65+) and gold. There is no regional cap. A founding draws ordained rabbis as Dayyan
    candidates and judges.
  - **Rosh Yeshiva:** the leader can hold it.
  - **The zman:** a mod-owned activity grown from today's Yeshiva Visit, not vanilla University
    Visit.
  - **Map building:** a great or special building in the host's province. Its host benefits are tied
    to Jewish attractiveness, development, a little prestige and charter goodwill.
  - **Travellers:** a vanilla travel point of interest whose events reach Jewish and non-Jewish
    travellers.
  - **Seeding:** Worms only. Not Baghdad: the Geonic academies had ended by about 1040.

- **H1. DONE — VERIFIED LIVE 2026-10-09 (Shabbat heartbeat 1)**
  *(SUPERSEDED 2026-10-11: the theocracy mechanic below was removed; see the lay-courtier entry above)*
  ([log](docs/testing/2026-10-09-lay-clerical-continuation-live-test-log.md)).
  Clerical continuation for lay (Parnas) leaders without a new trait. **The answer was a
  government field, not a trait.** `_governments.info` documents `mechanic_type = theocracy`
  as, verbatim, "Should rulers be considered clergy" — that is how vanilla's non-monk clerical
  rulers (bishops under `ecclesiastical_government`, `theocracy_government` holders) are
  clergy at all; neither carries the `devoted` monk trait. `kehillah_government` now sets
  it. Deliberately NOT the `government_is_theocracy` flag: church authority,
  bishop-theocratic succession and theocratic elective all gate on the flag or on a doctrine
  rabbinism lacks.
  - **Why the scripted `join_organization` never worked** (the other half of H1's question):
    vanilla keeps a faith organization's membership equal to its clergy — "A faith's
    organization members are exactly its clergy, so this never touches the laity"
    (`common/on_action/game_start.txt`) — so a script join onto a non-clergy character is
    reverted. That is also why the join read as absent on all three lay appointees right after an
    appointment succession. The call is left in `kehillah_update_leader_flavor_effect` as an
    inert fallback.
  - **One collision, guarded:** vanilla's `clerical_appointment_law` starts on any ruler with
    the theocracy mechanic at county tier or above, and `_laws.info` says starting laws are
    picked in *definition order* (index is display order only), so vanilla's file would win and
    the Kehillah would silently lose `kehillah_appointment_succession_law`.
    `common/scripted_triggers/kehillah_clerical_appointment_law_override.txt` forks vanilla's
    trigger with one exclusion for this government.
  - **Probes:** `kehillah_household_debug.8` reports clergy / organization / player heir /
    title heir / which succession law is actually in force, read-only; `.9` strips the Rabbi
    trait first so the pure lay path can be checked on its own.
  - **Live result:** with the Rabbi trait stripped, a pure lay leader reads `CLERGY YES`,
    `ORGANIZATION YES`, `PLAYER HEIR YES` and *non-dynastic* heir, and `kill 29176` produced
    **"Continue as Rav Mishael"** plus "Choose a New Destiny..." — not Game Over. Continuing
    worked: "Rav Mishael, 42 — This is you", holding Kehillah of Worms. The realm law was still
    `kehillah_appointment_succession_law`, so vanilla's `clerical_appointment_law` did not take the
    slot. No new `kehillah` errors.
  - **Still open, no longer gating:** the one unexplained rabbinic-path Game Over from the morning
    run. `kehillah_debug.104` only arms a trace flag, so it cannot have caused it, and clergy
    status no longer depends on a trait at all. Worth one rerun.

- **H2. CLOSED — VERIFIED LIVE 2026-10-10 (Shabbat heartbeats 3 and 4)**
  *(header corrected 2026-10-10, heartbeat 5: it still read "one path still open" while this
  entry's own body already said "H2 is now closed". The only remaining item is the honestly-null
  natural-move-on-an-unpaused-clock observation below, which the body calls close to settled. A
  stale header is exactly what made heartbeat 4 build a duplicate succession term today — see
  the ba'alei batim slice 2 entry.)*
  ([log](docs/testing/2026-10-10-baalei-batim-paths-live-test-log.md)). All four player-facing
  option paths exercised with real clicks and a real negative control, and the exact household
  count measured on each side of every click with a purpose-written `h2_count.txt` run file.
  - **All four options behave.** Arrival option b pays the player **+15** and the register goes
    3 → 4; option c refuses and the count holds, rendering the **refused-return** variant
    ("the family settles in the community it came from instead" — the origin holder, Speyer,
    existed). Departure option b costs **−50** and the family stays; option c costs nothing and
    the family stays; option a — the control — drops the count by exactly 1. That control is the
    load-bearing part: the "stays" options have no departure effect to cancel, so a no-op event
    would have faked both PASSes.
  - **One real bug, found and fixed: a player who receives a family was never told.**
    `kehillah_household.0003` gates on `exists = scope:kh_mig_house.var:kehillah_household_head`,
    but that variable is written in exactly one place (`kehillah_household_refresh_effect`) and
    `kehillah_household_migrate_effect` does not write it — so at the moment
    `kehillah_household_leave_effect` fires the event the head is absent (any AI donor whose
    yearly pass has never run, i.e. the normal early-game state) or stale (naming the *donor's*
    pick). `trigger_event` onto a false `trigger` fails **silently**: no event, no error, nothing
    in `debug.log`. The register moved correctly every time; nobody was informed. Fixed by
    refreshing the recipient before the event, which also fixes the new community's stale
    adults/seats/standing, plus a `debug_log` so the next silent non-firing is visible.
    **The fix is source-verified and ck3-tiger clean, NOT yet re-run live** — the next heartbeat
    should re-run `.10` and confirm `.0003` appears with its description naming the donor.
  - **Update 2026-10-10 (Shabbat heartbeat 4): the re-run happened, in heartbeat 3's lost
    subagent session, and its result was recovered from `debug.log`. The fix above is right
    and stays, but it could not be proven, because the family `.10` was handing over did not
    exist as people** — the new guard fired twice ("a player received a family with no head at
    their court"). No recipient-side refresh can invent a head for a family with no members.
    Two donor-side defects behind it, both now fixed:
    - `kehillah_household_save_lowest_effect` **preferred the ghost**. `order_by` is
      `0 - standing`, so every real family scored negative while an entry with no standing
      variable scored exactly 0 and beat all of them — the least-trustworthy entry on the
      register was always the one chosen to leave. Missing standing now sorts last, via a
      sentinel rather than an exclusion, so a community can always still lose a family.
    - **`.10` was not testing the real path.** Real play is refresh-then-depart
      (`kehillah_household_yearly_effect`), so a genuine departure always picks from a
      just-recounted register where every entry has a head and a standing. `.10` reached into
      an AI register nothing had ever refreshed; it now refreshes the donor first.
    Note the consequence: **ordinary play was never exposed to the first defect**, since
    refresh writes standing on every entry it keeps. Both are hardening, plus a probe that now
    represents the path it claims to test. Speyer's register gave it away — six entries, the
    first with neither `kehillah_household_of` nor `kehillah_household_head`, and
    `kehillah_household_add_effect` sets `household_of` unconditionally, so that entry cannot
    have arrived by the normal route. **VERIFIED LIVE 2026-10-10**
    ([log](docs/testing/2026-10-10-courtier-institution-live-test-log.md)): zero occurrences of
    the no-head guard line, both `.10` assertions pass, and the popup renders in real English
    naming the donor ("A Family Arrives" / "...has arrived from Kehillah of Córdoba..."). The
    migration's own delta is a clean +1, confirmed two ways — the `.10` internal assertions and
    a `kehillah_household_origin` probe — after the raw count (0 → 3) turned out to include two
    locally-founded households swept in by root's own bootstrap. Independent corroboration that
    a real person moved, which was the whole point: the arrived migrant appears as a Chief Rabbi
    candidate in Check C's appointment panel, which a ghost family could not do. **H2 is now
    closed.**
  - **A natural move on an unpaused clock: NOT OBSERVED**, honestly null — ≈2y9m of unpaused
    time, no popup. Close to settled anyway, because `.4` ran the real
    `kehillah_household_yearly_effect`, its real 30% roll **hit**, and a genuine `.0002` fired
    and resolved end to end. At 30% a year against a community sitting exactly at its cap, the
    null is unremarkable.
  - Also recorded from this run, in [the shim guide](docs/testing/automation-shim-guide.md): a
    skill change does not reach a trigger on a **paused** game without
    `force_character_skill_recalculation`, which is why `h2_setup.txt` could not clear
    `diplomacy >= 12` at +12, +15 or +100; and where `ck3.exe` actually lives (the E: drive).
  - *Historical note, superseded:* heartbeat 1 recorded an H2 test as "in flight" that was cut
    off and produced nothing, and heartbeat 2 correctly reset this item to untouched. Both are
    now moot.
- **H3. DONE 2026-10-09 (Shabbat heartbeat 1).** The `kehillah_restore_quarter_effect` /
  `kehillah_restore_track_2/3_effect` "Failed to fetch variable for 'kq_countinghouse' /
  'kq_workshops' / 'kq_market_stalls'" errors on `kehillah_on_title_gain`. They **predate
  today**: only the first `if` in each restore helper checked `exists = var:$VAR$`, so
  every tier comparison after it read `var:$VAR$ >= N` on a track the community never built —
  and that is from the file's first commit (7a64e2a, 2026-09-07). Pure log noise, never a
  behaviour bug: "no variable" and "variable below this tier" both correctly restore nothing.
  Every comparison is now paired with its own existence check. (**Correction, same session:** an
  earlier version of this entry credited the fix with dropping ck3-tiger's warning count from 127
  to 111. Don't rely on that — a controlled A/B of the same tree showed tiger's own totals move
  by ~10 warnings run to run, in vanilla files, so its counts are not a usable before/after
  measurement. The fix stands on the source read and on the error lines matching exactly the three
  unbuilt tracks.)

- **H4. All five slices built. Slices 3, 4 and 5 VERIFIED LIVE (slice 3 on 2026-10-10,
  heartbeat 2; slices 4-5 on 2026-10-10, heartbeat 4 —
  [log](docs/testing/2026-10-10-courtier-institution-live-test-log.md)). Slices 1-2 are the
  inert gate and the records layer both of the above exercise.**
  **The one carried qualification is now CLOSED: all three credit bands have a live verdict
  as of 2026-10-10 (Shabbat heartbeat 5) — [log](docs/testing/2026-10-10-credit-bands-live-test-log.md).**
  The FOUNDATION band (Learning 6-7) had never been observed; it now passes, on a real
  courtier, awarding the field credit and only the field credit.
  V21's ordination path: the Rabbi trait stops being
  reachable only through history, an office, or a Bet Din invitation. Slice numbering is
  [V21 section 6](docs/spec/v21-rabbi-ordination-paths.md)'s own.
  - **Slice 1 (gates) — built.** `common/scripted_triggers/kehillah_ordination_triggers.txt`:
    one named candidate trigger composing the faith, adult/free/capable, Learning and gender
    checks, reusing `is_rabbinic_authority_jewish_trigger` (not the broader Jewish trigger — a
    Karaite must not receive a trait called Rabbi) and the existing
    `kehillah_leadership_gender_eligible_trigger`. Thresholds live in
    `common/script_values/kehillah_ordination_values.txt`. Committed inert on purpose.
  - **Slice 2 (records) — built.** `kehillah_study_specific_work_effect` now guards every
    `add_trait_xp` and records an unordained reader's progress instead
    (`kehillah_mastered_works` plus `kehillah_apprentice_fields`).
  - **Slice 3 (Seek Semicha) — VERIFIED LIVE 2026-10-10**
    ([log](docs/testing/2026-10-10-semicha-ordination-live-test-log.md)). All eleven checks pass,
    with non-vacuous negative controls: the Greatness reward landed at exactly 15, the three
    requirement lines render as real English, and the ceremony shows one portrait because the
    player is the community's own holder. **One real bug found and fixed:** the readiness trigger
    read `variable_list_size` on lists that do not exist until a character has studied, which the
    engine logs as an error for most of the population the decision is shown to — the same shape
    of bug as H3, now paired with `has_variable_list`. Still untested: the landed-ruler and
    landless-adventurer institution branches, the defer option across a save/load, and losing
    access to the Beit Midrash (all V21 section 7). Learn Torah's decision and the study scheme admit a
    candidate, not only an ordained rabbi; a candidate with two works from two fields can
    present himself at a Beit Midrash and be recognised
    (`common/decisions/kehillah_semicha_decisions.txt`, `events/kehillah_semicha_events.txt`,
    `common/scripted_effects/kehillah_ordination_effects.txt`). Tier 1 is enough to ordain;
    a Yeshiva only improves the ceremony. **No roll on the outcome** — section 3.4 forbids a
    permanent random rejection after the player's investment — and deferring touches no
    variable at all, so recorded progress cannot be erased. Probes:
    `events/kehillah_semicha_debug_events.txt` (`.1` read-only state dump; `.2`/`.3`/`.4` force
    candidate, curriculum, study hall).
  - **Slice 4 (the rabbinic apprenticeship) — built 2026-10-10, NOT live-tested.** Section 3.3.
    One year per childhood birthday on which a qualifying rabbi is the guardian right then
    (`kehillah_observe_rabbinic_education_effect`, on vanilla's `on_birthday_childhood`), so four
    *accumulated* years in any order — swapping a rabbi in at fifteen buys one year, not four.
    At adulthood, Learning 8+ earns the whole curriculum as a variable the curriculum trigger
    accepts (not two fake library entries, per the spec); Learning 6-7 earns one study FIELD and
    nothing more; below 6, nothing, but the years record survives as biography.
    `kehillah_semicha.0002` is a hidden sorter five days after the sixteenth birthday — five
    because vanilla applies the education trait at birthday+2 and that trait is often what carries
    a student across Learning 8 — and `.0003` is the endorsement the player sees. Withheld only
    for mentor opinion at or below -50, or cynical AND arbitrary together. Probes: `.5` read-only,
    `.6` grant a completed apprenticeship, `.7` run the sorter without waiting for a birthday.
  - **Slice 5 (the older routes) — built 2026-10-10, NOT live-tested.** The Bet Din semicha offer,
    the Chief Rabbi office and `kehillah_hire_rabbi_effect` all now read
    `is_rabbinic_authority_jewish_trigger`. The Bet Din path had no faith check at all
    (`government_has_flag` says a character leads a Kehillah, not what it believes) and the office
    checked only same-faith-as-employer, which a Karaite leader's Karaite appointee passes. The
    Chief Rabbi grant itself is now behind the check too, not just the appointment. Nothing is
    removed from anyone. The slice-3 run's probe reporting `FAITH PASS` at Worms is what makes
    this safe — without it this was a plausible way to make the office unfillable at the only
    playable start.
  - **Slice 4's courtier branch was still broken, and fixed 2026-10-10 (Shabbat heartbeat 4).**
    Heartbeat 3 added the courtier branch to `kehillah_semicha_institution_available_trigger`
    and its live verdict — recovered from the lost run's `debug.log` — was
    `H4PUPIL: INSTITUTION FAIL`. The cause is one clause, and not the one anyone was looking at:
    **`government_has_flag` is TRUE for a COURTIER of a Kehillah ruler**, not only the ruler.
    Measured directly on the H4 pupil Huna Landsberg (65937), a titleless child ward at Worms:
    "pupil IS a Kehillah government holder". That single fact closed all three branches at once
    — branch 1 matched the flag then demanded `exists = domicile`, which a courtier has not got,
    while the `NOT = { government_has_flag ... }` guard shut branches 2 and 3. The community data
    was never at fault: Worms MATCHES his location and HAS a Beit Midrash tier 1+. Fixed by
    dropping that guard from branch 3; a Kehillah leader still cannot reach it (`is_ruler = no`
    is false for them), so leaders are still judged on their own quarter alone. Purely additive,
    and the mirrored resolver needed no change. Full write-up, the rule it implies, and an audit
    of every other `government_has_flag` call site in the mod (all already safe, so nothing else
    changed) are in **[implementation doc section 14](docs/implementation/v1-kehillah-implementation.md)**.
    **VERIFIED LIVE 2026-10-10**
    ([log](docs/testing/2026-10-10-courtier-institution-live-test-log.md)): the same probe that
    reported `INSTITUTION FAIL` before the fix now reports
    `H4PUPIL: INSTITUTION PASS -- the courtier branch added 2026-10-10 is working`, with the
    years record surviving the sorter as biography. Note this run does **not** prove the
    curriculum/foundation credit bands — that pupil's Learning was below the foundation band, so
    both credits were correctly absent.
  - **The credit bands, and a double-credit bug: fixed and VERIFIED LIVE 2026-10-10**
    (same log, "Follow-up run, same day"). **Correction:** an earlier note here credited
    heartbeat 3's recovered run with passing the bands, because its pupil held *both* credits.
    That was not a pass — the bands are exclusive, so holding both was the **symptom** of a
    defect. `kehillah_award_apprenticeship_credit_effect` tangled the band test with its
    don't-re-award test, so an already-credited pupil fell through to the lesser award and a
    Learning-8 student collected the consolation prize too. That matters because the readiness
    trigger's other OR arm counts `kehillah_apprentice_fields`, so one apprenticeship could be
    counted twice. **Ordinary play was never exposed** — the only caller, `kehillah_semicha.0002`,
    is scheduled from `on_16th_birthday` and fires once per character; the debug sorter `.7` is
    what reached it. Now idempotent, and live-verified across three sorter runs: exactly one
    credit after the first, unchanged after the second and third.
  - **The FOUNDATION band: CLOSED, VERIFIED LIVE 2026-10-10 (Shabbat heartbeat 5)**
    ([log](docs/testing/2026-10-10-credit-bands-live-test-log.md)). All three bands pass, on three
    distinct real courtiers at Worms: FULL (Naftali_Hertz Epstein, 65975), **FOUNDATION (Uriel
    Lowborn, 52527 — the first live observation of this band)**, BELOW (Hadassah Lowborn,
    65973). No double-credit in either run, no new `kehillah` errors.
    - **Two probes, and the first one's failure is the useful part.** `kehillah_semicha_debug.10`
      *sets* the subject's Learning per band. It confirmed FULL and then correctly **withheld**
      a verdict on the other two rather than reporting the band it aimed at. Measured reason:
      the Worms leader reads **Learning 17 with his base skill floored to 0**. 1.20 has no
      `set_learning_skill`, only the additive `add_learning_skill`, which moves the
      BASE while the `learning` trigger reads the TOTAL including modifiers — so the
      foundation band is unreachable in either direction on a scholarly character, i.e. on
      exactly the person one would naturally test on.
    - `kehillah_semicha_debug.11` inverts it: **select a courtier already in each band**
      instead of moving anyone into one. No modifier arithmetic, and it exercises the gate
      against a Learning value the game actually produces. `.10` is kept for
      modifier-free subjects, with a header pointing at `.11`.
    - Transferable: **prefer selecting a subject who already satisfies a condition over
      manufacturing one who does.** A probe that sets a skill and assumes the band is the same
      mistake as a probe that assumes a building got built.
  - **Slice 5 — VERIFIED LIVE 2026-10-10 (same log).** The faith gates did not make the Chief
    Rabbi office unfillable at the only playable start: the appointment panel at Worms offers
    7 of 7 characters as candidates.
  - **V21 section 7 gaps — two of three CLOSED 2026-10-10 (Shabbat heartbeat 4)**
    ([log](docs/testing/2026-10-10-section7-institution-gaps-live-test-log.md)). Two new probes
    for this: `kehillah_semicha_debug.8` (read-only branch coverage, one subject per branch) and
    `.9` (destroy the study hall; **often a one-way door** — it now says so before removing
    anything).
    - **Landed-ruler branch: CLOSED, both directions.** Positive verdict `BRANCH 2b PASS` with
      subject Al-Qa'im Abbasid (31533), seated in Baghdad — the province `d_kehillah_baghdad`
      occupies, found by scanning rather than hardcoding. Correct negative at Worms, where the
      host county's holder rules from another seat, so `capital_province` doesn't match. Note
      this is a *mechanics* result: the institution trigger has no faith gate by design, so a
      caliph passing it is not a claim he could be ordained — the candidate trigger refuses him.
    - **Losing the Beit Midrash: CLOSED.** Reproduced twice. Every branch flips to FAIL when the
      building goes, and the student's records survive — section 3.4's rule that only the
      *ceremony* needs an institution.
    - **Landless-adventurer branch: STILL OPEN, honest null.** No character with
      `landless_adventurer_government` stands in any community's province in 1066. Needs a save
      where one actually does; manufacturing one would test the probe's own character rather
      than the game.
    - **A real bug found along the way, in a different probe.** `.4` ("rebuild the study hall")
      reported success while `add_domicile_building` was being refused by `can_construct` — the
      stock Worms start sits under an unresolved Christian host charter, so new communal
      buildings are blocked, which is correct V16 behaviour wrongly reported. `.4` now asserts
      the building exists afterwards. **Second time this shape has bitten** (see the shim
      guide's "What ck3-tiger does NOT catch"); an audit of every `add_domicile_building` call
      site found no *gameplay* bug — `kehillah_worms_developed_start_effect` was already
      hardened on 2026-09-26.
  - **Next for H4:** the landless-adventurer branch above, and a slice-4 run on a pupil whose
    Learning sits in each band, to finish what the slice-4 pass left open (see the
    curriculum/foundation qualification above). (The "defer across a save/load" gap is already
    closed by source: `.0001` option b has no effects, so there is nothing to lose.)

### Kehillah council (V26) — added 2026-10-09

Built 2026-10-01/02 on `kehillah-council` but never entered here; see
[V26](docs/spec/v26-kehillah-council-and-baalei-batim.md). The council is on for Kehillot,
using vanilla's five seats renamed (Shtadlan, Gabbai, Rosh ha-Shmirah, Ne'eman, Dayyan), with
the Gabbai and Shtadlan court positions retired. Wave 1 task effects are scripted (revenue,
construction, bet din cooldown, host petition, Night Watch, spouse clones).

- **Wave 1: VERIFIED LIVE 2026-10-09** ([log](docs/testing/2026-10-09-council-wave1-live-test-log.md)).
  Seat names, Kehillah default tasks at game start, the quarterly fix-up, no leakage onto other
  rulers' councils, and the "Rebbetzin" spouse card all pass. Two bugs were found and fixed:
  `on_get_position` gated on an unset scope, and the spouse card read "Duchess". Probe:
  `events/kehillah_council_debug_events.txt`. Not yet measured: the wave 1 effect magnitudes.
- **Ba'alei batim slice 1: VERIFIED LIVE 2026-10-09** ([log](docs/testing/2026-10-09-baalei-batim-live-test-log.md); natural yearly moves not yet observed). Daniel asked for
  communities that feel alive and interconnected. Each community now keeps 2–4 registered
  householder families with standing. Families arrive from, and leave for, other real
  communities, nearby ones far likelier. Player events cover arrivals and departures, and a
  "Review the Householders" decision shows the register. See V26's "Slice 1 built" section.
- **Ba'alei batim slice 2: SHIPPED 2026-10-09, de-duplicated and LIVE-TESTED 2026-10-10
  (Shabbat heartbeat 5) — the term is correct and reaches nobody**
  ([log](docs/testing/2026-10-10-household-standing-succession-live-test-log.md)).
  A household-standing term in `kehillah_leadership`'s `candidate_score`, so leading families
  compete for the leadership. See V26's new "Slice 2" section.
  - **Correction, 2026-10-10.** The line above this entry used to read "Next: slice 2", and
    v26's spec said standing "does not yet feed succession". Both were already false: the term
    went in on 2026-10-09 in commit 84242d9, alongside H1's succession work, and nobody
    recorded it. The stale claim then caused a bug. Heartbeat 4 was cut off mid-task having
    read it, concluded the term was missing, and **added a second one** -- two terms counting
    the same family standing twice. Caught uncommitted at the start of heartbeat 5 and merged
    into one term. The lesson is the repo's own: a stale status line is not cosmetic, it is
    an instruction to the next session.
  - The merge kept the cut-off run's two genuine improvements -- a `has_variable`
    guard on `kehillah_household_of` before the `var:` read (the
    H3 "Failed to fetch variable" shape; most houses in a candidate pool have neither
    variable), and the weight extracted to `kehillah_household_standing_score_weight_value`.
    The weight stays at the shipped **0.5**, not the 0.4 that run proposed: retuning succession
    scoring in the same unattended change as a refactor would leave the live test unable to say
    which edit moved an ordering. Cap stays 30.
  - Net behaviour change is therefore just the bug fix: a family that has **migrated** no longer
    carries its former community's standing into a succession elsewhere.
  - **Live verdict 2026-10-10: GUARD passes 3/3 households, POOL fails 3/3.** The term reads a
    registered family's standing correctly. It then applies to nobody, because the candidate
    list contains no character it can reach. All six candidates for the Worms succession were
    either **Lowborn with no dynasty at all** — so `exists = house`, the term's first
    condition, fails before standing is consulted — or **of the leader's own house**, which V26
    never registers by design. The pool is composed entirely of the two groups the term cannot
    score.
  - **The A/B is NOT OBSERVED, not PASS and not FAIL.** The boosted family was POOL NO, so the
    unchanged heir ordering is what should happen whether the multiply-and-cap works or not;
    recording it as a pass would repeat heartbeat 3's credit-band mistake. It needs a save with
    a POOL YES household. The probe machinery is proven — `.12` saved and boosted, `.13` restored.
  - **Not structurally impossible, just unreached.** `kehillah_household_refresh_effect`
    already counts `kehillah_household_seats` as `is_councillor_of` over
    `every_house_member`, and standing pays 15 per seat — so a householder on the council
    would be both in the pool and high-standing. Nothing in the mod ever puts one there. The
    register and the officer corps are two populations that never meet.
  - **DECIDED 2026-10-12 (Daniel, v30): option 1, seat householders.** AI leaders now fill empty lay
    council seats from registered families, and the register is observed from the court. The text
    below is the original question.
  - **OPEN, needs Daniel (logged in BLOCKERS.md).** Connecting them is a design call, not an
    unattended fix: seat householders preferentially when filling council/court slots; give
    Kehillah officers dynasties so they have houses at all; or accept that only seated families
    compete and say so in the spec. Clean otherwise — no new `kehillah` errors, no
    `Failed to fetch variable`.
- **Later (V26 council build order step 2):** contracts/loans, sefarim, disputes, scholars,
  sister communities, charter petition.

### Rabbi gameplay loop — interactive direction, 2026-09-29

Daniel's current priority is to connect mentor/yeshiva semicha, book mastery, Bet Din
participation, source-based rulings, responsa, authored world works, and the Chief Rabbi
office. The incremental design and proof order are in
[V24](docs/spec/v24-rabbi-gameplay-loop.md); V21 and V23 remain proposals, not shipped
features. This explicitly takes priority over the older autonomous queue for this
interactive pass.

- **Bet Din writing and choice pass, scripted 2026-10-12; live UI check pending.**
  All nine case openings, outgoing questions and incoming letters now use one
  set of facts and the [writing guide](docs/implementation/kehillah-writing-style.md).
  Translated source context appears on citation-choice hovers. A returned
  responsum appears in the hearing, where the host may cite or ignore it,
  instead of stopping at a separate acceptance event. Trait and skill pairs,
  Talmudics experience, and specific mastered works now offer distinct routes
  to stronger arguments. Verdict events state the ruling and its quality.
  The detailed [implementation note](docs/implementation/kehillah-bet-din-writing-pass.md)
  records the score changes, remaining limits and source references. The
  active CK3 session was left untouched; the letter round-trip and UI text
  still need a live check.

- **Source-aware ransom ruling and named responsum: PLAYER-FACING EXCHANGE VERIFIED LIVE
  2026-10-10 (Shabbat heartbeat 5); the letter round-trip still unproven**
  ([log](docs/testing/2026-10-10-ransom-ruling-live-test-log.md)).
  *(Header corrected 2026-10-10: it read "FULL LIVE EXCHANGE PENDING 2026-09-29".)*
  - **Verified live:** reached through its real entry point (`kehillah_din_sources.71`),
    the case opens as "A Captive's Ransom" in clean English and offers the named-outside-Rabbi
    option ("Ask Rav Isaac for a responsum") with no missing loc keys. Dispatching it produced
    zero new script errors, and the docket ran on through judge 2, judge 3 and the closing
    ruling. The correspondent was confirmed by tooltip to be a different character (Rav Isaac
    the Bearded of Mainz, 9000101) — the first-name match with the player is coincidence, not a
    self-consult bug.
  - **Still unproven:** the 25-day letter round-trip (`.72` → `.73` → `.76`),
    which fires on the AI correspondent and did not complete inside the observation window.
    Reported as NOT OBSERVED rather than inferred from the dispatch succeeding.
  - **Probes for it, built 2026-10-10 (Shabbat heartbeat 6), NOT yet run live:**
    `kehillah_rabbi_loop_debug.9` (read-only: is a letter out, and who holds it),
    `.10` (deliver `.72` now, skipping its 3-day post), `.11` (fire `.73` now,
    skipping the second 3 days). `.11` refuses until the AI has actually answered, tested by
    the reply quality the AI's own option writes, so a PASS cannot come from poking a hidden
    event. The chain itself now logs `.72`'s arrival and chosen option, `.73` reached vs.
    discarded, and `.76` shown. Source note: the leg needs about **6** unpaused days, not
    25 — the 25 is the lifetime of the correspondent's reservation variables, and `.74`'s
    timeout sits at day 12.
  - **One real bug, found and fixed: all nine cases read**
    `involved_activity.var:kehillah_din_advice_case` **unguarded.** Written in exactly one
    place (the delayed-reply events), so it is unset whenever a case first opens — three engine
    errors per opening. One defect authored once and copied eight times; now paired with
    `exists` across 18 sites. **Log noise, not a behaviour bug** — the same verdict H3
    reached for this identical shape. See the header comment in
    `events/kehillah_bet_din_events.txt` before adding a tenth case.
  - **OPEN, needs Daniel (BLOCKERS 2026-10-10): there are two implementations of this consult,
    one of them dead code.** The `kehillah_bet_din_case7_*` / `kehillah_case7_*`
    family has real loc, tooltips and richer precedent archiving, but
    `kehillah_bet_din_case7_pick_correspondents_effect` has **zero call sites** (verified:
    it appears exactly once in the repo, its own definition), and the engine's static analysis
    reports its variables as used-but-never-set. The wired-up mechanism is the generic per-case
    `kehillah_din_sources.71`–`.76` chain. Wire the richer one in or delete it;
    leaving it is what misled probe `kehillah_rabbi_loop_debug.8`, which tests the dead
    path and therefore can never pass.
  - **What the feature is**, kept verbatim from the entry this header replaced:
    `kehillah_mastered_works` records
    successful study separately from encountered works. Mishnah and Bavli Nashim
    mastery unlock different arguments for the acting judges in the captive-ransom
    case. If all three judges lack both works, the host can choose a named outside
    Rabbi who mastered one; a delayed question and answer return to the current
    holder of the asking community, who may adopt the argument before the docket
    continues. The old generic annual responsa pulse is retired. The delayed
    title-routing primitive passed a live [scope spike](docs/testing/2026-09-29-responsa-letter-scope-spike.md),
    and the player-facing exchange is now proven too (see the verdict at the top of this
    entry). The player-recipient leg -- the reply arriving back -- is the part still
    unproven. *(That sentence read "the whole player-facing exchange and player-recipient
    path still need live proof" until 2026-10-10.)* This is the first V24/V23 case slice, not source integration for
    all cases or a full precedent archive; see the dated [V24 addendum](docs/spec/v24-rabbi-gameplay-loop.md).

- **Bet Din participant reward slice: LIVE-PROBED 2026-09-29; AI-hosted player guest still open.** Good/great rulings
  give the three actual ordained judges 1/3 Talmudics XP; a positive docket gives
  non-host attendees small piety, prestige, Learning XP, and a relationship gain.
  **AI-host status correction, 2026-10-16:** no AI Kehillah has hosted one in the
  20-year soak or the forced Jan-Dec 1087 retest. Eligibility, AI Watch priority,
  venue weight, a +10000 override with forced attempt, and the landless venue
  filter have all been checked or tried; the attempted activity never reaches
  creation. The venue filter remains as a correct landless venue definition,
  while AI hosting remains open. See the [soak report](docs/testing/2026-10-16-20-year-soak-report.md).
  Book mastery remains the main Rabbi XP source. A dedicated console probe is in
  `events/kehillah_rabbi_loop_debug_events.txt`. Do not mark the whole
  participant experience done until an AI-hosted player guest is checked. The first
  live pass (2026-09-29) confirmed a real case's +1 XP for all three judges,
  then exposed an older closing-event bug: both score triggers still read
  retired global variables even though the docket score lives on the activity.
  This made all tiered session rewards silently fall through. The triggers
  now read `involved_activity.var`. The fresh-boot retest reported a positive
  score and displayed the **adequate** close: host Greatness +10, Stability
  +5, Piety +50, and named non-host attendees each shown gaining +10
  Prestige, +10 Piety, +15 Learning XP and opinion. The close executed
  without a new reward error. This verifies the UI/effect path, though a
  numeric before/after on an attendee and an AI-hosted player guest remain
  untested. [Live log](docs/testing/2026-09-29-rabbi-loop-bet-din-live-test-log.md).
- **Bet Din case-writing pass, 2026-09-29:** The docket now includes a communal
  captive-ransom petition drawn from Mishnah Gittin 4:6 and Geniza evidence. The
  presiding judge chooses a funding policy; the second judge can persuade the
  bench to change it; ruling quality and funding cost resolve separately. The
  silversmith case's successful second-judge argument now changes the verdict.
  The dowry compromise now tests Diplomacy and its text no longer sides with
  the family demanding the original sum. The ransom host-to-resolution chain
  is [live-probed](docs/testing/2026-09-29-bet-din-ransom-live-test-log.md);
  player-controlled dissent and the revised silversmith response remain open.
- **V21 ordination through rabbi mentorship and local semicha: BUILT 2026-10-09/10**, all five
  slices, slice 3 verified live -- see the Shabbat queue's H4 above, which is the current account.
  This line previously read "Next: V21 ordination..."; it is kept so the ordering below still
  makes sense. **Next from here:** a
  book-mastery option in a Bet Din case and V23 letter from that case. Prove one dynamically
  authored circulating sefer end to end before adding the historical catalog.

### v0.1 milestone — Sukkot autonomous queue (added 2026-09-25; works ABOVE the numbered items below)

Daniel's v0.1 direction is in [docs/spec/v22-v0.1-milestone.md](docs/spec/v22-v0.1-milestone.md):
a fun, legible 50-year Ashkenaz 1066 loop, Jewish gameplay first. The Sukkot heartbeat runs
(2026-09-25 to 2026-09-28, branch `autonomous/sukkot-2026`, see CLAUDE.md "Overnight automation")
work this list top-down before the older numbered items.

**Daniel's instruction for this window (2026-09-25): iterate and LIVE-TEST, don't write detailed
specs he can't review.** The heartbeat has the PC to itself — it may launch, drive, and close CK3
freely. A BUILD item is done only once it has actually been played or probed live. When a build
needs a design choice, make the smallest reasonable one, write it down in a few lines (commit
message or a short dated note in the relevant existing doc), and keep building — no new multi-page
spec docs. Markings: **BUILD** = implement + live-test; **DANIEL-REVIEW** = do not build; at most
short research bullets for when Daniel is back.

- **S0. BUILD/TEST — Clear the pending live regressions in one batched session.** Bet Din semicha
  guard + restitution cap (item 7), V18 Norman Conquest founding (dynasty tie), V20 starting
  pillars, V16 §8 open tests. Turns "source-fixed" into "verified". One pass, record results, move
  on — don't let it eat the window.
  **PARTIAL, 2026-09-26.** Two runs, logged in
  [docs/testing/2026-09-25-s0-regression-live-test-log.md](docs/testing/2026-09-25-s0-regression-live-test-log.md)
  and [docs/testing/2026-09-26-s0-s2-live-test-log.md](docs/testing/2026-09-26-s0-s2-live-test-log.md).
  - **V18 Norman Conquest founding + dynasty tie: VERIFIED PASS** (2026-09-25). Closes the item
    BLOCKERS.md left open after three failed mechanisms.
  - **Bet Din semicha guard: VERIFIED PASS** (2026-09-26), with a genuinely non-vacuous positive
    control this time.
  - **Bet Din restitution clamp: ROOT CAUSE FOUND, FIXED, AND VERIFIED LIVE, 2026-09-26
    (heartbeat 4)** —
    [log](docs/testing/2026-09-26-s0-restitution-and-s2-tooltip-log.md) §1. `kehillah_debug.108`
    returns CLAMP PASS / DEBIT PASS / CREDIT PASS against a low-gold accused (7 against an award
    capped at `medium_gold_value`), with zero `add_gold`/`pay_short_term_gold`/`Negative value`
    lines anywhere in a fresh boot. *Caveat:* this exercises the transfer primitive under the real
    clamp, not `kehillah_bet_din.0051`'s option-to-direction wiring — a genuine Silversmiths'
    Quarrel on a real docket is still the only end-to-end confirmation.
    `add_gold` is **additive only** and cannot go negative by any
    shape. The engine says so itself, in its own generated
    `logs/effects.log`: `add_gold` — "adds gold to a character"; `remove_short_term_gold` —
    "removes gold from a character"; `pay_short_term_gold` — "the scope character pays gold to the
    target character, `{ target = X gold = Y }`". A literal negative is rejected at **script-load
    validation**, a computed one at runtime, which is exactly why the 2026-09-25 clamp fix moved
    the error's timing without removing it and why `.103` found the probe characters holding gold
    exactly as script read it. **There was never an affordability check to outwit.** Vanilla uses
    `add_gold = -` zero times in `common/` or `events/`, against 849 `remove_short_term_gold` and
    925 `pay_short_term_gold`; this mod already used the correct primitives in six other places,
    and this one effect was the lone hand-rolled exception — which is why it was the lone site
    that errored. Both restitution branches now make one `pay_short_term_gold` call, zero-sum by
    construction rather than by two calls agreeing. The min/max cap stays, for a design reason
    now (a Bet Din should not order restitution beyond a litigant's means) rather than an engine
    one. **How it was finally caught:** the previous heartbeat's own `.108` probe used three
    *literal* negative `add_gold` calls and was rejected at script load before it ever ran,
    logging the answer instead of the measurement it was written to take (commit `fe8ba31`).
    **Tooling note: `ck3-tiger` does NOT flag `add_gold = -5`** — only the live game's load
    validation does, so clean tiger output was never evidence here.
  - **V20 starting pillars and the V16 §8 open tests: NOT YET COVERED.** Neither run reached
    them. Still open for a later heartbeat.
    **Do the V20 check AFTER the 2026-09-26 Worms-start fix, or it verifies the wrong number.**
    `kehillah_worms_developed_start_effect` had been a no-op above synagogue tier 1 —
    `add_domicile_building` *does* consult `can_construct`, contrary to that effect's own header,
    so tier 2 failed its Greatness gate (150) and tiers 3–5 cascaded off the missing tier 2. V20's
    day-three snapshot was therefore keeping its "opening pillars equal the full baseline" promise
    faithfully against a baseline missing four synagogue tiers. Fixed by lifting Greatness for the
    duration of the grant and restoring it immediately (commit `4267d36`).
    **VERIFIED LIVE 2026-09-26 (heartbeat 5) — PASS.**
    [log](docs/testing/2026-09-26-heartbeat5-live-test-log.md) §1.
    `kehillah_debug.111` on a fresh Worms start reports `SYNAGOGUE 5` plus all eight other
    buildings `PRESENT`, with **zero** `add_domicile_building` lines in `error.log` against a
    pre-fix symptom of four. Note recorded there: zero errors alone was *not* accepted as the
    pass, since a boot into any other community shows zero too — the positive `SYNAGOGUE 5`
    reading is what closes it.
    **This check also found a separate, previously unknown bug, now fixed (commit `9236d57`):**
    every new 1066 game opened with a spurious "The Community Frays" collapse warning on day one,
    because the first quarterly pulse (1066.9.16) consumed the pillars two days before day three
    wrote them (1066.9.18) — reading all three as 0.00, seeding all three bands as Crisis, and
    burning the five-year warning cooldown so a *genuine* early crisis would have gone unwarned.
    Fixed by guarding the consumers on a new `kehillah_pillars_are_live_trigger` and having the
    day-three snapshot seed the bands itself. See the log's §1a for why initializing earlier was
    rejected (this codebase already rejected it, for a reason that still holds) and why the
    obvious `kehillah_start_pillars_initialized_from_baseline` marker is a trap.
    **FIX VERIFIED 2026-09-27 (heartbeat 8) — PASS**,
    [log](docs/testing/2026-09-27-heartbeat8-live-test-log.md) §1. It needed no boot: heartbeat 7's
    usage limit left its CK3 process running overnight, and its logs held a complete fresh
    1066-Worms boot no session had read. Zero `below the Stability floor`, zero `firing the
    Stability warning`, zero `Community Frays` in a boot that demonstrably passed day three.
    Zero was *not* accepted on its own (the watch logs nothing on the healthy path, so silence
    would also mean "never ran") — the positive control is `seeded a band for a community that had
    none recorded` appearing 45 times, all at day three, i.e. 15 communities × 3 pillars each
    reporting no band on record, which the day-one pulse would have already written. Still
    unverified: that the watch fires when Stability is *genuinely* low — that is S1 criterion 2.
    Same logs also turned up a separate game-start `set_employer` error on the **Troyes** start
    (Rashi's, so S4's and S7's showcase character), now fixed — log §2.
    **"The V16 §8 open tests" is under-specified as an S0 bullet — corrected 2026-09-26.** Read
    against the spec, V16 §8 is **nine** separate live tests, not a mop-up: several need multiple
    boots (host succession *and* a county changing realm by conquest; a fresh Christian *and*
    Muslim start), one needs a save-migration fixture (§8.3), one is a performance measurement
    rather than a pass/fail (§8.6's registry scan at scale), and **§8.8 (armed-watch retinue)
    overlaps S12, which is DANIEL-REVIEW** — it should not be built or promised in player-facing
    text before he weighs in, so testing it now would be testing ahead of a design decision.
    Treat this bullet as a pointer to that list rather than as one task, and pick individual
    numbered items off it; don't let it sit at the top of S0 looking like a single afternoon.
- **S1. BUILD — Leave the Kehillah (ruler → landless adventurer), and Stability dissolution
  (V2 §4.4, Wave 4), sharing ONE teardown effect.** A voluntary decision ("Step Down and Take to
  the Road" or similar) and the Stability-floor collapse both call the same effect: narrate,
  `change_government` to `landless_adventurer_government`, followers travel on, legacy fragment of
  Greatness. Voluntary departure hands the community to an AI successor; dissolution ends the
  title. Mirror the founding path's verified teardown order in reverse. High crash-risk area: read
  the implementation doc §6/§8 and the founding-path notes first. Add a warning event one band
  above the floor so collapse is never a surprise. **Done when**, live: (1) the player steps down,
  plays on as an adventurer, and the community continues under an AI leader; (2) Stability forced
  to 0 via debug event shows the warning, then collapse, and the player plays on as an adventurer;
  (3) that adventurer can re-found a community; error.log clean of new errors throughout.
  **CRITERION 1 LIVE-TESTED 2026-09-27 (heartbeat 8) — HALF PASS, and it found the real bug.**
  [log](docs/testing/2026-09-27-heartbeat8-live-test-log.md) §6.
  - **The departing leader's half: PASS.** The decision is available with a named heir, taking it
    visibly works (adventurer decision list, changed portrait, vacated-office and realm-teardown
    notices), and `kehillah_debug.100` returns **six for six**: landless_adventurer government, a
    domicile (camp) exists, holds a primary title, that title is no longer a Kehillah title, the
    adventurer succession law is active, the banked-Greatness scratch variable was cleaned up.
  - **The community left behind: FAIL.** `kehillah_debug.113` reports the handover happened
    (`HOLDER IS NOT ROOT`) and then: `FAIL the new holder does NOT have the Kehillah government`
    and `FAIL the new holder has NO domicile -- the 15-25 day Game Over fuse, now pointed at an
    AI`. Criterion 1 requires "**and the community continues under an AI leader**". It does not.
  - **Same bug as S3(a), now confirmed — and it is SILENT.** `error.log` did not grow across that
    group at all and holds no error text for any of it. Only the mod's own probes catch it; "error.log
    is clean" has never been evidence that a succession worked.
  - **Criteria 2 (collapse) and 3 (re-founding) remain untested.**
  - **Criterion 1 is now a FULL LIVE PASS, 2026-09-27.** The successor-
    domicile cause was fixed with the smallest engine-proven mechanism:
    `kehillah_succession.0010` creates a temporary dynamic title with
    `government = kehillah_government`, which atomically makes the Jewish
    Quarter, restores the pre-existing community title as primary, then
    destroys the scaffold. This preserves the title-owned pillars and the
    recorded quarter state rather than copying either. A real Worms
    **Step Down and Take to the Road** handoff passed the successor
    government/domicile/primary-title breadcrumbs, all six departing-
    adventurer invariants, and the watched community's continued holder,
    domicile, and pillar state after further time; no new succession or
    `change_government` errors. [Log](docs/testing/2026-09-27-successor-quarter-live-test-log.md).
    The ordinary death/appointment route uses this same deferred event
    but remains explicitly untested after a separate clean CK3 process
    became unresponsive before it could accept New Game input.
- **S2. BUILD — Pillar transparency and impact.** State as of 2026-09-25 (read from code): bands
  only gate building tiers (Greatness, one Prosperity tier), courtier quality (Greatness), one
  Crisis-Stability random event, and map-view colour. There is no band-change notice, no ongoing
  effect from simply *being* in a band, and no "what the next band gives" text. Build exactly:
  1. **Per-band leader modifiers, 3 pillars × 5 bands**, applied/replaced on the quarterly tick
     (remove the old band's modifier when the band changes; Healthy = small or none). Starting
     proposal, verify every modifier key exists in vanilla 1.19 before using it: Prosperity →
     `monthly_income_mult` (about −20% / −10% / 0 / +10% / +20%); Stability → influence gain and
     stress gain (Crisis hurts, Flourishing helps); Greatness → `monthly_prestige_gain_mult` plus a
     Learning bonus at Flourishing/Legendary. Numbers in script_values so they're tunable.
  2. **Band-change notice.** Store each pillar's previous band on the title; when it changes on the
     tick, send the player a `send_interface_message` saying the pillar, old → new band, and what
     modifier or unlock was gained or lost. No notice if the band didn't change.
  3. **Next-band text.** In the existing pillar tooltip/breakdown (map view row and community-list
     tooltip), add one line per pillar: current band, points to the next band up, and what that
     band adds.
  4. **Debug harness:** a debug event that sets a chosen pillar to each band in turn, so every
     modifier and notice can be triggered on demand.
  **Done when**, live: for each pillar, pushing it up one band and down one band shows the notice,
  swaps the modifier on the leader's character sheet, and the tooltip names the next band —
  downscaled screenshots in the test log. ck3-tiger clean. No change to how pillars are
  *calculated* in this item; that's S10's job if the soak test finds problems.
  **DONE, 2026-09-26 (all four parts live-verified). Parts 1, 2 and 4 verified 2026-09-26**
  ([log](docs/testing/2026-09-26-s0-s2-live-test-log.md) §3): pushing all three pillars up a band
  and then down a band produced the notice both ways (a real "The Community's Prosperity Has
  Shifted" banner), and `kehillah_debug.102` confirms exactly one band modifier per pillar
  afterwards with no stale leftovers from the previous band. **Part 3 (next-band text) is built and
  wired but NOT yet confirmed rendering** — it lives in `KehillahBdNextBand{Prosperity,Stability,
  Greatness}`, called from `KEHILLAH_BD_*_TOOLTIP` (`localization/english/
  kehillah_breakdown_l_english.yml:95-97`), which `gui/kehillah_community_map_view.gui:578,817`
  uses for the map-view widget's pillar rows. A 2026-09-26 tester reported it as dead code after
  hovering the *community-list interaction's* tooltip instead — the wrong surface, corrected in
  that log's §4.
  **S2 IS NOW COMPLETE — part 3 VERIFIED LIVE 2026-09-26 (heartbeat 5)**,
  [log](docs/testing/2026-09-26-heartbeat5-live-test-log.md) §2. All three pillar tooltips name
  the correct next band with the exact right number, measured against `kehillah_debug.111`'s
  independently-computed figures rather than against a tester's expectation: Prosperity 255
  (Strained) → "145 more to Healthy", Stability 369 (Strained) → "31 more to Healthy", Greatness
  459 (Healthy) → "241 more to Flourishing". `error.log` growth **+0 lines** on each of the three
  hovers, against the old ~2,000 lines/second, and process working set *fell* across the hovers.
  Worth keeping in mind for future checks of this kind: as originally briefed this test would have
  been taken at game start, where all three pillars are 0 and the tooltip renders its
  `always = yes` fallback — the very branch that produced the original wrong text. It was
  redirected mid-run to advance past day three first, and that redirection is what also turned up
  the day-one collapse-warning bug recorded under S0.
  **Part 3 history, 2026-09-26 (heartbeat 4)** —
  [log](docs/testing/2026-09-26-s0-restitution-and-s2-tooltip-log.md) §4. The correct surface was
  finally hovered. The line **does render** (so it was never dead code), but it rendered *wrong*
  — "0 more to Strained" on a community not in Crisis — and spammed `error.log` at roughly
  **2,000 lines/second** while hovered: 288 lines → 378,909 across three hovers, and ~2.2GB →
  ~5.1GB of process memory. One cause for both: the code was written for character scope and
  hopped back to the title with `primary_title = { var:... }`, but the pillar variables live on
  the **title** (implementation doc §10). Where that hop missed, the guarded custom-loc branches
  fell through to their `always = yes` fallback (the Strained line) while the *unguarded* script
  value threw every frame and clamped to 0. Now fixed by matching the sibling that always worked
  in this same widget, `[Title.Custom('KehillahProsperityScore')]`: `type = landed_title`, direct
  reads, `has_variable` on every branch, and all 15 loc call sites moved off `Title.GetHolder.*`.
  **Source-fixed and ck3-tiger clean; the re-hover to confirm the correct band name AND a quiet
  `error.log` is still outstanding.** Part 3 stays PARTIAL until then.
- **S3. BUILD — Succession hardening.** (a) Root-cause the recurring non-fatal `change_government`
  "illegal government" error on appointment succession (implementation doc, 2026-09-23 addition).
  (b) Live-verify that an officer with a better score beats a family heir (the long-open
  holder_court_position re-test, see "CORRECTED 2026-09-07" below). (c) Succession of a *founded*
  community (never tested). (d) Give the player a real role in choosing a successor — smallest
  workable version of V3 / iteration notes §4: an interaction "Endorse as Successor" on one
  eligible courtier (one at a time, adds a fixed score in `kehillah_leadership.txt`, shown in the
  succession candidate tooltip). **Done when**: (a) is fixed or its cause documented with
  evidence; (b), (c), (d) each observed in a live console-kill succession.
  **BUILT 2026-09-26, live test in flight.** (a) is deliberately *instrumented* rather than
  blind-fixed for the third time: `kehillah_trace_title_gain_effect`
  (`common/scripted_effects/kehillah_succession_effects.txt`, armed by `kehillah_debug.104`) logs
  whether the just-gained title is yet visible to `any_held_title` at the instant `on_title_gain`
  fires — which is `can_get_government`'s entire predicate — and
  `kehillah_on_title_gain` now guards the inline `change_government` with that same predicate,
  deferring to `kehillah_succession.0010` a day later when it would fail. That event logs its own
  verdict, so one live succession settles the cause and validates or refutes the guard at once.
  (d) is built: `kehillah_endorse_successor_interaction` writes
  `kehillah_var_endorsed_successor` on the community title and
  `kehillah_leadership.txt` adds `kehillah_endorsement_score_value` (30) to that one candidate.
  (b) and (c) still need the live observation.
  **(a) IS ANSWERED, 2026-09-27 (heartbeat 8) — cause CONFIRMED, deferral REFUTED, deliberately
  NOT patched.** [log](docs/testing/2026-09-27-heartbeat8-live-test-log.md) §6. A real voluntary
  step-down ran the exact path. Three findings, in order:
  1. **The `exists = domicile` gate works.** Zero `illegal government` and zero
     `change_government` errors anywhere in the boot, on the path that produced that error on
     2026-09-06, 09-20, 09-23 and in heartbeat 6. Four sessions of a recurring error, silenced.
  2. **The cause is the domicile, stated by the instrumentation rather than inferred.**
     `kehillah_succession.0010` one day later: *"the new leader STILL has NO domicile one day after
     title gain -- deferring longer would not help either"* and *"STILL cannot get the kehillah
     government a day later -- root holds a landless title but has NO domicile, so the engine has
     nowhere to put a kehillah_quarter."* `kehillah_government.txt:117` declares
     `domicile_type = kehillah_quarter`; nothing on the handover path gives the successor one.
     It was never a timing problem — which is why two rewrites aimed at timing both missed.
  3. **So the one-day deferral is refuted as a fix.** Waiting cannot help; nothing is in flight to
     wait for. Silencing the error also did not fix the succession — see S1 above for what the
     community is actually left in.
  **What makes it decidable now:** the *departing* leader's transition demonstrably DOES get a
  domicile, by dedicated code — `kehillah_departure_finish_effect` logs "leader has no domicile
  before the camp is created (expected)" → "created the wayfarer title" → "domicile exists after
  create". So creating a domicile at transition time is possible in script; the arriving heir just
  has no equivalent. **The remaining question is a design one — where does the successor's Jewish
  Quarter come from — and it is the top item for the next heartbeat.** Do not attempt a fifth blind
  fix: read implementation doc §6/§8 and the founding path first, and live-test any change on a
  real step-down.
  **FIXED AND LIVE-VERIFIED ON THE VOLUNTARY HANDOFF, 2026-09-27.** The
  missing domicile is now provisioned in `kehillah_succession.0010` by a
  temporary `create_adventurer_title` with `government =
  kehillah_government`, then the real community title is restored as
  primary and the temporary title is destroyed. This is the same
  engine primitive already live-proven by the founding path; no new
  timing guess or post-hoc `change_government` call is involved. The
  live handoff retained the community title's pillars and restored its
  recorded buildings. S3(b), (c), and (d) still need their own live
  observations; ordinary death/appointment is also still a worthwhile
  regression once CK3 accepts a new game.
- **S4. BUILD — Chief Rabbi: search like "Find a Physician", or serve yourself.** (Daniel,
  2026-09-25.) Build exactly:
  (1) **"Seek a Chief Rabbi" decision, modelled on vanilla's physician recruitment** (the
  `hire_physician_decision` item in `game/common/decisions/90_minor_decisions.txt`, which opens
  event `health.3001` offering candidates at skill tiers and gold costs, with a cooldown flag —
  copy that shape). Shown when the Chief Rabbi seat is empty and the Beit Midrash unlock exists.
  The event offers ~3 candidates: where possible, **real existing rabbis** (Jewish, rabbi-eligible
  under the existing gender/rabbi gates, not a community leader, preferring other communities'
  courts and landless scholars; Learning-ranked, cost scaled by Learning and by the gap between
  their community's Greatness and yours), padded with generated candidates at low/mid/high tiers
  if too few real ones exist. On choosing: move to your court and appoint to
  `chief_rabbi_kehillah_position`. AI communities with an empty seat use the same decision
  (`ai_chance`).
  (2) **The leader as their own Chief Rabbi.** A ruler can't hold a court position in their own
  court, so model it as an explicit toggle decision, "Serve as the Community's Rabbi": available
  when the leader has the rabbi trait and Learning ≥ a script_value threshold (~14 — **corrected
  2026-09-26: the build chose 12**, `kehillah_serve_as_rabbi_learning_threshold`, and Rashi's
  history was pinned to `learning = 12` to clear it exactly; read 12, not 14), and no rabbi
  is appointed. While active (character flag), every consumer of the Chief Rabbi seat — the pillar
  contribution in `kehillah_breakdown_values.txt`/`kehillah_scripted_effects.txt` and the dispute
  events in `kehillah_dispute_events.txt` — reads "the appointed Chief Rabbi, or the leader if
  serving". Do this through ONE new scripted trigger/value pair used at every site, not per-site
  special cases. Small drawback, so it's a choice (e.g. a stress or influence-gain cost for doing
  two jobs); appointing a rabbi ends the toggle. **Rashi starts the game serving as Troyes's own
  Chief Rabbi** (Daniel, 2026-09-25): `kehillah_setup_troyes_start_effect` turns the toggle on for
  him, and Troyes starts with no separately appointed rabbi. Check his actual in-game Learning and
  set the threshold so he qualifies; if the drawback makes his start feel punishing, soften it for
  him or overall and note it. He is also the Scholar in S7's bookmark, so this is his opening state
  there too.
  (3) One flavour event, "your student has been called to X": a rabbi you trained is recruited by
  another community's search; small Greatness gain for you.
  **Done when**, live: the player recruits a real rabbi from another community through the search
  event; Rashi begins a new 1066 game as Troyes's own Chief Rabbi and the breakdown tooltip shows
  his contribution; an AI community fills an empty seat.
  **ALL THREE PARTS BUILT 2026-09-26. (1) AND (2) VERIFIED LIVE 2026-09-27 (heartbeat 8); (3)
  STILL UNTESTED.** [log](docs/testing/2026-09-27-heartbeat8-live-test-log.md) §4-5.
  - **(1) "Seek a Chief Rabbi" — PASS, end to end.** The decision showed un-greyed, and the event
    "Word Comes Back" offered three candidates at real Learning/cost tiers: Ulla (16 Learning, 84
    gold), **Feivel Yitzhaki, "Son of Rav Shlomo"** (13, 72), Shimshon Horowitz (3, 32). Feivel was
    chosen deliberately as the one identifiable as a **real rabbi from a real other community**
    (Rav Shlomo is Rashi, at Troyes) — a generated-candidate pick would have satisfied the item
    vacuously. Afterwards: `SEAT FILLED`, `ACTING RABBI YES`, and `TOGGLE OFF` — **the appointed
    rabbi displaced the serving leader, which is S4's own "the appointed rabbi always wins" rule
    observed rather than assumed.**
  - **(2) Rashi as Troyes's own Chief Rabbi — PASS**, with no `CONTRADICTION` line. That silence is
    the load-bearing part: all four consumer sites read
    `kehillah_has_acting_chief_rabbi_trigger`, so the trigger disagreeing with the seat and the
    toggle would break every one of them at once.
  - **(3) is now the cheapest remaining S4 item and was reachable in that very run** — Feivel
    leaving Troyes should have fired `kehillah_rabbi_search.0002` at Rashi 3-10 days later. Nobody
    looked; the session had moved on. Pick it up in the next boot.
  - **(3) built 2026-09-26 (heartbeat 4).** `kehillah_install_chief_rabbi_effect` notes the
    rabbi's old liege *before* `add_courtier` moves them (afterwards the link is gone), and if
    that liege was a **different Kehillah**, fires `kehillah_rabbi_search.0002` to them 3–10 days
    later. Hiring a stranger, a landless scholar or some bishop's courtier fires nothing. The
    losing community *gains* Greatness (`kehillah_rabbi_departed_greatness_gain` = 6, against 10
    for hiring) — a community whose scholars are wanted elsewhere has exactly the reputation
    Greatness measures, and its real loss is already priced in without help, since the empty seat
    stops contributing that same tick. The two figures differ on purpose so two AI communities
    can't pump each other's Greatness by passing one rabbi back and forth.
  - **The live-test blocker on (1) is now cleared: `kehillah_debug.110`** grants the Beit Midrash
    (which is what gates the seat, via `has_domicile_parameter = kehillah_unlocks_chief_rabbi`),
    clears the search cooldown, and reports the seat/toggle state — including whether the shared
    `kehillah_has_acting_chief_rabbi_trigger` agrees with the seat's actual state, which is the
    load-bearing check on part (2), since all four consumer sites were rewired onto that one
    trigger.
  - (2) is built through one shared trio, as this item demands:
    `kehillah_has_acting_chief_rabbi_trigger`, `kehillah_acting_chief_rabbi_learning_value` and
    `kehillah_save_acting_chief_rabbi_effect`. All four previous call sites were rewired (the
    pillar value, the breakdown custom-loc row, the dispute-scope effect, both dispute events'
    Chief-Rabbi option gates). Toggle: `kehillah_serve_as_rabbi_decision`, drawback is stress
    (Influence is retired from this government, so an influence cost would cost nothing).
    Rashi now has an explicit `learning = 12` in `history/characters/troyes_1066.txt` so his
    documented starting state is deterministic rather than a stat roll.
  - (1) is built as `kehillah_seek_chief_rabbi_decision` →
    `events/kehillah_rabbi_search_events.txt`, on vanilla's physician-recruitment shape, with the
    candidate pool walked out of `kehillah_registered_communities` (real rabbis in real courts)
    and generated candidates only as a thin-pool fallback. Gated on the Beit Midrash, because
    that is what gates the court position itself.
  - Live-testing (1) needs a community that has actually built the Beit Midrash — a debug probe
    to reach that state is the missing piece for the next heartbeat.
- **S4b. BUILD — Chief Rabbi coherence pass.** (Daniel, 2026-09-27, interactive session — an
  unlisted item added above the remaining numbered ones because it is a correctness complaint
  about shipped S4/S5 content, not new scope.) His report, verbatim in substance: *"you can
  currently serve as chief rabbi and have an assigned chief rabbi"*; the office should only be
  available if you are not already the chief rabbi, and *"if there's already a chief rabbi, maybe
  you can replace him with yourself with the decision"*; *"chief rabbis should be the ones who
  preside over bet din conferences"*; and responsa should be *"gated on rabbi trait (with
  increased likelihood to target a player)"*.

  **BUILT 2026-09-27, `ck3-tiger`-clean, NOT YET LIVE-TESTED.** Four changes:
  - **The office and the seat are mutually exclusive, asymmetrically.** Appointment is refused
    while the leader holds the rabbinate (`chief_rabbi_kehillah_position`'s `valid_position`, plus
    `kehillah_seek_chief_rabbi_decision` greyed out so the search can't run for a prize that
    cannot be seated). The decision, in the other direction, **deposes** a sitting Chief Rabbi
    (`kehillah_replace_appointed_rabbi_effect`) at the cost of the ordinary
    `revoked_court_position_opinion`. The leader's own intent wins over the appointment system,
    never the reverse. The gate needed a new trigger,
    `kehillah_has_taken_up_rabbinate_trigger` — the existing
    `kehillah_serving_as_own_rabbi_trigger` yields to an appointed rabbi by design and so can
    never block one; its own header records why.
  - **The Chief Rabbi presides.** A Bet Din Conference cannot be convened without an acting Chief
    Rabbi by either route, and whoever that is is bound as Av Beit Din
    (`kehillah_bet_din_av_beit_din`, set in `kehillah_bet_din_open_docket_effect` through the
    shared S4(2) resolver — its sixth consumer site). **All 14 host-bench skill checks across the
    six cases now read the Av Beit Din's skill, not the convening leader's**, via
    `scope:kehillah_av_beit_din`. The two co-judge seats are untouched and still answer for
    themselves. Design consequence worth knowing: appointing a brilliant rabbi now genuinely
    decides your dockets, and a leader who would rather be the one judging takes the office
    himself — which is what ties this bullet to the one above.
  - **Responsa need semicha.** `kehillah_responsa_answerer_is_rabbi_trigger`, in lockstep with
    `kehillah_responsa_answerer_learning_value`'s two branches. Learning alone was the whole gate
    before, so a well-read leader with no semicha received she'elot addressed to a posek.
  - **The player is written to more often.** `chance_of_no_event` costs an AI 40% of its rolls
    (~33%/yr against the player's 55%). Done that way because `chance_to_happen` takes a literal
    only; `chance_of_no_event` takes a script value.

  Probes: `kehillah_debug.118` (read-only state, meant to be read alongside `.115`) and
  `kehillah_debug.119` (exercises the replacement path end to end and asserts seat/toggle/opinion).

  **Relation to `docs/spec/v23-responsa-network-and-precedent.md`**, written the same day by a
  parallel heartbeat run: V23 proposes retiring this automatic pulse as the *player-facing*
  responsa loop, keeping it at most as "a passive, infrequent incoming letter ... for an
  established scholar". The semicha gate and the player bias are exactly what that description
  wants, and cost nothing if V23 lands — they harden the prototype in the meantime rather than
  building against it. V23's own dependency note ("the office redesign must settle how a leader
  chooses to act as Rabbi, Shtadlan, or Gabbai") is the part this item moves: the leader's choice
  to act as Rabbi is now exclusive and reversible, which is the precondition V23 names.

  **That wart is fixed** — see S4c below, same day. It read: the office's
  `on_court_position_revoked` strips `kehillah_rabbi_trait`, so a rabbi dismissed by the
  replacement path loses his semicha even if he arrived holding it.

  **Open for a live pass:** whether the preside gate is too tight in practice. It thins the pool
  of communities that can host, and hosting is how a leader without semicha gets it
  (`kehillah_bet_din_grant_rabbi_trait_effect`). AI leaders take the serve-as-rabbi decision at
  `base = 100` and three historical leaders ship with the trait, so the pool should not go empty —
  but that is reasoning, not an observation. Watch it in the S10 soak run.
  **S4b LIVE-VERIFIED 2026-09-28 -- PASS.** [Log](docs/testing/2026-09-28-heartbeat-s4bcd-s5-live-test-log.md) sections 1 and 4. `kehillah_debug.119`
  returns five for five on the replacement path: `SEAT CLEARED PASS`, `TOGGLE EFFECTIVE PASS`,
  `OPINION PASS`, `SEMICHA PERMANENT PASS`, `PRESIDE GATE PASS`. The semicha assertion was **added
  for this run** -- `.119` exercised the replacement path but had never looked at the deposed
  rabbi's trait, and that path is exactly the site whose teardown hooks used to strip it. Mutual
  exclusion (`EXCLUSION PASS`) and the responsa semicha gate also read correctly.
  **The preside-gate question is partly answered, and the answer is worth knowing: the gate is
  visibly CLOSED on an untouched Worms start** (`PRESIDE GATE BLOCKED` -- no appointed rabbi, and
  the leader has not taken the office). That is the rule working rather than a bug, but it means a
  fresh community cannot convene a Bet Din until it settles its rabbinate. Not too tight here (the
  seat is trivially fillable, see S4c), but a *young* community is still the untested case.
- **S4c. BUILD — Semicha is permanent; the Chief Rabbi is not a building unlock.** (Daniel,
  2026-09-27, same session as S4b.) *"Let's not strip rabbi traits on removing a chief rabbi"* and
  *"make it so that the chief rabbi isn't gated by the bet midrash, and a community can always have
  one."*

  **BUILT 2026-09-27, `ck3-tiger`-clean, NOT YET LIVE-TESTED.**
  - **Semicha is permanent.** `chief_rabbi_kehillah_position`'s three teardown hooks
    (`on_court_position_revoked` / `_invalidated` / `_vacated`, each removing
    `kehillah_rabbi_trait`) are gone; the trait is granted on receipt and kept. It was making the
    trait a badge of current employment: S4b's replacement path unmade the other man's ordination,
    and a community whose beit midrash fell down unmade its rabbi. Semicha is not a job title. Side
    benefit: a dismissed Chief Rabbi stays a candidate S4(1)'s search can find in another court,
    which is exactly what that pool is trying to populate.
  - **The Beit Midrash no longer gates the office**, in `valid_position` or on the search
    decision's `is_shown`. A rabbi is the first thing a Jewish community has, not a reward for
    having built a study hall, and with S4b gating the Bet Din on having an acting Chief Rabbi it
    was gating the entire court system on masonry. The `kehillah_unlocks_chief_rabbi` domicile
    parameter is still set by all three tiers but has no consumer — left as the hook for a future
    "has somewhere to STUDY" check, which is a different claim. The Beit Midrash keeps Learn Torah,
    the library tiers and its Greatness contribution: it is a multiplier on scholarship now, not
    the permission slip. **The Treasurer still gates on the Countinghouse, deliberately** — the
    rule is now "gate when the building IS the work", and a treasurer with no chest has no work
    where a rabbi with no study hall still teaches, rules and buries the dead.
    **S4c LIVE-VERIFIED 2026-09-28 -- PASS, both halves.** [Log](docs/testing/2026-09-28-heartbeat-s4bcd-s5-live-test-log.md) section 5. It needed a
    new probe, `kehillah_debug.121`, because **every community in the 1066 setup starts with a Beit
    Midrash -- so nothing in ordinary play reaches the state S4c is about.** The probe tests the
    claim in the hard direction: demolish all three tiers, prove the demolition landed
    (`STRIP PASS`, checked on the unlock parameter -- without that control a pass would equally be
    satisfied by a probe that removed nothing), and only then appoint. `UNGATED PASS`,
    `SEMICHA GRANTED PASS`, `PRESIDE GATE PASS`.
    **The second half is the one the probe cannot do itself:** `valid_position` re-evaluates on a
    monthly tick, so the session ran on to 1067.6.12 (about seven months) and `.118` re-read
    `ACTING RABBI BOUND`. The un-gating survives revalidation, not merely the moment of
    appointment. Semicha permanence is verified separately, under S4b above.
  - **Bug fixed in S4b itself, found while doing the above.** The co-judge ranking in
    `kehillah_bet_din_open_docket_effect` ran *before* the Av Beit Din was bound, and
    `kehillah_bet_din_eligible_judge_trigger` excludes only the host — so an **appointed** Chief
    Rabbi (a learned courtier, i.e. population 2 of that trigger) could be drawn into a co-judge
    seat as well as the presiding one, staffing a court of three with two people and counting his
    Learning twice in the tally. He is now resolved first and excluded from the pool. Note this
    slightly *tightens* turnout math, which matters for the frequency question below.
- **S4d. BUILD — Bet Din frequency, first tuning pass.** (Daniel, 2026-09-27: *"help me
  brainstorm how to increase the bet din frequency"*, then approved levers 1-4 of the five
  offered.) **BUILT 2026-09-27, `ck3-tiger`-clean, NOT YET LIVE-TESTED.**

  What was actually braking it, read from code rather than guessed: 16 communities spread across 13
  tagged minhag regions, so the only population that scores highly as a co-judge — same-region
  community leaders — is typically 0–2 people. The Rhineland (Worms/Speyer/Mainz/Cologne) and
  Provence (Narbonne/Béziers/Lunel) clusters were fine; **Baghdad has no same-region peer at all**
  and Toledo is close to it, so both depended on a Learning-16 courtier or a wandering adventurer
  turning up. On top of that, a hard 3-year per-host cooldown.

  1. **Cooldown 3 → 2 years** (`kehillah_bet_din_conference_cooldown_years`). The hard ceiling;
     nothing else matters until it moves. 2 not 1 because the guest-arrival window ahead of a
     docket is up to three months, and a leader at a Beit Din more often than not stops reading as
     a leader who sometimes holds court. One number if still too rare.
  2. **Outside-scholar bar 16 → 12** (`kehillah_bet_din_scholar_guest_learning_threshold`). That
     number was set as a *prestige* bar ("a renowned scholar, not merely a capable one") but was
     doing duty as the *eligibility* bar in the shared judge trigger's population 2. 12 is what the
     cases themselves treat as a genuinely learned judge, so the feature now means one thing by it.
  3. **The host's own household can sit as dayanim**, at a new lower bar
     `kehillah_bet_din_local_dayan_learning_threshold = 8`, or on holding `kehillah_rabbi_trait` at
     any Learning. A Beit Din of three was normally three local men; requiring every seat but the
     host's to come from outside structured a routine communal court as a diplomatic summit.
     Implemented as population 4 of `kehillah_bet_din_eligible_judge_trigger` **and** a matching
     widening of `kehillah_bet_din_invite_rule_jewish_courtiers` — both, because a man the invite
     rules never offer a seat to never becomes an attendee and so can never be ranked into one,
     however eligible the trigger thinks he is. Pairs with S4c: semicha is permanent now, so a
     community accumulates eligible dayanim over a career instead of losing them.
  4. **`max_guests` 6 → 8.** This *replaces* the fourth lever as originally proposed, which was to
     halve the session length. **That proposal was wrong**: it read
     `kehillah_bet_din_case_phase_days = 30` as the pace of a case and concluded a session occupied
     the host ~90 days. It is a hang guard for an unanswered popup; a real docket runs about three
     weeks (`2 * kehillah_bet_din_case_step_days + 1` per phase). That value's comment now says so
     explicitly. What actually limits how often a Bet Din *happens* rather than is *attempted* is
     turnout — a session with fewer than two eligible attendees is invalidated outright — so with
     the invite pool widened by levers 2 and 3, six slots had become the binding constraint on it.

  Probe: `kehillah_debug.120`, read-only, reports the available co-judge count, the region-leader
  and own-household populations separately, both bars, the cooldown state and the S4b preside gate.
  The levers are otherwise invisible until a session runs or fails quorum months later.

  **S4d LIVE-PROBED 2026-09-28 -- PASS on a healthy region; the Baghdad question is untouched.**
  [Log](docs/testing/2026-09-28-heartbeat-s4bcd-s5-live-test-log.md) section 1. `kehillah_debug.120` on Worms: **co-judge count 30** against the
  invalidation floor of 2, region leaders 5, own household 5, off cooldown, both bars reading 12
  and 8 as set. Worms is the best case (the Rhineland cluster), so this shows the four levers did
  not break a healthy region and that this one has room to spare -- **it says nothing about Baghdad
  or Toledo, which is what the frequency problem was actually about.** Those two want the same
  probe, and a community with no same-minhag-region peer is the case that decides whether the
  unbuilt fifth lever is needed. Also recorded in the log because it is easy to misread later as a
  bug: an **appointed** rabbi is excluded from the co-judge count by design -- he presides, so he
  cannot also be one of the two judges beside the bench.

  **Open decision for Daniel, recorded not taken:** population 4 checks
  `kehillah_leadership_gender_eligible_trigger`, the hook every new leadership role in this mod goes
  through; the three older populations never have, so women can already sit as co-judges today via
  populations 2 and 3. Making the trigger consistent — in either direction — is one line, but it is
  a design call and not a tuning one, so it was not taken inside a tuning pass.

  **Not built, offered and deliberately left for review:** the fifth lever (adjacent-region or
  distance fallback when the home region cannot field a panel, which is the structural fix for
  Baghdad and Toledo rather than a probabilistic one), and the larger idea this conversation
  actually pointed at — **a second, smaller local Beit Din that is not an activity at all** (a 2–4
  event chain, own court, no travel, Chief Rabbi presiding, cooldown in months), fed by a **docket
  that accumulates real pending business** (disputes, semicha requests, agunah cases) so that the
  Chief Rabbi *asks permission to convene* when it fills. Frequency would then track how eventful
  the community is instead of a flat timer, and the officer would behave like an agent rather than a
  stat block. Also unbuilt: a landed or gentile host ruler convening a court for the Jews of his
  realm (S9a/Track B territory, roughly doubles who can start one).
- **S5. BUILD — Responsa.** Build exactly: an on_action pulse (roughly one question every 1-2
  years for a leader or Chief Rabbi with Learning ≥ ~12) firing an event where a named leader of
  another real community sends a question (start with 6 question texts, halakhic/communal flavour,
  no invented historical attributions). Three options (lenient / stringent / send to a greater
  authority), each a Learning-tiered check affecting Greatness, opinion with the asker, and a
  small effect on the asking community's Stability. A title counter `kehillah_responsa_count`,
  shown in the standing/map-view tooltip; at 10 answered, a decision to compile them into a book
  via the existing book system. **Done when**, live: the debug-fired event resolves all three
  options, the counter increments and displays, and the compile decision appears at the
  threshold.
  **BUILT 2026-09-27 (heartbeat 8), ck3-tiger clean, NOT YET LIVE-TESTED.** Files:
  `events/kehillah_responsa_events.txt` (one event, six questions — see its header for why one and
  not six), `common/scripted_effects/kehillah_responsa_effects.txt`,
  `common/decisions/kehillah_responsa_decisions.txt`,
  `common/customizable_localization/kehillah_responsa_custom_loc.txt`,
  `localization/english/kehillah_responsa_l_english.yml`, plus a `RESPONSA` section in
  `kehillah_script_values.txt`, three triggers, one opinion modifier, and the pulse in
  `kehillah_on_actions.txt`. Harness: **`kehillah_debug.116`** (reports every gate, states the tier
  it EXPECTS before the roll, then fires the event) and **`kehillah_debug.117`** (sets the counter
  to *exactly* the compile threshold, so the `>=` boundary itself is tested, not a comfortable
  margin above it). Run files ready in `run/`: `s5_responsa_state.txt`,
  `s5_responsa_arm_compile.txt`, `s5_responsa_readback.txt`.
  Three design choices recorded in the commit and the file headers rather than decided silently:
  the deferral is **not** Learning-tiered (a deferral is not an exercise of skill, and tiering it
  would mean a learned person defers *better*), only rulings increment the counter (a question
  passed along is not a responsum of yours), and the counter lives on the **title** because under
  this government the next leader need not be your son. The compile decision reuses the existing
  book system — genre `flag:talmudics`, tally 4/answer, which puts ten responsa at the book
  system's middle (famed) tier and fourteen at illustrious, checked against its actual cuts.
  **S5 LIVE-VERIFIED 2026-09-28 -- PASS on every criterion this item names.** [Log](docs/testing/2026-09-28-heartbeat-s4bcd-s5-live-test-log.md)
  sections 2 and 3.
  - **All three options resolve, and the counter reads exactly 2.** That last number is the
    load-bearing one: a deferral is deliberately not a responsum of yours, so three firings
    answered with lenient / stringent / defer must leave 2 on the books. They did.
  - **The tier tooltips agree with an independently computed figure**, not with a tester's
    expectation -- `.116` states the expected tier *before* the roll, and all three firings
    reported `EXPECT GREAT` against tooltips showing the great-tier text.
  - **The Greatness arithmetic was traced, not assumed:** 487 -> 501 (+14 great) -> 515 (+14 great)
    -> 512 (-3 deferral penalty).
  - **"Gather the Responsa" appears at exactly the threshold and produces a book.** `.117` sets the
    counter to exactly 10 rather than to a comfortable margin, so the `>=` boundary itself is what
    was tested. Taking it produced the artifact, reset the counter, set volumes to 1, and paid the
    famed-tier +80 Greatness (base 60 + 20 for a tally of 40 clearing the famed cut of 30) --
    computed independently and matched exactly.
  - **Two real bugs surfaced here, both in the shipped BOOK system rather than in S5**, and both
    fixed the same day. (1) **Every book this mod has ever produced came out masterwork**: eight
    tier reads inside `scope:newly_created_artifact` asked the *artifact* for a character variable,
    so all eight fell through to their masterwork `else`. The reward arithmetic reads the same
    variable in character scope and was always right, which is exactly why this survived a live
    test -- the numbers matched and nobody looked at the artifact. (2) **Compiling grew error.log by
    ~250,000 lines in one second**: a decision's effect block is evaluated to build its tooltip, and
    `set_variable` writes nothing in that pass, so calling `kehillah_book_complete_effect` inline
    right after setting the variables it reads threw on every rebuild frame (1,853 rebuilds x 9 read
    sites). Moved into a hidden `kehillah_responsa.0002` at `days = 0`. **The rule worth carrying
    forward: never write a variable and read it back in the same decision effect.** Log sections 6-8
    have the full account, including why `ck3-tiger` cannot catch either.
  - **Design change made during the run:** `kehillah_responsa_learning_threshold` lowered 12 -> 8.
    The gate was 12 and `kehillah_responsa_learning_good` is 12, so the gate admitted nobody who
    could land *below* the good cut -- the whole POOR tier, the only outcome where answering costs
    you standing, was unreachable script. 8 is `kehillah_bet_din_local_dayan_learning_threshold`,
    S4d's own bar for a real judge. Log section 9.
  - **Still untested:** the POOR and GOOD tiers (reachable now, but the Worms leader has Learning 32
    so every firing landed GREAT -- needs a low-Learning answerer, and it is the cheapest thing left
    on S5); and the yearly `on_action` pulse firing **on its own**, together with S4b's 40%
    against-the-AI bias. Every firing in this run was armed and fired by probe.
- **S6. BUILD — Community goals.** Build exactly: a decision "Set the Community's Goal" (one active
  goal at a time, 10-year deadline, stored as title variables) offering 4 goals checked on the
  quarterly tick: **Build the Yeshiva** (the building exists at tier N), **A Name Among the
  Communities** (Greatness reaches Flourishing), **Secure Our Rights** (the charter's security or
  construction term improves), **A Daughter Community** (a new community is founded by one of
  your courtiers or dynasty — if that turns out hard to detect, swap in "Prosperity reaches
  Flourishing" and note it). Completion: a notice, a pillar reward, and a permanent title modifier
  or counter as legacy; missing the deadline: a small Stability loss. Active goal + progress shown
  in the standing tooltip. AI communities pick a goal at random, weighted by their weakest pillar.
  **Done when**, live: one goal is set, completed via debug state, the reward and legacy appear,
  and a failed deadline applies its penalty.
  **DONE — VERIFIED LIVE 2026-09-29**, [log](docs/testing/2026-09-29-s6-goals-live-test-log.md).
  The decision and goal-choice event render with real text; after setting "A Name Among the
  Communities", `.123` reports GOAL ACTIVE / DEADLINE RUNNING and the standing tooltip shows the
  goal and "268 more Greatness to Flourishing" (432 + 268 = the 700 threshold). `.124`: all six
  asserts PASS (Greatness 432 → 472, exactly the +40 reward; counter 0 → 1). `.125`: all four PASS
  (Stability 369 → 344, exactly −25; counter unmoved), and the failure toast was seen rendering. No
  new error.log lines from any goal file. One bug, in the debug probe only: `.123` read
  `kehillah_var_goals_completed` unguarded and threw three error lines on any community that had
  never completed a goal. Fixed the same day.
  Original build note: **BUILT 2026-09-28 (Sukkot heartbeat), `ck3-tiger` clean — 0 fatal, 0 error, 58 warnings, which
  is BELOW the standing 59-warning baseline and with nothing anchored on any file the build
  touches.** Files: `common/scripted_triggers/kehillah_goal_triggers.txt` (read its header first —
  it carries the design account), `common/scripted_effects/kehillah_goal_effects.txt`,
  `common/decisions/kehillah_goal_decisions.txt`, `events/kehillah_goal_events.txt`,
  `common/customizable_localization/kehillah_goal_custom_loc.txt`,
  `localization/english/kehillah_goal_l_english.yml`, plus two message types, a COMMUNITY GOALS
  block in `kehillah_script_values.txt`, the `KehillahBdGoal` row appended to
  `KEHILLAH_BD_STANDING_TOOLTIP`, one call in the quarterly pulse and one in the founding effect.
  - **The deadline is the ENGINE's, not a stored date.** `kehillah_var_goal_timer` is set with
    `years = kehillah_goal_deadline_years` and CK3 removes it on expiry, so "goal set, timer gone"
    IS the expired state. Nothing ticks and nothing compares dates. Vanilla's own
    `00_councillor_effects.txt:690` uses a script value in that same `years` field, so the tunable
    is not a guess.
  - **Three design choices recorded rather than made silently** (full reasoning in the commit and
    the file headers): the daughter-community goal detects **dynasty only** and is **pushed** from
    `kehillah_found_community_effect` rather than polled, because a founder is a landless
    adventurer by the founding decision's own gate and the link to whatever court they once sat in
    is gone by then — the same erasure S4(3) works around by reading the old liege *before*
    `add_courtier`; legacy is a **counter, not a title modifier** (S6 allows either); and AI
    weighting is **absolute, not relative** — each pillar against the Healthy band rather than
    against the other two, which is a shape this codebase uses everywhere instead of one it has
    never used.
  - Harness: `kehillah_debug.123` (read-only, and it reports which goals would be OFFERED, not
    only the one set), `.124` (completion path end to end) and `.125` (failure path). Both `.124`
    and `.125` assert the **arithmetic** — exactly pre-value plus the reward, exactly one more
    completed goal, exactly pre-value minus the penalty — so a reward applied twice fails here
    where a "did it go up" test would pass; `.125` additionally asserts the legacy counter does
    **not** move on a failure. Run files: `s6_goal_state.txt`, `s6_goal_complete.txt`,
    `s6_goal_fail.txt`.
  - **KNOWN LIMITATION, found by source-reading during the build and NOT a live finding: "Secure
    Our Rights" is currently unreachable by anything the player does.** The charter rungs it reads
    (`kehillah_charter_cache_security` / `_construction`) are written once, at charter
    establishment, from the host realm's Jewish Settlement Policy — and the only things that write
    that policy today are debug events 72-75. `tributary_contract_set_obligation_level` appears in
    exactly two files: the charter effects (all at establishment) and the debug events. So in
    ordinary play the rung changes only when the **host changes**, via
    `kehillah_maintain_host_charter_effect` re-pointing the charter after a conquest. **S9a, the
    very next item in this queue, is what makes the goal player-drivable**; the goal was left in
    rather than cut because its mechanism is sound and its dependency is one item away.
- **S7. BUILD — Bookmark with the three prototype characters.** A 1066 bookmark featuring the
  Scholar (Rashi of Troyes), the Shtadlan (a Sh'um or Cologne leader), and the Financier (a landless
  Jewish adventurer near Rouen, created for this). ck3-tiger checks bookmark portraits — a missing
  one crashes the game. Must boot and be selectable live.
  **DONE — VERIFIED LIVE 2026-09-29**, [log](docs/testing/2026-09-29-s9a-s7-live-test-log.md). The
  bookmark boots and lists all three with real text; Yosef starts as an adventurer ("The Rodom
  Traders", "mi-Rodom", 406 gold = 300 scripted + the vanilla adventurer treasury), Rashi as leader
  of the Kehillah of Troyes. One bug: the two new cards had no per-character background art
  (`VFSOpen Error ... _troyes_rashi.dds / _rodom_yosef.dds`), so they drew a flat colour; fixed
  with copies of Isaac's art as placeholders (the founder-test bookmark has the same gap, left
  alone). Marker positions still unjudged against terrain.
  Build note: **BUILT 2026-09-29, `ck3-tiger` 0 fatal / 0 error.** Rashi (9000201, leads
  Troyes) and a new, explicitly **invented** Financier — Yosef ben Menahem "mi-Rodom" (9000300,
  dynasty 9000060, `history/characters/rouen_1066.txt`), a landless adventurer whose company
  `d_kehillah_rodom` is set up exactly as vanilla's `d_laamp_wake` — were added to the existing
  `bm_1066_kehillah_worms` rather than a new bookmark, so its art is reused and Isaac is the
  Shtadlan. Placeholder portraits (same shape as the founder test's). +4 tiger warnings, all the
  same missing-portrait-art / missing-coat-of-arms kinds Isaac already has. **Deferred:** renaming
  the bookmark away from "The Kehillah of Worms" (its loc is in `kehillah_l_english.yml`, which
  had uncommitted parallel edits at the time); "Rodom" as Rouen's Hebrew name is marked TO VERIFY;
  bookmark `position`s are guesses a screenshot should correct.
- **S8. BUILD — The Financier path.** The S7 adventurer can take up the post-Conquest invitation and
  found an English community themselves (V18 currently founds them only as AI): after the Conquest
  resolves, the player adventurer gets an invitation event (accept → travel/found in London via the
  existing founding effect with an Encouraged-tier charter; decline → AI founding as now). Then one
  royal-finance loop: reuse the existing loan contract with the King of England as a repeat
  borrower (larger sums, royal favour as opinion + charter security) — no new finance system.
  **Done when**, live: the invitation appears for a player adventurer, accepting founds the
  community with the right charter, and a royal loan originates, accrues and repays.
  **PART A (the invitation) DONE — VERIFIED LIVE 2026-09-29**,
  [log](docs/testing/2026-09-29-s8a-london-invitation-live-test-log.md). As the S7 Financier:
  accepting founds "Kehillah of London" under the player (Kehillah government, Jewish Quarter in
  Middlesex, a host charter, England Encouraged) and it survived 46 days past founding with no
  Game Over; declining leaves the AI to found it; exactly one London either way, and the 60-day
  fallbacks found nothing pending afterwards. The first run found the invitation throwing ~15,600
  tooltip-preview errors while on screen — the Decline option called the AI founding effect
  directly, and CK3 dry-runs option effects for tooltips. Decline now hands off to `.0012` a day
  later; retest: zero errors. The fallback is scheduled on both king and invitee (an event does
  not fire on a dead character). Code: `kehillah_norman_conquest.0010`-`.0012`,
  `kehillah_norman_london_invitation_eligible_trigger`, probes `kehillah_debug.130`/`.131`.
  **PART B (royal loans) DONE — VERIFIED LIVE 2026-09-29 (S8 COMPLETE)**,
  [log](docs/testing/2026-09-29-s8b-royal-loans-live-test-log.md). Every three years the host of a
  player-founded London asks it for a loan (`kehillah_norman_conquest.0020`) through the ordinary
  loan contract at 2x principal; sealing it earns +20 decaying Royal Favour. Live: request offered,
  full challenge chain, gold −300 exactly, crown owes 390, FAVOUR PASS, on the debtor list, and the
  next yearly request correctly SKIPPED while the crown still owed. **Found and fixed on the way:**
  (1) every loan to an AI ruler defaulted at term by construction (the repay decision is player-only)
  — an AI borrower now repays at term when it can afford to, a change to every community's loans;
  (2) `kehillah_loan_contract`'s `valid_to_continue` was false for the whole negotiation, so the
  engine voided the contract mid-chain and the next stage silently never fired — every loan since
  the 2026-09-17 chain overhaul. Repayment at term then verified in a focused run: accrual +0.25 per
  pulse, `an AI borrower repaid at term`, lender gold +391 over the window (390 + ordinary income),
  CROWN OWES NOTHING. **Backlog:** a debtor who dies or is purged
  takes the debt with him — no repayment, no default, a stale debtors-list entry; whether an heir
  inherits a royal debt is a design question for Daniel. Deferred: the charter-security half of
  royal favour (needs subject-contract writes).
- **S9a. BUILD — Host-ruler settlement-policy decisions (non-Jewish player).** Two decisions, "Raise"
  and "Lower Jewish Settlement Policy" (one rung each, 5-year cooldown), writing the existing V16
  title variable. Raising: costs piety/clergy opinion, grants a notice to Jewish communities in the
  realm. Lowering: small piety gain, lost income expectation spelled out in the tooltip. **No AI use
  yet** (V17 wants event-led AI; that's with Daniel). **Done when**, live: a non-Jewish player moves
  the policy both ways and the Kehillah sees the notice and the changed charter outlook.
  **DONE — VERIFIED LIVE 2026-09-29**, [log](docs/testing/2026-09-29-s9a-s7-live-test-log.md). `.127`/`.128`
  RUNG PASS and COOLDOWN PASS in both directions (Allowed → Encouraged → Allowed → Discouraged), no
  STORAGE FAIL, the Discouraged floor holds (`SKIP`, no `FLOOR FAIL`), six communities under the
  Emperor each notified, and the Lowered notice rendered with real names. The ledger badge followed
  every step, and at Discouraged the charter line reads "Grandfathered rights exceed the current
  policy — charter review needed". Taken through the UI as the Emperor (`play` needs his INTERNAL
  id): real text, 100 Piety paid exactly (963 → 863), the chaplain's −15 shown, Lower blocked with
  the floor reason, the cooldown blocking both. Zero error.log lines from any S9a file. The
  chaplain's actual opinion breakdown was not hovered (tool outage) — tooltip-evidenced only.
  Build note: **BUILT 2026-09-29, `ck3-tiger` 0/0/59 (baseline).** Files:
  `common/decisions/kehillah_settlement_policy_decisions.txt` (header carries the design limits),
  `common/scripted_effects/kehillah_settlement_policy_effects.txt`, a values file, an opinion
  modifier, a loc file, two message types, `kehillah_policy_review_on_cooldown_trigger`. Choices
  made, smallest-reasonable: shown only to an **independent** non-Kehillah ruler (a vassal's title
  is never the one its communities read); the cooldown lives on the **realm title**, so a successor
  inherits it; **Lower stops at Discouraged** until S9b exists (Raise still climbs out of a
  debug-set Banned); piety cost and chaplain objection are waived for a Jewish ruler/chaplain.
  **Finding: the host draws no tribute from any charter today** (the contracts carry only
  subject-side modifiers), so "lost income" is honestly phrased as lost future settlement — a real
  host income stream is a design question for Daniel (V17 / S12). Harness: `kehillah_debug.126`
  (state), `.127` raise and `.128` lower through the real effects asserting exactly one rung plus
  cooldown plus "Allowed is stored as absence", `.129` clears the cooldown; run files
  `s9a_state/raise/lower/clear_cooldown.txt`, fired **as the Kehillah player** against its host so
  the notice lands on the player it is for. The decision UI itself needs a `play` switch to the
  host (the Emperor, for Worms).
- **S9b: BUILT 2026-10-12, not live-tested** ([v30](docs/spec/v30-expulsion-and-householders.md)).
  The ending is dissolution (Daniel's call), not "S1's departure path with followers and treasury
  share" as written below. The original item:
- **S9b. BUILD — Expulsion.** Lowering to Banned starts a warning event for every community in the
  realm, then after ~1-2 years an expulsion event with counterplay options (petition/bribe the
  ruler via the Shtadlan → chance to restore Discouraged; leave in good order → S1's departure
  path with followers and treasury share; stay illegally → Stability drain, later forced exit).
  Depends on S1. **Done when**, live: both the reprieve and the departure outcome have been played
  through with no errors in error.log.
- **S10. BUILD/TEST — 50-year soak test.** Debug event + observe run logging every community's
  pillars yearly at speed 5; run it (the PC is free), record drift / dead loops / runaway numbers,
  fix the worst findings.
- **S11. DANIEL-REVIEW — Friendliness toward Jews and the Crusades chain.** Top priorities for v0.1
  but design-heavy; to be designed with Daniel after Sukkot. Runs may only add short research
  bullets to V22 §5 (e.g. which vanilla 1.19 on_actions/GHW hooks exist for a crusade call and army
  movement). No spec docs, no builds. **Research bullets DONE, 2026-09-25 (heartbeat 2)** --
  V22 §5's new "Vanilla 1.19 hooks available for the Crusade chain" block: no
  "crusade declared" on_action exists, but `on_army_enter_province` does and vanilla's own
  `great_holy_war.0060` already uses it to spot a crusading host arriving. Nothing built.
- **S12. DANIEL-REVIEW — Host charter polish; community watch → landed military force (vassal or
  independent).** Short research bullets at most.

4. ~~**Quick-win UI**: expand the Take Stock decision into a real breakdown...~~ **CLOSED, 2026-09-23,
   per user decision — no longer needed.** `kehillah_view_standing_decision` itself was never built
   out (still a one-line `custom_tooltip` stub, confirmed by reading it) — but the actual need this
   item was chasing (see what's growing/shrinking a pillar and why) is now served by the map view's
   per-pillar contributor breakdown (v12/v13, `kehillah_breakdown_custom_loc.txt` +
   `kehillah_breakdown_l_english.yml`, live-verified) and the community-list interaction's own
   Stability/Prosperity/Greatness tooltips (v9). A dedicated Take Stock rewrite would be duplicating
   visibility that already exists elsewhere, not adding new visibility. If a future session still
   wants a decision-based breakdown specifically (rather than the map view), the
   `KehillahBd*`-prefixed customizable-loc lines already do the per-line work and can be reused
   directly — nothing here needs to be re-derived, just wired to a different call site.
5. **DONE, 2026-09-10 (research), then 2026-09-10 (v9 build on top of it).** GUI feasibility research
   pass: [docs/spec/gui-spike-community-list.md](docs/spec/gui-spike-community-list.md) — ended up
   reading different files than this item originally named (the user's own Military-pane idea
   narrowed the actual question, see the spike's §2), but answered the same "concrete, evidence-based
   plan for opening a window bound to scripted data" ask: no cross-file additive `.gui` mechanism
   exists (5,166 `blockoverride` uses surveyed, all same-instantiation fill-ins), so any new window
   means either reusing a screen already driven by script (an activity's guest list; a character
   interaction's target-search list) or a permanent fork of a vanilla `.gui` file. Built on top of
   that, [docs/spec/v9-community-list-ui.md](docs/spec/v9-community-list-ui.md) shipped a real
   map-wide community list: `kehillah_view_communities_interaction` (common/character_interactions/
   kehillah_character_interactions.txt) reuses vanilla's own character-interaction target-search
   screen (`vbox_character_list`/`portrait_base`), populated from `kehillah_registered_communities`
   via `populate_recipient_list`, with a per-candidate Stability/Prosperity/Greatness breakdown
   tooltip via the interaction's own `ai_accept` acceptance-breakdown row — zero vanilla `.gui` file
   touched. See that file's own header comment for the full mechanism verification (a real correction
   to v9's own assumed design: decisions cannot open interactions by script; there is no dedicated
   button, the interaction is reached via the ordinary right-click interaction menu, same as vanilla's
   own `offer_courtier_interaction`). **Not live-tested** — see that same header. This item's own
   original "own-community" and "map-wide" dashboard split (items 9/10 below) is effectively answered
   for the map-wide half by this build; a richer own-community dashboard (more than
   `kehillah_view_standing_decision` already shows) is still open.
6. **DONE, 2026-09-08. Regional/unified leadership**: see
   [docs/spec/v4-regional-communities-and-batei-din.md](docs/spec/v4-regional-communities-and-batei-din.md)
   for the design (a titular duchy-tier `d_kehillah_shum` grouping Worms/Speyer/Mainz by de jure
   nesting, no new government/succession construct in v1) and
   [docs/testing/2026-09-08-shum-live-test-log.md](docs/testing/2026-09-08-shum-live-test-log.md)
   for the live-test pass that closed it out — Speyer and Mainz exist as AI-run peer communities,
   the Greatness-gated "Convene the Bet Din of Sh'um" decision and its three-option takkanah event
   are live and confirmed working end to end (UI, gate, and the symmetric per-title effect at the
   raw-value level). This still doesn't resolve the "aggregate score for a dashboard" question —
   the spec deliberately sidesteps it by applying takkanah effects symmetrically per-title rather
   than defining a blended regional number — so the sort-primitive and aggregate-definition
   problems flagged here originally are still open for whenever a real dashboard needs them.
   **PER-COMMUNITY AGGREGATE NOW DEFINED, 2026-09-14** (user decision, mid-build on item 10):
   `kehillah_var_standing`, the arithmetic mean of the three pillars, maintained as a real title
   variable — see [docs/spec/v12-community-map-view.md](docs/spec/v12-community-map-view.md) §2.3
   for the definition, why it is the mean and not the sum (it shares the pillars' scale, so their
   band thresholds and `kehillah_pillar_at_least_trigger` apply to it unchanged), and where it is
   maintained. v4's own symmetric-per-title takkanah mechanism is unaffected and unchanged. The
   *regional* roll-up — several communities into one figure — is still genuinely open and needs its
   own spec; do not improvise one.
   **SUPERSEDED, 2026-09-08 — see item 7 below.** The 15-year single-ruling decision this item
   shipped is being replaced, not kept alongside its replacement.
7. **Bet Din Conference, Part 1 — BUILT, ck3-tiger-clean; live-tested PASS 2026-09-08, then
   REOPENED the same day by two structural bugs that pass missed (docket fired all at once, activity
   never ended). Fixed, and the fix itself LIVE-TESTED — PASS — 2026-09-24, see the "DOCKET LOOP
   FIX" paragraph below.**
   Redesigns item 6's takkanah decision into a travelled-to gathering activity (Hunt/Grand Wedding-
   scale, not a lighter travel-event chain), convened every 3 years instead of every 15, drawing 3
   hardcoded test cases from what will eventually be a large pool. Each case is ruled on by the
   three community leaders (player and AI) via a stat-tiered skill check, affecting Prosperity/
   Stability/Greatness; one test case can add a permanent tenet to the faith (Rabbeinu Gershom's
   herem against polygamy) — **confirmed live**: a `doctrine_polygamy` → `doctrine_monogamy` change
   on rabbinism's faith actually fires in a running game, not just on paper. The live-test pass
   itself found a real bug `ck3-tiger` structurally cannot catch — an unguarded `global_var` read in
   a chained `after` block, re-evaluated every tooltip-rebuild frame while hovering an option, that
   turned one clean failure into a ~28MB/minute error-log storm — fixed with `exists =` guards at 16
   sites. Full build record, the live-test account, and what's still open going into a fuller pass:
   [docs/spec/v5-bet-din-conference.md](docs/spec/v5-bet-din-conference.md) sections 8-9 and
   [docs/testing/2026-09-08-bet-din-conference-live-test-log.md](docs/testing/2026-09-08-bet-din-conference-live-test-log.md).
   **Travel confirmed too, same day, in a follow-up pass**: the real activity-hosting UI is F9 in
   the right-edge HUD strip (found by reading `gui/hud.gui` after direct exploration missed it — a
   nearby cup/goblet icon had been mistaken for it). F9 lists "The Bet Din Conference" alongside
   Hunt/Pilgrimage/University Visit; hosting it opens a real map planner (Worms selectable, Brussels
   correctly rejected as "not your Realm Capital") with two real "Co-Judge" portraits. Starting it
   and unpausing showed the phase go `Waiting` → `Engaged` after ~12 in-game days of real travel,
   with the docket opening on its own via the real `on_phase_active` — confirming the one thing v5
   §3 chose a full custom activity_type *for* genuinely works. One cosmetic bug found: the host
   dialog's title renders as a raw loc key, unfixed. No art assets exist yet either (4 missing-icon
   warnings, cosmetic only). The hundreds-of-cases content pass is Part 2, and
   doesn't start until a case-idea draft exists (see the backlog entry below).
   **DOCKET LOOP FIX, 2026-09-08 — NOT YET LIVE-TESTED, and it downgrades the "LIVE-TESTED: PASS"
   above.** Playing the build described above showed two structural bugs the live-test pass missed:
   the whole docket (all ten events) fired inside a single day, and the activity never ended,
   because nothing in the activity type ever called `progress_activity_phase_after` — the one thing
   that ends a phase in CK3. The pass missed both because it never followed a real hosted session
   past case 1; its console-driven half exercised the event chain but never the phase lifecycle.
   **Fixed**: the docket is now three predefined phases, one case each, each case **drawn at random
   from those the session has not heard yet** (so the draw-without-repeat machinery Part 2 wanted
   exists now — only its case *content* is still gated on the case-idea draft); events within a case
   are 3 days apart; a case's resolution ends its phase instead of summoning the next case; and the
   activity's own `on_complete` fires a rewritten closing event that reads a new **session score**
   (each case's verdict tier summed: great +2 / good +1 / poor −1) and pays out on a landmark /
   strong / adequate / failed tier. `ck3-tiger` clean (0 fatal, 0 error). Full account, including
   why the earlier pass missed this and what specifically still needs a live pass:
   [v5 spec section 11](docs/spec/v5-bet-din-conference.md).
   **LIVE-TESTED, 2026-09-24 — PASS.** Hosted for real, followed through all three cases to the
   close: correctly paced (not one-day mass-fire), phases advance one case at a time, random draw
   varies (and turned up two cases not documented in this doc — Part 2's pool has grown since this
   was last updated), and the docket closes exactly once with the activity actually ending. Full
   account in v5 §11's own status paragraph. **Two new, unrelated, single-fire bugs found in the
   process**: a missing `exists =` guard in `kehillah_bet_din_semicha_events.txt`, and an unguarded
   negative `add_gold` in the Silversmiths' Quarrel case resolution. **Source-fixed 2026-09-25,
   awaiting live regression:** the Semicha event now refuses a stale host-dependent offer, and
   restitution is capped at the accused's actual gold while preserving a matched transfer to the
   accuser. See `BLOCKERS.md`.
   **Design-only addendum, 2026-09-08**: [v5 spec section 10](docs/spec/v5-bet-din-conference.md)
   proposes widening the panel with up to 2 additional non-leader Jewish scholars, found via a
   `guest_invite_rules` search and scored on proximity/Learning/Piety/traits, each getting a real
   event (not folded into the tally) — raising a case's event count from 3 to up to 5. Not built;
   worth weighing before Part 2's case format locks in, since it changes per-case authoring cost.
8. **Wave 4** (dissolution) and **Wave 5** (community lifecycle: creation/destruction/migration),
   per [docs/spec/v2-pillar-economy-and-lifecycle.md](docs/spec/v2-pillar-economy-and-lifecycle.md)
   §8's build order. **Creation half of Wave 5 is now built and live-tested** (2026-09-19 onward):
   "Found a Jewish Community" (`kehillah_found_community_effect`,
   `common/scripted_effects/kehillah_found_community_effects.txt`) places a new landless title
   anywhere a landless adventurer stands, with AI eligibility enabled — see
   `docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md` for the live-test PASS and the two
   real bugs it found and fixed. **Destruction and migration (dissolution, the actual rest of Wave 4
   and Wave 5) are still entirely unbuilt** — do not read the founding work above as having closed
   this item, only its creation half.
9. **Own-community GUI dashboard** — richer than `kehillah_view_standing_decision`'s current single
   desc block. Item 5's research has landed; this is now unblocked, just not built.
   **2026-10-12 UI polish:** the already-shipped HUD strip now shows each pillar's
   trend and a colored Roman tier (I–V), with a wider explicit background;
   exact scores and contributors remain on hover. **Verified live after
   the 2026-10-12 reboot:** the first rendering revealed a short background
   and displaced hover hitboxes; both were fixed with a fixed window/hbox
   layout. All three visible tiles and their matching breakdown hovers passed
   ([log](docs/testing/2026-10-12-pillar-hud-polish-live-check.md)).
   **Worth a second look now that item 4 is closed (2026-09-23) for the same underlying reason**:
   the map view (v12/v13) already shows your own community's row (highlighted) alongside everyone
   else's, with the same pillar/breakdown data this item wants. Not closed here unilaterally, since
   this item is specifically about a dedicated *own-community* view rather than "your row in the
   general list" — but if that distinction doesn't matter in practice, this may be another
   already-satisfied item, not a real gap.
10. **Map-wide/regional GUI dashboard** — **first draft shipped as part of item 5** (`kehillah_view_
    communities_interaction`, a clickable per-community list with pillar tooltips, reached via the
    right-click interaction menu rather than a dedicated window). What's still open past that first
    draft: a dedicated entry point (a real button, not "right-click anyone") needs either
    `gui/scripted_widgets/` to be live-test-verified first (the spike flagged it as real but unproven,
    zero vanilla usages found) or a Military-pane fork (the spike's confirmed-but-costly fallback);
    and the list itself is not sortable/filterable the way a true dashboard would be.
    **SECOND DRAFT BUILT 2026-09-14, CORE ROSTER CONFIRMED LIVE THE SAME DAY:**
    [docs/spec/v12-community-map-view.md](docs/spec/v12-community-map-view.md). This takes the
    `gui/scripted_widgets/` route the paragraph above names as unproven, and is this repo's first
    use of it — a dedicated toggle button and a roster panel of every community in the world, each
    row showing standing plus the three pillars and carrying a locate button that moves the camera
    to the community's live host county (`Title.SelectTitle`). No vanilla file is forked. The spec's
    §1 records why a literal CK3 map mode is not available to a mod at all (colouring is engine-side
    with no script-drivable `color_mode`; a Kehillah owns no county to colour; the map-mode bar is a
    hand-written button list, not a datamodel) — read that before anyone re-scopes "add a map mode"
    as though it were a data change. **Per v12's own status line (checked 2026-09-23, do not rely on
    this summary staying current — read that line directly): the roster itself is confirmed live**
    (button, draggable window, real rows with portraits/leaders/host counties/standing/pillars,
    sorted, own row highlighted) across five live passes the same day it was built.
    **Still unverified**: the 2026-09-20 rework of the map-mode recolor (painting only a community's
    own barony instead of its whole host county) hasn't been re-tested since; the region hierarchy
    (§7); the locate button and tooltips specifically. Sorting is script-side (standing, descending);
    filtering is still absent and still deliberate.

**Current state:** Phase 1 is verified working live, end to end, as of
2026-09-06 — bookmark start, buildings, officers, and a full
console-kill → appointment succession → continue-as-successor cycle all
confirmed in a running game, government/courtiers/treasury intact across
the handoff. The original crash was misdiagnosed the first time (section
6 of the implementation doc); the actual cause — vanilla's
`is_playable_character` trigger has no branch for a custom landless
government — is recorded in section 8 there, with the fix in
`common/scripted_triggers/kehillah_is_playable_character_override.txt`.
The same session also carried out a building/officer/pillar content
rework (implementation doc section 9): Shtadlan's Chambers and the
Communal Watch are gone, the Shtadlan and standing firm are now
ungated, Hekdesh/Sofer's Workshop/Slaughterhouse and four new minor
positions are in, and the four community goals are now three pillars
(Prosperity/Stability/Greatness, spec §3).

**2026-09-07 update — the three pillars now have a full economy, not
just a display.** See
[docs/spec/v2-pillar-economy-and-lifecycle.md](docs/spec/v2-pillar-economy-and-lifecycle.md)
for the full input/output design (band scale, baseline convergence,
dissolution) and its §8 for the 5-wave build order. Status:
- **Wave 1** (organic dispute event, epidemic/physician hooks) —
  implemented, live-tested for the epidemic hooks' non-interference;
  the dispute event itself is probabilistic and hasn't fired in a test
  window yet.
- **Wave 2** (Prosperity variable, band triggers, baseline convergence)
  — implemented and live-tested; see
  [docs/testing/2026-09-07-live-playtest-log.md](docs/testing/2026-09-07-live-playtest-log.md).
  This pass also found and fixed the session's one major bug (pillar
  variables were never `set_variable`-initialized, so `change_variable`
  silently no-op'd on all of them) and a benign-but-unresolved "illegal
  government" error firing on every succession.
- **Wave 3** (sfarim tiers, band-gated building tiers, courtier
  quality/cap/retention, light loan contracts) — implemented, not yet
  live-tested. Runbook and console test harness ready:
  [docs/testing/wave3-testing-runbook.md](docs/testing/wave3-testing-runbook.md)
  and `events/kehillah_debug_events.txt`.
- **Waves 4-5** (dissolution, community lifecycle) — not started.

**2026-09-08 update — regional/unified leadership shipped and live-tested**, outside the
Prosperity/Stability/Greatness wave numbering above (it's a v4 spec item, not v2's). See
[docs/spec/v4-regional-communities-and-batei-din.md](docs/spec/v4-regional-communities-and-batei-din.md)
and [docs/testing/2026-09-08-shum-live-test-log.md](docs/testing/2026-09-08-shum-live-test-log.md).
Speyer and Mainz now exist as AI-run Kehillot alongside Worms, all three nested under a titular
`d_kehillah_shum` duchy (the first landless-county-inside-a-duchy structure this mod has built,
confirmed clean live), and "Convene the Bet Din of Sh'um" is a real, working decision. This pass
also found and fixed a real pre-existing-adjacent bug: `kehillah_pillar_at_least_trigger` could
read a pillar variable before the same tick's `kehillah_init_pillars_effect` had set it (courtier
seeding at game start raced the variable-set); it now guards with `has_variable` first, matching
a vanilla precedent the trigger's own header already cited but hadn't fully copied.

**2026-09-10 update — v8 Task Contracts shipped, ck3-tiger-clean, not yet live-tested.** See
[docs/spec/v8-task-contracts.md](docs/spec/v8-task-contracts.md). Four `task_contract_type` entries
(`kehillah_translation_contract`, `kehillah_loan_contract`, `kehillah_exotic_goods_contract`,
`kehillah_hebrew_tutor_contract`, common/task_contracts/kehillah_task_contracts.txt) let a nearby
non-Kehillah, non-coreligionist county holder occasionally offer the community leader work through
CK3's real EP3 Task Contracts system, fired by a new `kehillah_task_contract_pulse` on_action
(chance_to_happen 40, common/on_action/kehillah_on_actions.txt) and a five-event offer chain
(events/kehillah_task_contract_events.txt, namespace `kehillah_task_contract`: a hidden router plus
one flavored Accept/Decline event per type). Translation, exotic goods, and hebrew tutoring all
resolve immediately, inside the contract type's own `on_accepted`, via a skill-tiered `complete_task_
contract` call — verified against a real non-travel vanilla contract (`admin_contracts.txt`'s
`overdue_taxes`) before choosing that shape over an engine-timed completion.

**The loan contract replaces `kehillah_extend_loan_decision`**, per explicit user request ("I think I
prefer the contract mechanic for loans over a decision! Feels more compelling and character driven").
Direction is inverted from the other three types — the employer IS the lender, the Kehillah ruler is
the borrower — and the contract's `on_accepted` writes the SAME three ledger variables
(`kehillah_loan_amount_owed`/`kehillah_loan_lender_title`/`kehillah_loan_years_elapsed`) the old
decision used to write, at the same values, via the same script values. `kehillah_repay_loan_decision`
and the quarterly accrual/default block (`common/scripted_effects/kehillah_scripted_effects.txt`) are
both completely untouched, per the task's own explicit constraint — which is also why the contract's
own closure (`on_invalidated`, once `var:kehillah_loan_amount_owed` clears either way) is deliberately
NEUTRAL rather than claiming success or failure: distinguishing repayment from default after the fact
would require touching one of those two untouched files, or building a fully parallel tracking system
duplicating a signal the player already sees directly. Documented as a real, deliberate scope cut, not
an oversight — see that contract type's own header comment for the full account. The retired decision
is preserved in git history with a documented pointer comment in its place (common/decisions/
kehillah_decisions.txt).

Also verified and corrected one thing the spec's own draft had gotten wrong: the real effect for a
player declining an offered contract is `invalidate_contract = yes`, called ON the contract scope —
not `invalidate_task_contract = <scope>`, which does not exist anywhere as a callable effect in the
installed game files. And confirmed `create_artifact`-family effects have no real precedent inside a
`task_contract_reward` block anywhere in vanilla, so the exotic goods contract's reward is gold +
opinion only, per the spec's own named fallback, rather than forcing an artifact in.

ck3-tiger clean (0 errors, 0 warnings on every file touched or created). Not yet live-tested.

**2026-09-14 update — Commission a Translation overhauled into a real challenge chain, at the
user's own explicit request, ck3-tiger-clean, not yet live-tested.** `kehillah_translation_contract`
(common/task_contracts/kehillah_task_contracts.txt) no longer resolves inside its own `on_accepted`
off a single learning-check; it now hands off to a five-event challenge chain
(events/kehillah_translation_events.txt, namespace `kehillah_translation`, effects in
common/scripted_effects/kehillah_translation_effects.txt) mirroring "Write a Book"'s own tally/
threshold shape: Securing the Text → The Difficult Passages → A Second Opinion (reuses
`kehillah_book.0003`'s exact random-courtier/lucky-roll shape under its own constants) → Revise or
Rush → The Finished Copy, which resolves a genuine TRIUMPH/SUCCESS/FAILURE tier (a real failure
floor, not just a quality band) and then poses the user's own requested final choice: deliver
honestly, or keep the true copy for the Kehillah's own library and hand over a lesser one, with a
real, Intrigue-modified risk of being caught. `create_artifact_book_effect` (EP1-gated, same macro
"Write a Book" already uses) fires for the stolen copy specifically — named after whichever of ten
real, dated pre-876 Greek/Arabic works was requested — which does not violate this file's own
earlier "no create_artifact precedent inside a task_contract_reward block" finding, since the
artifact is created in the calling EVENT, before `complete_task_contract` ever fires.

**The offer now names a specific, real work**, picked by `kehillah_translation_pick_work_effect` in
the router before the flavored offer event fires: five works transmitted from Greek (Euclid,
Ptolemy, Galen, Hippocrates, Dioscorides) and five original Arabic works (al-Khwarizmi's algebra and
astronomical tables, al-Kindi, Jabir ibn Hayyan, and Masha'allah ibn Athari — a Jewish-born
astronomer who helped cast Baghdad's own foundation horoscope, kept in the pool deliberately for
that resonance), all pre-876 or, for the Greek set, squarely Byzantine-court-held regardless of
exact Arabic-recension dating. **The employer gate is new**: `kehillah_translation_contract` is now
only offered to non-Muslim, non-Greek/Byzantine-heritage rulers (`faith.religion = religion:
islam_religion` and `culture = { has_cultural_pillar = heritage_byzantine }`, both real, precedented
vanilla triggers, checked rather than guessed — `heritage = heritage_byzantine` as a direct
comparison appears nowhere in the installed game; `has_cultural_pillar` is the real idiom), on the
in-fiction logic that a ruler who already reads Arabic or Greek has no need of a Latin translation.
**And "more learned rulers request it"** is a weighted-`random_list` change in the ROUTER event
(events/kehillah_task_contract_events.txt) — this contract type has only ever had one candidate
employer per pulse, so the lever available was making THAT candidate more likely to roll this
contract type specifically, not widening a pool.

ck3-tiger clean (0 fatal, 0 errors; one new warning, `strict-scopes: expects scope:story to be set`
on the new `create_artifact_book_effect` call, mirroring the identical pre-existing, already-accepted
warning on "Write a Book"'s own call to the same macro). Not yet live-tested.

**2026-09-17 update — the loan contract's direction was reversed back to the Kehillah as LENDER,
and both the loan and Hebrew tutor contracts got real challenge chains**, at the user's explicit
request ("Wait it should be that you loan money to them! Can we also set it up in a way that we
have an event chain with challenges to succeed? Same for the tutor in Hebrew even..."). See
`kehillah_loan_contract`'s own header (`common/task_contracts/kehillah_task_contracts.txt`) for the
full account.

**The reversal was not just a preference — it fixed a real, live bug.** The v8 build (2026-09-10,
above) had inverted the loan's direction so root/`task_contract_taker` (the Kehillah) was the
borrower and `scope:employer` was the lender. Tracing it end to end while making this change:
`kehillah_loan_debtors` (a `variable_list`) is only ever walked by the accrual/default block inside
`kehillah_quarterly_pillars_effect` (`common/scripted_effects/kehillah_scripted_effects.txt`,
~line 1867), which runs on `primary_title` and only ever fires via `kehillah_quarterly_pulse`
(`common/on_action/kehillah_on_actions.txt`), itself gated `government_has_flag =
government_is_kehillah`. Under the inverted design, `on_accepted` added the Kehillah to the
**employer's** (a non-Kehillah foreign ruler's) `kehillah_loan_debtors` list — since that character
never gets `kehillah_quarterly_pulse`, the list was never walked: `years_elapsed` never
incremented, loans never came due, and the quarterly default codepath was dead for every loan
originated through the contract since 2026-09-10. Restoring the original direction (the Kehillah
is the lender, `kehillah_loan_debtors` lives on the Kehillah's own title again) fixes this for
free — it is also what `kehillah_script_values.txt`'s own "THE LENDER IS THE TITLE" header note
(the succession-safety argument for storing the lender as a title, not a character) was written
for in the first place.

**The ledger itself is unchanged** — `kehillah_loan_amount_owed`/`kehillah_loan_lender_title`/
`kehillah_loan_years_elapsed` are still written with the exact same values, just onto the borrower
(now correctly `scope:employer`) instead of root. `kehillah_repay_loan_decision` and the quarterly
accrual/default block remain completely untouched, exactly as the original v8 constraint required
— both already operate on "whichever character holds the debt variable," so the reversal needed
zero edits to either.

**Both contracts now hand off to a real three-event challenge chain** instead of resolving inside
their own `on_accepted`, mirroring the translation contract's own v11 overhaul:
- `kehillah_loan_contract` → `events/kehillah_loan_events.txt`, namespace `kehillah_loan_challenge`
  (Assessing the Borrower → Negotiating Terms → Sealing the Loan). Resolves to SUCCESS or FAILURE
  only (two tiers, not three — a financial negotiation's one real stake is "does the loan happen at
  all"). On SUCCESS, the chain's final event runs the exact origination effect that used to live in
  `on_accepted`, relocated verbatim. On FAILURE, the deal falls through via `invalidate_contract =
  yes` (the same effect a declined offer already uses) — no gold changes hands, nothing is written
  to the ledger.
- `kehillah_hebrew_tutor_contract` → `events/kehillah_hebrew_tutor_events.txt`, namespace
  `kehillah_hebrew_tutor` (The First Lesson → Patient or Rigorous → The Pupil's Progress), the v11
  spec's own section 5 shape, written at the time but never built. `tutor_great`/`tutor_good`
  (`common/task_contracts/kehillah_task_contracts.txt`) keep their existing values verbatim — only
  a new `tutor_poor` failure tier was added (this contract previously had no failure state at all),
  mirroring `exotic_goods_poor`'s shape.

ck3-tiger clean (0 fatal, 0 errors) on every file touched or created. **Not yet live-tested** — a
future live-test session should confirm: the loan actually disburses to the employer on a SUCCESS
resolution, the Kehillah's own quarterly tick now correctly accrues and eventually
repays/defaults that loan (the bug this pass fixed), and the tutor chain's new `tutor_poor` tier
actually fires on a low tally.

**2026-09-08 update — the Bet Din takkanah mechanic has been redesigned, built, and live-tested,
superseding item 6 above.** Scoping conversation produced
[docs/spec/v5-bet-din-conference.md](docs/spec/v5-bet-din-conference.md); the same session built
and live-tested it: the 15-year single-ruling decision is now a travelled-to Conference activity
(this mod's first custom `activity_type`) convened every 3 years, drawing 3 hardcoded real-character
test cases, ruled on by the three community leaders via stat-tiered skill checks, with one test case
able to add a permanent tenet to the faith — **confirmed live**, a real `doctrine_polygamy` →
`doctrine_monogamy` change on rabbinism's faith. The live-test pass found and fixed a real bug
`ck3-tiger` cannot catch (an unguarded `global_var` read in a chained event block, spammed on every
tooltip-rebuild frame into a ~28MB/minute error-log storm), on top of two `ck3-tiger`-caught bugs
fixed pre-test. See spec sections 8-9 and
[docs/testing/2026-09-08-bet-din-conference-live-test-log.md](docs/testing/2026-09-08-bet-din-conference-live-test-log.md)
for the full record. **A same-day follow-up pass closed the one real gap that record initially
flagged**: the activity-hosting UI (F9, alongside Hunt/Pilgrimage/University Visit) was found, and
starting a real session confirmed the co-judges actually travel to Worms (~12 in-game days) before
the docket opens on its own — the full mechanic, not a console stand-in. See near-term TODO item 7.

**2026-09-11 update — v10 live-test fixes, the first REAL live-test session against the built mod
(everything above was console-driven verification or shorter test passes).** Seven issues, all
`ck3-tiger`-clean. See [docs/spec/v10-live-test-fixes.md](docs/spec/v10-live-test-fixes.md) for the
full spec, most of it already root-caused at triage time.
1. **Bet Din invited a Christian duke and unrelated courtiers.** `can_be_activity_guest`
   (common/activities/activity_types/kehillah_bet_din_conference.txt) had a purely-geographic OR
   branch (`kehillah_shares_minhag_region_trigger`, written for -- and only previously used on --
   a REGISTERED COMMUNITY's holder, not an arbitrary world character) with no religion/rulership
   check of its own. Fixed: `is_jewish_character_trigger` is now a top-level AND for every
   candidate, and the region-sharing branch additionally requires `is_ruler = yes` (confirmed real
   vanilla trigger). Confirmed the exact live symptom's mechanism too: `d_luxembourg` is tagged
   `western_ashkenaz` by `kehillah_tag_minhag_regions_effect`, so any Catholic Duke of Luxembourg
   passed the old check on geography alone.
2. **Speyer starts with zero Greatness.** Verified this was NOT an oversight as first triaged --
   history/characters/speyer_1066.txt and the effect's own header both deliberately chose zero,
   reflecting that Speyer's real Jewish community isn't documented until the 1070s/chartered 1084,
   after this scenario's 1066 start. The genuine gap was different: nobody connected "starts at
   literal 0" to Bet Din co-judge ranking (pure Greatness sort) once v7's minhag regions put Speyer
   in the same large western_ashkenaz pool as Mainz (180) and Troyes (140) -- making Speyer
   mathematically unable to ever win a co-judge seat at game start. Fixed with a starting Greatness
   of 150 (matching Worms, below Mainz's rabbinic-stature premium), not a full oversight-style
   backfill -- see `kehillah_setup_speyer_start_effect`'s own header for the corrected account.
   **A running save's already-set Speyer Greatness is NOT retroactively fixed by this** -- only new
   games get the new starting figure; a specific existing save would need its own one-time
   correction effect if wanted, not built here.
3. **Kehillah succession had no gender restriction at all**, only ranking. Verified the succession_
   appointment schema itself first (`_succession_appointment.info`): there is no candidate-
   disqualifying field, only `candidate_score` (ranks), `default_candidates` (categories),
   `allow_children`/`allow_same_tier_candidates` -- confirmed even vanilla's OWN strictest
   `male_only_law` (common/succession_appointment/admin_governor.txt) is a score-zeroing multiply,
   not a true pool exclusion, so the spec's hoped-for hard-exclusion field does not exist to find.
   Added the strongest real exclusion the schema supports -- a -100000 subtract, dwarfing every
   other term combined -- gated behind a new global variable, `kehillah_egalitarian_succession`
   (common/scripted_triggers/kehillah_scripted_triggers.txt's `kehillah_leadership_gender_eligible_
   trigger`), unset by default (male-only default), with nothing in this pass ever setting it --
   a documented hook for a future law/reform/decision, per explicit instruction not to build that
   unlock now.
4. **Rabbi trait/semicha had no gender gate either.** Found and gated all three real grant sites
   with the same flag: the Chief Rabbi court position's `valid_character` (common/court_positions/
   types/kehillah_officers.txt -- a REAL hard gate, unlike succession's score-only schema),
   `kehillah_bet_din_grant_rabbi_trait_effect`, and `kehillah_bet_din_semicha.0001`'s own trigger
   (events/kehillah_bet_din_semicha_events.txt) -- the semicha event no longer offers the choice to
   a female character under the default flag state, not just a silent no-op.
5. **Agunah's "missing" husband sat visibly in the player's own court.** The alive-branch (50%) of
   `kehillah_bet_din_pick_agunah_litigants_effect` (common/scripted_effects/kehillah_bet_din_
   scripted_effects.txt) really did nothing beyond `employer = root` at creation, exactly as its own
   old comment admitted. Fixed with a real relocation: `set_employer` (confirmed real, already used
   elsewhere in this mod) to a `random_independent_ruler` filtered on `NOT = { in_diplomatic_range =
   root }`, both confirmed real vanilla (game/common/scripted_effects/10_dlc_tgp_scripted_effects.txt's
   own homeless-families fallback-liege picker uses the identical any_/random_ + in_diplomatic_range
   shape), falling back to any other independent ruler if the game world is too small/early for a
   genuinely out-of-range one to exist. 50/50 dead/alive split unchanged.
6. **`scope:kbd_book_courtier` reportedly "can't resolve."** The SCRIPT side checked out completely
   correct: re-grepped every reference (all in events/kehillah_book_events.txt, nowhere else) and
   every one is already correctly guarded, and the two live theories about it (an optionally-set
   scope feeding a trigger-gated `right_portrait`, or the same feeding a trigger-gated option's own
   `name` text) both checked out safe against real, shipped vanilla code doing the identical thing
   (game/events/birth_events.txt's `scope:second_adult`, game/events/harm_events.txt's `scope:
   medic`). The REAL bug was in localization, and `ck3-tiger`'s own mandatory verification run
   caught it directly: `kehillah_l_english.yml` wrote `[scope:kbd_book_courtier.GetFirstName]` --
   invalid CK3 loc syntax (`scope:` is a script-side prefix; loc bracket links use the bare scope
   name, confirmed both against vanilla and against this mod's own correct usage everywhere else,
   e.g. `[kbd_litigant_a.GetFirstName]`). Fixed all 8 affected lines (4 on kehillah_book.0003, 4 more
   on kehillah_book.0007 with the identical mistake on `kehillah_book_author`) by removing the
   `scope:` prefix. A strong, mechanically-confirmed match for "can't resolve," though not live-
   verified against the original report -- still worth the user's own re-check, but now with an
   actual confirmed defect fixed rather than only a theory ruled out.
7. **Not a bug, just explained**: "why Rashi/Mainz, not Speyer" for co-judge slots was pure
   Greatness ranking meeting Speyer's structural zero (§2's root cause) -- no separate code change,
   §2's fix is the same fix.

A separate, deliberately unimplemented design pass for succession —
theocratic pool succession, an appoint-successor override, and a
resignation decision — is written up in
[docs/spec/v3-meritocratic-succession.md](docs/spec/v3-meritocratic-succession.md).
Its problem statement needs a correction pass (see the succession note
below) before anyone picks it back up: the holder_court_position fix
may have already closed some of the gap it was designed to solve.

Everything from Phase 2 onward remains unimplemented.

**CORRECTED 2026-09-07 — the paragraph below is wrong and kept only so
the correction is legible.** `holder_court_position` and
`holder_councilor` are real, shipped, working candidate categories —
vanilla's `common/succession_appointment/japanese_admin_governor.txt`
uses both. The original crash that produced the belief below came from
a typo (`invested_candidates` instead of `default_candidates`), not
from the category. `kehillah_leadership.txt` now includes both
categories for real, plus a `+25` score bonus for holding a community
office — see that file's own 2026-09-07 header note for the full
account. **This is not yet independently re-verified live**: the one
succession this session's live-testing actually watched (Isaac →
Mordechai, his son) is ambiguous evidence either way — Mordechai could
have won on family alone under the old broken pool, or won on genuine
merit under the fixed one, since family candidates are still eligible
and were never excluded, just no longer the *only* eligible ones. A
dedicated re-test (built a Shtadlan with a stronger score than the
likely heir, then trigger succession, confirm the Shtadlan wins) is on
the near-term TODO below before this gets marked resolved.
[docs/spec/v3-meritocratic-succession.md](docs/spec/v3-meritocratic-succession.md)'s
own §1 problem statement repeats the now-disproven claim and needs the
same correction.

~~**Meritocratic succession is still family-only**, unchanged by the
above. The plan had been for the three community officers to be
succession candidates via the `holder_court_position` category, but
that category is documented in the game files and not implemented.
Every other non-family candidate category is an administrative-
government construct that contributes nobody to a landless independent
community. So the headline promise below — "the player always continues
as the community's leader, regardless of bloodline" — is not yet true
in the way it reads. Three routes to fix it are laid out in section 2c
of the implementation doc; the cheapest is heir designation, which
vanilla already combines with appointment succession on
`acclamation_succession_law`.~~

**Review notes on the first iteration**, covering communal welfare,
personal versus communal wealth, player-directed succession and a
commentary activity, are captured in
[docs/iteration/v1-iteration-notes.md](docs/iteration/v1-iteration-notes.md)
(building flavour, its first section, was addressed by the 2026-09-06
rework above — see the note at the top of that section). Those are
unscheduled and deliberately not folded into the phases below until
they are chosen.

## Track A — Diaspora Communities

### Phase 1 — Kehillah Community Baseline (current focus; verified working live, content rework in progress)
The core non-landed government mechanic, with no historical/regional flavor
yet: currencies (Gold, the real vanilla Influence resource), meritocratic
**appointment** succession (the player always continues playing as the
community's leader, regardless of bloodline — see spec §5; **note the
current-state caveat above: this is family-only today**), a
Synagogue-quarter estate-building system (visible community growth, gates
the Chief Rabbi and Treasurer officer roles and four minor communal
positions; the Shtadlan is a person-driven role, not building-gated — see
spec §3c), a minimal internal decision set, one generic playable start.
Goal: prove the government type is fun and functional end-to-end before
spending art/writing budget on regional variants.
See [spec/v1-kehillah-community.md](docs/spec/v1-kehillah-community.md). The
concrete playable start is the Kehillah of Worms, 1066 — see
[docs/scenarios/worms-1066.md](docs/scenarios/worms-1066.md), using
vanilla's own `judaism_religion` (faith: `rabbinism`) and `heritage_israelite`
culture family (culture: `ashkenazi`) — no custom faith/culture build-out
needed, corrected from an earlier draft that assumed otherwise.

### Phase 2 — First Regional Overlay
Reskin/extend the baseline with one historically-anchored variant. Babylonia
(Exilarch/Geonim) is the leading candidate — most self-contained, clearest
historical throughline — but not yet finalized. Vanilla already has a
matching culture ready to use: `bavlim` (Babylonian Jews, part of the
`heritage_israelite` family) — confirmed while researching the Worms
scenario, see docs/scenarios/worms-1066.md §5.

### Phase 3 — Additional Regional Overlays
Ashkenaz (Synodic Council — no central executive, players vote on regional
decrees) and Sepharad/Islamicate (Negidim — influence via host-court
placement) once Phase 2 validates the overlay pattern. Vanilla's `sephardi`
culture is the matching ready-made asset for the latter (same source as
the Phase 2 note above).

**2026-10-30 — revision for the Negidim (design agreed, not built):** the
[Nagid spec](docs/spec/2026-10-30-the-nagid.md) replaces the Sepharad-only overlay with one
host-realm office:
- it is seated at the capital's community;
- it is founded only by a realm that favours its Jews beyond its faith's teaching;
- it is named by region;
- its rules bias it toward Muslim courts.

The Exilarch is a special case of the same office.

### Phase 4 — Host Dynamics
The host-realm relationship layer: Christian-sphere loop (usury, charters,
expulsion threat) vs. Islamic-sphere loop (trade posts, Dhimma pact, purge
threat). Deliberately deferred past the baseline — it's the largest,
riskiest system in the original design doc and depends on the community
mechanic already working.

**Started 2026-09-23, out of phase order, by explicit request.** A four-pass research spike
([docs/spec/spike-host-charter-interaction.md](docs/spec/spike-host-charter-interaction.md)) de-risked
the Host Charter piece specifically — reusing CK3's own tributary subject-contract system and its
engine-owned negotiation window rather than building a bespoke UI — and it was then implemented the
same day ([docs/spec/v15-host-charter.md](docs/spec/v15-host-charter.md)): every Kehillah now has a
real, permanent (by design — see that doc §1) contract relationship with its host, with two charter
terms (moneylending rights, walled-quarter rights). **This is the charter mechanism only.** The
expulsion threat, the Islamic-sphere loop (trade posts/Dhimma pact/purge threat), and any resistance
mechanic are all still entirely unbuilt and unscoped — v15's §4 lists exactly what was deliberately
left out and why. **Live-tested, two passes, same day** (v15 §5): automatic establishment, correct
UI render, exit-suppression, stability, and idempotency all confirmed; one real bug found (a `root`
scope mistake under `kehillah_on_game_start`'s iteration wrapper) and fixed, fix itself confirmed.
**Succession now live-tested too, both directions (v15 §5)**: the community leader's own death
(charter carried by vanilla's `tributary_heir_succession`) and the host's own death (charter
re-pointed with zero lag by vanilla's `suzerain_heir_succession`, confirmed at the raw engine level
before any mod code ran) both pass clean. One separate, pre-existing, non-fatal bug resurfaced during
that test (`change_government` "illegal government" on appointment succession, third time this exact
error has appeared across two different unverified diagnoses) — not caused by Host Charter, not
fixed, see `BLOCKERS.md` and the implementation doc's 2026-09-23 addition. Still not independently
tested: a newly founded community actually getting a charter, and the host-changes-by-conquest
backstop path specifically.

**2026-09-23/24 — Jewish Settlement Policy and Charter redesign underway, at explicit request.**
[V16](docs/spec/v16-jewish-settlement-policy-and-charters.md) defines a realm-wide, default-Allowed
Jewish Settlement Policy (Encouraged / Allowed / Discouraged / Banned) as the entitlement envelope
for a local Host Charter, rather than a duplicate pillar modifier. The first implementation slice
is now source-validated: new Christian/Muslim charters select distinct regional row groups; each
policy bounds and supplies their ordinary default offer; founding is disabled under Banned; and
only the *actual* charter flags feed the pillar breakdown. County development now contributes a
small, visible local-opportunity band to Prosperity and Stability, while the first bounded
Goldilocks-network cache runs only at initial registry/foundation time, not on the quarterly pulse. Existing V15
moneylending/walled-quarter contracts are deliberately retained; other host traditions use that
legacy group until research supplies their own rows. A policy becoming more restrictive never
silently revokes an existing charter — the map-ledger tooltip instead marks grandfathered rights
for review. Construction is now mechanically bound to the actual construction term: free terms
permit new Quarter institutions, permission terms require a paid five-year Host Construction
Permission, and forbidden terms block new institutions while leaving recognized upgrades alone.
The live default-selection/contract-window spike, construction-gate UI, save/reload, distance calibration,
and armed-watch MaA tests remain open and are recorded in V16 §8 and
`docs/testing/2026-09-24-v16-settlement-wiring-live-test-log.md`. Policy-change AI, warning
events, expulsion, migration, Indian-specific terms, and a destination-picker are intentionally
not being silently built by this slice.

**2026-09-25 — policy-change AI is now specified, not built.**
[V17](docs/spec/v17-settlement-politics-and-charter-revision.md) records the
decision that host politics must be event-led, visible, one-rung-at-a-time,
and followed by a separately negotiated charter response. Faith is legal
context, personality a bounded modifier, and economic/local conditions named
pressures; none is a universal hidden hostility score. Its first work is a
pulse/AI-initiation spike, not a silent AI policy writer. Banned remains
warning-only until migration and crisis counterplay exist.

**2026-09-25 — Norman Conquest founding event, and four new Sepharad/Bavel
communities, built same session, by direct request.**
[V18](docs/spec/v18-norman-conquest-and-new-communities.md). Two pieces:

1. **Retcon + event chain.** London/York/Lincoln/Norwich no longer exist as
   pre-authored 1066 game-start communities (removed from landed_titles,
   history/titles, history/characters, and their old start-effects/registry
   calls) — a deliberate, user-confirmed departure from four communities'
   worth of prior (v6/v7) design, chosen when asked directly how to resolve
   the conflict between "these four already exist at game start" and the
   user's new ask to have a Norman Conquest event found them. They are now
   founded dynamically, mid-game, once a running playthrough's own Norman
   Conquest actually resolves (`on_title_gain` on `title:k_england`, since
   vanilla has no scripted mechanic for this at all — checked directly).
   Three weighted branches (William 80%, Harald Hardrada 45%, anyone else
   30% chance to fire at all), each founding all four communities via the
   same `create_adventurer_title` mechanism Wave 5's own founding decision
   uses, and setting the host realm's V16 Jewish Settlement Policy to
   Encouraged before the fresh Host Charter is created. New leaders share a
   dynasty with an existing community's own named leader when William wins
   (Rashi of Troyes's own `dynn_Yitzhaki`) — the user's own explicit
   "personal connections... especially French communities if William wins"
   ask, realized as a real, in-game-verifiable shared house rather than only
   a flavor sentence.
2. **Four new baseline communities**, same authoring pattern as the
   existing fifteen, not a new government/overlay mechanic: Toledo,
   Córdoba, Granada (Southern Sepharad — already-tagged minhag region, no
   new geography work needed) and Baghdad (Bavel). Granada's leader is
   named directly: Joseph ibn Naghrilla, a real, extraordinarily
   well-documented vizier of the Taifa of Granada at this exact bookmark
   date — with the real December 1066 Granada massacre that killed him
   flagged honestly as unbuilt future content (see V18 §2 and the backlog
   entry below), the same restraint this mod already applies to York's
   1190 and Lincoln's 1255. A new dynasty, `dynn_Naghrilla`, was added for
   him (common/dynasties/ha_levi.txt).

ck3-tiger clean (0 fatal, 0 error) on every file touched or created.
**Not yet live-tested** — a future live-test session should confirm: the
founding chain actually fires and produces real playable/AI-run communities
at the correct English counties; the settlement-policy-then-charter
ordering actually yields an Encouraged-tier charter, not a default one; and
the new leaders' shared dynasty actually renders as kinship in a real game.
See V18 §3 for the full test list.

**2026-09-25 — historical starting pillars now equal their dynamic
baselines; awaiting live regression.** [V20](docs/spec/v20-starting-pillars-equal-baseline.md)
supersedes V19's fixed-reserve pass before it was live-tested. All fifteen
pre-authored 1066 communities are initialized, once, from the exact same
building/office/leader/urban/network/actual-charter values their quarterly
convergence uses. The snapshot waits until day three because V16's network
and deferred charter caches are not truthful earlier. The old direct
Prosperity/Greatness grants are removed; starting balance now has one source
of truth, so live feedback can tune contributors instead of arbitrary opening
bonuses. New founders remain a separate difficulty model and do not receive
this historical snapshot.

**2026-10-12 — BUILT, not live-tested: host arrest and exile
([V32](docs/spec/v32-host-arrest-and-exile.md)).** Daniel approved implementing it the same day,
with refusal meaning exile (leader steps down into an adventurer; a courtier becomes a wanderer).
It uses the scripted-crime + gate-override route rather than the custom "Arrest" interaction
sketched below. Needs the live pass in V32's "Live test" section, since a refusal runs the
step-down succession handoff. The original candidate note follows, kept for the record.

**2026-10-12 — candidate, not approved: host arrest of Kehillah members.** Raised by Daniel
while reviewing forced conversion (V27 2026-10-12 addendum). Today the host cannot imprison a
Kehillah leader or courtier at all: `cannot_be_vassal_or_liege` keeps the leader independent, and
the V15 tributary charter makes the host a suzerain, not a liege, which vanilla's
`basic_allowed_to_imprison_character_trigger` does not recognise. War capture is the only route.
Proposed shape, to be specced before building: a host-side "Arrest" interaction that calls
`imprison` directly, gated on the charter relationship and real grounds (charter breach,
royal-loan default, proselytizing a Christian under an Encouraged rite). The community answers by
ransoming from its treasury, appealing upward, or refusing ransom, after Meir of Rothenburg,
imprisoned by Rudolf of Habsburg in 1286. **Risk:** an imprisoned leader touches succession, the
mod's crash-prone subsystem (implementation doc sections 6 and 8), so this needs a live test,
not just a source check.

### Phase 5 — Crypto-Jewish Survival Loop
The secret-practice/detection/forced-conversion system for communities that
lose the Phase 4 expulsion/purge struggle. Depends on Phase 4 existing.

## Track B — Landed Realms
Playable bookmarks for Jewish-majority landed polities, using vanilla
government/succession/title systems with Judaism/Israelite (or regional)
culture and religion content. Picked up once Track A Phase 1 ships.

## Candidate future loops (backlog, unscheduled)

Ideas raised during design discussion, sorted by how cheaply they'd fit —
not yet assigned to a phase. Pull one into a phase's scope explicitly
before building it; nothing here is approved by default.

**Cheap, reinforces an existing v1 pillar (candidates to pull into Phase 1):**
- **The Granada massacre, December 1066.** Flagged 2026-09-25 (V18 spec) when
  Granada was added as a new community with Joseph ibn Naghrilla, the real
  historical vizier assassinated in the real massacre that followed barely
  three and a half months after this scenario's own 1066.9.15 start —
  an unusually strong, dated fit for a crisis chain, given how tightly it
  lines up with this mod's own bookmark date, the same way York's 1190 and
  Lincoln's 1255 are flagged without being built. Needs its own design pass
  on stakes, tone, and player agency (does the player-led case play
  differently from an AI-led one? what survives?) before anyone starts
  writing events — not a slot to fill in by default.
- **Yeshiva pipeline (Study).** Actively choosing tutors/mentors for
  promising children to raise their Learning — vanilla guardian/education
  assignment, reflavored. Makes meritocratic succession something you
  cultivate, not just a die roll at the death screen.
- **Tzedakah / charity meter (Steward).** A recurring decision spending
  Gold for Influence and family contentment. One decision, one modifier.
- **DONE, 2026-09-09 — Turn the Rabbi trait into a lifestyle trait.** Completed in two passes.
  **Pass 1** added three real, XP-driven tracks to `kehillah_rabbi_trait` — Parshanut (biblical
  exegesis), Talmudics (Talmudic argumentation), Halakha (legal ruling) — fed by Bet Din Conference
  case resolutions: Talmudics + Halakha on every case (any tier) a trait-holding judge sits on,
  Parshanut ("more rarely Tanakh") only on a GREAT-tier verdict specifically, reusing the existing
  tier check as the rarity gate rather than a second random roll. **Pass 2, same day, at further
  user request**, went further than pass 1's own text had assumed necessary:
  - **`category` changed from `fame` to `lifestyle`** after all — pass 1 kept it `fame` reasoning
    that changing it would cost the trait its exemption from the lifestyle-trait slot limit. Checked
    against vanilla before reversing that: `theologian` and `scholar` are both `category = lifestyle`
    and routinely coexist on the same character, so the category field alone does not enforce
    single-slot exclusivity — there was no real tradeoff being protected, so this is now a real
    lifestyle-category trait as originally asked.
  - **A third acquisition route**: sitting on a Bet Din Conference panel at all — host or either
    co-judge — now OFFERS the trait if not already held (`kehillah_bet_din_grant_rabbi_trait_effect`,
    called from `kehillah_bet_din_open_docket_effect`), on top of the original two (Chief Rabbi
    office, Isaac's history entry). "You become a rabbi when you go to a bet din as a judge," per
    the user's own framing — **not silently, per a same-day follow-up request**: it fires a real
    event, `kehillah_bet_din_semicha.0001` (events/kehillah_bet_din_semicha_events.txt), not an
    unprompted `add_trait`. One event, not two — its desc distinguishes the host's own version
    ("no one more senior in the room to grant it," self-recognition by the panel) from a
    co-judge's ("granted by the convening Av Beit Din," i.e. the host, by name) via a
    `triggered_desc` on whether root is the host. Accept becomes a rabbi; decline is not a dead
    end — the same NOT-already-holding-the-trait guard means it is offered again next session, not
    permanently refused.
  - **Each track extended from two thresholds to three (30/65/100 — 100 is the engine's own hard
    cap on trait XP, caught by ck3-tiger before this reached a live game)**, so the tally-based
    "Write a Book" chain below has masterwork/famed/illustrious to land on.
  Not done, and still a real gap from the original "perk-by-perk path" phrasing: no actual
  lifestyle-tree/perk-point *acquisition* path exists — a character still cannot spend lifestyle
  points to become a rabbi the way one commits to Diplomat or Scholar; the three routes above are
  still all script/event-granted, not a perk tree with an XP curve and lifestyle-selection UI.

  **PLANNED, 2026-09-25 — Rabbi ordination path.**
  [V21](docs/spec/v21-rabbi-ordination-paths.md) resolves the design question before code: a
  rabbinic-authority Jewish candidate studies through the existing Learn Torah scheme, records two
  distinct fields of study, then explicitly seeks semicha at a Beit Midrash. A four-year
  rabbinic-guardian apprenticeship can satisfy that curriculum at adulthood unless Learning is very
  low or the mentor-pupil relationship seriously fails. Learning 8 is the entry floor; Piety
  supports ceremony rather than becoming an opaque hard gate. It preserves history, Chief Rabbi
  appointment, and Bet Din recognition as institutional routes, reuses the current gender-law hook,
  and explicitly defers broad AI evaluation until a live spike. **No V21 code is built yet.**

- **DONE (fleshed out), 2026-09-09 — Write a Book.** The three flat, single-effect book decisions
  above were rebuilt, same day, into one real event chain at user request: `kehillah_write_book_
  decision` (common/decisions/kehillah_rabbi_book_decisions.txt) now just opens `kehillah_book.0001`
  (events/kehillah_book_events.txt), a 7-event chain —
  1. **choose a genre**: Halakha/responsa, Torah commentary (Parshanut), Talmud commentary
     (Talmudics) — each gated on the matching `kehillah_rabbi_trait` track at 30+, setting the
     tally's baseline from whichever threshold (30/65/100) is actually met — or **Hebrew poetry**,
     a fourth genre gated on vanilla's own `lifestyle_poet` trait instead, not tied to the rabbi
     trait at all;
  2. **choose an inspiration** (study alone / seek a colleague / draw on real experience) — two
     stat-gated, one flat/safe;
  3. **discuss it with a courtier** (`random_courtier`, weighted toward Learning) — a stat-gated
     debate option that also carries the chain's one genuine `random_list` roll (a real *chance*
     for a better tier, not just a deterministic stat check, per the user's own phrasing), a safer
     "just listen," or working alone;
  4. **revise or publish** — a Stress-for-quality tradeoff;
  5. **completion** (`kehillah_book_complete_effect`, common/scripted_effects/kehillah_book_
     effects.txt) — reads the final tally against two thresholds for the tier, then creates the
     artifact genre-specifically: two name variants per genre (random-picked; one built from
     `[owner.GetTitledFirstNamePossessiveNoTooltip]`, vanilla's own confirmed artifact-name
     scope-link syntax, one a real historical-style title — Novellae for Talmudics, Diwan for
     poetry, etc.) and two possible ownership modifiers per genre (common/modifiers/kehillah_book_
     modifiers.txt, random-picked, independent of tier — "an interesting range of possible
     boosts"), plus a flat-and-tier-scaling Greatness/Piety/Prestige reward bigger than any single
     Bet Din case's own — "a big contribution," per request;
  6. **sending copies**, which reads a NEW `kehillah_registered_communities` global_variable_list
     (populated at game start in common/on_action/kehillah_on_actions.txt with Worms/Speyer/Mainz)
     instead of naming the three communities directly — "register communities as a scope," per the
     user's own suggestion, deliberately built as general-purpose infrastructure, not a one-off for
     this feature;
  7. **arrival**, fired on every other registered community's own leader, naming the author by
     scope (saved before the scope switch into each recipient) and giving that leader a small
     Piety/Learning payoff for the gift.

  **Two honest, stated scope cuts, not silent ones**: (a) "nearest" communities are not actually
  distance-ranked — every other registered community gets notified, which is indistinguishable from
  "the nearest ones" while the registry only holds three communities, but will need real
  `ordered_in_global_list` distance-ranking once it grows past a handful; (b) the registry itself
  only ever gets populated at game start — nothing yet calls `add_to_global_variable_list` when a
  new Kehillah is founded, because nothing in this mod can found one yet (Wave 5, unbuilt). Whoever
  builds Wave 5 must remember to register there too. ck3-tiger-clean (one new, already-familiar
  false-positive `strict-scopes` warning on `create_artifact_book_effect` through an extra
  wrapper-effect layer, same class already accepted for `kehillah_compose_commentary_decision`);
  not live-tested.

**Blocked on a content draft, not engineering — pull in once the draft exists:**
- **Bet Din Conference, Part 2 (the case pool) — IN PROGRESS, 2026-09-09: case 4 of an eventual
  dozens/hundreds shipped.** This expands the halachic-case pool so a playthrough doesn't see
  repeats. **Case 4, "The Recalcitrant Husband,"** is built and ck3-tiger-clean (not yet
  live-tested): a wife petitions for a get, her husband (created with `callous`/`arbitrary`
  traits) refuses outright, and the panel picks one of three real institutional responses —
  cherem (the `excommunicated` trait, no forced divorce), coercion (`maimed` plus a forced
  `divorce` plus a huge `reverse_add_opinion` from him toward all three judges), or upholding his
  refusal (a Piety cost, still scored on the normal great/good/poor tally like every other case).
  Independent of case 2 ("The Agunah's Plea") — no shared state, can be drawn in the same session
  or neither. See kehillah_bet_din_recalcitrant_husband_resolution_effect (common/scripted_effects/
  kehillah_bet_din_scripted_effects.txt) for the full account.

  **2026-10-12 update:** Cases 10–13, covering a schoolroom, a slaughterer's knife,
  a Shabbat alley entrance, and a marked purse, are scripted after user approval.
  The pool is now thirteen; each conference still hears three. The new cases have
  case-specific sefer, trait, rabbinic-experience, co-judge and named-responsum
  choices, with visible direction and quality outcomes. Source checks and ck3-tiger
  have run; live rendering and letter-flow checks remain. See
  `docs/implementation/kehillah-bet-din-case-expansion.md` for the case matrix and
  the deliberate off-map inventory limit.

  **2026-10-18 update:** Case 14, **“The Goose on the Driftwood,”** adds the
  medieval barnacle-goose kashrut controversy at user request. A merchant seeks
  certification for unfamiliar northern geese that sailors claim grow from shells
  on timber; the court may permit them as fowl requiring shechita, forbid them, or
  keep them alive while examining witnesses and the birds. The source choice uses
  Mishnah Chullin 3:6 and Bavli Kodashim mastery. It deliberately names no later
  rabbi or responsum, so it can run in both 876 and 1066. The fiction preserves the
  legal puzzle without establishing spontaneous generation as game fact. The pool is now fourteen;
  source checks, ck3-tiger and a fresh CK3 1.20.1.1 load check pass. Live rendering and
  letter-flow verification remain pending; see the
  [load report](docs/testing/2026-10-18-barnacle-goose-case-load-check.md).

  **2026-10-12 balance addendum:** Cases 11 and 13 now draw a visible evidence fact
  before any letter is sent. It changes which argument is easier to defend and the
  direction's costs; case 12's continued alley use has a trade benefit. Cases 1 and
  8–13 now give litigants reactions based on the order and the quality of the
  reasoning. Source and ck3-tiger checks passed; live fact, tooltip and letter
  round-trip checks remain. See `docs/implementation/kehillah-bet-din-balance-pass.md`.

  **Drafted, not built: "The Returning Husband."** Raised by the user in the same conversation as
  case 4 — a genuine follow-on to case 2 this time, not independent: a husband case 2's DEAD
  branch declared gone returns after his widow has already remarried on the Bet Din's own
  approval. The user's own assessment stands: "that's a really hard one" — it needs case 2's
  outcome (which litigant, which branch, who she remarried) to persist across sessions, which
  nothing in the docket does yet (case 2's own scratch global_vars are cleared at session close).
  Whoever picks this up next needs a real design pass on what persists and for how long before
  writing events, not just a fourth case slot.

  Case 1-3 (dowry, agunah, second wife) were the Part 1 proof-of-concept; case 4 is the first case
  built without a "prove the mechanic" mandate attached, so it's also the first real test of
  whether the case-authoring pattern (litigant creation/picking effect + host/co-judge/resolution
  events + tally-tier Stability/Greatness + docket_draw_effect entry + activity-log loc) scales
  cleanly to new content. It did, on this one data point.

  **2026-09-15 update — cases 5 and 6 added, ck3-tiger-clean, not yet live-tested**, at explicit
  user request (case prompts supplied verbatim, not drafted here). Pool is now six cases; a session
  still hears three of them (`kehillah_bet_din_docket_case_count` is unchanged, per its own
  "documentation value, not a mechanical one" header).
  - **Case 5, "A Cursed Amulet."** A customer accuses a scribe (sofer) of selling him a curse
    disguised as a blessing — nonsense-Hebrew letters in a rhythmic repeating pattern the scribe
    himself can't fully explain, insisting only that he was "channeling the divine names." Three
    genuinely different methods, not three facings of one ruling: studying the text directly
    (Learning 16, the hard route), dismissing amulets' power outright (no check at all, an
    ALWAYS-fail tally penalty for sidestepping the actual question, plus `minor_stress_gain` for a
    ruling judge who personally holds `zealous`/`paranoid` and a real opinion hit — new modifier
    `kehillah_bet_din_dismissed_mysticism_opinion` — from every courtier holding either trait), or
    judging the scribe's own character (Learning 8, a much lower bar, verdict driven entirely by
    `num_sinful_traits`/`num_virtuous_traits`, real vanilla triggers checked against the character's
    own faith). THE KEY MECHANIC: a hidden ground truth is rolled once, at case start, and never
    shown to the player in any tooltip — "the true meaning can be either way" made literal. Only
    the text-study option ever reads it (success reveals it correctly; failure is a fresh, honest
    50/50 guess, not a disguised free answer). Guilty: Cherem (`add_trait = excommunicated`, same
    real mechanic case 4's own cherem branch uses) plus the amulet destroyed (flavor-only, a
    deliberate scope cut mirroring this mod's own established "no create_artifact precedent inside
    a task_contract_reward block" finding — see common/task_contracts/kehillah_task_contracts.txt).
    Innocent: the accuser is reprimanded (`minor_stress_gain`, deliberately much lighter than
    Cherem). Either way, every sitting judge gets a real memory of the case (this mod's first use
    of `create_character_memory` and its first entry in `common/character_memory_types/` —
    `kehillah_bet_din_amulet_case_memory_guilty`/`_innocent`, two fixed-text types picked at
    creation time rather than one type with a triggered description, since a memory's own
    description can be re-read by the UI long after `involved_activity` stops resolving to
    anything). Full account: `kehillah_bet_din_amulet_resolution_effect` (common/scripted_effects/
    kehillah_bet_din_scripted_effects.txt).
  - **Case 6, "The Silversmiths' Quarrel."** One Jewish silversmith's shop is smashed by a gentile
    mob; a rival silversmith is accused of putting them up to it. Three real, distinct Talmudic
    frameworks, not three emotional stances on one question: **Mesirah** (informing on/inciting
    gentiles against a fellow Jew — historically the community's gravest betrayal; Intrigue 14,
    proving actual intent is the hard part), **Gerama** (Bava Kamma's own direct-vs-indirect
    damage distinction — liable for damage caused through an intermediate agent, a real but lesser
    liability than direct damage; Learning 12), or **dismissal** (kin'at sofrim — ordinary trade
    rivalry alone isn't proof of incitement; Diplomacy 10, the skill here is holding the community
    together around an unresolved grievance). UNLIKE every case before it, the tally check's stat
    is NOT uniform across the three options — a deliberate departure from case 4's own uniform-
    Diplomacy precedent, documented as such in the event file's own header, because these three
    really do call on three different kinds of legal reasoning. Mesirah and Gerama both order
    restitution (a real character-to-character `add_gold` transfer, `medium_gold_value`, no
    dedicated "transfer gold" effect exists in the installed game so this is two calls, not one);
    Mesirah additionally adds Cherem on top. Dismissal leaves the accused untouched but costs the
    panel: the uncompensated accuser's opinion of the host (`kehillah_dispute_ruling_disfavor_
    opinion`, reused rather than a new modifier) plus `medium_piety_loss`, the same "ruling away
    from the injured party costs the panel's own standing" shape case 4's own direction 3 already
    established. Full account: `kehillah_bet_din_silversmiths_resolution_effect` (common/
    scripted_effects/kehillah_bet_din_scripted_effects.txt).

  **2026-09-15 follow-up — memories for cases 1-4/6, and a real Bet-Din-to-book payoff,
  ck3-tiger-clean (warning count actually DROPPED, 79 → 65, since the same pass retired
  `kehillah_compose_commentary_decision` below and took its own false-positive `strict-scopes`
  warning with it), not yet live-tested.** Five more memory types (`common/character_memory_types/
  kehillah_memory_types.txt`: `kehillah_bet_din_case1/2/3/4/6_memory` — case 3 declares no
  participants, having none) join case 5's existing guilty/innocent pair, all seven now gated the
  same way: created ONLY on a great- or good-tier verdict, never poor (retrofitted onto case 5's own
  resolution effect too), specifically so "holds one of these memories" reliably means "ruled well."
  That fact is what `kehillah_has_good_bet_din_memory_trigger` (common/scripted_triggers/
  kehillah_scripted_triggers.txt) reads, gating a genuinely new fourth option in `kehillah_book.0002`
  ("Write a Book"'s own inspiration step) — per explicit user request, "draw on a bet din memory of a
  good ruling to improve the quality of your book, particularly for Talmudics and Halakha works."
  Visible only for those two genres, no stat gate and cannot fail (unlike the two existing stat-gated
  options), and pays more than either's own pass value (`kehillah_book_bet_din_memory_gain = 16` vs.
  `kehillah_book_inspiration_gain = 12`) — recalling something that actually happened outranks a
  favorable roll on generic inspiration.

  **`kehillah_compose_commentary_decision` is RETIRED**, same pass, same explicit request ("remove
  the compose commentary skeleton decision while we're at it") — the older, flatter one-click
  "compose a scholarly work" mechanic, superseded now that "Write a Book" is the fully fleshed-out
  version of the same idea (see that decision's own retirement note, `common/decisions/
  kehillah_decisions.txt`, for the full account and the loc/script-value cleanup that came with it).
  `kehillah_write_book_decision` is now this mod's only such decision.

  **2026-09-15, open panel — WHO CAN CONVENE and THE PANEL both loosened,
  ck3-tiger-clean (0 fatal, 0 error), not yet live-tested.** Two separate
  passes, same day, same underlying goal ("frontier communities can still
  call batei din"):
  - **WHO CAN CONVENE**: the Greatness-leadership gate (only the region's
    currently-greatest community could host) is REMOVED — any member of a
    known minhag region may now convene (`activity_kehillah_bet_din_
    conference`'s own `is_shown`, common/activities/activity_types/
    kehillah_bet_din_conference.txt).
  - **THE PANEL**, at explicit user request ("the two co-judges don't need
    to be other community leaders -- they could also be courtiers or
    adventurers, but nearby community leaders are favored"): the co-judge
    `select_character` blocks now rank a merged pool of THREE candidate
    sources — other same-region community leaders (favored, scored
    1,000,000 + Greatness so they always win when available), the host's
    own high-Learning Jewish courtiers, and qualifying independent Jewish
    rulers (landless adventurers or high Learning, the same population
    `kehillah_bet_din_invite_rule_jewish_scholars/_adventurers` already
    draws the open-invite pool from) — instead of requiring three total
    region member communities. `kehillah_region_can_field_bet_din_panel_
    trigger` (common/scripted_triggers/kehillah_scripted_triggers.txt) was
    rewritten to sum these same three pools via a new script value,
    `kehillah_bet_din_available_co_judges_value` (common/script_values/
    kehillah_script_values.txt), so a lone or paired frontier outpost with
    a learned court can now field a panel that a bare regional headcount
    used to refuse outright. Also fixed in the same pass: two broken
    `[GetPlayer.GetPrimaryTitle.GetDeJureLiege...]` loc chains (`activity_
    kehillah_bet_din_conference_host_desc`/`_guest_help_text`) left over
    from the v6-era de jure duchy design and resolving to a blank/"None"
    name ever since the v7 pass flattened every Kehillah county title —
    reported live by the user ("resolving to 'Bet Din of None of'").

  **2026-09-15, both co-judge slots resolving to the same character —
  THREE attempts, first two both disproven live, before landing on the
  actual fix.** First reported playing Prague (Eastern Ashkenaz, exactly
  two member communities — the frontier case THE PANEL above exists for).
  1. First fix attempt: judge_2's own pool build excluded judge_1's pick
     via `scope:kehillah_bet_din_co_judge_1`, which the vanilla schema doc
     claims should be visible across special_guests slots. **Reported
     STILL broken on a second playtest, as Worms** (Western Ashkenaz, SIX
     member communities — ruling out "pool too small" as the cause).
  2. Second fix attempt: replaced the scope reference with a self-
     expiring character variable (`kehillah_bet_din_co_judge_reserved`)
     judge_1 set on its own pick, checked via `has_variable` instead.
     **Also reported broken**, same Worms retest.
  3. **Actual fix**: both exclusion mechanisms most likely failed for the
     same underlying reason — `select_character`'s own effects are almost
     certainly run by the activity-planning UI as repeated live preview
     computation, not committed once, so nothing written by judge_1's own
     evaluation (a scope OR a variable) can be trusted to still be there
     when judge_2's separate evaluation runs. Removed exclusion logic
     entirely: both slots now build the identical three-pool list with NO
     side effects and no cross-slot reads, differing only in `position = 0`
     vs `position = 1` of that same deterministic ranking — the exact
     mechanism this file's original 2026-09-08 single-pool build already
     proved live ("position = 0 for judge_1, position = 1 for judge_2...
     not a second independent search that could collide with judge_1's
     own pick"), now just ranking a 3-pool merge instead of 1 pool.
     ck3-tiger-clean (0 fatal, 0 error), not yet re-tested live -- if this
     one is ALSO wrong, the deterministic-tie-order assumption the
     original build rested on is the next thing to question, not a fourth
     exclusion mechanism.

  **2026-09-15, AI hosting frequency raised, at user request ("increase
  the likelihood of AI deciding to host a Bet Din").** `ai_will_do` was
  already at its ceiling (100, "given selected, always follows through"),
  so the only remaining script-side lever was `ai_check_interval` -- how
  often an eligible character even re-evaluates hosting at all -- lowered
  24 -> 6 months, matching Coronation's own vanilla value (game/common/
  activities/activity_types/coronation.txt) for a comparably significant,
  occasional-not-routine activity. Also removed a stale comment claiming
  eligibility was still "the current Greatness leader among the three
  Sh'um communities... a narrow, infrequent window" -- long superseded by
  both the v6/v7 generalization to all regions and the same day's own
  Greatness-leadership-gate removal above, so real competing-activity
  pressure is now higher than that comment assumed, not lower.
  Separately: confirmed against the installed game (grepped common/ and
  events/ for start_activity/create_activity and any activity-cooldown
  effect, found neither) that CK3 has NO scripted way to force-start an
  activity for a character at all -- hosting can only come from the
  player's own planner UI or the AI's autonomous decision loop, so there
  is no debug event this mod could add to literally force an AI to host
  one. To inspect the co-judge/guest experience directly, host as the
  player (now broadly eligible after THE PANEL above) and use the
  console's `play <id>` to switch into a picked guest once the activity
  starts, rather than waiting on or forcing AI. ck3-tiger-clean.

  **2026-09-17, co-judges are now real declinable invites, not a
  compelled pick -- THE PANEL rebuilt a fourth time, replacing
  special_guests outright.** Follow-up to the two live-tested duplicate-
  pick failures above: asked "is there a way to not force the co-judges
  to come? Should it be an invite? Would that require a total
  restructure?" -- answered with an audit (~84 direct `judge2`/`judge3`
  references across the case-resolution content, many gating which
  narrative branch is even available, not just decoration) showing a
  declinable *special_guest* would need auditing most of that by hand.
  Then asked "how about the two people who accept with the highest score
  become the co-judges? ... cap the number of people who can accept" --
  which sidesteps that audit entirely, and is what got built:
  - **special_guests kehillah_bet_din_co_judge_1/2 removed outright.**
    Every population that used to feed their select_character pools (same-
    region community leaders, the host's own high-Learning courtiers,
    qualifying independent Jewish rulers/adventurers) is now open-invite
    instead, via two NEW guest_invite_rules (`kehillah_bet_din_invite_
    rule_jewish_regional_leaders`/`_courtiers`, common/activities/
    guest_invite_rules/kehillah_bet_din_invite_rules.txt) alongside the
    existing `_scholars`/`_adventurers`. `can_be_activity_guest` and the
    old select_character pools' hand-duplicated eligibility logic are
    both replaced by one shared trigger, `kehillah_bet_din_eligible_
    judge_trigger` (common/scripted_triggers/kehillah_scripted_
    triggers.txt) -- three formerly-independent copies of "who could be a
    co-judge" collapsed into one.
  - **`kehillah_bet_din_open_docket_effect`** (common/scripted_effects/
    kehillah_bet_din_scripted_effects.txt) now decides judge2/judge3 by
    ranking real `ordered_attending_character` (confirmed real vanilla
    iterator, coronation.txt's own precedent) via `kehillah_bet_din_
    judge_score_value` (common/script_values/kehillah_script_values.txt)
    -- region-sharing leaders scored far above courtiers/adventurers, so
    the FAVORED property survives, computed from settled attendance
    instead of a pre-committed pick. This is also what makes it immune to
    the class of bug that broke special_guests twice: nothing here reads
    another slot's still-pending decision.
  - **QUORUM**: if fewer than two eligible people actually show up,
    `invalidate_activity` cancels the whole session rather than let the
    docket run short-handed -- the one guard that lets the ~84 case-
    content references stay completely untouched, keeping the promise
    "the docket only ever runs with a full panel" true by construction
    instead of by audit. Halachically apt besides: a court that can't
    muster three is not a valid Beit Din.
  - **`max_guests` 5 -> 6**, `reserved_guest_slots` removed (nothing left
    to reserve room for) -- the literal answer to "cap the number of
    people who can accept."
  - Discovered along the way: script VALUES do not support
    `save_scope_as` (ck3-tiger: "unknown token") -- unlike TRIGGERS,
    which do support $PARAM$ substitution (this mod's own established,
    confirmed-safe pattern) and do NOT need scope-saving at all when the
    parameter is just `root`, since root is fixed to a script's original
    invocation scope and is unaffected by nested scope-shift blocks.
    kehillah_bet_din_eligible_judge_trigger takes a real
    $HOST$ parameter for this reason; kehillah_bet_din_judge_score_value
    (a value, not a trigger) reads scope:host directly instead, since its
    one real caller already provides it natively.
  ck3-tiger-clean (0 fatal, 0 error, same 63-warning baseline), not yet
  live-tested.

**Needs more than one Kehillah on the map, or a regional anchor to travel
to — natural Phase 2/3 content, not v1:**
- **Inter-communal correspondence/responsa network.** Sister communities
  in other cities exchange letters, aid, and rulings (historically this is
  what the Cairo Geniza actually preserves). Arguably the truest expression
  of "diaspora as differentiator," but only means something once multiple
  Kehillot exist to talk to.
- **Craft/guild specialization per family.** Different notable families
  specialize (goldsmith, physician, textile trade) — variety pass on top
  of the Prosper pillar's baseline economy.
- **A second starting scenario: Kehillah of Troyes, c. 1070+, led by
  Rashi.** Checked and ruled out for the Worms 1066 scenario specifically
  — he'd returned to Troyes by 1065 and hadn't founded his own yeshiva
  yet (1067–1070) — but he's a strong real candidate for his own scenario
  once this mod supports more than one starting Kehillah. See
  docs/scenarios/worms-1066.md's backlog note for the sourcing.
- **Pilgrimage**, reusing the vanilla Pilgrimage activity — travel to
  Jerusalem or a great yeshiva for Learning/Influence/artifacts. Lands
  better once Phase 2's academies exist as real destinations.

  **2026-09-15 — "Learn Torah" v1 SHIPPED, ck3-tiger-clean, not yet live-tested.** Raised as a
  design sketch, spiked ([docs/spec/spike-book-inventory.md](docs/spec/spike-book-inventory.md)),
  confirmed by the user as the general umbrella all three rabbi tracks study through, then built
  the same day — the "first version" of the spike's own recommended lighter path, per explicit
  user request.

  **The track split this depends on shipped in the same pass**: `kehillah_rabbi_trait` (common/
  traits/kehillah_traits.txt) is now parshanut/talmudics/hashkafa, not parshanut/talmudics/halakha
  — Halakha is RETIRED as a separate track and merged into Talmudics (every place that granted both
  at once, chiefly the Bet Din docket's own per-case XP grant, now grants talmudics alone, at the
  SUM of the two old amounts, so total payout is unchanged), and Hashkafa takes its vacated slot,
  with its own distinct track bonus (`opinion_of_different_faith`, a real vanilla field, not
  invented) reflecting worldview broadened by engaging outside wisdom rather than more of either
  surviving track's own flavor. "Write a Book" (`events/kehillah_book_events.txt`) follows the same
  rename — its old Halakha genre is now Hashkafa, re-flavored (philosophy/mysticism artifact
  descriptions and modifiers, not legal-authority ones) rather than just relabeled. Also deleted in
  this pass: `common/scripted_effects/kehillah_rabbi_book_effects.txt`, found to be dead code from
  before "Write a Book" was unified into one chain — defined, never called anywhere.

  **The community library is real, per the spike's own recommended shape**: a `variable_list`,
  `kehillah_library_works`, on each community's primary title (not a character, not a real
  artifact) — six new triggers (`kehillah_owns_/missing_<track>_work_trigger`, common/scripted_
  triggers/kehillah_scripted_triggers.txt) read it. Twelve real works, four per track (Targum
  Onkelos/Mekhilta/Genesis Rabbah/Pirkei De-Rabbi Eliezer for Parshanut; the Mishnah/Jerusalem
  Talmud/Babylonian Talmud/Halakhot Gedolot for Talmudics; Sefer Yetzirah/Saadia Gaon's Emunot
  ve-Deot/Bahya ibn Paquda's Chovot HaLevavot/Yehuda Halevi's Kuzari for Hashkafa) — the same
  curated-real-corpus idiom the Translation Contract already established. Every community starts
  owning exactly two (Targum Onkelos, the Mishnah — `kehillah_seed_starting_library_effect`, common/
  scripted_effects/kehillah_library_effects.txt, called once per registered community from
  `kehillah_on_game_start`); Hashkafa starts with nothing at all, and everything else across all
  three tracks must be studied for or acquired, per the user's own "gated on actually having books"
  request.

  **Two flat decisions** (`common/decisions/kehillah_learn_torah_decisions.txt`, events in
  `events/kehillah_learn_torah_events.txt`) — deliberately ONE decision opening ONE event each,
  not a multi-step chain, the same shape "Write a Book" itself started as before it grew into one:
  - `kehillah_learn_torah_decision` — study a track the community's library already owns a work
    for (gated on `has_trait = kehillah_rabbi_trait`, matching "Write a Book"'s own gate exactly,
    not a looser learning-only alternative); a Learning check picks pass/fail XP into that track,
    naming which of the track's owned works was actually studied.
  - `kehillah_acquire_torah_work_decision` — commission a copy of a work not yet owned, for gold,
    gated on the Sofer's Workshop's own `kehillah_has_scriptorium` parameter (tier 2) — exactly the
    building the spike found already carrying the right pre-existing flavor comment ("texts copied
    here circulate to other communities") for this, unused until now.

  **Deliberately NOT in v1, per the spike's own tiering and explicit scope discipline**: no
  per-work choice in the Acquire decision (it picks a random missing work within whichever track you
  choose, not the exact title); no Sefer Torah requirement (a separate, easy, low-risk piece the
  spike explicitly scoped itself away from); no real spawned book artifacts (the spike's own
  "cheaper than expected" full-artifact path, `artifact_succession_title`, remains a real upgrade
  option, not built here). Destination-travel (below) and already-studied tracking (below) were
  both v1 gaps too, and both shipped the same day at user follow-up request.

  **2026-09-15 follow-up — travel to study elsewhere, and already-studied tracking, both SHIPPED,
  ck3-tiger-clean, not yet live-tested.**
  - **`kehillah_visit_library_interaction`** (common/character_interactions/kehillah_character_
    interactions.txt) is the destination-travel half the spike flagged as separately provable —
    proved the SAME way, but lighter than expected: not the Bet Din Conference's own full
    activity_type machinery (host, guest list, phases), but `start_travel_plan` directly, the real
    vanilla effect `common/scripted_effects/00_task_contract_scripted_effects.txt`'s own
    `governor_contract_travel_or_progress_effect` already demonstrates ("if not already there,
    travel with `on_arrival_event`; else fire it directly"), reused verbatim. Reuses `kehillah_view_
    communities_interaction`'s own already-verified target-search mechanism (same file) to pick a
    destination community, filtered to ones whose library actually holds something. Which community
    is stored as a character variable holding a TITLE, not a saved scope — travel can take real
    in-game time, well past this mod's own proven same-session scope-persistence guarantees — and
    the CURRENT holder is read at arrival, so a succession at the destination mid-journey doesn't
    break anything. The return trip is a second, explicit `start_travel_plan` issued once study
    resolves (`events/kehillah_learn_torah_journey_events.txt`), not a `return_trip` field — that
    field's real semantics could not be confirmed from any installed file (every citation found only
    ever used `return_trip = no`), so this mod does not lean on an unconfirmed default.
  - **The three `kehillah_study_<track>_effect` (common/scripted_effects/kehillah_library_
    effects.txt) are now SHARED** between local study (`kehillah_learn_torah.0001`) and travelled
    study (`kehillah_learn_torah_journey.0001`), parameterized on `$LIBRARY$` (which title's
    collection to read from) — the same parameterized-scripted-effect/trigger idiom this mod's own
    `kehillah_pillar_at_least_trigger` already established, now also applied to the six `kehillah_
    owns_/missing_<track>_work_trigger` entries so both contexts share one trigger family too.
  - **Already-studied tracking**, per explicit user request ("keep track of which books you've
    already studied... a much smaller boost"): `kehillah_studied_works`, a character (not
    community) `variable_list` — what a scholar has personally read doesn't reset when they travel
    or when their own community's shelves change. A repeat pays `kehillah_learn_torah_xp_repeat_
    pass/_fail` (5/2) instead of `kehillah_learn_torah_xp_pass/_fail` (15/5) — roughly a third,
    "a much smaller boost," never zero. Detected per-work inside each track effect's own random_list
    (a literal `is_target_in_variable_list` check per entry, not `target = var:X` with a variable —
    that specific form was checked against the installed game and not found anywhere, so it was not
    risked), signalled to the shared pass/fail block via a plain number variable, not a second flag
    comparison.

  **2026-09-15 follow-up #2 — candidate scoring by unstudied books, SHIPPED that day, then SUPERSEDED
  the SAME day by follow-up #3 below** when the interaction it scored was itself retired. Kept here,
  struck through in spirit rather than deleted, for the record: it scored `kehillah_visit_library_
  interaction`'s own target-search list on unstudied-work counts per track via three transient
  character variables read by both `ai_accept`'s modifiers and their own `.MakeScope.Var(...)` display
  text. The interaction this scoring lived on no longer exists; see follow-up #3 for what replaced
  both the interaction and this scoring mechanism together.

  **2026-09-17 library book levels** what if we gave books in Kehillah libraries levels. Before studying a level 3 book of parshanut, you need to study a level 2 book of parshanut, and so on. This would represent complexity of a text. We should also have inventory management. I think the level of your bet midrash should affect how many books you can have. And how many books you have, modified by their level, affects your greatness and the attractiveness of your kehillah to other scholars who want to study in a yeshiva to level up their rabbinics skills. Studying higher level books should give more xp, and maybe once you max out a track it gives you another benefit--like a temporary skill boost.

  **2026-09-15 follow-up #3 — the journey rebuilt as a real activity_type, ck3-tiger-clean, not yet
  live-tested**, at explicit user request: "the interaction is awkward. Maybe we should make it
  another activity like bet din? But with more targets than just your home community" — and
  separately, "studying should happen when you reach the target court, not when you return home"
  (which, per `kehillah_visit_library_interaction`'s own retirement note, was already true of the
  interaction's own `on_arrival_event` — not a bug this rebuild fixed so much as a property the
  activity delivers more directly, `on_phase_active` only ever firing once the host has arrived).
  - **`activity_kehillah_learn_torah_journey`** (common/activities/activity_types/kehillah_learn_
    torah_journey.txt) replaces the interaction outright — retired the same pattern this mod already
    uses for a retired decision (full account in the interaction's own retirement note, common/
    character_interactions/kehillah_character_interactions.txt). HOST = the traveller, solo
    (`open_invite = no`), unlike Bet Din Conference where the host stays home and guests travel to
    them — the one structural way this activity could not reuse Bet Din's own shape, and the reason
    HOST travel specifically (not just guest travel) needs to work, this build's one real, explicitly
    flagged unverified assumption (this mod's own confirmed-live travel evidence to date is for
    guests travelling to a host, not a host travelling to a self-picked destination — the general
    mechanism is standard CK3 activity behavior, not invented for this file, but not independently
    live-tested here for this specific direction).
  - **`province_filter = all`**, deliberately, despite the schema's own warning against it — none of
    `_activity_type.info`'s other named filters (capital/domain/realm/holy_sites*/domicile*/
    landed_title/geographical_region) can express "wherever any of sixteen scattered, independently-
    ruled communities happens to be," which is this mod's own actual map shape now that the old
    `d_kehillah_<region>` duchies are gone. `is_location_valid` narrows the real candidate set back
    to the registry immediately, bounding the practical cost the same way `kehillah_bet_din_invite_
    rule_jewish_scholars/_adventurers` already accepted for iterating `every_independent_ruler`. The
    AI never pays this cost at all: `ai_province_filter = capital` plus `ai_will_do = 0`, two
    independent reasons the AI can never host this, not one.
  - **`province_score`** now does what the retired interaction's own `ai_accept` modifiers used to —
    ranks candidates by unstudied-work count — but CANNOT reproduce their literal per-track
    breakdown tooltip: confirmed, from a real shipped vanilla example (`hunt.txt`'s own
    `province_score`), to be a plain script value with no `modifier`/`desc` fields anywhere in that
    system, unlike `ai_accept`. A second candidate route (stacking informational `custom_tooltip`
    lines onto `is_location_valid`) was considered and deliberately not taken either — confirmed
    real usage of that pattern is specifically for explaining validity FAILURES
    (`can_start_showing_failures_only`'s own naming), not a general always-on breakdown surface, and
    this file does not guess that it also does the latter. Real, flagged gap, not solved on a guess:
    the exact per-track count now only shows once you have already arrived (each of kehillah_learn_
    torah_journey.0001's own three options still names the specific work found there).
  - **`kehillah_learn_torah_journey.0001`** (events/kehillah_learn_torah_journey_events.txt) no
    longer needs ANY persisted destination variable — the interaction's old `kehillah_journey_
    destination_title` character variable existed only because travel could cross this mod's own
    proven same-session scope-persistence window; firing from `on_phase_active` instead means root
    is already physically at the destination (`root.location`) by the time this event's own
    `immediate` runs, so the destination is looked up fresh, in the same effect chain, every time —
    which registered community's own domicile occupies `root.location`, right now. The "after" block
    is now just `progress_activity_phase_after` (matching `kehillah_bet_din_advance_docket_effect`'s
    own precedent) — the engine's own activity-completion machinery is trusted for the actual trip
    home, not a second hand-built `start_travel_plan` the way the retired interaction needed.

**2026-09-19 — Learn Torah rebuilt as a continuous scheme, `kehillah_study_torah`, ck3-tiger-clean,
not yet live-tested.** At user request, following a discussion of whether Learn Torah (until now a
flat, one-shot decision) should instead work the way base-game "continuous background activity"
mechanics do — the user specifically flagged vanilla's own `learn_language` scheme, and the "By God
Alone" expansion's forthcoming (announced, not yet released) Study Scripture scheme for ecclesiastic
Christian characters, as the closest parallels.

**Self-targeted schemes are real, confirmed vanilla precedent, not a guess** — `study_confucian_
classics` (`common/schemes/scheme_types/tgp_study_scheme.txt`, Tours & Tournaments) is a
`target_type = character` scheme whose own `valid = { scope:target = scope:owner }` makes it a
character's scheme against themselves, and its `on_phase_completed`/`on_monthly`/`on_invalidated`
hook set (progress loops via `reset_scheme_progress = yes` rather than ending) is what `kehillah_
study_torah` (`common/schemes/scheme_types/kehillah_study_torah_scheme.txt`) copies. `kehillah_
learn_torah_decision` now only starts it (`start_scheme` + picking the first work), instead of
resolving a study session itself; `kehillah_acquire_torah_work_decision` and the whole travel-journey
activity (`kehillah_learn_torah_journey`) are UNCHANGED — commissioning a copy has no "continuous"
framing to convert to, and the journey was explicitly out of scope.

**The actual pass/fail and reward logic was deliberately NOT rebuilt** — `kehillah_study_specific_
work_effect` (common/scripted_effects/kehillah_library_effects.txt, unchanged since 2026-09-17 and
still shared with the travel journey) still owns it (a plain `learning >= 10` gate, repeat-vs-first
tiering via `kehillah_studied_works`). Routing the scheme's own probabilistic `scheme_success_chance`
into that gate instead was considered and rejected specifically because the effect is SHARED with
the untouched journey — changing it would have silently changed journey behavior too, not just the
scheme's. `base_success_chance` exists on the scheme purely because every scheme type requires one
(it feeds the UI's own odds display); nothing branches on it.

**Continuing indefinitely once out of unstudied books, with a clearly smaller reward** — explicit user
request ("you should be able to continue the scheme even when out of books, but it should be very
clear that the rewards are now much less"). Needed no new mechanism at all: the pick-next-work step
now draws from every work the library owns, not just unstudied ones, and `kehillah_study_specific_
work_effect`'s own repeat-vs-first tiering (built 2026-09-15, "a much smaller boost, not zero") was
already exactly this. The only real change is surfacing it clearly — the same `kehillah_study_torah.
<track>.<work>_tt` "You take up X" line used since 2026-09-15 now fires at PICK time (naming what's
about to be reread), where before it only fired as an after-the-fact reveal.

**The numeric-ID bridge, and why it's twelve if/elif branches, not a generic lookup** — a scheme
phase and its own `on_phase_completed` are two different script moments, months apart, with no
"phase started" hook to pair with it, so "which work is currently being read" has to be decided once
(at pick time) and read back later (at resolve time). Storing an arbitrary flag reference in a
variable and comparing against it later was already investigated and explicitly rejected once
before, in `kehillah_study_specific_work_effect`'s own 2026-09-17 header ("checked against the
installed game and NOT found anywhere as real precedent"). Rather than re-risking that, `kehillah_
study_current_work_id` is a plain NUMBER (1-12, one literal work per number by fixed convention),
read back via if/elif-per-literal (an effect: `kehillah_study_torah_resolve_current_work_effect`) or
OR-of-AND-per-literal (a trigger: `kehillah_study_torah_current_work_still_owned_trigger`) — more
lines than a generic lookup, but the confirmed-safe shape already used everywhere else in this file
family, not an invented one.

**No cached list, by design — the library query is live, at every pick.** `kehillah_study_torah_
pick_next_work_effect` queries the community's CURRENT `kehillah_library_works` every time it runs
(scheme start, every phase completion, and whenever `on_monthly` detects the current book is gone) —
never a snapshot taken once and reused. This means "detect new books" needs no extra code at all
(the very next pick already sees them); "detect a book donated away mid-read" (relevant now that the
library panel's own donate-for-piety action exists) is the one case that genuinely needed an active
check, so `kehillah_study_torah_monthly_effect` runs `kehillah_study_torah_current_work_still_owned_
trigger` every month and, on a miss, toasts the player and re-picks immediately — `scheme_progress`
itself is left untouched, since it represents time spent at the Beit Midrash, not attachment to one
specific volume.

**Flavor events, not mechanical ones, for the "insight mid-study" ask.** `kehillah_study_torah.0002`
(events/kehillah_study_torah_events.txt) fires from `on_monthly` at a flat 12%/month chance while the
current work is still owned, with a twelve-way `triggered_desc` naming which work the insight is
about — pure flavor, no reward, specifically so it never double-pays what `kehillah_study_torah.0001`
(the real phase-completion resolve+pick event) already pays.

**2026-09-19, same-day follow-up — Learn Torah opened up beyond Kehillah leaders, ck3-tiger-clean,
not yet live-tested.** At user request: "make this available to non-Kehilla ruler Jews too... Jewish
unlanded adventurers can use the books of the kehilla where their domicile is based... Jewish rulers
can use the library of the kehilla in their capital." Three populations now covered, via a new
`kehillah_study_torah_has_accessible_library_trigger` (common/scripted_triggers/kehillah_scripted_
triggers.txt) and matching `kehillah_study_torah_resolve_library_effect` (common/scripted_effects/
kehillah_library_effects.txt): a Kehillah leader's own community (unchanged); a landed Jewish ruler
who is not a Kehillah, via the registered community whose domicile sits in their own capital county;
a landless Jewish adventurer, via the registered community whose domicile sits at their own CURRENT
location instead of a domicile.

**Landless adventurers do not have a domicile at all in vanilla** — checked directly against the
installed game before building on the premise: `estate`/`yurt` (common/domiciles/types/00_domicile_
types.txt) and this mod's own Kehillah domicile type are all gated on holding a noble-family or
landed title, never on `landless_adventurer_government`. Using their current location instead
(the same anchor `kehillah_learn_torah_journey.0001` already uses for an arriving traveller) reads
better anyway for a wandering adventurer, at the cost of the library re-resolving if they wander away
mid-scheme rather than staying fixed for the whole run — which, per the point below, it already does
for everyone, not just adventurers.

**A real scope bug, caught by ck3-tiger, not by inspection.** The first draft of both new
triggers/effects used bare `root` for "the studying character" inside `holder = { domicile.
domicile_location = root.capital_province }`-style checks. That is exactly the confirmed-safe idiom
`kehillah_bet_din_available_co_judges_value` already established elsewhere in this file — EXCEPT that
idiom is only safe when root, at the point of the call, already equals the right character, and here
it sometimes did not: `kehillah_study_torah_monthly_effect` runs inside the scheme's own `on_monthly`
hook, where root is the SCHEME itself, not the owner. Fixed by giving both a `$CHARACTER$` parameter
(this mod's own established $PARAM$-substitution idiom) instead of guessing root vs. `this` per call
site — every caller now passes whichever reference is actually stable there: `root` from the
decision's own effect or the phase-completion event's option (both genuinely stable), `scope:owner`
from the scheme's own `valid` block and from `kehillah_study_torah_monthly_effect` (both natively
provided/already saved, and — unlike root or `this` — correct no matter how deeply the parameter is
later referenced inside the callee).

**No persisted "which library" variable, deliberately.** `kehillah_study_torah_resolve_library_effect`
is re-run fresh every time a library is needed (the decision's own effect, every phase completion,
every monthly tick) rather than resolved once and remembered — the same "live query, not snapshot"
choice `kehillah_study_torah_pick_next_work_effect` already made for "which work," now extended to
"which library" too. This is what lets a moved capital or a relocated adventurer be handled by simply
re-running the same search next time, with no separate move-detection code of its own; a title-valued
character variable (the retired `kehillah_visit_library_interaction`'s own approach) was considered
and rejected specifically because that mod's own reason for persisting one — surviving a real-time gap
between two different effect chains — does not apply here.

**2026-09-19 — Starting library seed randomized, ck3-tiger-clean, not yet live-tested.** At user
request ("mix it up... each community gets random books from the initial list... expand the initial
list") — every community used to get the literal same two works (Targum Onkelos + the Mishnah,
2026-09-15's own seed). `kehillah_seed_starting_library_effect` (common/scripted_effects/kehillah_
library_effects.txt) now rolls a count of 1-3 (equal odds) and draws that many DISTINCT works from
the 8-work Parshanut+Talmudics pool via a new `kehillah_seed_one_random_torah_work_effect` (called
1-3 times per community), using the same trigger-filtered `random_list` idiom `kehillah_study_torah_
pick_next_work_effect` already established, so a work already drawn can never be drawn again in the
same seed. Asked the user explicitly rather than deciding silently: **Hashkafa stays OUT of the
random pool**, preserving 2026-09-15's own deliberate "Hashkafa starts at zero" scarcity design
(kehillah_scripted_triggers.txt's own header, just above the six `kehillah_owns_/missing_<track>_
work_trigger` entries) — the user chose to keep it rather than open Hashkafa to the starting draw
too. Corpus itself is unchanged (still the same 12 real works); "expand the initial list" meant
growing the pool a community's start can draw from (2 fixed → 8 eligible), not adding new works to
the corpus, which nothing in the request actually asked for.

**2026-09-19, SAME-DAY FOLLOW-UP — the Talmud corpus split into Sedarim, and three anachronistic
Hashkafa works date-gated, ck3-tiger-clean, not yet live-tested.** Two user requests handled together
since they both touch the same 12-work corpus the entry above just finished tuning: "can we split up
the Talmuds into different Seders or Mashectot?" and, separately, "exclude the Kuzari and anything
else written after 867 from the initial pool... have a creatable pool of books that can become
available later... replace them in the initial pool though." Corpus grew from 12 real works to 23 —
every file that enumerated the twelve by literal flag (the owns/missing triggers, the acquire event,
the travel journey's tooltip/is_location_valid/province_score, the study scheme's numeric-ID bridge,
the unstudied-count script values, the map-view GUI's per-work donate/studied functions, the donate
confirmation event, and all their localization) needed the same mechanical expansion — done with a
small Python script (not by hand) specifically to keep 11 near-duplicate blocks consistent instead of
risking a typo'd flag name in one of them; ck3-tiger came back clean on the result.

**The split itself, per the user's own choice ("keep Mishnah together, split Bavli and Yerushalmi")**:
the Mishnah stays one work; the Babylonian Talmud splits into all six of its real Sedarim (Zeraim,
Moed, Nashim, Nezikin, Kodashim, Tahorot — the same six volumes a real Vilna Shas edition prints, even
though its own Gemara only substantially covers four of them, Zeraim/Tahorot being mostly Mishnah-only
outside Berakhot/Niddah respectively); the Jerusalem Talmud splits into only the four Sedarim it
actually has real Gemara for (Zeraim, Moed, Nashim, Nezikin — Kodashim/Tahorot were not invented for
it, since it has none). This is a documented assumption about seder-level granularity and which
Sedarim to include for Bavli, not independently confirmed with the user beyond the two questions
actually asked (Seder- vs. Masechet-level granularity, and which texts to split) — flagging it here in
case Masechet-level (individual tractate) granularity turns out to be wanted later, which would be
another full pass of the same shape, not a small follow-up.

**The date-gating, per the user's own choice of mechanism ("direct current_date gate")**: Emunot
ve-Deot (933), Chovot HaLevavot (~1080) and Kuzari (~1140) are genuinely anachronistic before their
own real composition year, not just before 867 — Chovot HaLevavot and Kuzari are even later than the
flagship Worms 1066 start, so this was a real latent anachronism the acquire decision could already
trigger, not only a hypothetical concern for an earlier bookmark. `kehillah_missing_hashkafa_work_
trigger` (common/scripted_triggers/kehillah_scripted_triggers.txt) and the acquire event's own Hashkafa
option (`kehillah_acquire_torah_work.0001.c`, events/kehillah_learn_torah_events.txt) both gate each of
the three behind `current_date >= <year>.1.1` directly, ANDed with the existing not-owned check — no
new state, unlike the alternative (a global unlock list plus an announcement toast) the user was also
offered and did not choose. **Replacements, to keep Hashkafa's own immediately-available roster at
four works instead of dropping to one**: Hekhalot Rabbati, Shi'ur Qomah (Merkabah/Hekhalot mysticism,
Talmudic-Geonic era) and Sefer HaRazim (an ancient Jewish magical-cosmological text, ~3rd-4th century)
— all three real, documented, pre-867 texts, proposed by the assistant and confirmed by the user before
writing any content. Hashkafa is still excluded from the community-seed random pool entirely (the
entry above), so this backfill matters for the acquire decision and the travel journey, not the
starting-library roll.

**2026-09-19 — "Found a Jewish Community" shipped for rabbinic landless adventurers, ck3-tiger-clean,
NOT YET LIVE-TESTED** (still true as of 2026-09-20 evening — see the correction below), at user request ("create a 'found a jewish community' decision for Rabbinic
adventurers"). This resolves v2 spec section 5.1's own "open technical question, not solved here" —
what actually places a new landless title at a chosen location — which had sat unanswered since that
spec was written, flagged as "residual risk, not a blocker." Checked directly against the installed
1.19 files before building anything: vanilla's own `create_adventurer_title` (the engine effect behind
"Abandon Realm to Become an Adventurer" and every other laamp-creation path, `common/scripted_effects/
07_dlc_ep3_scripted_effects.txt`) is genuine, general-purpose runtime title creation — no landed_titles
entry backs the title it produces, unlike this mod's own sixteen pre-authored `c_kehillah_*` titles
(`common/landed_titles/kehillah_landed_titles.txt`), so a Kehillah can now be founded literally
anywhere a landless adventurer is standing, not just at one of the sixteen.

**Scope shipped**: `kehillah_found_community_decision` (`common/decisions/kehillah_found_community_
decisions.txt`) and `kehillah_found_community_effect` (`common/scripted_effects/kehillah_found_
community_effects.txt`) — this is specifically v2 spec section 5.1's "landless character founds a
title" primitive in its simplest form (founding from nothing), NOT the "Found a Sister Community"
variant still listed below in the backlog (an existing Legendary-Prosperity/Greatness Kehillah sending
a courtier elsewhere) — that variant is unbuilt and can reuse the same effect once it exists. **The
gate**: `is_rabbinic_authority_jewish_trigger` (rabbinism/kabarism/merkabah specifically — the faith
half of "rabbinic") AND `kehillah_leader_is_rabbinic_trigger` (this mod's existing personal bar for
"reads as a rabbi": the trait, `theologian`, top-two Learning education, or `learning >= 12` as
fallback — reused rather than re-invented, so a founder and a credible Chief Rabbi candidate are held
to literally the same definition) AND `has_government = landless_adventurer_government` AND ten Jewish
camp followers. It also requires the camp's current location not already to host a registered
Kehillah, preventing duplicate communities in one place. The founding
effect mirrors `kehillah_on_title_gain`'s own body (`common/on_action/kehillah_on_actions.txt`) almost
exactly — `change_government`, `kehillah_restore_quarter_effect` (a safe no-op with no prior building
record), `kehillah_init_pillars_effect`, leader-flavor — plus the three follow-up calls that on_action's
own comments already flagged as required "if Wave 5 ever adds founding" (registering into
`kehillah_registered_communities`, seeding the starting library, refreshing the map-view mirror). Also
extended `is_kehillah_title_trigger` (`common/scripted_triggers/kehillah_scripted_triggers.txt`) with an
additive `is_target_in_variable_list` branch alongside its sixteen hardcoded names, so a founded
community is recognized everywhere that trigger is checked (domicile naming, the two on_title_gain
hooks) exactly as the original sixteen are — the original name-based check's own documented reason
(answerable during history execution, before the registry exists) is untouched for those sixteen.

**A real bug caught before it ever reached a running game**: the first pass called
`kehillah_restore_quarter_effect` without first setting `scope:kq_title`, the scope name that effect's
own restore-track calls read — `ck3-tiger` flagged it immediately as a `strict-scopes` warning (0
fatal/0 error throughout, but this one warning was real, not a false positive per this repo's own
"verify before patching" norm). Fixed by saving the newly created title as `scope:kq_title` before the
restore call, matching exactly what `kehillah_on_title_gain` already does. Exactly the kind of mistake
CLAUDE.md's testing section exists to catch standing still, without ever booting the game.

**Deliberately NOT built**: AI eligibility (`ai_potential = { always = no }`) — this is a genuinely new,
unverified primitive (`create_adventurer_title` has never been called from this mod before), and
CLAUDE.md's own guidance treats succession/government-law code as this codebase's highest-risk area,
needing a live playtest before it's trusted at all, let alone handed to every AI-played rabbinic
landless adventurer on the map at once. Also not built as of 09-19: a dynamic, location-based title name.
**AI ENABLED 2026-09-23**, per Daniel's decision, once the 09-23 live-test pass met this
paragraph's own stated bar. `ai_potential` mirrors `is_shown`'s core eligibility (adventurer
government + rabbinic leader); `is_valid`'s gates (ten Jewish followers, no existing community at
the location) apply to the AI exactly as to the player. `ck3-tiger` 0 fatal/0 error. Not yet
live-verified for AI use specifically (single-run player verification only) — Daniel's own call
was to ship it and watch `error.log` for anything a many-AI-characters-at-once scenario surfaces,
rather than gate on another live pass first.

**2026-09-20 — a Codex session claimed a live PASS on this path, renamed `c_kehillah_worms` to a duchy-tier
`d_kehillah_worms`, and both claims were wrong; reverted and re-fixed the same day.** Daniel re-ran the
decision himself: still Game Over, and no county-based name. Full account in
`docs/testing/2026-09-20-found-community-live-test-log.md` ("Correction"). Short version: (1) county-tier
landless titles are fine — Worms has been one since 09-07 through three live playtests, vanilla's
`c_nf_yamato` is one — and the Isaac Game Over was caused by that session re-adding `title_tier = duchy`
to `kehillah_government.can_get_government`; everything Worms-related is back to the 09-07 shape.
(2) The real founding bug was title ordering: the founder already holds a `d_laamp_*` title, the new
community title was never made primary and the old one was never destroyed, so `add_realm_law` hit
the wrong title and both titles ended up with invalid succession. `kehillah_found_community_effect`
now mirrors vanilla's own adventurer-becomes-landed teardown: create → `set_primary_title_to` →
destroy the old adventurer title → `change_government` → `add_realm_law`, with `debug_log`
breadcrumbs. (3) The title name is now `Kehillah of [kehillah_founding_county.GetNameNoTierNoTooltip]`
(county, captured before creation, vanilla's `adventurer_name_010` mechanism) — a fresh later re-test
confirmed it renders as intended. The same re-test confirmed the old title is destroyed, the founder
does not Game Over, and the standard Kehillah decisions appear; the Worms bookmark also remained stable
past 1066-10-01. A dedicated test start `bm_1066_kehillah_founder_test` (rabbinic adventurer
"Yitzhak", fixture title `d_kehillah_founder_test`, placeholder portrait) exists for exactly this
check; whether it should ship to players or be console-only is an open call (BLOCKERS.md). ck3-tiger
0/0.

**2026-09-20 evening — ROOT CAUSE of the founding Game Over, and the fix.** The 12:49 re-test above
was already running on the fixed build; here is why it passed. The ordering fix was necessary but not
sufficient: the real decision still Game-Overed 15-25 days later. Eleven scripted live probes
(subagent-driven, `run <file>.txt` + `debug_log`; full sequence in the test log's "Root cause and
fix") found the second bug: the founder ended up in `kehillah_government` with **no domicile** —
`change_government` never creates one, it only destroys the adventurer's camp — and the engine
silently resets a domicile-government with no domicile to feudal, which for a landless title is the
"lost all titles" Game Over. Nothing in script can create a domicile after the fact (no such effect
exists; confirmed against the engine's own `script_docs` output). The fix is a parameter no vanilla
script uses: `create_adventurer_title = { government = kehillah_government }` creates title +
government + Jewish Quarter in one engine operation. Verified on a fresh launch via the real UI
decision: "Rav Yitzhak of the Kehillah of Worms", Communal Realm, Jewish Quarter Level 1, Kehillah
decisions live, ran to Oct 1067 with no Game Over; Worms control unaffected. Same commit:
flavorization no longer tier-gated (runtime titles are duchy-tier, so the founder read as "Duke"),
title name via `GetNameNoTierNoTooltip` ("Kehillah of Worms", not "Kehillah of County of Worms").

**2026-09-20 later — title tier unified at duchy, per Daniel's decision.** All fifteen
pre-authored communities now use `d_kehillah_*` IDs, matching the runtime duchy created by
`create_adventurer_title` in Found a Jewish Community. The earlier county-tier Worms
regression above was caused by a government eligibility gate, not by duchy rank; that gate
remains tier-agnostic. The flat, landless title layout and each real host county's ownership
are unchanged. CK3's alternate `create_dynamic_title` rejected `tier = county` in both
ck3-tiger and a live console probe; the briefly prototyped finite county-slot approach was
discarded after Daniel chose duchy parity. See
[docs/spec/v14-kehillah-title-tier.md](docs/spec/v14-kehillah-title-tier.md).
  **Source-verified and ck3-tiger-clean (0 fatal/0 error); Daniel will run the
  fresh live regression manually.** Kehillah leaders now receive plain
  commoner portrait clothing instead of ducal attire, and Isaac's bookmark
  placeholder no longer wears royal clothing. The portrait appearance also
  awaits Daniel's visual check.
The title-ID change requires a new campaign rather than an old `c_kehillah_*` save.

**2026-09-20, that live regression — two real bugs found and fixed, unrelated to duchy
tier.** Daniel reported every Jewish Quarter building reading as locked despite a Level 1
Synagogue. Subagent-driven live diagnosis (both a freshly founded Frankfurt community and a
brand-new Worms 1066 start) found:
1. **The external-slot lock is real and was present on Worms too, not just founded
   communities** — so this was never a duchy-tier regression at all. `base_external_slots = 6`
   (`common/domiciles/types/kehillah_domicile_types.txt`), added 2026-09-17 on the assumption it
   alone sets a domicile's starting unlocked-slot count, left every external slot — all six,
   including the first — stuck on vanilla's generic "Locked Slot" state; hovering showed the
   engine's own "New Slots can be unlocked by upgrading the central Domicile Building" tooltip.
   Every vanilla domicile type actually pairs a small `base_external_slots` (2) with a
   `domicile_external_slots_capacity_add` character modifier on its tier-1 main building — this
   mod had removed that modifier on 2026-09-17 and never replaced it. Fixed by adding
   `domicile_external_slots_capacity_add = 6` to `kehillah_synagogue_01`
   (`common/domiciles/buildings/kehillah_domicile_buildings.txt`), which inherits automatically
   to every later Synagogue tier per `_domicile_buildings.info`'s own inheritance rule for
   `character_modifier`. Not yet re-verified live.
2. **Founded communities were never actually recognized as Kehillah titles.** The 2026-09-19
   addition to `is_kehillah_title_trigger` (`common/scripted_triggers/kehillah_scripted_
   triggers.txt`) checked `is_target_in_variable_list`, the plain/character-scope checker, against
   `kehillah_registered_communities` — a list populated with `add_to_global_variable_list`. CK3
   has three separate, non-interchangeable variable-list namespaces (confirmed against the
   installed 1.19 files' own generated `logs/triggers.log`: `is_target_in_variable_list`,
   `is_target_in_local_variable_list`, `is_target_in_global_variable_list` are three distinct
   entries), and checking the wrong one doesn't error, it just always returns false. Live:
   `kehillah_debug.61` reported "primary title is NOT registered" for a freshly founded
   community, and `error.log` filled with 22,000+ lines of `kehillah_domicile_name_vanilla_
   fallback` loc errors from `KehillahDomicileName` falling through every single frame the
   domicile panel was open. Fixed by changing the check to
   `is_target_in_global_variable_list`, matching the `add_to_global_variable_list` call it reads
   back. This bug is independent of bug 1 (Worms hit bug 1 without ever touching this code path)
   and was masking bug 1's own symptom on the founded-community repro case with a second, louder
   one. Not yet re-verified live.

**Remaining founder-path work: LIVE-TESTED PASS, 2026-09-23** — all six items below are now
confirmed, via a subagent-driven pass on `bm_1066_kehillah_founder_test`. Full account:
[docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md](docs/testing/2026-09-23-founder-path-cleanup-live-test-log.md).
The `kehillah_restore_quarter_effect` removal and the tooltip-hover fix both held up as designed
(0/0 error growth on hover, 0 restore errors and all six breadcrumbs on taking the decision). The
new gates (ten Jewish camp followers, no registered Kehillah already at the location) gate
correctly in both directions. The two 2026-09-20-later fixes ("Ungating domicile buildings":
external-slot unlock, community-registration namespace) both hold live too. A month-plus run (15
Sep 1066 → 7 Oct 1067) produced no Game Over, with normal downstream community flavor events
firing.

**Two real bugs found and fixed in the course of this pass, both re-verified live:**
1. `d_kehillah_founder_test`'s `capital` was `c_worms` — the founder always spawned standing on
   top of Isaac's already-registered Kehillah of Worms, so the new empty-location gate
   permanently (and correctly) refused him. Fixed: `capital = c_frankfurt`
   (`common/landed_titles/kehillah_landed_titles.txt`).
2. The 2026-09-20 tooltip fix was incomplete: `hidden_effect` alone suppresses only the block's
   own tooltip *summary line*, not per-frame evaluation of everything nested inside it — opening
   the decision's confirmation dialog (distinct from hovering the list row, which is all the
   09-20 pass checked) produced 127k+ new `error.log` lines from one ~10-second view, worse than
   the original bug. Fixed by gating the whole block on `exists = scope:kehillah_new_community_
   title` (`common/scripted_effects/kehillah_found_community_effects.txt`), this mod's own
   established idiom for a possibly-not-yet-existing scope. `ck3-tiger` 0 fatal/0 error
   throughout (56 warnings post-fix, down from 57).

**Still genuinely open, unaffected by this pass:** no founded-community *succession* has ever
been live-tested (this pass ran past the founding, not past a leadership handoff). The fixture
bookmark remains player-visible (Daniel's call, 2026-09-23 — see BLOCKERS.md). AI eligibility,
open as of this pass, was enabled separately the same day — see the "AI ENABLED 2026-09-23" note
earlier in this section.

**Partly resolved, and reopened by the first playtest:** open,
community-wide leadership succession (any notable family can be
appointed, not just the outgoing leader's own).

The part that *is* resolved is the one that worried us: it needs no
separate "rival family head" playable mode. Appointment-based succession
(`succession_appointment`, the same framework vanilla uses for
administrative governors) has no "losing candidate who keeps playing a
demotion" case to design for. There is one outcome per vacancy and the
player becomes it. That still holds.

**UPDATED 2026-09-07 — the premise below turned out to be wrong; see the
current-state note at the top of this file for the full correction.**
`holder_court_position` does work, and `kehillah_leadership.txt` now
uses it — the community's officers are genuinely in the candidate pool,
not just family. What's actually still open is verifying this live with
a test built to distinguish "the Shtadlan won because merit really
outscored inheritance" from "family happened to outscore the Shtadlan
this one time too" — see the near-term TODO. Section 2c of the
implementation doc still documents the (now moot) three-routes analysis
for historical reference, not as a live task list.

~~**What is not resolved is getting the notable families into the
candidate pool in the first place.** The Phase 1 implementation assumed
the community's officers would qualify through the
`holder_court_position` category; that category is documented but not
implemented, and using it crashed the game. Succession is family-only
today. This is back on the critical path for Phase 1 rather than being
backlog — see the current-state note at the top of this file and section
2c of the implementation doc for the three candidate fixes.~~

**Track to revisit once released, not buildable yet:** CK3's upcoming "By
God Alone" expansion (dev diary, unreleased as of this writing) introduces
Ecclesiastical Titles (`clerical_region_titles`), a Clerical Appointment
score picking the next officeholder from a broad clergy pool, and a
Cathedral Complex Domicile that persists and grows independent of any one
office-holder — i.e. Paradox's own native version of almost exactly what
Phase 1 approximates today with a forked succession_appointment entry plus
a manual domicile-copy effect. The dev diary explicitly calls out
`clerical_region_titles` as intended for mod reuse. Once this ships,
revisit whether it offers a cleaner substrate than our custom Kehillah
title/domicile plumbing — but nothing in Phase 1 should wait on it.

That last point is worth restating now that the first playtest has
found the family-only succession problem, because the temptation to wait
is real. The Clerical Appointment score — picking an officeholder from a
broad clergy pool, with no dynastic component — is Paradox solving
exactly the problem Phase 1 just ran into, and it would likely solve it
better than any of our three workarounds. It is also unreleased, with no
date. **Build the workaround anyway.** Heir designation is small, it is
independently worth having as a player-facing feature, and if By God
Alone eventually makes it redundant, a small forked interaction is a
cheap thing to have thrown away. The alternative is a mod whose central
promise stays broken for an unbounded period.

**Bigger, and overlaps a system already scheduled later — don't build twice:**
- **Takkanot/Synod as a Bet Din Conference activity variant, 2026-09-23 (Daniel's idea) —
  DEFERRED pending the "By God Alone" DLC (expected ~1 week out as of this writing).** Instead of
  a separate regional-council mechanic, a special Bet Din activity type callable by the
  highest-Standing community leader in a region, producing binding takkanot the same way the
  existing Sh'um Bet Din does (v4 spec) but without needing a pre-authored `d_kehillah_shum`-style
  duchy grouping. Open question, and the reason to wait: what defines "a region" for who can call
  it and who it binds — Ashkenaz-wide is one option, but Daniel's own instinct is this might map
  more naturally onto a **rite** once one exists (Ashkenazi rite, Sephardi rite, Bavli rite,
  possibly player-formable), which is a cleaner, more mechanically real scoping unit than a
  hardcoded region list. If the DLC restructures faiths/tenets/rites as expected, this could
  resolve for free; building region-scoping logic now risks throwing it away regardless. Unlike
  the Clerical Appointment/`clerical_region_titles` precedent elsewhere in this file (where
  "build the workaround anyway" was the right call because the mod's central promise was broken
  without it), nothing here is currently broken by waiting — Sh'um's existing per-title symmetric
  takkanot mechanism still works fine in the meantime.
- **Legends system integration** (martyrs, great sages memorialized for
  lasting bonuses) — pair with Phase 4/5, where persecution and memory are
  the actual theme.
- **Voluntary "found a sister community" expansion.** A lighter, non-crisis
  version of Phase 4's Unlanded Migration Journey. Fold into Phase 4 rather
  than building two migration systems. **The underlying "place a new Kehillah
  title" primitive this depends on now exists** — see the 2026-09-19 "Found a
  Jewish Community" entry above (`kehillah_found_community_effect`, common/
  scripted_effects/kehillah_found_community_effects.txt) — so this item is now
  "send a courtier + endowment, gated on Legendary Prosperity/Greatness, then
  call the existing effect," not "solve title placement from scratch."

## Explicitly not scheduled yet
Anything not listed above (additional overlays beyond the three named,
further survival-loop depth, multiplayer considerations, etc.) is out of
scope until the phases above are further along.
