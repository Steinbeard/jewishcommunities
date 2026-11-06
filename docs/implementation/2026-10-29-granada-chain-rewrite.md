**Status:** Implemented and source/xTiger checked, 2026-10-29. Live verification
is **UNRUN**: the Luna tester could not inspect CK3 process ownership. This is
a writing and character-staging pass, not the proposed Nagid-office or Granada
balance feature. Supersedes the opening presentation and prose of
[V39 section 9](../spec/v39-pogroms-and-the-popular-crusade.md) and
[V43 slice 1](../spec/v43-after-the-violence-and-granada.md); their mechanical
outcomes remain in force. Follows the [writing guide](kehillah-writing-style.md).

# Granada: establish the inheritance before the warning

Daniel asked for a clearer event-chain rewrite and suggested a letter from an
Abu Ishaq character at Badis's court. The revised sequence gives Yoseph his own
introduction to the material previously explained more fully to other communities.

| Day from 15 September 1066 | Event | Purpose |
|---|---|---|
| 7 | `kehillah_granada.0008`, Your Father's Office | Two petitions establish the minister's work, communal patronage, Samuel's legacy, and the Sanhaja ruling establishment. |
| 30 | `.0019`, hidden dispatcher | Checks whether the named poet is alive at the host's court. |
| 30 | `.0018`, A Letter from Abu Ishaq | Native `letter_event`, sender 9000235; a fictional covering letter explains the argument of the verses addressed to the emir. |
| On acknowledgement, or immediately if the sender is unavailable | `.0001`, The Verses Reach the Street | The elders' response scene retains the existing four choices and their effects. |
| 45 | `.0006`, The Road to Lucena | The family considers shelter with the existing Lucena contacts. |
| 65 | `.0002`, The Emir's Confidence | Identifies the old poisoning allegation and the new Almeria charge as accusations. |
| 106, unless accelerated by the existing Almeria failure | `.0003`, hidden resolution | Existing cancellation/mob branch; narrative no longer announces 30 December when the attack occurred earlier. |

The quiet ending, palace/quarter attack, death notice, and the four Sephardi
correspondence reports are rewritten. They no longer claim an unobserved casualty
total or the complete disappearance of Granada's Jews. The surviving-son clause
only asserts survival, matching its actual alive check; it no longer assumes a
living son must already be in Lucena. Household refuge reports avoid claiming that
both wife and son travelled when only one might have remained with Yoseph.

The bookmark introduction now explains the dual offices and immediate political
conflict without introducing a separate Almoravid thread.

## Historical evidence and authored staging

- Abu Ishaq Ibrahim ibn Masud al-Ilbiri was a Muslim jurist and poet. His invective
  against the Jewish minister addresses Badis, attacks Jewish authority over
  Muslims and calls for lethal violence and confiscation. Its exact date and its
  role in causing the massacre are uncertain. Nicola Carpentieri,
  [Abu Ishaq al-Ilbiri: a Literary Revisitation](https://doi.org/10.5565/rev/medievalia.385),
  pp. 67-69, distinguishes the poem from the later causal account; Ibn al-Khatib's
  explicit association is three centuries later. An accessible
  [author-posted text](https://www.researchgate.net/publication/338636920_Abu_Ishaq_al-Ilbiri_a_Literary_Revisitation)
  was consulted.
- Yoseph's succession to Samuel, scholarly patronage and the family's refuge in
  Lucena are discussed in the
  [Jewish Encyclopedia entry](https://jewishencyclopedia.com/articles/11271-nagdela-nagrela-abu-husain-joseph-ibn).
  That older account's assertions about motives and character are not treated as
  omniscient narration in the new events.
- **Authored, not documented:** Abu Ishaq's residence in Badis's CK3 court, his
  personal covering letter to Yoseph, the petitions and private conversations.
  The letter paraphrases the political argument; it is not a translation or a
  surviving historical document. The original poem is not presented as a private
  letter originally addressed to Yoseph.
- Character `9000235`, `history/characters/kehillah_abu_ishaq.txt`: birth 990 is an
  estimate for a late-tenth-century birth; death 1067 is the recorded year, with
  estimated day/month. Andalusian culture, Maliki rite, skills and traits are
  gameplay representations. The author was Arab, not a Sanhaja chief.
- Vanilla Badis is `45016` in `game/history/characters/berber.txt`. Placement runs
  only when he is the physical host's top ruler, and once per poet, so a probe
  never forces a poet who left during play back into his court. His absence or
  death falls back to the ordinary report without a letter from a dead sender.

## Scope and validation

The startup scheduler is now once-only, confined to Yoseph and the 1066 opening.
Existing saved queues still point to `.0001` and remain valid. The Historical
Crises game rule continues to suppress the chain. The new introduction is flavor
only. No pillar, building, income, office, council, succession, chance, mob-size
or severity balance is changed. The larger Nagid institution and starting-standing
revision remain separate work; this pass does not claim to implement them.

`kehillah_mob_debug.10` now runs the intro, warning, family and existing crisis on
a short clock. `kehillah_mob_debug.30` reports sender availability without changing
state. Source comparison checks the unchanged option effects and probabilities.
xTiger before/after: **0 fatal, 8 errors, 80 warnings, 1 untidy, 43 tips**;
no new reports. The existing missing Gaon nickname warning in the older Granada
family file is unchanged. Text retains UTF-8 BOMs and valid localization keys.

See the [test record](../testing/2026-10-29-granada-chain-rewrite-live-test.md)
for the blocked live attempt and the remaining rendering/runtime checks.

## Isolated source and publication

The usual Codex worktree could be read but was outside this session's writable
paths. Creating an independent Git checkout was also denied at Git metadata
writes. The primary checkout was initially left untouched. A Git archive of `origin/master`
was exported to `C:\Users\Daniel\AppData\Local\Temp\kehillah-granada-source-20261029`;
the GitHub connector independently confirmed that its base,
`e66049c379643661db60c8724abef19a390766bf`, was current remote `master`.
This source export was edited and validated. The connector rejected branch
creation with HTTP 403, so publication resumed through the authenticated GitHub
browser on `codex/granada-letters-20261029`, based on the then-current remote
`master` (`2ca503e`). Source comparison confirmed that later master changes did
not overlap the nine files in this feature.

Daniel subsequently requested the same changes in the main worktree. Its nine
target files still matched the archive base, and the patch was applied there
without changing its branch or existing commits. Main-worktree xTiger results
are unchanged: **0 fatal, 15 errors, 103 warnings, 1 untidy, 43 tips**. The
original isolated-source result above remains a separate baseline. Main-worktree
originals were backed up before copying. A future live check may use this updated
main source, with explicit process ownership, or the published branch; the usual
Codex worktree has not been updated.

## 2026-10-29 revision: the poem brought by a clerk

**Supersedes:** the private-letter staging, sender-dependent dispatch and relevant
live-check descriptions above. Daniel requested an actual excerpt and preferred
someone sharing the poem with Yoseph. `.0018` is now a normal character event,
**A Copy of the Verses**. An unnamed clerk brings a circulating text; this delivery
is an authored scene. `.0019` remains a hidden relay for existing event queues,
but always opens `.0018`. The poem can circulate after its author dies or leaves
court. Acknowledgement still opens `.0001`; all four response option blocks,
probabilities and the hidden resolution remain unchanged. Abu Ishaq remains a
character at Badis's court as previously requested, without acting as sender.

The italicized passage is a new English translation from the public-domain Arabic
of *Ala qul li-Sanhajatin ajma'in* ("Say to all the Sanhaja"), not invented
threatening prose or a quotation copied from a modern English translation. The
selected couplets occur at Arabic Wikisource lines 244-246 and 256-258:
[Arabic text](https://ar.wikisource.org/wiki/ألا_قل_لصنهاجة_أجمعين).
The wording was cross-checked against the Arabic reproduced at
[Qaseda](https://qaseda.com/abuishaqalllbiri/ألا-قل-لصنهاجة-أجمعين/).
These are online transcriptions, not a new manuscript collation. The historical
qualification about dating and the massacre's causes above remains in force.

> فبادر إلى ذبحه قربة / وضح به فهو كبش سمين
>
> ولا تحسبن قتلهم غدرة / بل الغدر في تركهم يعبثون

Translated for this mod:

> Hasten to slaughter him as an offering;
> sacrifice him, for he is a fattened ram.
> ...
> Do not think killing them is treachery;
> treachery is leaving them to run riot.

The ellipsis marks the two omitted couplets, which demand pressure on the Jews
and seizure of their wealth. The surrounding event explains that demand. The
first quoted couplet targets Yoseph; the later one extends the incitement to his
people. The narration attributes the demands to the poem. No modern political
analogy or broader claim about Muslims is introduced.

Source checks compare the response and resolution blocks with the pre-revision
snapshot; the debug report now describes court placement as optional for the
poem scene. Live rendering of line breaks and italics remains pending.

**2026-11-06 addendum:** at Daniel's request `.0018` is now **Crisis: Sinister
Verses**. It opens on the growing resentment and closes on the risk of violence.
While Abu Ishaq lives, the clerk heard him recite it himself in the town square.
This supersedes the unnamed-text delivery above, which survives as a fallback if
he is dead: the clerk heard it recited and names him as its author. The translated
couplet is unchanged. The scene is authored; the historical qualification above
still applies.

**2026-11-06 addendum:** at Daniel's request `.0008`, Your Father's Office, now
opens with a short paragraph as the chain's first scene: ten years since Samuel's
death (1056), what each office means, and a light hint of resentment that leaves
the sharper statement to `.0018`. One clause carries the second petition from
Yoseph's desk to the palace. Text only; live rendering is unchecked.

**2026-11-06 addendum, `.0002`:** at Daniel's request The Emir's Confidence now offers three bets. The defense is a Diplomacy `duel`, 35 against 65, moved by Diplomacy x 2 and his opinion x 0.25; this replaces `kehillah_granada_loyalty_chance_value`. Naming Samuel's debt stays a sure +12 Spared for Prestige and now also costs 10 of his opinion. Staying at work adds +5 Stability to its Prestige gain and +6 Armed.

**2026-11-06 addendum, later:** this supersedes the Burn and Emir odds in the table below. Both now use a `duel` against `medium_skill_rating`, so the game shows the skill and factors. Burn is 50 +/- 3.5 per skill point, at least 15. The emir is 35 against 65, moved by Diplomacy x 2, his opinion x 0.25 and `kehillah_lord_outlook_odds_modifier`. `kehillah_granada_burn_chance_value` is removed. Each gamble now sends a toast, because the result was otherwise invisible.

**2026-11-06 addendum:** at Daniel's request the three `.0018` answers are now
different bets, so none is simply best. This supersedes their earlier effects:
the elders gave +6 Spared, burning gave +12 Armed, and the emir gave +12 Spared
or +6 Armed. The old hover showed the catalyst's default 12 for every push, so the
elders looked twice as strong as they were.

| Answer | Effect |
|---|---|
| Elders | Certain +6 Spared, -5 Stability, -5 attack severity |
| Burn | Stress relief. Intrigue roll (30 + 2 x Intrigue, 15 to 75): +12 Spared, or +6 Armed |
| Emir | Existing Diplomacy and opinion roll: +12 Spared and `kehillah_mob_condemned`, or +12 Armed |

Race pushes now sit in `hidden_effect`, and the tooltips name their sizes. Balance
is by calculation only; it has not been played.

## 2026-10-29 correction: al-Mariyyah's political position

Daniel observed that al-Mariyyah is Badis's vassal in the game. The installed
1.20.1.2 `game/history/titles/k_andalusia.txt` confirms this: `c_almeria` has
holder `45006` (al-Mu'tasim) from 1052 and an explicit `liege = d_granada` entry
at 1066.1.1; the next independence entry is 1073.1.1. `d_granada` is held by
Badis (`45016`) from 1038. The existing event's county-holder scope therefore
selects the intended character, but the prose's assumption of a foreign sovereign
was wrong for this bookmark.

All six Almeria references in this localization file now use
`[GetTitleByKey('c_almeria').GetNameNoTier]`, allowing the title's current localized
name (vanilla `cn_al_mariyyah`, "al-Mariyyah") to follow the map and culture
rather than hardcoding either spelling. The warning describes seeking another
lord's protection. The treason allegations concern helping that lord seize
Granada; they do not assert that he rules an independent state. No vanilla
political history, scope target, option odds or balance was changed.

### Historical rivalry retained

Daniel then observed al-Mariyyah's ruler declare war on Badis. The earlier
wording correction concerns **independent foreign status**, not the existence of
political rivalry. The *Encyclopaedia of Islam*, second edition, XI, "Zirids",
p. 515, records Ibn Sumadih's seizure of Guadix and Badis's recovery in 459/1067.
Amelina Ramon Guerrero, [Samuel ibn Nagrella y su hijo Jose en las Memorias de
'Abd Allah](https://revistaseug.ugr.es/index.php/meahhebreo/article/download/12989/11212/36779),
pp. 435-436, discusses the allegations of Yoseph's collusion and explicitly
questions the claimed surrender plot. These allegations remain allegations in
the events. The revised prose supports a hostile vassal, a rebel or an independent
lord without a hardcoded change to vanilla's political setup. No historical war
has been newly scripted or inferred from the reported in-game declaration.

Final source/validator pass for the poem and place-name revisions: unchanged
0 fatal, 15 errors, 103 warnings, 1 untidy, 43 tips; six localized title-name
references; UTF-8 BOM and localization markup checks pass. Native event rendering
remains unrun. The separate adult-personality completion is documented in
[its own record](2026-10-29-personality-trait-completion.md).

Publication remains unfinished: the feature branch was created, but no feature
commit or PR was published. Connector writes returned HTTP 403, and the browser
route stopped when it could not verify the active URL. Local Git metadata is
read-only in this session, so the main-worktree changes remain available for
play and review without a commit directly to master.
