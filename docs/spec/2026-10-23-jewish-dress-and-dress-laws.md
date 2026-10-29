**Status: PROPOSAL — 2026-10-23. Research and design only; no portrait assets, dress laws, or gameplay rules are implemented.** This addendum depends on [V14's existing Kehillah portrait rule](v14-kehillah-title-tier.md#portraits) and [V16's realm settlement policy](v16-jewish-settlement-policy-and-charters.md). It does not supersede either. Dress regulation is a separate host-realm question, not an extra rung of settlement policy. Implementation belongs after the current ROADMAP work unless Daniel explicitly prioritizes it.

# Jewish dress, headwear, and imposed dress laws

## Purpose and historical boundary

Jewish characters should look like people who live in their own region and century. A Kehillah leader in Worms, a scholar in Baghdad, and a married woman in Fustat should not share one generic "Jewish costume." Some headwear expressed communal identity; other garments and badges were imposed by rulers. The portraits should show both experiences without treating an imposed mark as a religious custom or making all Jews of an area dress alike.

The first playable scene is Worms in 1066. It predates the Fourth Lateran Council (1215) and the best documented later badge ordinances. Do not start Worms with a yellow badge or assume that every male Jew already wears a pointed Judenhut. The pointed hat is a candidate for later northern European variety; its depiction in medieval art is not a census of actual wearers. In the Islamic world, the ordinary base is similarly local dress, with colour restrictions added only where supported by a particular rule.

## Historical evidence and design consequences

| Evidence | Design consequence |
|---|---|
| The [Fourth Lateran Council's Canon 68 (1215)](https://www.laits.utexas.edu/bodian/me-canon68.html) required Jews and Muslims of both sexes to be distinguishable by public dress in Christian lands. It prescribed no universal badge shape or colour and observed that dress already differed in some provinces but not others. | 1215 unlocks Christian dress-law pressure; it does not automatically put one asset on every Jewish portrait in Christian Europe. |
| The [English Statute of Jewry (1275)](https://www.nationalarchives.gov.uk/education/teaching-resources/jews-in-england-in-1290/) required Jews over seven to wear a yellow, double-tablet badge. England had earlier badge orders, but the National Archives distinguishes those from the 1275 broad requirement. | Use a yellow tablet-shaped badge for a 1275 English historical rule. Do not use a yellow star or assume universal enforcement from 1215. |
| [Louis IX's French ordinance (1269)](https://telma.irht.cnrs.fr/outils/relmin/extrait270990/) required a yellow circular badge. The [transcribed ordinance](https://oaja.org/acts/1269-06-19-law-issued-by-louis-ix/) specifies badges on the outer garment at the chest and back. | Use a round *rouelle* for this French rule; a portrait can display its chest mark, while UI text can describe the full requirement. |
| A [study of a Mamluk account of the 1301 decree](https://www.cambridge.org/core/journals/journal-of-the-royal-asiatic-society/article/abs/if-the-cap-fits-going-mongol-in-thirteenth-centurysyria/6754A11FD98E26B28F2EC9BE304AD6A4) records yellow turbans for Jews and blue for Christians. A [study of Almohad differentiation](https://www.tandfonline.com/doi/full/10.1080/09503110.2024.2306087) records special clothing and later yellow clothing or turbans in the Maghrib. | Yes, rulers sometimes required distinct colours, including yellow. Model only a dated regional law; yellow is neither an inherent Jewish colour nor a blanket Muslim-realm rule. |
| [Research on the pointed Jewish hat](https://www.jstor.org/stable/24709777) traces it as a distinguishing sign especially in German-speaking regions from the twelfth century onward. [The Met's fourteenth-century cup](https://www.metmuseum.org/art/collection/search/469869) bears three Jewish hats in a heraldic device. | Offer a northern European pointed-hat asset with a date and region gate. It may appear without a coercive dress law; a badge law and a hat should not be conflated. |
| [Cairo Geniza bridal inventories](https://www.cambridge.org/core/journals/ajs-review/article/abs/three-trousseaux-of-jewish-brides-from-the-fatimid-period/2470B5BF9E7176246B4D9B2114645592) include women's headwraps and veils. [A study of Egyptian dress](https://www.tandfonline.com/doi/full/10.1080/09503110.2017.1416855) notes both face veils in Jewish inventories and turbans used by men. | Married women's regional hair coverings and Middle Eastern men's caps/turbans are valuable portrait variety. They do not need a hostile law to appear. |

The European evidence also supports ordinary regional tunics, gowns, cloaks, and veils instead of a unique Jewish cut for every garment. Married women's hair covering should follow marriage and regional style, not Jewish faith alone; unmarried women's appearance should remain varied. Do not introduce modern-looking wigs or a universal modern kippah as medieval defaults.

## Portrait layers

1. **Regional base outfit.** Keep V14's rank correction: a landless duchy-tier Kehillah leader does not dress as a duke. Extend its regional commoner clothing into a few modest, prosperous, and scholarly variants where art is available. Other Jewish characters retain the clothing of their region and standing. This is cultural variety, not a coercive policy signal.
2. **Personal headwear.** Candidate assets: a northern European brimmed or pointed hat, ordinary European caps, Middle Eastern caps and wrapped turbans, and regionally appropriate veils or wraps for married women. Use weighted variety and a date/region check for the pointed hat. Religious/situational outfits and player barbershop choices should have precedence unless live testing shows a reason to override them.
3. **Imposed visible mark.** A separate realm dress law can add a badge or mandate a colour. The first Christian badge assets are the French round *rouelle* and English double tablets. The mark should remain legible on a bust portrait at normal UI scale. The same law applies to eligible Jewish women as well as men unless that specific rule says otherwise; the underlying veil or hat stays regional.

Where CK3 cannot layer a badge cleanly over an arbitrary garment, make compatible marked variants of a small set of outer garments. The art spike must establish whether a separate accessory can anchor to the torso and remain visible across poses, clothing variants, and male/female body shapes before choosing that path. Do not fork all vanilla outfits merely to place one badge.

## Dress-law model

Store an optional **Jewish dress rule on the host realm title**, resolved through the same host as V16's settlement policy. Its absence means no imposed distinction. Keep the two systems independent: an Encouraged realm can retain an inherited dress mandate, and a Discouraged realm need not have one. Show both facts separately in UI. A later design may let a ruler enact, relax, or exempt the rule; this spec does not silently add a new player decision or policy effect.

Proposed values are `none`, `distinctive_badge`, and `distinctive_headwear_or_colour`, with a regional form key rather than a universal colour. The exact storage representation is an implementation choice. The applicable law must resolve from the character's **actual host realm**, including landless community leaders and Jewish courtiers; verify the scope path rather than assuming the character's own primary title is the host. A visitor or exile should use the location where the portrait is being represented only if that is mechanically reliable; otherwise limit the first pass to resident characters and say so in its tooltip.

For the first historical content pass:

| Setting/date | Proposed form | Default treatment |
|---|---|---|
| Worms, 1066 | No imposed mark | Regional clothing and optional ordinary headwear only. |
| Christian Europe after 1215 | Dress-law pressure becomes possible | No continent-wide instant badge. A ruler, event, or authored local rule must choose a form. |
| France, 1269 | Yellow circular *rouelle* | Authored historical rule for the relevant French realm at or after the ordinance, subject to alternate-history ownership and a live-tested initialization path. |
| England, 1275 | Yellow double-tablet badge | Authored historical rule while a Jewish community exists there. Earlier orders are historical context, not an assumed fully enforced 1215 start. |
| Mamluk realm, 1301 | Yellow turban for Jewish men | A later regional package; do not apply to all Middle Eastern Jews. Research women’s rule before choosing a female asset. |
| Almohad Maghrib, late twelfth–early thirteenth century | Distinctive garment, then yellow clothing/turban where dated | Separate regional research and event; do not copy the Mamluk form. |

These dated defaults are research targets, not implemented events. Check which CK3 title holder, faith, and geography correspond to each ordinance before authoring history. Law changes must update portraits without making existing charters or settlement policies change automatically. On repeal or departure from the host, the imposed mark disappears; ordinary dress remains.

## Asset and implementation path

Start with a **single northern European pointed hat and one torso-visible round badge**, then expand to English tablets and other regional clothing after the portrait pipeline passes. AI text-to-3D or image-to-3D can produce a reference mesh; Blender work is expected for shape, topology, UVs, materials, head/hair fit, and the game's export format. Do not assume an AI-generated FBX/GLB is already a CK3 accessory. Confirm licences for any generated or third-party material before including it in the repo.

Register each finished mesh/entity as a portrait accessory and gene template, then select it with `kehillah_` portrait modifiers and scripted triggers. Inspect CK3 1.20's installed accessory/entity and portrait-modifier definitions while implementing. V14's existing `kehillah_plain_clothing` has priority 2 and explicitly removes headgear; the new headwear selection must replace or be ordered after that rule while preserving higher-priority religious and situational dress. Avoid copying a broad vanilla portrait file when a small additive modifier works.

Use art references as evidence of period form, not as proof that every illustrated person actually wore a garment. A stylized hat silhouette is acceptable if the date and place are honest; badge shapes and colours should follow the particular ordinance.

## Verification before shipping

- Source-check every region/date gate and the host-realm lookup. A 1066 Worms debug portrait must have no imposed badge; the France and England historical dates must select different badge shapes; a realm with no dress rule must not inherit one from its settlement policy.
- Run xTiger on every changed script/loc/gui file, comparing findings to the branch baseline. Add console-only debug events or `debug_log` probes for host, date, selected dress rule, and whether the law was repealed.
- Have a Luna subagent perform the live CK3 check required by this repo: male/female adult portraits, married/unmarried women, ordinary/religious/situational outfits, multiple zoom scales, and policy change/repeal. Check `error.log` for portrait asset and tooltip errors. Record a dated testing note. Asset rendering cannot be declared verified from script inspection alone.
- Confirm that portrait changes do not grant economic or stability effects by themselves. Any gameplay cost, exemption, resistance, or communal response to an imposed law needs a separately documented design decision.
