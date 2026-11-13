# Expanded historical catalogue

**Status: BUILT 2026-11-12; source validated, live UI check pending.**

This is a catalogue expansion requested by Daniel. It builds on the language
and standing systems in [the 2026-11-10 language specification](../spec/2026-11-10-sefer-languages.md)
and the one-scale standing model in [the 2026-11-11 specification](../spec/2026-11-11-standing-one-scale.md).
The source of truth is `scripts/kehillah_library_catalog.json`; generated
catalogue, study, acquisition, ledger, shelf, language and review files must
not be edited by hand.

## What was added

- **Tannaitic and Amoraic / classical rabbinic:** *Sifra*, *Sifre Numbers*,
  *Sifre Deuteronomy*, *Seder Olam Rabbah*, *Avot de-Rabbi Natan*, *Pesikta
  de-Rav Kahana*, *Leviticus Rabbah*, *Lamentations Rabbah*, *Midrash
  Tanhuma*, *Targum Jonathan*, and *Targum Pseudo-Jonathan*.
- **Historical and disputable reading:** *Sefer Yosippon*, Philo's
  allegorical treatises, Josephus' *Jewish War*, and *Toldot Yeshu*.
  *Toldot Yeshu* is intentionally a Contested (tier 3) Machshavah work: a
  family of polemical narratives, not an authoritative theology text. Its
  in-game description says this explicitly and lets a rite's normal review,
  haskamah and cherem systems decide its later reception.
- **Karaite:** David al-Fasi's *Agron*, Salmon ben Jeroham's commentary, and
  Levi ben Yefet's *Sefer ha-Mitzvot*, alongside the existing Anan,
  Qirqisani and Yefet works.
- **Samaritan:** the Samaritan Pentateuch, Samaritan Targum, *Memar Marqah*,
  and the *Defter*.
- **Beta Israel:** the Ge'ez *Orit* and *Te'ezaza Sanbat*. They introduce
  CK3's already-vanilla `language_ethiopic` to this catalogue; Haymanot now
  treats Ge'ez as liturgical.
- **Indian Jewish:** the Copper Plates of Joseph Rabban, a Tamil community
  charter remembered in the Cochin tradition. It is deliberately a modest,
  Obscure historical-memory text, not a fictional Indian Jewish Talmud or
  school of philosophy.

## Standing and languages

The catalogue formerly had only Rabbanite and Toraic/Karaite baselines. It
now accepts optional `samaritan` and `haymanot` baselines. Unspecified works
remain Obscure to those traditions, rather than accidentally inheriting a
Rabbanite ranking.

The Samaritan Pentateuch and *Orit* are new special canon kinds. Each is
Divine only in its own tradition, and Obscure to other Jewish rites. This
keeps the existing Torah, Nevi'im and Ketuvim model intact while not treating
either as merely a low-ranked commentary. The two new language keys map to
vanilla `language_ethiopic` and `language_tamil`; Tamil is not made a
liturgical language.

Dates are deliberately approximate when a work is composite or transmitted
in recensions. In particular, *Te'ezaza Sanbat* is placed at 1200 as a
medieval availability marker, not a claim of a settled date of composition.

## Historical guardrails

The entries distinguish medieval Jewish reception from an author's date:
*Yosippon*, not Josephus' Greek work, is the ordinary medieval Jewish history;
the Greek Josephus and Philo entries are rare. The catalogue labels this in
their detail text. *Toldot Yeshu* is dated 1050 as the earliest secure
medieval-circulation marker for gameplay, not as a confident date of a single
original composition.

The Cochin community did preserve a learned Hebrew tradition, but evidence
does not warrant inventing an early medieval Indian Jewish scholarly canon.
Future work should add editions, liturgy or regional acquisition routes only
when the evidence and the language-edition design support them.

## Test checklist

1. Run `python scripts/kehillah_library_catalog.py` and confirm the generated
   files update without an unknown-language error.
2. Run xTiger against this checkout. New catalogue flags must have generated
   localization and no new parser errors.
3. In a Haymanot library, check that *Orit* is Divine and the Talmud remains
   unavailable/Obscure; in a Samaritan view, check that the Samaritan
   Pentateuch is Divine and the Samaritan Targum is readable with the Aramaic
   liturgical modifier.
4. In a Rabbanite library, check that *Toldot Yeshu* displays as Contested,
   not a foundational theological work; check that Ge'ez and Tamil work
   tooltips show their vanilla language names and an appropriate foreign
   language penalty for non-speakers.
