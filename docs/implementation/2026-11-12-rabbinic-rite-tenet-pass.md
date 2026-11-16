# Rabbinic rite tenet and authority pass

**Status: built 2026-11-12 in the shared worktree; source and xTiger checked; fresh-game live UI and runtime checks pending.** This extends [the medieval minhagim implementation](2026-11-12-medieval-rabbinic-minhagim.md) and the [Gaonate design](../spec/v47-gaon-and-the-seat-of-the-sanhedrin.md). It does not alter the Sefer canon or create a new rationalist rite.

## Starting cores

| Rite | Core tenets | Reason |
|---|---|---|
| Minhag Bavel (`rabbinism`) | Legalism, Ge'onut, Talmud Torah | Academy authority, law and the Bavli. The Ge'onut tenet does not require a living Gaon: the 1066 title remains vacant. |
| Minhag Ashkenaz | Legalism, Asceticism (*Hasidut*), Talmud Torah | Communal legal practice with penitence and demanding piety. This does not posit a separate Hasidei Ashkenaz rite or make the later Pietist circle coextensive with Ashkenaz in 1066. |
| Minhag Sepharad | Legalism, Religious Legal Pronouncements, Talmud Torah | Keeps its legal and Geonic inheritance without labeling all Sephardim philosophical rationalists. |
| Minhag Yerushalmi | Legalism, Ritual Celebrations, Talmud Torah | Palestinian liturgy, festival practice and rabbinic learning; the Yerushalmi canon remains a separate Sefer-system distinction. |
| Yordei Merkavah (`merkabah`) | Esotericism, Inner Journey, Talmud Torah | Esoteric ascent within Rabbinic textual tradition. Replaces Asceticism, which duplicated Inner Journey's contemplative emphasis. Vanilla's Inner Journey remains restricted when selecting new tenets; its inherited starting use needs a reform-UI check. |

All starting Rabbinic rites keep Talmud Torah as their Oral Torah identity tenet. The alternatives here are meant to express practice and emphasis, not incompatible theologies. The custom Ge'onut tenet still needs the separate all-governments and cross-religion audit requested by Daniel; this pass adds a modest Learning lifestyle bonus for all followers of a core Ge'onut rite, including landed rulers while its headship is vacant. Its additional headship effect remains Jewish-specific.

## Doctrines and authority

Ashkenaz keeps monogamy; Sepharad and Yerushalmi keep the faith's polygamy. All four regional Rabbinic minhagim have Recognition of the Sages. Yordei Merkavah now has it too and inherits the Jewish religion's pluralism, rather than using an unexplained stricter override. Marriage and other inherited doctrines stay as they were.

Rabbinic Judaism's `faith_details.head_of_rite = d_kehillah_gaonate` points to a **single title**. Vanilla Chalcedonian Christianity points the same field to `k_papal_state` while containing both Roman and Carolingian rites. Thus the earlier claim that the title can head only its holder's rite was too strong. The exact Rabbinic multi-rite scope still needs a runtime probe; the mod's yearly selection does stop offering a second holder while the title is occupied. A faith head could exercise overarching authority, but the existing landless head-of-faith test changed a Kehillah leader's government and lost his domicile; a landed Sanhedrin seat is the project's separate faith-head plan.

The vanilla Excommunicate interaction checks central sacraments and clergy, so the title alone does not grant Jewish excommunication. The mod's Pronounce a Cherem interaction does accept a head of rite; it previously allowed him to ban a member of **any** rite in his faith. It now checks whether he actually heads the **recipient's rite**, including a second rite if the engine recognizes him there. The head of faith or Sanhedrin Nasi may address any member of the faith. The existing yearly AI cherem pass already targets the penitent's own head of rite.

## Verification and outstanding checks

- Source audit: all five rite cores have three tenets; Ashkenaz's marriage doctrine is preserved; Yordei Merkavah no longer overrides pluralism.
- xTiger baseline before edit: 0 fatal, 16 errors, 110 warnings. After all changes: 0 fatal, 16 errors, 107 warnings, with no new fatal/error findings in changed files. The three missing Yordei adjective/adherent warnings were resolved.
- `git diff --check` passed after all changes.
- Fresh 867, 1066 and 1178 starts: confirm rite tenets and inherited doctrines in the faith UI; check Bavel's historical Gaon in 867, vacancy in 1066, and Baghdad Gaon in 1178. Test a same-rite and different-rite Pronounce a Cherem target, and inspect `error.log`. The delegated Luna tester could not establish CK3 process ownership because CIM access failed; no xTiger/CK3 MCP tools were available. Live test and log baseline are unrun; no game process was controlled.
