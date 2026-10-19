**Status: Implemented, source-checked, and fresh-boot verified on 2026-10-19.**

# Auxerre Kehillah

Daniel requested a 1066 Kehillah at Auxerre after learning that Rashi corresponded with its scholars.

## Historical basis

The *Jewish Encyclopedia* describes an important eleventh-century community whose rabbis were known as the sages of Auxerre and corresponded with Rashi: https://www.jewishencyclopedia.com/articles/2156-auxerre. The *Encyclopaedia Judaica* entry likewise treats a responsum from Rashi to the area's scholars as the first reference to the community: https://www.jewishvirtuallibrary.org/auxerre. Robert Chazan's study of northern French settlement also places Auxerre's leaders in the inter-communal network around Troyes: https://doi.org/10.3406/rjuiv.1969.1620.

Those sources establish the community and its scholarly character, but they do not securely name its officeholder on the CK3 start date. The mod therefore uses Yehuda (`9000225`), an explicitly representative, lowborn rabbi. This avoids moving the later Rabbi Hezekiah of Auxerre into 1066 or inventing a historical dynasty.

## Implementation

- `d_kehillah_auxerre` is an independent landless Kehillah duchy with vanilla `c_auxerre` as its capital county. Installed CK3 1.20.1 data confirms both `c_auxerre` and `b_auxerre`.
- Title history grants it to Yehuda on 1066.9.15 with the existing Kehillah government and appointment law.
- The start effect gives a modest 70-gold communal chest and runs the shared seed, quarter-record, and leader-flavor effects. Yehuda's rabbi trait makes the scholarly emphasis character-driven rather than a fabricated wealth claim.
- Startup registers Auxerre in `kehillah_registered_communities`; the title trigger recognizes it before that registry exists. The existing `d_burgundy` minhag tag places it in Western Ashkenaz without another geography override.
- Hidden console event `kehillah_debug.135` reports the complete starting-state checklist without mutating the campaign.

## Verification

A corrected fresh isolated boot reached the 1066 selector. `kehillah_debug.135` passed all eight assertions: holder, Yehuda, registry, Western Ashkenaz minhag, Kehillah government, domicile, `c_auxerre` location, and the Christian Host Charter. The targeted fresh error-log search found no Auxerre history, character, setup, or encoding error. See `docs/testing/2026-10-18-auxerre-kehillah-live-test.md`.
