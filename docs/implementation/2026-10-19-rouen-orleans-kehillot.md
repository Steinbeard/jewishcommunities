**Status:** Implemented and source-checked on 2026-10-19; intentionally not live-tested at Daniel's request.

# Rouen and Orléans Kehillot

This user-directed unit adds `d_kehillah_rouen` and `d_kehillah_orleans` as titular, landless
Kehillah duchies at the 15 September 1066 start. Their capitals are the verified CK3 1.20.1 county
keys `c_rouen` and `c_orleans`. Both use the established Kehillah government, appointment law,
startup effect, global registry and Western Ashkenaz geography pipeline.

Orléans is securely suitable as an eleventh-century start: Encyclopaedia Judaica describes its
community as already numerous at the beginning of the century and an important center of learning.
Rashi's Responsum 241 preserves a dispute between two Orléans Jews and places it in the scholarly
network linking Orléans, Paris and Troyes. Because no securely identified officeholder on the exact
bookmark date was found, Yitzhak (9000226) is an explicitly representative, lowborn rabbinic leader.

Rouen had an established medieval Jewish community and belongs in the 1066 Norman setting, but
claims about a formal invitation by William and some institutional reconstructions remain debated.
The implementation therefore makes only the conservative claim that a community existed. Yaakov
(9000227) is an explicitly representative, lowborn lay leader. He is not related to, and does not
replace, Yosef ben Menahem of Rodom (9000300). `d_kehillah_rouen` represents the local community;
`d_kehillah_rodom` remains Yosef's mobile financier/adventurer company.

Sources:

- Encyclopaedia Judaica / Jewish Virtual Library, “Orléans”:
  https://jewishvirtuallibrary.org/jsource/judaica/ejud_0002_0015_0_15199.html
- Simon Schwarzfuchs, “La médiation dans l'Orléans médiéval: le Responsum 241 de Rachi”:
  https://cris.iucc.ac.il/en/publications/la-m%C3%A9diation-dans-lorl%C3%A9ans-m%C3%A9di%C3%A9val-le-responsum-241-de-rachi/
- Norman Golb, *The Jews in Medieval Normandy*, Cambridge front matter and overview:
  https://assets.cambridge.org/97811074/06872/frontmatter/9781107406872_frontmatter.pdf
- The Medieval Review, review of *The Jews in Medieval Normandy*:
  https://scholarworks.iu.edu/journals/index.php/tmr/article/view/14762

`kehillah_debug.136` is a read-only future live probe for both starts. Per Daniel's instruction,
this unit does not launch CK3; validation is limited to source review, `git diff --check` and
`ck3-tiger` against the edited checkout.
