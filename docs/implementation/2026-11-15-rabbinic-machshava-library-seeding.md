# Rabbinic Machshavah library seeding

**Status: BUILT 2026-11-15 at Daniel's request; source checks pass and the xTiger baseline is unchanged; live check pending.**

This small seeding correction extends the community-library rules in
[the Sefer redesign](../spec/2026-11-08-sefer-system-redesign.md) and the
[library shelf and ledger record](2026-11-08-library-shelf-and-ledger.md).
It does not change canonical foundations, the Yeshiva curriculum, or the
standing of any work.

## What changed

New Rabbinic community-library seeds now include two basic Machshavah works
when their dates have passed:

- *Sefer Yetzirah* (400);
- Saadia Gaon's *Emunot ve-Deot* (933).

They are ordinary owned copies. They neither count as foundational works nor
become prerequisites for founding a Yeshiva. The gate remains the subject of
the separate rite-foundations follow-up identified during this review.

The effect explicitly uses `is_rabbinic_authority_jewish_trigger`; Karaites,
Samaritans, Haymanot, and non-Jewish holders do not receive these Rabbinic
copies. The existing Tanakh and rite-specific Talmud/curriculum seeds are
unchanged. The change applies to fresh game-start and newly founded-community
seeds; it deliberately does not conjure copies into an existing save.

## How discovery works

The Sefarim Ledger lists a work in circulation only when the shown community
or rite knows it. For a non-canonical, non-Foundational/Essential work, that
means one of:

1. the community owns it;
2. the player or a courtier has mastered it; or
3. it is at least Celebrated in that rite and a copy exists somewhere.

Before this change, the general starting seed excluded Machshavah completely.
That meant that the first two conditions could not occur in a fresh Rabbinic
1066 start, while most of those works were too obscure to meet the third.
The two entry works now make the field visible and seekable. More obscure,
esoteric, or polemical works remain intentionally discoverable only through
the same ownership/mastery/reputation path; there is not yet a separate
random-book-discovery action.

## Verification

- Source audit: both work flags exist in the catalogue; the date and Rabbinic
  authority gates surround each seed; neither appears in the generated
  foundational-missing calculation.
- `scripts/kehillah_library_catalog.py --check` must remain clean because no
  catalogue data or generated output changes.
- xTiger baseline: 0 fatal, 28 errors, 109 warnings, 37 untidy, 122 tips;
  the after result is recorded with delivery.
- Live test pending: start a new 1066 Rabbinic game, open the Sefarim Ledger,
  and confirm both entries appear under Machshavah and are held. Confirm a
  Karaite start does not receive them.
