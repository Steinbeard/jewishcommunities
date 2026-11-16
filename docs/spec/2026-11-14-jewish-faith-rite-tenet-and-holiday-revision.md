# Jewish faiths, rites, tenets, and festivals: revision proposal

**Status:** BUILT with the implementation decisions below; source verification completed, live/save/UI verification pending (2026-11-14). This records the November 13–14 design discussion. The sections below preserve the original target proposal; the dated implementation decisions and linked build record describe the current source. It supersedes the proposed tenet roster and holiday assumptions in `2026-11-08-sefer-system-redesign.md` §§4.2–4.3 and `2026-11-08-sefer-tenet-mechanics.md` where they conflict. Runtime initialization and save migration still require the checks linked below.

## Implementation decisions — 2026-11-14

Daniel resolved the implementation questions during the build:

- Use **Option A**: generic Religious Legal Pronouncements remains available
  outside Rabbinism; its Rabbinic institutional bonuses require the authority
  doctrine. **Retain Malabar's Toraic doctrine** pending separate review.
- Use **Legalism for Kabarism's third core**. Yordei Merkavah's third core is
  the new **Piyyut / Sacred Liturgy**, with **Poet as a virtue**. No new Midrash
  tenet and no Warmongering core.
- Build **independent non-DLC scholarly and liturgical tenets** rather than
  extending the By God Alone tenets. Bavel uses Scholarly Study / Iyyun
  ha-Talmud; Sepharad and Yordei Merkavah use Sacred Liturgy / Piyyut. They
  provide their own modest effects/actions, without copying DLC-only systems.

These decisions supersede the tentative third cores and vanilla-DLC choices
in sections 1–2 and 5–6 below. The historical proposal remains for rationale.
The definitive built roster, migration mapping, behavioral details, and
research limits are in [the implementation record](../implementation/2026-11-14-faith-rite-tenet-holiday-revision.md).
In particular, devotional legacy index 4 maps to Unrelenting Faith, while
Piyyut is appended as **13**; existing book integers and reform replacement
ordinals are not renumbered. Historical book arguments are reviewed separately
from those mechanical mappings. Runtime results are **not** claimed: see
[the test record and checklist](../testing/2026-11-14-faith-rite-tenet-holiday-revision.md).

## 1. Design rules and unresolved choices

* A **doctrine** identifies sources of binding law, scriptural canon, priesthood, and headship. A **tenet** describes an emphasis a rite can choose. Being Rabbinic must not consume a universal `Talmud Torah` core slot; being Karaite must not require `Ba'alei ha-Miqra` as a core slot.
* All tenets must give useful vanilla-scale effects to rulers, courtiers, and adventurers of **every government type**. Kehillah, Bet Din, libraries, yeshivot, sermon, crisis, and holiday hooks supplement the general effects. No tenet's only reward may require the Kehillah government.
* Give every tenet a **rite-wide follower effect** and a **personal-adoption effect**. Use `parameters`/`character_modifier` for the former, `personal_tenet_parameters`/`personal_tenet_modifier` for the latter; show the two separately in the faith UI. Check whether a rite core and the character's personal tenet can stack, and cap repeated event rewards.
* Three core tenets per rite. Faith-level known/permitted/prohibited statuses are shared by all rites of that faith. Do not fabricate different faith statuses for Bavel and Sepharad. Core selection, local event variation, and rite doctrines distinguish them.
* An ordinary tenet description should communicate a belief and its appeal to adherents. It should not narrate all modifiers, specify a government type, call a Jewish tenet by a Hebrew name for non-Jewish followers, or imply that all people of a faith hold identical views.
* **Open design decisions:** Yordei Merkavah's third core and whether a new Midrash tenet earns a slot; Kabarism's third core (Warmongering is a candidate, not approved); DLC support for Scholasticism and Divine Liturgy; the final separation between generic Religious Legal Pronouncements and specifically Rabbinic *Pesak Halakha*; headship offices and eligibility; Malabar's currently Toraic doctrine. The tentative rows below must not silently settle these.

## 2. Proposed core roster

| Rite | Three cores, proposed | Distinctive play |
|---|---|---|
| Bavel (`rabbinism`) | Religious Legal Pronouncements / Rabbinic *Pesak Halakha*; Scholasticism / *Iyyun ha-Talmud*; Communal Identity | Geonic scholarly networks and responsa. A Gaon's office is not a tenet. |
| Ashkenaz (`minhag_ashkenaz`) | Asceticism / *Hasidut*; Legalism; Communal Identity | Pietism, lawful conduct, communal bonds. |
| Sepharad (`minhag_sepharad`) | **Hokhmah**; Religious Legal Pronouncements; Divine Liturgy / *Piyyut* | Machshavah, law, and Hebrew liturgical composition. Ibn Daud is a particularly good later expression of *ḥokhmah* and Greek wisdom; his twelfth-century account should not imply universal Aristotelian study in 867. |
| Yerushalmi (`minhag_yerushalmi`) | Sacred Homeland; Ritual Celebrations / *Mo'adim le-Simchah*; Communal Identity | Attachment to Jerusalem and local festival practice. Reserve *Avelei Tziyon* as Karaite-specific flavor, not the generic Rabbinic name. |
| Yordei Merkavah (`merkabah`) | Esotericism; Inner Journey; **third TBD** (Midrash only if distinct) | Mystical ascent; retain Rabbinic authority in doctrine. |
| Karaite (`karaism`) | Literalism / *Peshuto shel Miqra*; Legalism; Communal Identity | Scriptural legal interpretation. Karaite Mourners of Zion may personally adopt Sacred Homeland/Asceticism; do not impose that movement on all Karaites. |
| Haymanot | Communal Identity; Asceticism; Ritual Celebrations | Distinct Ethiopian canon, observance, and priesthood; no Talmudic study bonus. |
| Malabar | Communal Identity; Adaptive; Eastern Syncretism | Indian setting and coexistence; review canon before assigning Rabbinic book rewards. |
| Samaritan | Communal Identity; Literalism; Ritual Celebrations | Samaritan Torah, priesthood, Gerizim, and its own festival forms. |
| Kabarism | Adaptive; Religious Legal Pronouncements; **third TBD** | Khazar Jewish state among subjects of several religions. Warmongering is a candidate if religious conquest is intentionally part of its identity; vanilla Warmongering's invasion/holy-war effects and Jewish selection restriction must be reviewed first. Legalism is a known alternative, not a default core. |

The proposed roster removes Legalism from the Sephardi three-law combination. Legalism means lawful conduct and ruler accountability; Scholasticism means disciplined intellectual argument; Religious Legal Pronouncements means recognized adjudicative authority. Both Legalism and Religious Legal Pronouncements currently give Just/Arbitrary virtue/sin effects, so their distinctiveness must be tested in the displayed tenet wheel.

## 3. Faith-level status proposal

The following is a **reviewed-tenet matrix**, not an exhaustive list of all vanilla tenets. Every listed core must be known or otherwise supplied by the engine. Keep vanilla history entries that still fit. `Kiddush ha-Shem` is **unlisted initially** and becomes known only after a qualifying crisis; a faith's status cannot be inferred from another faith's crisis.

| Faith | Known in addition to the starting cores | Permitted | Prohibited |
|---|---|---|---|
| Rabbinic (all five rites) | The union of the five rites' cores; Aniconism, Literalism, and suitable wider Jewish teachings | Adaptive and compatible local expressions; generic symbolism if Midrash exists | No generic study or *peshat* tenet. Rejection of a competing binding canon belongs in doctrine. |
| Karaite | Aniconism; Hokhmah; Asceticism; Sacred Homeland (*Avelei Tziyon* for its particular Jerusalem movement); Ritual Celebrations; Divine Liturgy where supported | Generic Scholasticism, Inner Journey, suitably localized Esotericism, Adaptive, nonbinding symbolism | **Binding Rabbinic Oral Torah and Geonic jurisdiction** through doctrine. Rabbinic *Pesak Halakha* may be prohibited only if the tenet itself is explicitly defined around that authority. |
| Haymanot | Aniconism; Legalism; its core practices | Literalism, Hokhmah, Sacred Homeland, generic Scholasticism, appropriately localized Divine Liturgy | Rabbinic Oral Torah and Rabbinic-specific Pesak, not the general possibility of religious judgments. |
| Malabar | Aniconism; Legalism; Ritual Celebrations; its core practices | Hokhmah, Divine Liturgy, generic Scholasticism, Sacred Homeland | Rabbinic-only Pesak **if** its authority remains non-Rabbinic; revisit with the canon doctrine. |
| Samaritan | Aniconism; Legalism; Sacred Homeland **only with Gerizim-aware effects**; its cores | Asceticism, Divine Liturgy, generic scholarly or symbolic interpretation | Rabbinic Oral Torah and Rabbinic-specific Pesak. |
| Kabarism | Aniconism; Legalism; Ritual Celebrations; Hokhmah; its cores | Communal Identity, Sacred Homeland, Scholasticism, possibly Warmongering | No reviewed tenet needs a special ban beyond the Rabbinic authority doctrine. |

**Karaite Pesak decision:** vanilla `tenet_religious_legal_pronouncements` is generic and Karaites developed their own law. Do not prohibit that ID merely because a Jewish localization calls it *Halakha*. Option A (preferred for minimum custom IDs): make its Rabbinic flavor and Bet Din bonuses depend on a Rabbinic authority doctrine, provide non-Rabbinic flavor and functioning general effects elsewhere, and do **not** prohibit the generic tenet for Karaism. Option B: explicitly make the entire tenet a Rabbinic institutional tenet, prohibit it for Karaism/Haymanot/Samaritan and reconsider Malabar, and replace its current Haymanot and Malabar cores. Decide one option before changing statuses. The table describes the authority boundary, not an unconditional vanilla-ID prohibition.

## 4. Doctrines and headship

1. Keep a separate **binding source/canon** distinction: Rabbinic Written + Oral Torah, Karaite Scripture without binding Rabbinic Oral Torah, Samaritan Torah and Gerizim, and Haymanot's transmitted canon and Ethiopian priestly practice. Audit Malabar instead of assuming it is historically Toraic. Route book standing, study, Bet Din citations, and holidays through these doctrines or explicit capability triggers, not `tenet_talmud_torah` or a hard-coded faith list.
2. Separate **headship office** from canon and from a tenet: Gaon as head of one or more recognizing Rabbinic rites when supported; a restored Sanhedrin's Nasi; a restored Jerusalem Kohen Gadol requiring priestly legitimacy and Temple institutions; the existing Samaritan High Priest at Gerizim. Define whether an office is head of rite or head of faith, its succession, jurisdiction, and powers independently. Do not give every office excommunication or appointments merely because a title exists.
3. Remove vanilla `special_doctrine_prophecy_of_malachi` from Jewish rites after replacing its only actual effect, `block_from_create_hof_parameter`, with explicit creation gates for each office. Its wording treats founding any headship as naming a new High Priest. Check creation decisions and existing title holders in all bookmarks and old saves.
4. Keep `kehillah_recognition_of_sages` only where the rite recognizes a Gaon, and review inheritance from the main Rabbinic rite. Kabarism's Open Peoplehood remains: Khazars need not become an Israelite culture to be Jewish.
5. Restored animal offerings and renewed prophecy are **not** the vanilla human-sacrifice/astrology tenets. If ever implemented, make Temple service and prophetic movements contingent on their own restoration events and institutions, not starting cores.

## 5. Tenet mechanics: follower and personal effects

The table is an effect budget, not an instruction to stack every bonus. Retain useful vanilla effects unless they contradict the new theme; give a clear general effect plus at most one major mod-specific hook per tenet. Personal adoption should create a choice or stronger personal expression, not merely repeat the same rite-wide number.

| Tenet | Rite-wide follower effect and mod hook | Personal adoption | Audit or open issue |
|---|---|---|---|
| **Hokhmah** (custom; generic “Reasoned Theology”) | Learning-oriented vanilla-scale effect; improved Machshavah study/challenges. Unlock a reasoned debate interaction using Learning and Diplomacy, with opinion, prestige/piety, or support toward a **known** teaching, never instant rite change. | Better odds and a distinct debate outcome or reduced debate cost; a modest study advantage. | Build meaningful AI use and cooldown. Distinguish the debate from vanilla Literalist Debate. Do not make Zealous automatically sinful merely for being devout. |
| **Sacred Homeland** (custom; Jewish name TBD) | Pilgrimage/access to the faith's holy sites, stewardship of a controlled site, and support for its resident communities; never hard-code Jerusalem for Samaritans. | A pilgrim/alms choice with stronger personal reward, available to landed, landless, and Kehillah characters. | Existing Send Alms to Jerusalem is too narrow and Kehillah-biased. *Avelei Tziyon* belongs especially to a Karaite ascetic movement. Avoid free conquest incentives or a duplicate of Armed Pilgrimages. |
| **Kiddush ha-Shem** (custom; generic “Witness Through Sacrifice”) | Conversion resistance; principled protection/solidarity options in persecution. Qualifying grave+ crisis with deaths or forced conversions makes it known to the **affected faith**. | Endurance/commemoration or aid to survivors, with stress/piety benefit tied to choices rather than casualty counts. | Current distinct effect raises martyr deaths. Rework so death is never mechanically rewarded; cap post-crisis Greatness and show its cause in the event tooltip, not an overloaded tenet description. No starting core. |
| **Scholasticism / Iyyun ha-Talmud** (vanilla DLC) | Keep general learning/university and study effects. Add Talmudics reading, jurisprudential checks, and yeshiva teaching bonuses **only** with Rabbinic authority; a Karaite follower instead gets a Scripture-based scholarly hook. | Personal study or disputation bonus and scholarly advancement for any government. | Replace Pilpul ID carefully. Vanilla `can_pick` is Christian and requires *By God Alone*; design behavior without DLC before assigning starting cores. “Pilpul” is too specific and often later for general medieval study. |
| **Religious Legal Pronouncements / Pesak Halakha** (vanilla) | Keep generic lawful-pronouncement effect; for Rabbinic rites, improve Bet Din adjudication and responsa. Recognized authority follows doctrine. | Personal judge/ruler bonus or a responsum action if eligible; usable without Kehillah government. | The Bet Din consultation-by-responsa path is currently disabled. A custom Pesak tenet would duplicate this unless the tenet becomes explicitly Rabbinic. See §3. |
| **Legalism** (vanilla) | Preserve Just/Arbitrary and political rule-of-law/faction effects. | Keep lawful-authority personal expression; optional mod judgments keyed to fairness rather than religious scholarly authority. | Do not reflexively add Bet Din bonus, which would erase its difference from Pesak. Not a required Rabbinic or Kabarism core. |
| **Literalism / Peshuto shel Miqra** (vanilla) | Parshanut/Scripture study and interpretation bonus, independently of Rabbinic authority; retain its existing Literalist Debate. | Better Scripture-based argument or study; no blanket reward for rejecting metaphor. | Scripture-centered is not “incapable of allegory.” Check vanilla holy-war/combat effects and their fitness for Karaite/Samaritan cores. |
| **Divine Liturgy / Piyyut** (vanilla DLC) | Liturgical composition and worship, with personal Poet/piyyut and sermon hooks; no requirement for a feast or a communal government. | Compose/perform a prayer or liturgical poem with a meaningful piety, opinion, or prestige result. | Christian-only `can_pick`, DLC gate, choir/saints language and building-piety effect require localization/eligibility review. Karaite and Haymanot liturgy must not receive Rabbinic texts by default. |
| **Ritual Celebrations / Mo'adim le-Simchah** (vanilla) | More eligible holiday scenes and the vanilla feast/festival effects; festival rewards differ from composing liturgy. | Higher personal chance or holiday-specific choice, without double-queuing; existing personal parameter retained. | Current yearly roll is 60% for a player, 75% with tenet; AI 12%/16%. Preserve cadence deliberately and filter eligible scenes before drawing. |
| **Communal Identity** (vanilla) | Keep vanilla group solidarity; optional small, portable support for shared observances and aid between co-religionists. | Personal mutual-aid or relationship benefit. | Prefer out-of-box mechanics. No need to make it a Kabarism core merely because its rulers are Jews. |
| **Asceticism / Hasidut** and **Esotericism / Kabbalah** (vanilla) | Retain vanilla mechanics, check existing study, sermon, and crisis hooks. | Retain distinct spiritual practice, not extra government-only rewards. | Jewish names must depend on tradition/rite: Karaite spirituality is not automatically Rabbinic Kabbalah. Asceticism is not intrinsically Ashkenazi. |
| **Inner Journey**, **Adaptive**, **Eastern Syncretism**, and possible **Warmongering** (vanilla) | Keep their general effects. Add only a justified small contextual hook if needed. | Preserve vanilla personal expression. | Warmongering is currently unavailable to Judaism and grants conquest/invasion/holy-war mechanics. Do not enable it for Kabarism without an explicit historical/design choice and live balance pass. |

**Candidate Midrash / symbolic interpretation:** create a new generic tenet only if it sustains a different playstyle from Literalism, Esotericism, and Divine Liturgy: sermon interpretation, symbolic/parabolic readings of books, and persuasion across characters and governments. A Rabbinic name may be *Midrash*, but generic allegory must not be automatically prohibited for Karaites. A tenet asserting **binding Rabbinic midrash** is instead incompatible by Karaite doctrine. If this distinction does not yield varied choices and meaningful follower/personal effects, do not add the tenet; choose Yordei Merkavah's third core from existing vanilla options after review.

## 6. Retired/merged custom IDs and saved games

| Existing custom tenet | Target |
|---|---|
| `tenet_talmud_torah` | Retire as core. Move Oral Torah authority and its book-standing boundary into doctrine; preserve general Jewish study and canonical re-reading without requiring a tenet. |
| `tenet_baalei_hamiqra` | Retire after Karaite Scripture access and study are covered by authority doctrine plus Literalism. |
| `tenet_kehillah_pilpul` | Map to Scholasticism's Jewish flavor/hook, subject to DLC resolution. |
| `tenet_kehillah_pesak` | Map to Religious Legal Pronouncements where semantically appropriate; do not merge until the Karaite authority choice in §3 is decided. |
| `tenet_kehillah_geonut` | Move to Gaon headship/academy doctrine and systems. |
| `tenet_kehillah_minhag_avoteinu` | Move practice effects to Communal Identity or Ritual Celebrations, avoid a duplicate tenet. |
| `tenet_kehillah_emunah_temimah` | Remove only after devotional/sermon effects have a vanilla home; otherwise flag shallow and reassess. |
| `tenet_kehillah_avelei_tziyon` | Preserve numeric save identity while changing display/mechanics to Sacred Homeland; use *Avelei Tziyon* for Karaite-specific movements rather than all adherents. |
| `tenet_kehillah_hokhmah`, `tenet_kehillah_kiddush_hashem` | Retain IDs; improve effects, names, and descriptions. |

Audit all literal and generated references in `scripts/kehillah_library_catalog.py`, the catalog JSON, generated study/citation/standing effects, personal tenets, book arguments, reform choices, custom localization, and faith history. Authored-work tenets use stable numeric indices: **never renumber old values in a save**. Retired IDs may remain as hidden legacy definitions or a migration bridge if the engine needs them; specify a deterministic mapping for rites and personal convictions, including DLC-off behavior. No startup `set_tenet_status` on a new game: put known/permitted/prohibited in `history/faiths/`; migrate old saves only once with an explicit version marker and check notifications.

## 7. Holiday eligibility and variation

Current files: `common/scripted_triggers/jewish_holiday_scripted_triggers.txt`, `common/on_action/jewish_holiday_on_actions.txt`, `events/jewish_holiday_events.txt`, `common/customizable_localization/jewish_holiday_feast_custom_loc.txt`. The first presently gives the six Jewish faiths (including the several Rabbinic rites) the five Torah festivals, gates Hanukkah to Rabbinic/Kabarism, and Purim to the wider Hebrew canon (including Karaism and Malabar). That is only an **occasion-level** distinction. Thirteen scenes include customs that cannot safely be reused for every observer of the occasion.

| Occasion / current IDs | Eligibility and required revision |
|---|---|
| Day of the seventh month / 0001–0002 | Shared calendrical occasion, **not one universal Rabbinic Rosh Hashanah script**. Honey and the Days of Awe wording need Rabbinic gate or separate rite text. Samaritan seventh-month observance and Haymanot New Year/atonement practice need their own verified descriptions; avoid automatic shofar, fixed Rabbinic date, and identical mood. |
| Passover / 0003–0004 | Shared liberation/Passover occasion. Four Questions and bedikat chametz are specific liturgical/halakhic forms: Rabbinic gate or authored non-Rabbinic variants, not mere name substitution. Samaritan Passover centers Gerizim and its own sacrificial practice; do not present it as a restored Jerusalem Temple cult. |
| Hanukkah / 0005–0006 | Rabbinic authority rites (including Kabarism if its adoption of the holiday is justified). Exclude Karaism, Haymanot, and Samaritanism. Review Malabar's historically transmitted practice rather than inferring it from a Toraic doctrine alone. |
| Purim / 0007–0008 | Esther-accepting traditions: Rabbinic, Karaite, and Malabar pending evidence. Exclude Samaritan and historically Haymanot. `Ad lo yada` and *mishloach manot* specifically need Rabbinic gate or a different Karaite Purim scene; accepting Esther does not imply accepting every Rabbinic custom. |
| Yom Kippur / 0009–0010 | Shared Day of Atonement with faith-specific theological, fasting, and prayer wording. Inspect Rabbinic liturgical phrases and Haymanot practice rather than treating all seven as identical. |
| Sukkot / 0011–0012 | Shared booths/festival occasion; inspect four species, roof rules, hospitality, Samaritan/Gerizim wording, and local customs at scene and option level. |
| Shavuot / 0013 | Shared festival, **different calendar calculations and emphases**. A worn book/study scene is possible, but a Rabbinic all-night study custom must not be universal. |
| Distinct Ethiopian/Samaritan observances | Research and add compact occasional scenes (for example Sigd and Samaritan Gerizim observances) only after date, practice, and period are verified. No modern liturgical detail presented as universal medieval practice. |

**Selection mechanics:** define scripted, doctrine-driven capabilities for each occasion (`observes_*`) and, separately, each practice (`uses_rabbinic_seder`, `observes_rabbinic_purim_custom`, `accepts_esther`, etc.). A rite-specific exception may be data-driven rather than a faith-name `OR` list where doctrine cannot distinguish the practice. Filter **before the yearly random draw**, then re-check at queue and display time after conversion or rite change; clear invalid pending flags and do not show a ghost event. Preserve one queued scene per character and the intended player/AI cadence; avoid one faith seeing fewer scenes solely because invalid events silently became quiet years. Only queue a scene with a compatible variant. The quarterly month windows are approximations, not a claimed Hebrew/Samaritan/Karaite calendar; text must not invent exact dates. The feast localization must check the host's practice, not merely `is_jewish_character_trigger`, for specific foods/Passover phrases. Expand the matrix to courtiers, landed rulers, and Kehillah leaders; use the same eligibility triggers for every path and for AI.

Ritual Celebrations increases the rate of **eligible** scenes and may add a small optional festival pool for its followers. Divine Liturgy instead affects prayer/piyyut performance. Personal adoption of either tenet can change the character's response/reward without causing a prohibited observance to fire. A personal tenet never changes the faith's canon.

## 8. Vanilla-style descriptions, icons, and tooltips

* Use a familiar **generic name** (Reasoned Theology, Sacred Homeland, Sacred Liturgy) and conditional Jewish name (Hokhmah, appropriate local homeland expression, Piyyut). Avoid Hebrew-only universal loc. Check rite-specific names where `rite_religion_tag = judaism_religion` is too coarse (Esotericism currently becomes Kabbalah for Karaites too).
* Description: two or three short, in-world sentences stating **belief, practice, and social consequence**, with no percentages, file keys, speculative historical universals, or developer language. Keep the effect panel as the source of mechanical numbers. Compare length and cadence to nearby vanilla tenets; avoid copywriting that promises mechanics we have not implemented.
* Effects panel: distinguish **Followers of this Rite** and **Personally Adopted**. Use vanilla modifiers for exact numbers and short localized parameter tooltips for unlocks. Name actions with player-facing verbs (“Challenge a scholar to debate,” “Compose a liturgical poem”), use one-line outcome descriptions and hover detail for chance/requirements. Do not display a Kehillah-only action as if every ruler can use it; either supply an equivalent general action or scope the line clearly.
* Show contested status and unavailable requirements accurately. Never advertise an ability whose `can_pick`, DLC gate, government, or doctrine prevents it. Use a legible unavailable reason, not hidden choices or a generic “nothing happens” outcome.
* Reuse a vanilla tenet icon only when its meaning survives the Jewish flavor; review Hokhmah's Alexandrian Catechism icon, Sacred Homeland's Inner Journey icon, Kiddush ha-Shem's Unrelenting Faith icon, and the current Hebrew-only/Christian imagery. Prefer vanilla-style silhouettes and contrast over visually identical icons across adjacent cores. No arbitrary Torah scroll for unrelated effects.
* Flavorful event details (e.g. reduced crisis stress, a particular book genre, holiday option) belong in event/decision tooltips and in hoverable examples, not an exhaustive tenet description. Check loc for non-Jewish adopters, dynamic rite changes, personal tenets, and both DLC states.

## 9. Implementation order and verification

1. Record the final open decisions in this document. Inventory tenet/holiday references and baseline xTiger. Keep concurrent dirty work in the shared main worktree intact.
2. Introduce capability triggers for canon, practice, and office; remove Prophecy of Malachi only once headship creation remains gated. Test all start dates and head/rite titles.
3. Fix holiday eligibility first: variant matrix and queue/display conversion cases. Do not broaden the event pool before existing thirteen are safe. Human-check one event per occasion for Rabbinic, Karaite, Haymanot, Samaritan, Malabar, and Kabarism.
4. Add generalized tenet hooks and split follower/personal effects. Confirm no bonus is Kehillah-only and no double application on rite plus personal adoption. Test vanilla literalist debate and new Hokhmah debate separately.
5. Migrate rite cores, faith history statuses, book catalog IDs, old saves and DLC-off fallback. Start a fresh 867, 1066, and 1178 game: **no “Rite Changed” startup notifications** for initial known statuses. Reload an old save and check personal tenets, books, holy sites, rites, and headships.
6. Run xTiger before and after script changes, compare findings, and record manual UI checks for names, icon clarity, tooltips, option availability, and player/AI holiday cadence. The current dirty worktree is not part of this proposed implementation.

## Research anchors to verify during implementation

* Ibn Daud's twelfth-century philosophical and historical works: <https://plato.stanford.edu/archives/spr2026/entries/abraham-daud/>.
* Karaite legal scholarship (not merely strict literalism): <https://cris.bgu.ac.il/en/publications/karaite-philosophy/>.
* Karaite Mourners of Zion and ascetic Jerusalem observances: <https://cris.bgu.ac.il/en/publications/karaite-mourning-of-zion-as-an-ascetic-movement/>.
* Samaritan calendar as described by the community: <https://www.israelite-samaritans.com/religion/calendar/>.
* Karaite versus Rabbinic observances and festival interpretations require period-specific source review; do not promote a present-day community description into an unqualified medieval claim.
