# Hokhmah and Andalusi Diwan Catalog Research

**Status: research used by the built 2026-11-15 library-catalog addition.** Supports [rite-weighted library seeding](../implementation/2026-11-15-rite-weighted-library-seeding.md) and the generated Sefarim catalog. It does not create a separate science display genre: this small, deliberately explicit natural-philosophy corpus uses the existing Machshavah shelf.

## Arabic philosophy and medicine

- *Theology of Aristotle* — circulation gate **840**. The [Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/theology-aristotle/) identifies it as an Arabic reworking of Plotinus' *Enneads*, given Aristotle's name, and places the relevant ninth-century Arabic adaptation in the circle of al-Kindi. The catalog calls it an attribution rather than accepting the title's claim. Its `composer` field names Arabic adapters of Plotinus, and its prose makes the uncertainty playable rather than hiding it.
- Galen, *On the Usefulness of the Parts* — circulation gate **850**. The [US National Library of Medicine's Arabic Galen collection](https://mainweb.awsprod.nlm.nih.gov/hmd/arabic/galen.html) documents the Arabic translation of this work associated with Hubaysh ibn al-Hasan; its broader account of [Galen's Arabic reception](https://www.ncbi.nlm.nih.gov/books/NBK519309/) places Greek scientific and medical translation in the eighth-century and later Islamicate world. The game's 850 is a conservative representative availability date, not a claim about a particular surviving manuscript.

Both works are shared-tradition, non-canonical and Obscure. They teach `tenet_kehillah_hokhmah`, allowing the existing Machshavah "change minds" machinery to treat philosophy and medicine as contested intellectual learning rather than as Jewish foundational doctrine.

## Andalusi Hebrew poetry

- Dunash ben Labrat, *Poems* — circulation gate **990**. The [Princeton Geniza Project profile](https://geniza.princeton.edu/en/people/dunash-ben-labrat/) dates Dunash roughly from 920 to after 985 and notes both Arabic-meter Hebrew poetry and liturgical work. The catalog title says “Poems,” not “Diwan,” because the entry represents surviving work rather than a falsely definite authorial volume.
- Samuel ha-Nagid, *Diwan* — circulation gate **1056**. The [Jewish Encyclopedia entry](https://sefaria.jewishencyclopedia.com/articles/11272-nagdela-samuel-ibn) describes his surviving diwan manuscripts and *Ben Mishle*. The catalog uses his death year as a clean availability threshold while explicitly saying that only part of the manuscript tradition survives.
- Solomon ibn Gabirol, *Diwan* — circulation gate **1058**. The project's [historical character tracker](../data/historical-character-tracker.csv) records a death date around 1058 with later uncertainty. The catalog uses that representative date and names the uncertainty in its prose instead of inventing a precise publication event.

All three are Rabbanite Parshanut works with the `poetry` kind and teach Sacred Liturgy. That lets the existing sermon routing recognize them and gives a Sacred-Liturgy Rabbinic community one date-valid poetic collection during its opening seed. The seed is a single separate draw, not a general Parshanut-weight boost: liturgy shapes its own shelf without making all communities poetry-heavy.

## Deliberate limits

This is not an attempt to simulate a complete Andalusi canon, a universal Arabic translation market, or a generic “science” category. Further additions should be individually sourced and date-gated. Candidate future material includes Euclid and Ptolemy, but they should not enter as a broad random list until their Arabic circulation, player-facing framing, and gameplay role have been audited.
