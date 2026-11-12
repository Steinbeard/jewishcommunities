"""Generate the Beit Midrash library catalog from one table.

Run from the repository root:  python scripts/kehillah_library_catalog.py

ADDED 2026-10-15; WIDENED 2026-11-08 for the Sefer redesign
(docs/spec/2026-11-08-sefer-system-redesign.md, build record in
docs/implementation/2026-11-08-sefer-redesign-build.md).

Each work is ONE row in kehillah_library_catalog.json.  Since 2026-11-08 this
script also writes every per-work list the mod used to keep by hand -- study
dispatch, ownership triggers, the selected-book GUI actions, donation, the
reader roster, the yeshiva's mastery draw -- so a new work is added in one
place.  Its outputs:

  common/script_values/kehillah_library_catalog_values.txt
      per-work numbers the GUI reads dynamically, keyed by the work's flag:
        kehillah_lib_genre_<flag>      1 parshanut, 2 talmudics, 3 hashkafa
        kehillah_lib_rank_<flag>       shelf band 1 foundational .. 5 obscure
        kehillah_lib_frame_<flag>      frame in kehillah_sefer_rank_frames.dds
        kehillah_lib_year_<flag>       composition year (the game date)
        kehillah_lib_corpus_<flag>     0 none, 1 Bavli, 2 Yerushalmi, 3 Tanakh
        kehillah_lib_canon_<flag>      0 none, 11 Oral Torah, 12 Prophets and
                                       Writings, 13 Torah
        kehillah_lib_tradition_<flag>  1 Rabbanite, 2 Karaite, 3 shared
        kehillah_lib_slot_<flag>       genre * 10 + band (shelf order), 0 in a corpus
      Authored-slot works read genre, year and slot from global variables.
  common/script_values/kehillah_library_standing_values.txt
      standing: per-work ceiling, floor and baseline (rite scope) and the
      viewer's standing (character scope), section 3 of the spec.
  common/scripted_effects/kehillah_library_study_generated_effects.txt
      study dispatch by numeric ID, the yeshiva's mastery draw, the per-work
      after-study hooks (tenets taught) and the standing dispatchers.
  common/scripted_triggers/kehillah_library_generated_triggers.txt
      track ownership, the current-work checks and per-work availability.
  common/scripted_guis/kehillah_library_study_gui.txt
  common/scripted_guis/kehillah_library_readers_gui.txt
  common/scripted_guis/kehillah_library_work_actions_gui.txt  (donate, studied)
  localization/english/kehillah_library_catalog_l_english.yml
  localization/english/kehillah_library_catalog_prose_l_english.yml
      prose for works added after 2026-11-08 (older works keep hand-written
      prose in kehillah_library_panel_l_english.yml).
  common/customizable_localization/kehillah_library_authored_custom_loc.txt
      the titles and kinds of books written during play.
  common/script_values/kehillah_library_language_values.txt
  common/scripted_effects/kehillah_library_language_generated_effects.txt
      2026-11-10: the reader's fluency in each work's language (`lang`), the
      Learning a mastery needs, and reading as practice in Hebrew or Aramaic.
  plus, as before, the acquisition and V49 journey files listed below.

The authors the hover card links to are NOT generated: they are real
characters written by hand in history/characters/kehillah_library_authors.txt.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/kehillah_library_catalog.json"
VALUES = ROOT / "common/script_values/kehillah_library_catalog_values.txt"
STANDING_VALUES = ROOT / "common/script_values/kehillah_library_standing_values.txt"
STUDY_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_study_generated_effects.txt"
TRIGGERS = ROOT / "common/scripted_triggers/kehillah_library_generated_triggers.txt"
STUDY_GUI = ROOT / "common/scripted_guis/kehillah_library_study_gui.txt"
READERS_GUI = ROOT / "common/scripted_guis/kehillah_library_readers_gui.txt"
ACTIONS_GUI = ROOT / "common/scripted_guis/kehillah_library_work_actions_gui.txt"
LOC = ROOT / "localization/english/kehillah_library_catalog_l_english.yml"
PROSE_LOC = ROOT / "localization/english/kehillah_library_catalog_prose_l_english.yml"
AUTHORED_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_library_authored_custom_loc.txt"
ACQUIRE_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_acquisition_effects.txt"
ACQUIRE_GUI = ROOT / "common/scripted_guis/kehillah_library_acquire_work_gui.txt"
ACQUIRE_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_library_acquisition_custom_loc.txt"
CATALOG_LIST_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_catalog_list_effects.txt"
JOURNEY_GUI = ROOT / "common/scripted_guis/kehillah_library_journey_gui.txt"
JOURNEY_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_journey_generated_effects.txt"
JOURNEY_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_library_journey_custom_loc.txt"
STUDY_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_study_torah_custom_loc.txt"
# 2026-11-08: the Beit Midrash shelf and the Sefarim ledger.
SHELF_VALUES = ROOT / "common/script_values/kehillah_library_shelf_values.txt"
SHELF_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_shelf_effects.txt"
LEDGER_LOC = ROOT / "localization/english/kehillah_library_ledger_catalog_l_english.yml"
# 2026-11-10: the languages a book is written in (docs/spec/2026-11-10-sefer-languages.md).
LANGUAGE_VALUES = ROOT / "common/script_values/kehillah_library_language_values.txt"
LANGUAGE_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_language_generated_effects.txt"
# 2026-11-11: the Bet Din docket by order of the Mishnah
# (docs/spec/2026-11-11-rulings-sermons-and-gates.md section 2).
CITE_TRIGGERS = ROOT / "common/scripted_triggers/kehillah_din_citation_generated_triggers.txt"
CITE_EFFECTS = ROOT / "common/scripted_effects/kehillah_din_citation_generated_effects.txt"
CITE_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_din_citation_custom_loc.txt"
# 2026-11-11: sermons cite Parshanut works by kind (same spec, section 3).
SERMON_EFFECTS = ROOT / "common/scripted_effects/kehillah_sermon_generated_effects.txt"
SERMON_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_sermon_custom_loc.txt"
# 2026-11-11: Machshavah changes minds (same spec, section 4).
MINDS_EFFECTS = ROOT / "common/scripted_effects/kehillah_minds_generated_effects.txt"
MINDS_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_minds_custom_loc.txt"
# 2026-11-11: reviews, haskamah and cherem (docs/spec/2026-11-11-reviews-and-cherem.md).
REVIEW_TRIGGERS = ROOT / "common/scripted_triggers/kehillah_review_generated_triggers.txt"
REVIEW_EFFECTS = ROOT / "common/scripted_effects/kehillah_review_generated_effects.txt"
REVIEW_GUI = ROOT / "common/scripted_guis/kehillah_review_gui.txt"
REVIEW_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_review_custom_loc.txt"
STANCE_VALUES = ROOT / "common/script_values/kehillah_review_stance_values.txt"
REVIEW_AI_EFFECTS = ROOT / "common/scripted_effects/kehillah_review_ai_generated_effects.txt"
# 2026-11-11: the cherem trait's teshuvah surrenders forbidden books.
CHEREM_TRIGGERS = ROOT / "common/scripted_triggers/kehillah_cherem_generated_triggers.txt"
CHEREM_EFFECTS = ROOT / "common/scripted_effects/kehillah_cherem_generated_effects.txt"
# A work's `lang` key and its CK3 language. All vanilla; vanilla's Hebrew is
# language_israelite (spoken by the extinct `hebrew` culture). Judeo-Arabic is Arabic.
READING_LANGUAGES = {
    "hebrew": "language_israelite",
    "aramaic": "language_aramaic",
    "arabic": "language_arabic",
    "greek": "language_greek",
    "latin": "language_latin",
    # Ge'ez is CK3's Ethiopic language; vanilla's Middle Tamil includes
    # Malayalam, the closest useful language for the Cochin charter.
    "ethiopic": "language_ethiopic",
    "tamil": "language_tamil",
}
# 2026-11-10, revision 4 (Daniel): no in-between fluency. Knowing a language is
# vanilla's yes or no; the liturgical tongue of the reader's faith
# (kehillah_liturgical_language_trigger) softens the penalty for not knowing
# it, and is the only language learned by reading.
# The first works of the catalog have their own hand-written opening text in
# kehillah_study_torah.0002 (kehillah_l_english.yml); every later work opens with
# its per-work study line instead.
OPENING_DESC_WORKS = 23

GENRES = {"parshanut": 1, "talmudics": 2, "hashkafa": 3}
GENRE_BY_N = {v: k for k, v in GENRES.items()}
# rank name -> (shelf band, frame in the rank-frame strip). The band only orders
# the shelf; a work's standing is per rite (kehillah_lib_standing_<flag>).
RANKS = {"Foundational": (1, 1), "Essential": (2, 1), "Celebrated": (3, 2), "Popular": (4, 3), "Obscure": (5, 4)}
CORPORA = {"": 0, "bavli": 1, "yerushalmi": 2, "tanakh": 3}
# 2026-11-11 (one scale): 0 Anathema .. 8 Authoritative earned; canon 9
# Foundational, 10 Prophetic, 11 Divine. 2 Rejected is also where a rite puts
# canon it does not receive (the Talmud for a Karaite). The Samaritan Torah
# and Beta Israel Orit are scripture only in their respective traditions.
TOP_EARNED = 8
OUTSIDE_CANON = 2
# 2026-11-11 (Daniel): a Jewish faith with neither tradition (the Beta Israel,
# the Samaritans) has simply not met the other works: Obscure.
UNKNOWN_TO_FAITH = 4
CANON = {"": 0, "oral_torah": 9, "neviim_ketuvim": 10, "torah": 11,
         "samaritan_torah": 11, "haymanot_orit": 11}
TRADITIONS = {"rabbanite": 1, "karaite": 2, "shared": 3,
              "samaritan": 4, "haymanot": 5}
GAMEPLAY = "#bold;color_porple "
BOM = "﻿"
HEADER = [
    "# GENERATED by scripts/kehillah_library_catalog.py from",
    "# scripts/kehillah_library_catalog.json -- edit the catalog, not this file.",
]

# Authored-slot book kinds (the composing chain's first choice) and titles.
AUTHORED_KINDS = {
    1: ("Commentary on the Torah", 1),
    2: ("Commentary on the Talmud", 2),
    3: ("Responsa", 2),
    4: ("Code of Law", 2),
    5: ("Treatise of Philosophy", 3),
    6: ("Book of Piyyutim", 1),
    7: ("Novellae on the Talmud", 2),
    8: ("Polemic", 3),
}
# (2026-11-08: authored works are named by author and kind; no title list.)

# Tenets a book written in play can argue for, by index (global_var:
# kehillah_wk_<slot>_tenet_a / _b). Must match kehillah_sefer_teach_dynamic_
# tenet_effect in common/scripted_effects/kehillah_sefer_effects.txt.
TENET_INDEX = [
    "tenet_talmud_torah", "tenet_baalei_hamiqra", "tenet_kehillah_hokhmah",
    "tenet_kehillah_emunah_temimah", "tenet_kehillah_pesak", "tenet_kehillah_pilpul",
    "tenet_kehillah_geonut", "tenet_kehillah_minhag_avoteinu", "tenet_kehillah_avelei_tziyon",
    "tenet_esotericism", "tenet_asceticism", "tenet_kehillah_kiddush_hashem",
]


def dynamic_tenet_branches(f, body):
    """For an authored slot: one branch per (which, tenet index) pair."""
    out = []
    for which in ("a", "b"):
        for i, t in enumerate(TENET_INDEX, start=1):
            out += body(f"global_var:kehillah_wk_{f}_tenet_{which} ?= {i}", t)
    return out


AUTHOR_NAMES = {}


def load():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    AUTHOR_NAMES.update(data.get("author_names", {}))
    return data["order"], data["works"]


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BOM + "\r\n".join(lines) + "\r\n", encoding="utf-8", newline="")


def authored(w):
    return bool(w.get("authored"))


def needs_writing(w):
    """Named and authored works exist in the world only once written."""
    return bool(w.get("named") or w.get("authored"))


def short(f):
    return f.removeprefix("work_")


def circulation_year(w):
    return w.get("circulation_year", w["year"])


def avail_lines(f, w, ind):
    """Trigger lines: the work is in circulation in this campaign."""
    out = []
    if needs_writing(w):
        out.append(f"{ind}has_global_variable = kehillah_wk_{f}_written")
    elif circulation_year(w) > 1:
        out.append(f"{ind}current_date >= {circulation_year(w)}.1.1")
    return out


def held(f, ind="", lst="kehillah_library_works"):
    return f"{ind}is_target_in_variable_list = {{ name = {lst} target = flag:{f} }}"


def study_call(f, w, ind):
    """Call the shared study effect for f with its literal track."""
    if authored(w):
        out = []
        for n, g in ((2, "talmudics"), (3, "hashkafa")):
            out += [
                f"{ind}{'if' if n == 2 else 'else_if'} = {{",
                f"{ind}\tlimit = {{ kehillah_lib_genre_{f} = {n} }}",
                f"{ind}\tkehillah_study_specific_work_effect = {{ WORK = flag:{f} TRACK = {g} KEY = {f} }}",
                f"{ind}}}",
            ]
        out += [
            f"{ind}else = {{",
            f"{ind}\tkehillah_study_specific_work_effect = {{ WORK = flag:{f} TRACK = parshanut KEY = {f} }}",
            f"{ind}}}",
        ]
        return out
    return [f"{ind}kehillah_study_specific_work_effect = {{ WORK = flag:{f} TRACK = {w['genre']} KEY = {f} }}"]


def study_tt_key(f, w):
    """The per-work study flavor line, e.g. kehillah_study_torah.talmudics.mishnah_tt."""
    if authored(w):
        return f"kehillah_study_torah.authored.{short(f)}_tt"
    return f"kehillah_study_torah.{w['genre']}.{short(f)}_tt"


# ---------------------------------------------------------------------------
# Catalog values
# ---------------------------------------------------------------------------

def dyn_value(name, default, gvar):
    return [
        f"{name} = {{",
        f"\tvalue = {default}",
        f"\tif = {{ limit = {{ has_global_variable = {gvar} }} value = global_var:{gvar} }}",
        "}",
    ]


def write_values(order, works):
    out = HEADER + [
        "# The library panel reads these dynamically per work flag, e.g.",
        "# ScriptValue( Concatenate( 'kehillah_lib_genre_', Scope.GetFlagName ) ).",
        "",
        "# 1 parshanut, 2 talmudics, 3 hashkafa",
    ]
    for f in order:
        w = works[f]
        if authored(w):
            out += dyn_value(f"kehillah_lib_genre_{f}", 1, f"kehillah_wk_{f}_genre")
        else:
            out.append(f"kehillah_lib_genre_{f} = {GENRES[w['genre']]}")
    out += ["", "# shelf band: 1 foundational, 2 essential, 3 celebrated, 4 popular, 5 obscure"]
    for f in order:
        out.append(f"kehillah_lib_rank_{f} = {RANKS[works[f]['rank_name']][0]}")
    out += [
        "",
        "# frame in gfx/interface/icons/kehillah_library/kehillah_sefer_rank_frames.dds,",
        "# by the work's standing in the viewer's rite (scope: the player): canon 1,",
        "# Authoritative 2, Celebrated or Esteemed 3, lower 4.",
    ]
    for f in order:
        out += [
            f"kehillah_lib_frame_{f} = {{",
            "\tvalue = 4",
            f"\tif = {{ limit = {{ kehillah_lib_standing_{f} >= 9 }} value = 1 }}",
            f"\telse_if = {{ limit = {{ kehillah_lib_standing_{f} >= 8 }} value = 2 }}",
            f"\telse_if = {{ limit = {{ kehillah_lib_standing_{f} >= 6 }} value = 3 }}",
            "}",
        ]
    out += ["", "# composition year (the game date; Jan 1 is a dating convention)"]
    for f in order:
        w = works[f]
        if authored(w) or w.get("named"):
            out += dyn_value(f"kehillah_lib_year_{f}", w["year"], f"kehillah_wk_{f}_year")
        else:
            out.append(f"kehillah_lib_year_{f} = {w['year']}")
    out += ["", "# 0 stands alone, 1 a Bavli seder, 2 a Yerushalmi seder, 3 a division of the Tanakh"]
    for f in order:
        out.append(f"kehillah_lib_corpus_{f} = {CORPORA[works[f]['corpus']]}")
    out += ["", "# canon tier, fixed by doctrine: 0 none, 9 Foundational, 10 Prophetic, 11 Divine"]
    for f in order:
        out.append(f"kehillah_lib_canon_{f} = {CANON[works[f].get('canon', '')]}")
    out += ["", "# 1 Rabbanite, 2 Karaite, 3 shared scripture"]
    for f in order:
        out.append(f"kehillah_lib_tradition_{f} = {TRADITIONS[works[f].get('tradition', 'rabbanite')]}")
    out += [
        "",
        "# Shelf slot = genre * 10 + band (so a genre box lists Foundational first,",
        "# Obscure last); 0 for a work shown inside its corpus card instead.",
    ]
    for f in order:
        w = works[f]
        if authored(w):
            out += [
                f"kehillah_lib_slot_{f} = {{",
                f"\tvalue = kehillah_lib_genre_{f}",
                "\tmultiply = 10",
                "\tadd = 5",
                "}",
            ]
            continue
        slot = 0 if CORPORA[w["corpus"]] else GENRES[w["genre"]] * 10 + RANKS[w["rank_name"]][0]
        out.append(f"kehillah_lib_slot_{f} = {slot}")
    out += [
        "",
        "# 1 when the hover card can link the work's author: for a historical work,",
        "# the author character is stored on the player; for a work written in this",
        "# campaign, its author is recorded in a global variable. Scope: the player.",
    ]
    for f in order:
        w = works[f]
        slug = w.get("composer_char")
        if needs_writing(w):
            out += [
                f"kehillah_lib_author_ready_{f} = {{",
                "\tvalue = 0",
                f"\tif = {{ limit = {{ exists = global_var:kehillah_wk_{f}_author }} add = 1 }}",
                "}",
            ]
        elif slug:
            out += [
                f"kehillah_lib_author_ready_{f} = {{",
                "\tvalue = 0",
                f"\tif = {{ limit = {{ exists = var:kehillah_lib_author_{slug} }} add = {{ value = 1 }} }}",
                "}",
            ]
        else:
            out.append(f"kehillah_lib_author_ready_{f} = 1")
    for genre, n in GENRES.items():
        out += [
            "",
            f"# Works of this genre the title's library holds ({genre}); scope: title.",
            "# 2026-11-10 (Daniel): each corpus volume counts on its own -- the Torah,",
            "# the Prophets and the Writings are three works, each Bavli order one.",
            f"kehillah_lib_genre_{n}_held_count_value = {{",
            "\tvalue = 0",
        ]
        for f in order:
            w = works[f]
            if authored(w):
                out += [
                    "\tif = {",
                    f"\t\tlimit = {{ {held(f)} kehillah_lib_genre_{f} = {n} }}",
                    "\t\tadd = { value = 1 }",
                    "\t}",
                ]
            elif w["genre"] == genre:
                out += [
                    "\tif = {",
                    f"\t\tlimit = {{ {held(f)} }}",
                    "\t\tadd = { value = 1 }",
                    "\t}",
                ]
        out.append("}")
    write(VALUES, out)


# ---------------------------------------------------------------------------
# Standing values (spec section 3)
# ---------------------------------------------------------------------------

def write_standing_values(order, works):
    out = HEADER + [
        "# Standing, docs/spec/2026-11-08-sefer-system-redesign.md section 3.",
        "# One scale (docs/spec/2026-11-11-standing-one-scale.md): 0 Anathema,",
        "# 1 Banned, 2 Rejected, 3 Contested, 4 Obscure, 5 Popular, 6 Celebrated,",
        "# 7 Esteemed, 8 Authoritative; canon 9 Foundational, 10 Prophetic, 11 Divine",
        "# is fixed by doctrine and never stored. Canon a rite does not receive (the",
        "# Talmud for a Karaite) reads 2 Rejected.",
        "",
        "# ---- ceilings (rite scope): the least favourable status among the tenets a",
        "# work argues for sets how high it may climb in this rite; a core tenet it",
        "# argues against takes two tiers off.",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [f"kehillah_lib_ceiling_{f} = {{", f"\tvalue = {TOP_EARNED}"]
        if authored(w):
            # Compact form (one line per status): 100 slots x 2 tenets x 12.
            out += dynamic_tenet_branches(f, lambda cond, t: [
                f"\tif = {{ limit = {{ {cond} }}",
                f"\t\tif = {{ limit = {{ has_tenet_status = {{ tenet = {t} status = prohibited }} }} max = 3 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = known }} }} }} max = 5 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = permitted }} }} }} max = 6 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = core }} }} }} max = 7 }}",
                "\t}",
            ])
            # 2026-11-10 (Sefer languages): a book in its author's own tongue is
            # less esteemed than one in Hebrew or Aramaic, by how prestigious that
            # tongue is among vanilla's royal courts (_lang_prestige 2 / 1 / 0).
            out += [f"\tif = {{ limit = {{ global_var:kehillah_wk_{f}_lang ?= flag:vernacular }}",
                    f"\t\tif = {{ limit = {{ global_var:kehillah_wk_{f}_lang_prestige ?= 2 }} max = kehillah_book_vernacular_ceiling_great }}",
                    f"\t\telse_if = {{ limit = {{ global_var:kehillah_wk_{f}_lang_prestige ?= 1 }} max = kehillah_book_vernacular_ceiling_court }}",
                    "\t\telse = { max = kehillah_book_vernacular_ceiling }",
                    "\t}"]
        for t in w.get("argues_for", []):
            out += [
                "\tif = {",
                f"\t\tlimit = {{ has_tenet_status = {{ tenet = {t} status = prohibited }} }}",
                "\t\tmax = 3",
                "\t}",
                "\telse_if = {",
                f"\t\tlimit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = known }} }} }}",
                "\t\tmax = 5",
                "\t}",
                "\telse_if = {",
                f"\t\tlimit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = permitted }} }} }}",
                "\t\tmax = 6",
                "\t}",
                "\telse_if = {",
                f"\t\tlimit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = core }} }} }}",
                "\t\tmax = 7",
                "\t}",
            ]
        for t in w.get("argues_against", []):
            out += [
                "\tif = {",
                f"\t\tlimit = {{ rite_has_tenet = {t} }}",
                "\t\tsubtract = 2",
                "\t}",
            ]
        out += ["\tmin = 1", "}"]
    out += ["", "# ---- floors (rite scope): antiquity, and a core tenet the work argues for."]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [f"kehillah_lib_floor_{f} = {{", "\tvalue = 1"]
        if w.get("floor"):
            out += [
                "\tif = {",
                "\t\tlimit = { kehillah_rite_rabbanite_trigger = yes }",
                f"\t\tmin = {w['floor']}",
                "\t}",
            ]
        for t in w.get("argues_for", []):
            out += [
                "\tif = {",
                f"\t\tlimit = {{ rite_has_tenet = {t} }}",
                "\t\tmin = 5",
                "\t}",
            ]
        out += [f"\tmax = kehillah_lib_ceiling_{f}", "}"]
    out += ["", "# ---- baselines (rite scope): the tier a work starts at, by faith family."]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        b = w.get("baseline", {"rabbinic": 4, "karaite": 4})
        other = UNKNOWN_TO_FAITH
        out += [
            f"kehillah_lib_baseline_{f} = {{",
            f"\tvalue = {other}",
            "\tif = {",
            "\t\tlimit = { kehillah_rite_rabbanite_trigger = yes }",
            f"\t\tvalue = {b['rabbinic']}",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { kehillah_rite_toric_trigger = yes }",
            f"\t\tvalue = {b['karaite']}",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { kehillah_rite_samaritan_trigger = yes }",
            f"\t\tvalue = {b.get('samaritan', UNKNOWN_TO_FAITH)}",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { kehillah_rite_haymanot_trigger = yes }",
            f"\t\tvalue = {b.get('haymanot', UNKNOWN_TO_FAITH)}",
            "\t}",
            "}",
        ]
    out += [
        "",
        "# ---- the viewer's standing (character scope): canon by doctrine, otherwise",
        "# the stored tier of the viewer's rite, or the baseline before it is seeded.",
    ]
    for f in order:
        w = works[f]
        canon = w.get("canon")
        out.append(f"kehillah_lib_standing_{f} = {{")
        if canon == "torah":
            out += [f"\tvalue = {CANON['torah']}"]
        elif canon == "neviim_ketuvim":
            out += [
                f"\tvalue = {CANON['neviim_ketuvim']}",
                "\tif = {",
                "\t\tlimit = { rite ?= { kehillah_rite_samaritan_trigger = yes } }",
                f"\t\tvalue = {OUTSIDE_CANON}",
                "\t}",
            ]
        elif canon == "oral_torah":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { rite ?= { kehillah_rite_rabbanite_trigger = yes } }",
                f"\t\tvalue = {CANON['oral_torah']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { kehillah_rite_toric_trigger = yes } }",
                f"\t\tvalue = {OUTSIDE_CANON}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { NOT = { faith.religion = religion:judaism_religion } }",
                f"\t\tvalue = {CANON['oral_torah']}",
                "\t}",
            ]
        elif canon == "samaritan_torah":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { rite ?= { kehillah_rite_samaritan_trigger = yes } }",
                f"\t\tvalue = {CANON['samaritan_torah']}",
                "\t}",
            ]
        elif canon == "haymanot_orit":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { rite ?= { kehillah_rite_haymanot_trigger = yes } }",
                f"\t\tvalue = {CANON['haymanot_orit']}",
                "\t}",
            ]
        else:
            b = w.get("baseline", {"rabbinic": 4, "karaite": 4})
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                f"\t\tlimit = {{ rite ?= {{ has_variable = kehillah_standing_{f} }} }}",
                f"\t\tvalue = rite.var:kehillah_standing_{f}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { kehillah_rite_rabbanite_trigger = yes } }",
                f"\t\tvalue = {b['rabbinic']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { kehillah_rite_toric_trigger = yes } }",
                f"\t\tvalue = {b['karaite']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { kehillah_rite_samaritan_trigger = yes } }",
                f"\t\tvalue = {b.get('samaritan', UNKNOWN_TO_FAITH)}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { kehillah_rite_haymanot_trigger = yes } }",
                f"\t\tvalue = {b.get('haymanot', UNKNOWN_TO_FAITH)}",
                "\t}",
            ]
        out.append("}")
    # 2026-11-10 (Daniel): the Sefarim ledger can show how ANOTHER rite ranks
    # the world's books. The same rules as the viewer's standing above, read
    # on the rite itself (scope: a rite) instead of through a character.
    out += [
        "",
        "# ---- a rite's standing (rite scope), for the ledger's rite selector: the",
        "# viewer's standing above, read on the rite itself.",
    ]
    for f in order:
        w = works[f]
        canon = w.get("canon")
        out.append(f"kehillah_lib_rite_standing_{f} = {{")
        if canon == "torah":
            out += [f"\tvalue = {CANON['torah']}"]
        elif canon == "neviim_ketuvim":
            out += [
                f"\tvalue = {CANON['neviim_ketuvim']}",
                "\tif = {",
                "\t\tlimit = { kehillah_rite_samaritan_trigger = yes }",
                f"\t\tvalue = {OUTSIDE_CANON}",
                "\t}",
            ]
        elif canon == "oral_torah":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { kehillah_rite_rabbanite_trigger = yes }",
                f"\t\tvalue = {CANON['oral_torah']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { kehillah_rite_toric_trigger = yes }",
                f"\t\tvalue = {OUTSIDE_CANON}",
                "\t}",
            ]
        elif canon == "samaritan_torah":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { kehillah_rite_samaritan_trigger = yes }",
                f"\t\tvalue = {CANON['samaritan_torah']}",
                "\t}",
            ]
        elif canon == "haymanot_orit":
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                "\t\tlimit = { kehillah_rite_haymanot_trigger = yes }",
                f"\t\tvalue = {CANON['haymanot_orit']}",
                "\t}",
            ]
        else:
            b = w.get("baseline", {"rabbinic": 4, "karaite": 4})
            out += [
                f"\tvalue = {UNKNOWN_TO_FAITH}",
                "\tif = {",
                f"\t\tlimit = {{ has_variable = kehillah_standing_{f} }}",
                f"\t\tvalue = var:kehillah_standing_{f}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { kehillah_rite_rabbanite_trigger = yes }",
                f"\t\tvalue = {b['rabbinic']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { kehillah_rite_toric_trigger = yes }",
                f"\t\tvalue = {b['karaite']}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { kehillah_rite_samaritan_trigger = yes }",
                f"\t\tvalue = {b.get('samaritan', UNKNOWN_TO_FAITH)}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { kehillah_rite_haymanot_trigger = yes }",
                f"\t\tvalue = {b.get('haymanot', UNKNOWN_TO_FAITH)}",
                "\t}",
            ]
        out.append("}")
    # 2026-11-11 (Daniel): owned books add Greatness by their standing in the
    # leader's rite; banned books take it away (kehillah_greatness_baseline_value).
    out += ["", "# ---- the library's Greatness (scope: a Kehillah leader): every work his",
            "# community holds, weighted by its standing in his rite, between",
            "# kehillah_lib_greatness_min and kehillah_lib_greatness_max.",
            "kehillah_bd_library_works_value = {", "\tvalue = 0"]
    for f in order:
        st = f"kehillah_lib_standing_{f}"
        out += [
            "\tif = {",
            f"\t\tlimit = {{ primary_title ?= {{ {held(f)} }} }}",
            f"\t\tif = {{ limit = {{ {st} >= 9 }} add = kehillah_lib_greatness_canon }}",
            f"\t\telse_if = {{ limit = {{ {st} = 8 }} add = kehillah_lib_greatness_authoritative }}",
            f"\t\telse_if = {{ limit = {{ {st} = 7 }} add = kehillah_lib_greatness_esteemed }}",
            f"\t\telse_if = {{ limit = {{ {st} = 6 }} add = kehillah_lib_greatness_celebrated }}",
            f"\t\telse_if = {{ limit = {{ {st} = 5 }} add = kehillah_lib_greatness_popular }}",
            f"\t\telse_if = {{ limit = {{ {st} = 4 }} add = kehillah_lib_greatness_obscure }}",
            f"\t\telse_if = {{ limit = {{ {st} = 1 }} add = kehillah_lib_greatness_banned }}",
            f"\t\telse_if = {{ limit = {{ {st} = 0 }} add = kehillah_lib_greatness_anathema }}",
            "\t}",
        ]
    out += ["\tmin = kehillah_lib_greatness_min", "\tmax = kehillah_lib_greatness_max", "}"]
    out += ["", "# ---- copies (any scope): how many registered libraries hold the work."]
    for f in order:
        out += [
            f"kehillah_lib_copies_{f} = {{",
            "\tvalue = 0",
            "\tevery_in_global_list = {",
            "\t\tvariable = kehillah_libraries",
            f"\t\tlimit = {{ exists = holder {held(f)} }}",
            "\t\tadd = 1",
            "\t}",
            "}",
        ]
    out += ["", "# ---- the index (in TENET_INDEX, 1-based) of the first tenet a work argues",
            "# for; 0 when it argues for none. A Machloket's outcome queues a reform",
            "# question on that tenet (any scope)."]
    for f in order:
        w = works[f]
        ts = w.get("argues_for", [])
        if authored(w):
            out += dyn_value(f"kehillah_sefer_first_tenet_{f}", 0, f"kehillah_wk_{f}_tenet_a")
        else:
            idx = TENET_INDEX.index(ts[0]) + 1 if ts and ts[0] in TENET_INDEX else 0
            out.append(f"kehillah_sefer_first_tenet_{f} = {{ value = {idx} }}")
    out += ["", "# ---- the viewer rite's ceiling for the work (character scope), for the Standing row."]
    for f in order:
        w = works[f]
        if w.get("canon"):
            out.append(f"kehillah_lib_view_ceiling_{f} = {{ value = {CANON[w['canon']]} }}")
            continue
        out += [
            f"kehillah_lib_view_ceiling_{f} = {{",
            f"\tvalue = {TOP_EARNED}",
            "\tif = {",
            f"\t\tlimit = {{ rite ?= {{ has_variable = kehillah_ceiling_{f} }} }}",
            f"\t\tvalue = rite.var:kehillah_ceiling_{f}",
            "\t}",
            "}",
        ]
    write(STANDING_VALUES, out)


# ---------------------------------------------------------------------------
# Generated triggers
# ---------------------------------------------------------------------------

def write_triggers(order, works):
    out = HEADER + [
        "# Moved here from kehillah_scripted_triggers.txt on 2026-11-08 so new works",
        "# need no hand-kept lists. Same names, same parameters, same meaning.",
        "",
    ]
    for genre in GENRES:
        members = [f for f in order if works[f]["genre"] == genre and not authored(works[f])]
        out += [f"kehillah_owns_{genre}_work_trigger = {{", "\t$LIBRARY$ = {", "\t\tOR = {"]
        out += [held(f, "\t\t\t") for f in members]
        for f in order:
            if authored(works[f]):
                out.append(f"\t\t\tAND = {{ {held(f)} kehillah_lib_genre_{f} = {GENRES[genre]} }}")
        out += ["\t\t}", "\t}", "}", ""]
        out += [f"kehillah_missing_{genre}_work_trigger = {{", "\t$LIBRARY$ = {", "\t\tOR = {"]
        for f in members:
            if works[f].get("tradition") == "karaite":
                continue
            av = avail_lines(f, works[f], "\t\t\t\t")
            if av:
                out += ["\t\t\tAND = {"] + av + [f"\t\t\t\tNOT = {{ {held(f)} }}", "\t\t\t}"]
            else:
                out.append(f"\t\t\tNOT = {{ {held(f)} }}")
        out += ["\t\t}", "\t}", "}", ""]
    out += [
        "kehillah_owns_any_torah_work_trigger = {",
        "\tOR = {",
        "\t\tkehillah_owns_parshanut_work_trigger = { LIBRARY = $LIBRARY$ }",
        "\t\tkehillah_owns_talmudics_work_trigger = { LIBRARY = $LIBRARY$ }",
        "\t\tkehillah_owns_hashkafa_work_trigger = { LIBRARY = $LIBRARY$ }",
        "\t}",
        "}",
        "",
        "# Scope: the studying character. Does $LIBRARY$ still hold the work named by",
        "# kehillah_study_current_work_id (the scheme's numeric bridge, 1..N in catalog order)?",
        "kehillah_study_torah_current_work_still_owned_trigger = {",
        "\tOR = {",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            "\t\tAND = {",
            f"\t\t\tvar:kehillah_study_current_work_id = {i}",
            f"\t\t\t$LIBRARY$ = {{ {held(f)} }}",
            "\t\t}",
        ]
    out += ["\t}", "}", "", "# The current work has another already-studied work of the same field.",
            "kehillah_study_torah_has_same_track_reference_trigger = {", "\tOR = {"]
    for i, f in enumerate(order, start=1):
        w = works[f]
        if authored(w):
            continue
        others = [g for g in order if g != f and not authored(works[g]) and works[g]["genre"] == w["genre"]]
        out += [
            "\t\tAND = {",
            f"\t\t\tvar:kehillah_study_current_work_id = {i}",
            "\t\t\tOR = {",
        ]
        out += [held(g, "\t\t\t\t", "kehillah_studied_works") for g in others]
        out += ["\t\t\t}", "\t\t}"]
    out += ["\t}", "}", ""]
    out += ["# Per-work: in circulation in this campaign (any scope)."]
    for f in order:
        av = avail_lines(f, works[f], "\t")
        out += [f"kehillah_lib_available_{f}_trigger = {{"] + (av or ["\talways = yes"]) + ["}"]
    redeemable = [f for f in order if not works[f].get("canon") or works[f].get("canon") == "oral_torah"]
    redeemable = [f for f in redeemable if works[f]["corpus"] != "tanakh"]
    out += [
        "",
        "# Scope: a character with var:kehillah_own_library. The ransom pool holds a",
        "# work his library lacks.",
        "kehillah_lib_can_redeem_trigger = {",
        "\tvar:kehillah_own_library ?= {",
        "\t\tOR = {",
    ]
    for f in redeemable:
        out += [
            "\t\t\tAND = {",
            f"\t\t\t\tis_target_in_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }}",
            f"\t\t\t\tNOT = {{ {held(f)} }}",
            "\t\t\t}",
        ]
    out += ["\t\t}", "\t}", "}"]
    out += ["", "# Per-work: the work argues for a tenet, so a Machloket over it can split a rite."]
    for f in order:
        ts = works[f].get("argues_for", [])
        out.append(f"kehillah_sefer_work_can_split_{f}_trigger = {{ {'always = yes' if ts else 'always = no'} }}")
    out += ["", "# Per-work, scope a reader: the work argues for a tenet his rite prohibits."]
    for f in order:
        ts = works[f].get("argues_for", [])
        out.append(f"kehillah_sefer_work_heterodox_{f}_trigger = {{")
        if authored(works[f]):
            out += ["\trite ?= {", "\t\tOR = {"]
            out += dynamic_tenet_branches(f, lambda cond, t: [
                f"\t\t\tAND = {{ {cond} has_tenet_status = {{ tenet = {t} status = prohibited }} }}"
            ])
            out += ["\t\t}", "\t}"]
        elif len(ts) == 1:
            out += ["\trite ?= {", f"\t\thas_tenet_status = {{ tenet = {ts[0]} status = prohibited }}", "\t}"]
        elif ts:
            out += ["\trite ?= {", "\t\tOR = {"]
            out += [f"\t\t\thas_tenet_status = {{ tenet = {t} status = prohibited }}" for t in ts]
            out += ["\t\t}", "\t}"]
        else:
            out.append("\talways = no")
        out.append("}")
    out += ["", "# Scope: the studying character. The work named by kehillah_study_current_work_id",
            "# (the scheme's numeric bridge) is a Hashkafa work. Read by kehillah_study_torah.0003."]
    out += ["kehillah_study_current_work_is_hashkafa_trigger = {", "	OR = {"]
    out += [f"		var:kehillah_study_current_work_id = {i}"
            for i, f in enumerate(order, start=1) if works[f]["genre"] == "hashkafa"]
    out += ["	}", "}"]
    # 2026-11-11 (Daniel: offer "one option of each genre that you haven't
    # read"): scope the reader. $LIBRARY$ holds a work of genre <g> (1-3)
    # that the reader has not mastered.
    for g in (1, 2, 3):
        out += [
            "",
            f"kehillah_study_torah_unread_in_genre_{g}_trigger = {{",
            "\tOR = {",
        ]
        for f in order:
            w = works[f]
            if not authored(w) and GENRES[w["genre"]] != g:
                continue
            genre_test = f"kehillah_lib_genre_{f} = {g} " if authored(w) else ""
            out.append(
                f"\t\tAND = {{ {genre_test}$LIBRARY$ = {{ {held(f)} }} "
                f"NOT = {{ {held(f, '', 'kehillah_mastered_works')} }} }}"
            )
        out += ["\t}", "}"]
    write(TRIGGERS, out)


# ---------------------------------------------------------------------------
# Generated effects: study dispatch, yeshiva draw, per-work hooks, standing
# ---------------------------------------------------------------------------

def write_study_effects(order, works):
    out = HEADER + [
        "# Moved here from kehillah_library_effects.txt / kehillah_yeshiva_effects.txt",
        "# on 2026-11-08. THE NUMERIC-ID BRIDGE: kehillah_study_current_work_id is the",
        "# work's 1-based position in the catalog's order list. Never reorder that list;",
        "# new works are appended.",
        "",
        "# Scope: the studying character. Draw a work $LIBRARY$ holds. Tanakh, Talmud",
        "# and the reader's own tradition are drawn more often.",
        "kehillah_study_torah_pick_next_work_effect = {",
        "\trandom_list = {",
    ]
    for i, f in enumerate(order, start=1):
        w = works[f]
        weight = 2 if w.get("canon") else 1
        out += [
            f"\t\t{weight} = {{",
            f"\t\t\ttrigger = {{ $LIBRARY$ = {{ {held(f)} }} }}",
        ]
        out += [
            f"\t\t\tset_variable = {{ name = kehillah_study_current_work_id value = {i} }}",
            f"\t\t\tcustom_tooltip = {study_tt_key(f, w)}",
            "\t\t}",
        ]
    out += ["\t}", "}", ""]

    # 2026-11-11 (Daniel: "change it to offer one option of each genre that you
    # haven't read, if you have one available, and also a come back later to
    # choose option"). The completion event (kehillah_study_torah.0001) offers,
    # per genre, one work $LIBRARY$ holds that the reader has not mastered:
    # var:kehillah_study_offer_<g> its numeric ID, var:kehillah_study_offer_<g>_work
    # its flag (for the option's name). Canon works are drawn twice as often, as
    # in the old picker.
    out += [
        "# Scope: the studying character. One unmastered work per genre, for the",
        "# completion event's options.",
        "kehillah_study_torah_offer_effect = {",
        "\tkehillah_study_torah_clear_offers_effect = yes",
    ]
    for g in (1, 2, 3):
        out += [
            "\tif = {",
            f"\t\tlimit = {{ kehillah_study_torah_unread_in_genre_{g}_trigger = {{ LIBRARY = $LIBRARY$ }} }}",
            "\t\trandom_list = {",
        ]
        for i, f in enumerate(order, start=1):
            w = works[f]
            if not authored(w) and GENRES[w["genre"]] != g:
                continue
            weight = 2 if w.get("canon") else 1
            cond = [f"$LIBRARY$ = {{ {held(f)} }}", f"NOT = {{ {held(f, '', 'kehillah_mastered_works')} }}"]
            if authored(w):
                cond.insert(0, f"kehillah_lib_genre_{f} = {g}")
            out += [
                f"\t\t\t{weight} = {{",
                f"\t\t\t\ttrigger = {{ {' '.join(cond)} }}",
                f"\t\t\t\tset_variable = {{ name = kehillah_study_offer_{g} value = {i} }}",
                f"\t\t\t\tset_variable = {{ name = kehillah_study_offer_{g}_work value = flag:{f} }}",
                "\t\t\t}",
            ]
        out += ["\t\t}", "\t}"]
    out += [
        "}",
        "",
        "# Scope: the studying character. Take the offered work of genre $GENRE$:",
        "# it becomes the course's current work, with its own study line.",
        "kehillah_study_torah_take_offer_effect = {",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            f"\t{'if' if i == 1 else 'else_if'} = {{",
            f"\t\tlimit = {{ var:kehillah_study_offer_$GENRE$ ?= {i} }}",
            f"\t\tset_variable = {{ name = kehillah_study_current_work_id value = {i} }}",
            f"\t\tcustom_tooltip = {study_tt_key(f, works[f])}",
            "\t}",
        ]
    out += ["}", "", "# Scope: the studying character. Resolve the work the numeric ID names.",
            "kehillah_study_torah_resolve_current_work_effect = {"]
    for i, f in enumerate(order, start=1):
        out += [
            f"\t{'if' if i == 1 else 'else_if'} = {{",
            f"\t\tlimit = {{ var:kehillah_study_current_work_id = {i} }}",
        ]
        out += study_call(f, works[f], "\t\t")
        out.append("\t}")
    out += [
        "}",
        "",
        "# Scope: a present student, in the yeshiva tick (scope:kehillah_tick_title,",
        "# scope:kehillah_tick_leader). He masters one work the library holds and he has",
        "# not mastered -- a work of the yeshiva's focus three times as likely, a work",
        "# its standing in his rite makes Authoritative or better twice as likely.",
        "kehillah_yeshiva_master_a_work_effect = {",
        "\trandom_list = {",
    ]
    for f in order:
        w = works[f]
        if authored(w):
            continue
        g = w["genre"]
        out += [
            "\t\t1 = {",
            "\t\t\ttrigger = {",
            f"\t\t\t\tscope:kehillah_tick_title = {{ {held(f)} }}",
            f"\t\t\t\tNOT = {{ {held(f, '', 'kehillah_mastered_works')} }}",
            "\t\t\t}",
            "\t\t\tmodifier = {",
            "\t\t\t\tadd = 2",
            f"\t\t\t\tscope:kehillah_tick_title = {{ var:kehillah_yeshiva_specialization ?= flag:{g} }}",
            "\t\t\t}",
            "\t\t\tmodifier = {",
            "\t\t\t\tadd = 1",
            f"\t\t\t\tkehillah_lib_standing_{f} >= 8",
            "\t\t\t}",
            f"\t\t\tkehillah_yeshiva_record_work_effect = {{ WORK = {f} TRACK = {g} }}",
            "\t\t}",
        ]
    out += ["\t}", "}", ""]

    # Per-work hooks after a first mastery: teach tenets and record reception.
    out += [
        "# ---- per-work hooks. kehillah_sefer_work_tenets_<flag>_effect: scope the reader,",
        "# after a FIRST mastery. Teaches the tenets the work argues for (vanilla",
        "# knowledge for a playable reader; kehillah_book_tenets for anyone) and nudges",
        "# their popularity in the reader's faith. See section 4.1 of the spec.",
    ]
    for f in order:
        w = works[f]
        out.append(f"kehillah_sefer_work_tenets_{f}_effect = {{")
        tenets = w.get("argues_for", [])
        if not tenets:
            out.append("\t# argues for no tenet")
        for t in tenets:
            out.append(f"\tkehillah_sefer_teach_tenet_effect = {{ TENET = {t} }}")
        if authored(w):
            out += [
                f"\tif = {{ limit = {{ exists = global_var:kehillah_wk_{f}_tenet_a }}",
                f"\t\tkehillah_sefer_teach_dynamic_tenet_effect = {{ SLOT = {f} WHICH = a }}",
                "\t}",
                f"\tif = {{ limit = {{ exists = global_var:kehillah_wk_{f}_tenet_b }}",
                f"\t\tkehillah_sefer_teach_dynamic_tenet_effect = {{ SLOT = {f} WHICH = b }}",
                "\t}",
            ]
        out.append("}")
    out += [
        "",
        "# kehillah_sefer_work_fit_<flag>_effect: scope the reader. Sets",
        "# var:kehillah_sefer_fit to 1 when one of his personal tenets is one the work",
        "# argues for, -1 when it is one the work argues against (spec section 4.1).",
    ]
    for f in order:
        w = works[f]
        out += [f"kehillah_sefer_work_fit_{f}_effect = {{", "\tset_variable = { name = kehillah_sefer_fit value = 0 }"]
        if authored(w):
            out += dynamic_tenet_branches(f, lambda cond, t: [
                f"\tif = {{ limit = {{ {cond} has_personal_tenet = {t} }} set_variable = {{ name = kehillah_sefer_fit value = 1 }} }}"
            ])
        for t in w.get("argues_for", []):
            out += [f"\tif = {{ limit = {{ has_personal_tenet = {t} }} set_variable = {{ name = kehillah_sefer_fit value = 1 }} }}"]
        for t in w.get("argues_against", []):
            out += [f"\tif = {{ limit = {{ has_personal_tenet = {t} }} set_variable = {{ name = kehillah_sefer_fit value = -1 }} }}"]
        out.append("}")
    out += [
        "",
        "# kehillah_sefer_work_corpus_<flag>_effect: scope the reader, after a",
        "# successful reading. Counts the volume toward the current round of its",
        "# corpus (spec section 5.3); a work in no corpus does nothing.",
    ]
    for f in order:
        c = works[f]["corpus"]
        body = f"\tkehillah_sefer_round_progress_effect = {{ CORPUS = {c} KEY = {f} }}" if c else "\t# in no corpus"
        out += [f"kehillah_sefer_work_corpus_{f}_effect = {{", body, "}"]
    out += [
        "",
        "# Scope: none. Named works whose historical date has passed by the start",
        "# of this game (or the first year this save runs the redesign) count as",
        "# written; later ones wait for a scholar's ambition (Daniel, 2026-11-08).",
        "kehillah_sefer_mark_historical_works_effect = {",
    ]
    for f in order:
        w = works[f]
        if not w.get("named"):
            continue
        out += [
            "\tif = {",
            "\t\tlimit = {",
            f"\t\t\tcurrent_year >= {w['year']}",
            f"\t\t\tNOT = {{ has_global_variable = kehillah_wk_{f}_written }}",
            "\t\t}",
            f"\t\tset_global_variable = {{ name = kehillah_wk_{f}_written value = yes }}",
            f"\t\tset_global_variable = {{ name = kehillah_wk_{f}_year value = {w['year']} }}",
            f"\t\tkehillah_sefer_ensure_counters_effect = {{ KEY = {f} }}",
            "\t}",
        ]
    out += ["}", ""]
    out += [
        "# Scope: a faith. Nudge the popularity of the tenets a work argues for",
        "# ($AMOUNT$ may be negative) -- a Machloket's resolution (section 6.4).",
    ]
    for f in order:
        w = works[f]
        out.append(f"kehillah_sefer_work_popularity_{f}_effect = {{")
        ts = w.get("argues_for", [])
        for t in ts:
            out.append(f"\tchange_tenet_popularity = {{ target = tenet:{t} change = $AMOUNT$ }}")
        if authored(w):
            out += dynamic_tenet_branches(f, lambda cond, t: [
                f"\tif = {{ limit = {{ {cond} }} change_tenet_popularity = {{ target = tenet:{t} change = $AMOUNT$ }} }}"
            ])
        if not ts and not authored(w):
            out.append("\t# argues for no tenet; the argument is still read so every call has one shape")
            out.append("\tsave_temporary_scope_value_as = { name = kehillah_unused_amount value = $AMOUNT$ }")
        out.append("}")
    out += [
        "",
        "# Scope: a champion of the work. Found a rite with its first tenet as core:",
        "# a Machloket's schism, through vanilla's own dynamic rite (section 6.4).",
        "# A work arguing for no tenet cannot split a rite.",
    ]
    for f in order:
        w = works[f]
        ts = w.get("argues_for", [])
        out.append(f"kehillah_sefer_work_schism_{f}_effect = {{")
        if ts:
            out += [
                "\tcreate_dynamic_rite = {",
                "\t\tsave_scope_as = kehillah_schism_rite",
                "\t\tconvert = yes",
                f"\t\tcore_tenet_override_entry = tenet:{ts[0]}",
                "\t}",
            ]
        else:
            out.append("\t# argues for no tenet")
        out.append("}")
    out += [
        "",
        "# 2026-11-11: kehillah_sefer_cite_in_ruling_effect (a random citation after a",
        "# good ruling) is replaced by the judge's own choice of authority:",
        "# common/scripted_effects/kehillah_din_citation_generated_effects.txt.",
    ]
    def dispatch(name, test, call, keys, comment):
        lines = ["", f"# {comment}", f"{name} = {{"]
        for i, k in enumerate(keys):
            lines += [
                f"\t{'if' if i == 0 else 'else_if'} = {{",
                f"\t\tlimit = {{ {test} ?= flag:{k} }}",
                f"\t\t{call.format(k=k)}",
                "\t}",
            ]
        if not keys:
            lines.append("\t# none")
        lines.append("}")
        return lines

    named_keys = [f for f in order if works[f].get("named")]
    noncanon = [f for f in order if not works[f].get("canon") and works[f]["corpus"] != "tanakh"]
    out += dispatch("kehillah_sefer_write_named_work_dispatch_effect", "var:kehillah_book_named_work",
                    "kehillah_sefer_write_named_work_effect = {{ KEY = {k} }}", named_keys,
                    "Scope: the author. Write the named work his ambition chose.")
    out += dispatch("kehillah_sefer_count_commentary_dispatch_effect", "var:kehillah_book_comment_on",
                    "kehillah_sefer_bump_counter_effect = {{ KEY = {k} COUNTER = commentaries }} "
                    "kehillah_standing_add_reception_effect = {{ KEY = {k} AMOUNT = kehillah_reception_commentary_value }}",
                    noncanon, "Scope: the author of a gloss. The work he glossed gains a commentary.")
    out += dispatch("kehillah_sefer_approbation_dispatch_effect", "scope:kehillah_appr_asker.var:kehillah_sefer_my_latest_work",
                    "kehillah_sefer_approbation_effect = {{ KEY = {k} }}", noncanon,
                    "Scope: the approver. Endorse the asker's latest work.")
    out += dispatch("kehillah_sefer_endorse_dispatch_effect", "var:kehillah_sefer_named_work",
                    "kehillah_sefer_endorse_effect = {{ KEY = {k} }}", noncanon,
                    "Scope: a head of rite. Endorse the work he chose.")
    out += dispatch("kehillah_sefer_condemn_dispatch_effect", "var:kehillah_sefer_named_work",
                    "kehillah_sefer_condemn_effect = {{ KEY = {k} }}", noncanon,
                    "Scope: a head of rite. Condemn the work he chose.")
    out += [
        "",
        "# Scope: the author. Take the first free authored slot; with none free the",
        "# book stays news only (slot recycling is a recorded follow-up).",
        "kehillah_sefer_claim_authored_slot_effect = {",
    ]
    slots = [f for f in order if authored(works[f])]
    for i, f in enumerate(slots):
        out += [
            f"\t{'if' if i == 0 else 'else_if'} = {{",
            f"\t\tlimit = {{ NOT = {{ has_global_variable = kehillah_wk_{f}_written }} }}",
            f"\t\tkehillah_sefer_write_authored_work_effect = {{ SLOT = {f} }}",
            "\t}",
        ]
    out += ["}", "", "# Per named work, scope the author: a commentary counts toward the work it glosses."]
    for f in order:
        w = works[f]
        if not w.get("named"):
            continue
        target = w.get("commentary_on")
        out.append(f"kehillah_sefer_count_commentary_target_{f}_effect = {{")
        if target and target in noncanon:
            out.append(f"\tkehillah_sefer_bump_counter_effect = {{ KEY = {target} COUNTER = commentaries }}")
        else:
            out.append("\t# glosses a canonical text or nothing")
        out.append("}")
    out += [
        "",
        "# Scope: a head of rite. Load the works he may endorse or condemn: written,",
        "# non-canon, held somewhere, Popular or better (to endorse) in his rite.",
        "kehillah_sefer_build_judgeable_works_effect = {",
        "\tclear_variable_list = kehillah_sefer_judgeable",
    ]
    for f in noncanon:
        out += [
            "\tif = {",
            "\t\tlimit = {",
            f"\t\t\tkehillah_lib_available_{f}_trigger = yes",
            f"\t\t\tkehillah_lib_copies_{f} >= 1",
            f"\t\t\tkehillah_lib_standing_{f} >= 5",
            "\t\t}",
            f"\t\tadd_to_variable_list = {{ name = kehillah_sefer_judgeable target = flag:{f} }}",
            "\t}",
        ]
    out += ["}"]
    out += [
        "",
        "# ---- seized books and the ransom pool (section 7.1). Title scope: a",
        "# library whose books are sold off -- every work but the Tanakh enters",
        "# the global pool any Jewish library may redeem from.",
        "kehillah_lib_move_all_to_ransom_effect = {",
    ]
    for f in noncanon + [g for g in order if works[g].get("canon") == "oral_torah"]:
        out += [
            "\tif = {",
            f"\t\tlimit = {{ {held(f)} }}",
            f"\t\tremove_list_variable = {{ name = kehillah_library_works target = flag:{f} }}",
            f"\t\tif = {{ limit = {{ NOT = {{ is_target_in_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }} }} }}",
            f"\t\t\tadd_to_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }}",
            "\t\t}",
            "\t}",
        ]
    out += [
        "\tkehillah_lib_refresh_cache_effect = yes",
        "}",
        "",
        "# Title scope: a library emptied (burned, or given away), Tanakh aside.",
        "kehillah_lib_clear_all_but_tanakh_effect = {",
        "\tclear_variable_list = kehillah_library_works",
        "\tkehillah_lib_seed_tanakh_effect = yes",
        "\tkehillah_lib_refresh_cache_effect = yes",
        "}",
        "",
        "# Scope: a library holder. Redeem one seized work his library lacks, a",
        "# missing Bavli order first.",
        "kehillah_lib_redeem_one_effect = {",
        "\tvar:kehillah_own_library ?= { save_scope_as = kehillah_redeem_library }",
        "\tif = {",
        "\t\tlimit = { exists = scope:kehillah_redeem_library }",
        "\t\trandom_list = {",
    ]
    for f in noncanon + [g for g in order if works[g].get("canon") == "oral_torah"]:
        weight = 5 if works[f]["corpus"] == "bavli" else 1
        out += [
            f"\t\t\t{weight} = {{",
            "\t\t\t\ttrigger = {",
            f"\t\t\t\t\tis_target_in_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }}",
            f"\t\t\t\t\tscope:kehillah_redeem_library = {{ NOT = {{ {held(f)} }} }}",
            "\t\t\t\t}",
            f"\t\t\t\tremove_list_global_variable = {{ name = kehillah_ransom_pool target = flag:{f} }}",
            f"\t\t\t\tscope:kehillah_redeem_library = {{ add_to_variable_list = {{ name = kehillah_library_works target = flag:{f} }} kehillah_lib_refresh_cache_effect = yes }}",
            f"\t\t\t\tset_variable = {{ name = kehillah_sefer_named_work value = flag:{f} }}",
            "\t\t\t}",
        ]
    out += ["\t\t}", "\t}", "}"]
    out += [
        "",
        "# Scope: a scholar arriving at scope:kehillah_chest_library (section 7.1).",
        "# He brings a copy of one work he mastered that the library lacks, a",
        "# Bavli order more often; nothing if he has none to give.",
        "kehillah_sefer_scholar_chest_pick_effect = {",
        "\tif = {",
        "\t\tlimit = {",
        "\t\t\tOR = {",
    ]
    chest = [f for f in order if works[f]["corpus"] != "tanakh"]
    for f in chest:
        out.append(f"\t\t\t\tAND = {{ {held(f, '', 'kehillah_mastered_works')} scope:kehillah_chest_library = {{ NOT = {{ {held(f)} }} }} }}")
    out += ["\t\t\t}", "\t\t}", "\t\trandom_list = {"]
    for f in chest:
        weight = 4 if works[f]["corpus"] == "bavli" else 1
        out += [
            f"\t\t\t{weight} = {{",
            f"\t\t\t\ttrigger = {{ {held(f, '', 'kehillah_mastered_works')} scope:kehillah_chest_library = {{ NOT = {{ {held(f)} }} }} }}",
            f"\t\t\t\tscope:kehillah_chest_library = {{ add_to_variable_list = {{ name = kehillah_library_works target = flag:{f} }} kehillah_lib_refresh_cache_effect = yes }}",
            "\t\t\t}",
        ]
    out += ["\t\t}", "\t}", "}"]
    out += [
        "",
        "# Title scope: a sack seizes one volume (never the Tanakh) into the",
        "# ransom pool (section 7.2).",
        "kehillah_lib_seize_one_effect = {",
        "\tif = {",
        "\t\tlimit = {",
        "\t\t\tOR = {",
    ]
    out += [f"\t\t\t\t{held(f)}" for f in chest]
    out += ["\t\t\t}", "\t\t}", "\t\trandom_list = {"]
    for f in chest:
        out += [
            "\t\t\t1 = {",
            f"\t\t\t\ttrigger = {{ {held(f)} }}",
            f"\t\t\t\tremove_list_variable = {{ name = kehillah_library_works target = flag:{f} }}",
            f"\t\t\t\tif = {{ limit = {{ NOT = {{ is_target_in_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }} }} }}",
            f"\t\t\t\t\tadd_to_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }}",
            "\t\t\t\t}",
            "\t\t\t}",
        ]
    out += ["\t\t}", "\t\tkehillah_lib_refresh_cache_effect = yes", "\t}", "}"]
    out += [
        "",
        "# Scope: none (yearly). An authored work is forgotten -- no copy in any",
        "# library, none in the ransom pool, no living reader in the index -- and",
        "# its slot is freed for a new book (Daniel, 2026-11-08: 100 slots, recycled).",
        "kehillah_sefer_recycle_slots_effect = {",
    ]
    for f in slots:
        out += [
            "\tif = {",
            "\t\tlimit = {",
            f"\t\t\thas_global_variable = kehillah_wk_{f}_written",
            f"\t\t\tkehillah_lib_copies_{f} < 1",
            f"\t\t\tNOT = {{ is_target_in_global_variable_list = {{ name = kehillah_ransom_pool target = flag:{f} }} }}",
            "\t\t\tNOT = {",
            "\t\t\t\tany_in_global_list = {",
            "\t\t\t\t\tvariable = kehillah_sefer_masters",
            "\t\t\t\t\tis_alive = yes",
            f"\t\t\t\t\t{held(f, '', 'kehillah_mastered_works')}",
            "\t\t\t\t}",
            "\t\t\t}",
            "\t\t}",
            f"\t\tkehillah_sefer_forget_slot_effect = {{ SLOT = {f} }}",
            "\t}",
        ]
    out += ["}"]
    out += [
        "",
        "# Scope: a champion with var:kehillah_sefer_named_work set (event option).",
        "kehillah_sefer_schism_dispatch_effect = {",
    ]
    first = True
    for f in order:
        if not works[f].get("argues_for"):
            continue
        out += [
            f"\t{'if' if first else 'else_if'} = {{",
            f"\t\tlimit = {{ var:kehillah_sefer_named_work ?= flag:{f} }}",
            f"\t\tkehillah_sefer_work_schism_{f}_effect = yes",
            "\t}",
        ]
        first = False
    out += ["}", ""]

    # Standing: seeding and yearly recalculation, rite scope.
    out += [
        "# ---- standing (rite scope). Seed every non-canon work's tier and reception from",
        "# its baseline, inheriting from the faith's main rite when that is already seeded.",
        "kehillah_standing_seed_rite_effect = {",
    ]
    for f in order:
        w = works[f]
        if w.get("canon") or needs_writing(w):
            continue
        out.append(f"\tkehillah_standing_seed_work_effect = {{ KEY = {f} }}")
    out += [
        "\tset_variable = { name = kehillah_standing_ready value = yes }",
        "}",
        "",
        "# Rite scope. Seed one written work (named or authored) when it is written.",
        "kehillah_standing_seed_written_works_effect = {",
    ]
    for f in order:
        w = works[f]
        if not needs_writing(w):
            continue
        out += [
            "\tif = {",
            "\t\tlimit = {",
            f"\t\t\thas_global_variable = kehillah_wk_{f}_written",
            f"\t\t\tNOT = {{ has_variable = kehillah_standing_{f} }}",
            "\t\t}",
            f"\t\tkehillah_standing_seed_work_effect = {{ KEY = {f} }}",
            "\t}",
        ]
    out += [
        "}",
        "",
        "# Rite scope. Yearly: recalculate every seeded work.",
        "kehillah_standing_yearly_rite_effect = {",
        "\tkehillah_standing_seed_written_works_effect = yes",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [
            "\tif = {",
            f"\t\tlimit = {{ has_variable = kehillah_standing_{f} }}",
            f"\t\tkehillah_standing_recalc_work_effect = {{ KEY = {f} }}",
            "\t}",
        ]
    out += [
        "}",
        "",
        "# Rite scope. After a reform changes a tenet's status or a rite's core",
        "# tenets, every seeded work's ceiling is refreshed at once and its tier",
        "# clamped to the new ceiling and floor (the tenet-reform loop, 2026-11-08).",
        "kehillah_standing_refresh_ceilings_rite_effect = {",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [
            "\tif = {",
            f"\t\tlimit = {{ has_variable = kehillah_standing_{f} }}",
            f"\t\tset_variable = {{ name = kehillah_ceiling_{f} value = kehillah_lib_ceiling_{f} }}",
            f"\t\tif = {{ limit = {{ var:kehillah_standing_{f} > 0 }} clamp_variable = {{ name = kehillah_standing_{f} min = kehillah_lib_floor_{f} max = kehillah_lib_ceiling_{f} }} }}",
            "\t}",
        ]
    out += [
        "}",
        "",
        "# Rite scope. 2026-11-11 (one scale): an older save's Classic, Authoritative",
        "# and Venerated (8-10) all become Authoritative (8); kehillah_sefer_migrate_save_effect.",
        "kehillah_standing_one_scale_rite_effect = {",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out.append(f"\tif = {{ limit = {{ has_variable = kehillah_standing_{f} var:kehillah_standing_{f} > {TOP_EARNED} }} "
                   f"set_variable = {{ name = kehillah_standing_{f} value = {TOP_EARNED} }} }}")
    out += [
        "}",
        "",
        "# Rite scope. 2026-11-11 (Daniel): a Jewish rite of neither tradition (the Beta",
        "# Israel, the Samaritans) had seeded other traditions' works as Banned or",
        "# Rejected; they are Obscure to it. Once, from kehillah_sefer_migrate_save_effect.",
        "kehillah_standing_other_faiths_obscure_rite_effect = {",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out.append(f"\tif = {{ limit = {{ has_variable = kehillah_standing_{f} var:kehillah_standing_{f} < {UNKNOWN_TO_FAITH} }} "
                   f"set_variable = {{ name = kehillah_standing_{f} value = {UNKNOWN_TO_FAITH} }} "
                   f"set_variable = {{ name = kehillah_reception_{f} value = {UNKNOWN_TO_FAITH * 10 - 5} }} }}")
    out += [
        "}",
        "",
        "# Title scope (a library). Count its Banned works in its holder's rite into",
        "# var:kehillah_lib_banned_count. Section 4 of Daniel's 2026-11-08 decisions.",
        "kehillah_lib_count_banned_effect = {",
        "\tset_variable = { name = kehillah_lib_banned_count value = 0 }",
        "\tif = {",
        "\t\tlimit = { exists = holder }",
        "\t\tholder = { save_scope_as = kehillah_banned_viewer }",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [
            "\t\tif = {",
            f"\t\t\tlimit = {{ {held(f)} scope:kehillah_banned_viewer = {{ kehillah_lib_standing_{f} <= 1 }} }}",
            "\t\t\tchange_variable = { name = kehillah_lib_banned_count add = 1 }",
            "\t\t}",
        ]
    out += ["\t}", "}", ""]

    write(STUDY_EFFECTS, out)


# ---------------------------------------------------------------------------
# GUI: selected-book study, readers, donate/studied
# ---------------------------------------------------------------------------

def write_study_gui(order, works):
    out = HEADER + [
        "# Selected-book starters for the Learn Torah personal scheme. 2026-11-08:",
        "# each takes scope:library, the library whose shelf the button sits on (the",
        "# Library body's Title, or the library picked in the Learn Torah decision),",
        "# and is valid wherever kehillah_study_can_read_library_trigger lets the",
        "# reader study. The course remembers that library (var:kehillah_study_library).",
        "# 10 Piety, as the decision costs.",
        "# 2026-11-11: or, for a course waiting for its next book (\"choose later\" in",
        "# kehillah_study_torah.0001), the next book, free: the course goes on.",
        "# 2026-11-11 (Daniel: \"make the learn button able to replace the current",
        "# scheme with a confirmation\"): partway through a book, the button stores",
        "# the new book and asks first (kehillah_study_torah.0008).",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            "",
            f"kehillah_lib_study_{f} = {{",
            "	scope = character",
            "	saved_scopes = { library }",
            "	is_shown = { always = yes }",
            "	is_valid = {",
            "		custom_tooltip = {",
            "			text = kehillah_lib_study_cannot_tt",
            "			kehillah_lib_can_choose_study_trigger = yes",
            "		}",
            "		custom_tooltip = {",
            "			text = kehillah_lib_study_reading_now_tt",
            f"			NOT = {{ var:kehillah_study_current_work_id ?= {i} }}",
            "		}",
            f"		scope:library = {{ is_target_in_variable_list = {{ name = kehillah_library_works target = flag:{f} }} }}",
            "		custom_tooltip = {",
            "			text = kehillah_study_library_not_readable_tt",
            "			kehillah_study_can_read_library_trigger = { CHARACTER = root LIBRARY = scope:library }",
            "		}",
            "	}",
            "	effect = {",
            "		if = {",
            "			limit = { kehillah_study_can_switch_book_trigger = yes }",
            f"			set_variable = {{ name = kehillah_study_pending_work_id value = {i} }}",
            "			set_variable = { name = kehillah_study_pending_library value = scope:library }",
            "			trigger_event = kehillah_study_torah.0008",
            "		}",
            "		else = {",
            "			kehillah_lib_study_start_course_effect = {",
            f"				WORK_ID = {i}",
            "			}",
            "		}",
            "	}",
            "}",
        ]
    write(STUDY_GUI, out)


def write_readers_gui(order):
    out = HEADER + [
        "# Reader roster for selected books. The global index is populated on mastery.",
        "# A player's older-save mastery is indexed when that player opens a roster.",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            "",
            f"kehillah_lib_readers_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = { always = yes }",
            "\teffect = {",
            "\t\tclear_variable_list = kehillah_lib_readers",
            "\t\tkehillah_lib_index_yeshiva_readers_effect = yes",
            f"\t\tset_variable = {{ name = kehillah_lib_readers_work_id value = {i} }}",
            "\t\tif = {",
            "\t\t\tlimit = {",
            f"\t\t\t\t{held(f, '', 'kehillah_mastered_works')}",
            "\t\t\t\tNOT = { is_target_in_global_variable_list = { name = kehillah_sefer_masters target = this } }",
            "\t\t\t}",
            "\t\t\tadd_to_global_variable_list = { name = kehillah_sefer_masters target = this }",
            "\t\t}",
            "\t\tsave_scope_as = kehillah_lib_reader_viewer",
            "\t\tevery_in_global_list = {",
            "\t\t\tvariable = kehillah_sefer_masters",
            "\t\t\tlimit = {",
            "\t\t\t\tis_alive = yes",
            "\t\t\t\tOR = {",
            "\t\t\t\t\thas_trait = kehillah_rabbi_trait",
            "\t\t\t\t\thas_trait = lifestyle_scholar",
            # 2026-11-08: Karaites have no clergy; every Karaite reader counts.
            "\t\t\t\t\tkehillah_is_karaite_character_trigger = yes",
            "\t\t\t\t}",
            f"\t\t\t\t{held(f, '', 'kehillah_mastered_works')}",
            "\t\t\t}",
            "\t\t\tsave_scope_as = kehillah_lib_reader_candidate",
            "\t\t\tscope:kehillah_lib_reader_viewer = {",
            "\t\t\t\tadd_to_variable_list = { name = kehillah_lib_readers target = scope:kehillah_lib_reader_candidate }",
            "\t\t\t}",
            "\t\t}",
            "\t}",
            "}",
            "",
            f"kehillah_lib_readers_loaded_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            f"\tis_valid = {{ has_variable = kehillah_lib_readers_work_id var:kehillah_lib_readers_work_id = {i} }}",
            "}",
        ]
    write(READERS_GUI, out)


def write_actions_gui(order, works):
    out = HEADER + [
        "# Moved from kehillah_map_view_gui.txt 2026-11-08. Donate a copy (Tanakh never",
        "# leaves: every library keeps it), and the mastered check mark.",
    ]
    for f in order:
        w = works[f]
        valid = [f"\t\tkehillah_lib_own_library_has_trigger = {{ WORK = flag:{f} }}"]
        if w["corpus"] == "tanakh":
            valid = ["\t\talways = no"]
        out += [
            "",
            f"kehillah_lib_donate_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = {",
        ] + valid + [
            "\t}",
            "\teffect = {",
            "\t\tkehillah_lib_refresh_own_library_effect = yes",
            f"\t\tsave_scope_value_as = {{ name = kehillah_donate_work value = flag:{f} }}",
            "\t\ttrigger_event = kehillah_library.0001",
            "\t}",
            "}",
            "",
            f"kehillah_lib_studied_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            f"\tis_valid = {{ {held(f, '', 'kehillah_mastered_works')} }}",
            "\teffect = { }",
            "}",
        ]
    write(ACTIONS_GUI, out)


# ---------------------------------------------------------------------------
# Localization
# ---------------------------------------------------------------------------

def author_link(slug):
    return f"[GetPlayer.MakeScope.Var('kehillah_lib_author_{slug}').Char.GetShortUIName]"


def written_author_possessive(f):
    return f"[GetGlobalVariable('kehillah_wk_{f}_author').GetCharacter.GetFirstNamePossessiveNoTooltip]"


def written_author_link(f):
    return f"[GetGlobalVariable('kehillah_wk_{f}_author').GetCharacter.GetShortUIName]"


def write_loc(order, works):
    lines = ["l_english:"]
    lines += [
        ' KEHILLAH_LIB_ROW_GENRE:0 "Genre"',
        ' KEHILLAH_LIB_ROW_RANK:0 "Canonicity"',  # 2026-11-11: was Standing (Daniel)
        ' KEHILLAH_LIB_ROW_COMPOSER:0 "Composer"',
        ' KEHILLAH_LIB_ROW_COMPOSED:0 "Composed"',
    ]
    for genre, n in GENRES.items():
        lines.append(
            f" KEHILLAH_LIB_GROUP_{genre.upper()}:0 "
            f"\"$KEHILLAH_LIB_TRACK_{genre.upper()}$ (#weak [Title.MakeScope.ScriptValue('kehillah_lib_genre_{n}_held_count_value')|0]#!)\""
        )
    for f in order:
        w = works[f]
        subject = f"$kehillah_lib_subject_{f}$"
        plain_name = w.get("composer_name") or AUTHOR_NAMES.get(w.get("composer_char") or "", "")
        if needs_writing(w):
            lines.append(f' kehillah_lib_composer_{f}:0 "{written_author_link(f)}"')
            lines.append(f' kehillah_lib_composer_plain_{f}:0 "{w["composer"] or plain_name}"')
        else:
            lines.append(f' kehillah_lib_composer_{f}:0 "{w["composer"]}"')
            lines.append(f' kehillah_lib_composer_plain_{f}:0 "{w["composer"]}"')
        if w.get("composer_linked"):
            lines.append(f' kehillah_lib_composer_linked_{f}:0 "{w["composer_linked"]}"')
        if needs_writing(w):
            lines.append(f' kehillah_lib_year_text_{f}:0 "[GetPlayer.MakeScope.ScriptValue(\'kehillah_lib_year_{f}\')|0]"')
        elif w.get("year_text"):
            lines.append(f' kehillah_lib_year_text_{f}:0 "{w["year_text"]}"')
        else:
            lines.append(f' kehillah_lib_year_text_{f}:0 "c. {w["year"]}"')
        lines.append(f' kehillah_lib_summary_{f}:0 "Work of {subject}"')
        if w.get("canon"):
            who_line = f"{w['credit']} {{who}}."
        elif needs_writing(w):
            who_line = f"{w['credit']} {{who}}."
        else:
            who_line = f"{w['credit']} {{who}} around {w['year']}."
        if needs_writing(w):
            who = written_author_link(f)
            plain = plain_name
        elif w.get("composer_char"):
            who = author_link(w["composer_char"])
            plain = AUTHOR_NAMES[w["composer_char"]]
        else:
            who = w["composer_name"]
            plain = who
        blurb = lambda name: f"A work of {GAMEPLAY}{subject}#!. " + who_line.format(who=name)
        lines.append(f' kehillah_lib_blurb_{f}:0 "{blurb(who)}"')
        lines.append(f' kehillah_lib_blurb_plain_{f}:0 "{blurb(plain)}"')
    write(LOC, lines)


def write_prose_loc(order, works):
    lines = ["l_english:"]
    track = {"parshanut": "PARSHANUT", "talmudics": "TALMUDICS", "hashkafa": "HASHKAFA"}
    for f in order:
        w = works[f]
        if authored(w):
            n = int(f.split("_")[-1])
            name = f"{written_author_possessive(f)} [GetPlayer.Custom('KehillahAuthoredKind{n:02d}')]"
            lines += [
                f' kehillah_lib_name_{f}:0 "{name}"',
                f' kehillah_lib_subject_{f}:0 "[GetPlayer.Custom(\'KehillahAuthoredKind{n:02d}\')]"',
                f' kehillah_lib_desc_{f}:0 "A [GetPlayer.Custom(\'KehillahAuthoredKind{n:02d}\')|l] written in this campaign by {written_author_link(f)}."',
                f' kehillah_lib_detail_{f}:0 "$kehillah_lib_desc_{f}$ Its standing in each rite is earned: copies, readers, approbations, teaching and citations raise it, controversy can sink it."',
                f' kehillah_lib_tt_{f}:0 "#T $kehillah_lib_name_{f}$#!\\n#weak $kehillah_lib_subject_{f}$#!\\n\\n$kehillah_lib_detail_{f}$"',
                f' {study_tt_key(f, w)}:0 "You take up $kehillah_lib_name_{f}$ and read it closely."',
                f' kehillah_yeshiva_msg_work_{f}:0 "[kehillah_msg_talmid.GetTitledFirstName] has mastered $kehillah_lib_name_{f}$ at the yeshiva."',
            ]
            continue
        p = w.get("prose")
        if not p:
            continue
        t = track[w["genre"]]
        lines += [
            f' kehillah_lib_name_{f}:0 "{p["name"]}"',
            f' kehillah_lib_subject_{f}:0 "$KEHILLAH_LIB_TRACK_{t}$"',
            f' kehillah_lib_desc_{f}:0 "{p["desc"]}"',
            f' kehillah_lib_detail_{f}:0 "{p["detail"]}"',
            f' kehillah_lib_tt_{f}:0 "#T $kehillah_lib_name_{f}$#!\\n#weak $KEHILLAH_LIB_TRACK_{t}$#!\\n\\n$kehillah_lib_detail_{f}$"',
            f' {study_tt_key(f, w)}:0 "{p["study"]}"',
            f' kehillah_yeshiva_msg_work_{f}:0 "[kehillah_msg_talmid.GetTitledFirstName] has mastered $kehillah_lib_name_{f}$ at the yeshiva."',
        ]
    write(PROSE_LOC, lines)


def write_authored_custom_loc(order, works):
    out = HEADER + [
        "# The kind of each book written during play, one per slot; its name is",
        "# the author's name and this kind, as medieval works were cited.",
        "# Set by kehillah_sefer_write_authored_work_effect. Type character: any",
        "# character root works, since the triggers read global variables.",
    ]
    for f in order:
        if not authored(works[f]):
            continue
        n = int(f.split("_")[-1])
        out += [f"KehillahAuthoredKind{n:02d} = {{", "\ttype = character"]
        for k in AUTHORED_KINDS:
            out += [
                "\ttext = {",
                f"\t\ttrigger = {{ global_var:kehillah_wk_{f}_kind ?= {k} }}",
                f"\t\tlocalization_key = KEHILLAH_AUTHORED_KIND_{k}",
                "\t}",
            ]
        out += ["\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = KEHILLAH_AUTHORED_KIND_NONE", "\t}", "}"]
        # 2026-11-10: the language its author chose (docs/spec/2026-11-10-sefer-languages.md).
        out += [f"KehillahAuthoredLang{n:02d} = {{", "\ttype = character",
                "\ttext = {", f"\t\ttrigger = {{ global_var:kehillah_wk_{f}_lang ?= flag:aramaic }}",
                "\t\tlocalization_key = language_aramaic_name", "\t}",
                "\ttext = {", "\t\ttrigger = {", f"\t\t\tglobal_var:kehillah_wk_{f}_lang ?= flag:vernacular",
                f"\t\t\texists = global_var:kehillah_wk_{f}_lang_culture", "\t\t}",
                f"\t\tlocalization_key = kehillah_lib_lang_vernacular_{f}", "\t}",
                "\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = language_israelite_name", "\t}", "}"]
    write(AUTHORED_CUSTOM_LOC, out)


# ---------------------------------------------------------------------------
# Acquisition (V48) and journey (V49), as before, now with availability
# ---------------------------------------------------------------------------

def write_acquisition_effects(order, works):
    out = HEADER + [
        "# Rebuilds the title-owned list shown by the Library's acquisition page.",
        "# A work is added only once it circulates in this campaign and only while",
        "# unowned. Missing Bavli orders are kept on a second, priority list so the",
        "# page and the AI put completing the Shas first (spec section 5.2).",
        "# Scope: the acquiring character; LIBRARY is the title to acquire for.",
        "",
        "kehillah_library_refresh_acquisition_candidates_effect = {",
        "\tkehillah_lib_resolve_own_library_effect = yes",
        "\tscope:kehillah_own_library_scope ?= {",
        "\t\tclear_variable_list = kehillah_library_acquisition_candidates",
        "\t\tclear_variable_list = kehillah_library_acquisition_priority",
    ]
    for f in order:
        w = works[f]
        if w["corpus"] == "tanakh":
            continue
        av = avail_lines(f, w, "\t\t\t\t")
        out += ["\t\tif = {", "\t\t\tlimit = {"] + av + [
            f"\t\t\t\tNOT = {{ {held(f)} }}",
            "\t\t\t}",
            f"\t\t\tadd_to_variable_list = {{ name = kehillah_library_acquisition_candidates target = flag:{f} }}",
        ]
        if w["corpus"] == "bavli":
            out += [f"\t\t\tadd_to_variable_list = {{ name = kehillah_library_acquisition_priority target = flag:{f} }}"]
        out.append("\t\t}")
    out += ["\t}", "}"]
    write(ACQUIRE_EFFECTS, out)


def ledger_order(order, works):
    """The Sefarim ledger lists works by date: historical works by year (catalog
    order breaks ties), then the books written in play, by slot."""
    fixed = [f for f in order if not authored(works[f])]
    fixed.sort(key=lambda f: (works[f]["year"], order.index(f)))
    return fixed + [f for f in order if authored(works[f])]


def known_lines(f, w, ind):
    """Trigger lines (scope: the player): the community has heard of the work.
    Shelf-and-ledger design, docs/implementation/2026-11-08-library-shelf-and-ledger.md:
    the canon and the great works (Foundational, Essential) are known to all once
    they circulate; anything else only once it is met -- held in the player's own
    library, mastered by the player or a courtier, or respected in the player's
    rite with a copy somewhere. Obscure and forbidden books stay off the ledger
    until then."""
    if w.get("canon") or w["rank_name"] in ("Foundational", "Essential"):
        return []
    return [
        f"{ind}OR = {{",
        f"{ind}\tvar:kehillah_own_library ?= {{ {held(f)} }}",
        f"{ind}\t{held(f, '', 'kehillah_mastered_works')}",
        f"{ind}\tany_courtier = {{ {held(f, '', 'kehillah_mastered_works')} }}",
        f"{ind}\tAND = {{",
        f"{ind}\t\tkehillah_lib_standing_{f} >= 6",
        f"{ind}\t\tkehillah_lib_copies_{f} >= 1",
        f"{ind}\t}}",
        f"{ind}}}",
    ]


def rite_known_lines(f, w, ind):
    """Trigger lines (scope: the player; scope:kehillah_ledger_view_rite = a rite
    other than the player's): the rite's followers know of the work. 2026-11-10
    (Daniel: "a way to view other rites' and religions' book tiers and known
    books"). The canon and the great works are known everywhere once they
    circulate, as in known_lines; anything else once a library of that rite holds
    it, or once the rite respects it and a copy exists somewhere."""
    if w.get("canon") or w["rank_name"] in ("Foundational", "Essential"):
        return []
    return [
        f"{ind}OR = {{",
        f"{ind}\tany_in_global_list = {{",
        f"{ind}\t\tvariable = kehillah_libraries",
        f"{ind}\t\texists = holder",
        f"{ind}\t\tholder = {{ rite ?= scope:kehillah_ledger_view_rite }}",
        f"{ind}\t\t{held(f)}",
        f"{ind}\t}}",
        f"{ind}\tAND = {{",
        f"{ind}\t\tscope:kehillah_ledger_view_rite = {{ kehillah_lib_rite_standing_{f} >= 6 }}",
        f"{ind}\t\tkehillah_lib_copies_{f} >= 1",
        f"{ind}\t}}",
        f"{ind}}}",
    ]


def write_catalog_list_effects(order, works):
    """The Sefarim ledger (2026-11-08): every work the community knows of."""
    out = HEADER + [
        "# The Sefarim ledger (2026-11-08; it replaced the Library's All works page",
        "# the same day): rebuilds the player's kehillah_lib_catalog_works with every",
        "# work in circulation that the community knows of (known_lines in the",
        "# generator), by date, and counts them (var:kehillah_lib_catalog_count). A",
        "# GUI cannot read a global list, so the ledger reads this character list.",
        "# Scope: the player (scripted guis kehillah_lib_catalog_refresh and",
        "# kehillah_lib_ledger_open, common/scripted_guis/kehillah_library_catalog_page_gui.txt).",
        "",
        "kehillah_lib_refresh_catalog_list_effect = {",
        "\tkehillah_lib_refresh_own_library_effect = yes",
        "\tclear_variable_list = kehillah_lib_catalog_works",
        "\tset_variable = { name = kehillah_lib_catalog_count value = 0 }",
    ]
    def append_rows(sequence, known=known_lines):
        for f in sequence:
            add = [
                f"add_to_variable_list = {{ name = kehillah_lib_catalog_works target = flag:{f} }}",
                "change_variable = { name = kehillah_lib_catalog_count add = 1 }",
            ]
            cond = avail_lines(f, works[f], "\t\t\t") + known(f, works[f], "\t\t\t")
            if cond:
                out.extend(["\tif = {", "\t\tlimit = {"] + cond + ["\t\t}"] + [f"\t\t{a}" for a in add] + ["\t}"])
            else:
                out.extend(f"\t{a}" for a in add)

    append_rows(ledger_order(order, works))
    out += ["}", "", "# The same known-work rules, sorted by displayed catalog name.",
            "kehillah_lib_refresh_catalog_name_effect = {",
            "\tkehillah_lib_refresh_own_library_effect = yes",
            "\tclear_variable_list = kehillah_lib_catalog_works",
            "\tset_variable = { name = kehillah_lib_catalog_count value = 0 }"]
    # The historical display names live in the generated localization. Authored
    # slots receive names in play, so keep them after the fixed titles.
    names = {}
    for path in (LOC, PROSE_LOC):
        for flag, name in re.findall(r'^\s*kehillah_lib_name_(work_[a-z0-9_]+):0 "([^"]*)"', path.read_text(encoding="utf-8-sig"), re.M):
            names[flag] = name
    by_name = sorted(order, key=lambda f: (authored(works[f]), names.get(f, f).casefold()))
    append_rows(by_name)
    out += ["}"]
    # 2026-11-10: the same list as ANOTHER rite knows it (rite_known_lines), for
    # the ledger's rite selector. The ledger's dispatcher
    # (kehillah_ledger_rebuild_effect, common/scripted_effects/
    # kehillah_library_ledger_effects.txt) picks the pair to run.
    for name, sequence in (("list", ledger_order(order, works)), ("name", by_name)):
        out += ["",
                f"# Scope: the player. var:kehillah_ledger_rite = the rite to list for ({'by date' if name == 'list' else 'by name'}).",
                f"kehillah_lib_refresh_rite_catalog_{name}_effect = {{",
                "\tkehillah_lib_refresh_own_library_effect = yes",
                "\tclear_variable_list = kehillah_lib_catalog_works",
                "\tset_variable = { name = kehillah_lib_catalog_count value = 0 }",
                "\tvar:kehillah_ledger_rite ?= { save_scope_as = kehillah_ledger_view_rite }",
                "\tif = {",
                "\t\tlimit = { exists = scope:kehillah_ledger_view_rite }"]
        start = len(out)
        append_rows(sequence, rite_known_lines)
        out[start:] = ["\t" + line for line in out[start:]]
        out += ["\t}", "}"]
    write(CATALOG_LIST_EFFECTS, out)


# ---------------------------------------------------------------------------
# The shelf and the ledger (2026-11-08)
# ---------------------------------------------------------------------------

# Binding tier by the viewer's standing: (lowest standing, tier). Tier 1 is an
# Anathema, kept only to answer it; 7 the canon binding (2026-11-11, one scale).
SPINE_TIERS = [(1, 2), (3, 3), (5, 4), (7, 5), (8, 6), (9, 7)]
# Spine width in pixels by tier, as drawn by scripts/kehillah_generate_library_ui_assets.py.
# 2026-11-11: the spines are painted 1.25x larger; the shelf viewport has no
# scrollbar margin now (about 500 px inside the smaller, domicile host).
SPINE_WIDTH = {1: 18, 2: 12, 3: 18, 4: 22, 5: 28, 6: 32, 7: 38}
SPINE_GAP = 2
SHELF_ROW_WIDTH = 470
SPINE_VARIANTS = 4
# Works shown in a centrepiece instead of on the shelf: the Tanakh (the ark),
# the Bavli (the Shas case) and the Yerushalmi (its own set on the Talmud shelf).
CENTREPIECE_CORPORA = ("tanakh", "bavli", "yerushalmi")


def spine_variants(order, works):
    """A colour variant per work, cycling within its genre in catalog order, so
    neighbouring books on a shelf differ. Books written in play cycle by slot."""
    seen = {g: 0 for g in GENRES}
    out = {}
    for f in order:
        w = works[f]
        if authored(w):
            out[f] = int(f.split("_")[-1]) % SPINE_VARIANTS + 1
            continue
        out[f] = seen[w["genre"]] % SPINE_VARIANTS + 1
        seen[w["genre"]] += 1
    return out


def write_shelf_values(order, works):
    variants = spine_variants(order, works)
    out = HEADER + [
        "# The Beit Midrash shelf (2026-11-08). Every book has the same height; its",
        "# width and the quality of its binding follow its standing in the viewer's",
        "# rite, so a book that rises or falls is rebound on the next draw. Design:",
        "# docs/implementation/2026-11-08-library-shelf-and-ledger.md.",
        "",
        "# ---- binding tier (scope: the viewer) from kehillah_lib_standing_<flag>:",
        "# 1 Anathema, 2 a loose quire (Banned, Rejected), 3 limp vellum (Contested,",
        "# Obscure), 4 half-leather (Popular, Celebrated), 5 tooled leather (Esteemed),",
        "# 6 gilt leather (Authoritative), 7 the canon binding (Foundational and up).",
    ]
    for f in order:
        out += [f"kehillah_lib_spine_tier_{f} = {{", "\tvalue = 1"]
        # highest first so each branch is a plain lower bound
        branches = list(reversed(SPINE_TIERS))
        for i, (lo, tier) in enumerate(branches):
            kw = "if" if i == 0 else "else_if"
            out.append(f"\t{kw} = {{ limit = {{ kehillah_lib_standing_{f} >= {lo} }} value = {tier} }}")
        out.append("}")
    out += ["", "# ---- shelf width in pixels, gap included (scope: the viewer)."]
    for f in order:
        out += [f"kehillah_lib_spine_width_{f} = {{", f"\tvalue = {SPINE_WIDTH[1] + SPINE_GAP}"]
        for i, tier in enumerate(sorted(SPINE_WIDTH, reverse=True)[:-1]):
            kw = "if" if i == 0 else "else_if"
            out.append(f"\t{kw} = {{ limit = {{ kehillah_lib_spine_tier_{f} = {tier} }} value = {SPINE_WIDTH[tier] + SPINE_GAP} }}")
        out.append("}")
    out += ["", "# ---- frame in each kehillah_spine_t<tier>.dds strip (any scope): four",
            "# colours per genre, (genre - 1) * 4 + variant."]
    for f in order:
        w = works[f]
        if authored(w):
            out += [
                f"kehillah_lib_spine_frame_{f} = {{",
                f"\tvalue = kehillah_lib_genre_{f}",
                "\tsubtract = 1",
                f"\tmultiply = {SPINE_VARIANTS}",
                f"\tadd = {variants[f]}",
                "}",
            ]
        else:
            out.append(f"kehillah_lib_spine_frame_{f} = {(GENRES[w['genre']] - 1) * SPINE_VARIANTS + variants[f]}")
    out += ["", "# ---- stable work mark, independent of rite and binding tier."]
    for index, f in enumerate(order, 1):
        out.append(f"kehillah_lib_spine_mark_{f} = {index}")
    out += ["", "# ---- 1 when the scoped library title holds the work (scope: a library title)."]
    for f in order:
        out += [f"kehillah_lib_held_{f} = {{", "\tvalue = 0", f"\tif = {{ limit = {{ {held(f)} }} value = 1 }}", "}"]
    out += [
        "",
        "# ---- shelf entries the scoped library holds, every genre (scope: a library",
        "# title). Each corpus volume counts on its own, as in the genre counts.",
        "kehillah_lib_shelf_count_value = {",
        "\tvalue = kehillah_lib_genre_1_held_count_value",
        "\tadd = kehillah_lib_genre_2_held_count_value",
        "\tadd = kehillah_lib_genre_3_held_count_value",
        "}",
    ]
    out += ["", "# ---- 1 when the scoped library has commissioned a copy of the work (scope:",
            "# a library title)."]
    for f in order:
        out += [
            f"kehillah_lib_sought_{f} = {{",
            "\tvalue = 0",
            f"\tif = {{ limit = {{ {held(f, '', 'kehillah_library_commission_work')} }} value = 1 }}",
            "}",
        ]
    write(SHELF_VALUES, out)


def write_shelf_effects(order, works):
    out = HEADER + [
        "# Lays out the Beit Midrash shelf (2026-11-08). The GUI cannot measure the",
        "# books it lists, so this fills each genre's shelves here: books in band order",
        "# (Foundational first), a new shelf when the next binding would overflow",
        f"# {SHELF_ROW_WIDTH} px. It also picks each genre's reading-stand book: the held work",
        "# of the highest standing in the viewer's rite. The stand is shown for",
        "# Machshavah, which has no foundational work, and for Talmudics when the viewer's",
        "# rite does not hold the Bavli canonical (a Karaite library).",
        "# Scope: the viewer; scope:library is the library shown. Results are variables",
        "# on the viewer: kehillah_lib_row_<flag> (shelf number, 0 when the book is",
        "# not on a shelf), kehillah_lib_rows_<genre> (shelves used) and",
        "# kehillah_lib_stand_<genre> (the stand's work, when there is one).",
        "# Run by the scripted gui kehillah_lib_shelf_layout.",
        "",
        "kehillah_lib_shelf_layout_effect = {",
    ]
    for g in GENRES.values():
        out += [
            f"\tset_variable = {{ name = kehillah_lib_acc_{g} value = 0 }}",
            f"\tset_variable = {{ name = kehillah_lib_rowc_{g} value = 1 }}",
            f"\tset_variable = {{ name = kehillah_lib_best_{g} value = -1 }}",
            f"\tset_variable = {{ name = kehillah_lib_stand_{g} value = flag:none }}",
        ]
    shelf = [f for f in order if works[f]["corpus"] not in CENTREPIECE_CORPORA]
    # Every work's row is kept set (0 = not on a shelf), the centrepieces'
    # included, and an empty stand holds flag:none, so the GUI never reads an
    # unset variable.
    for f in order:
        out.append(f"\tset_variable = {{ name = kehillah_lib_row_{f} value = 0 }}")

    def per_genre(f, effect, genres=tuple(GENRES.values())):
        w = works[f]
        if authored(w):
            return [f"\tif = {{ limit = {{ kehillah_lib_genre_{f} = {g} }} {effect} = {{ G = {g} F = {f} }} }}"
                    for g in genres]
        if GENRES[w["genre"]] not in genres:
            return []
        return [f"\t{effect} = {{ G = {GENRES[w['genre']]} F = {f} }}"]

    # Machshavah always has a stand; Talmudics only where the viewer's rite does
    # not hold the Bavli canonical. Parshanut has the ark instead.
    out += ["", "\t# The reading stands."]
    for f in shelf:
        out += per_genre(f, "kehillah_lib_shelf_stand_try_effect", (3,))
    out += ["\tif = {", f"\t\tlimit = {{ kehillah_lib_standing_work_bavli_moed < {CANON['oral_torah']} }}"]
    for f in shelf:
        out += ["\t" + ln for ln in per_genre(f, "kehillah_lib_shelf_stand_try_effect", (2,))]
    out += ["\t}"]
    out += ["", "\t# The shelves, band by band."]
    for band in range(1, 6):
        for f in shelf:
            w = works[f]
            if RANKS[w["rank_name"]][0] != band:
                continue
            out += per_genre(f, "kehillah_lib_shelf_place_effect")
    out += [""]
    # Remove-then-set: only the GUI reads these, and reading them in a limit keeps
    # the engine's set-but-never-used lint quiet (as in kehillah_library_authors_effects).
    for g in GENRES.values():
        out += [
            f"\tif = {{ limit = {{ exists = var:kehillah_lib_rows_{g} }} remove_variable = kehillah_lib_rows_{g} }}",
            f"\tset_variable = {{ name = kehillah_lib_rows_{g} value = var:kehillah_lib_rowc_{g} }}",
            f"\tif = {{ limit = {{ var:kehillah_lib_acc_{g} = 0 }} set_variable = {{ name = kehillah_lib_rows_{g} value = 0 }} }}",
        ]
    out += ["}", ""]
    out += [
        "# Parameters G (genre) and F (work flag): the held work of the highest",
        "# standing so far takes the genre's reading stand.",
        "kehillah_lib_shelf_stand_try_effect = {",
        "\tif = {",
        "\t\tlimit = {",
        "\t\t\tscope:library ?= { is_target_in_variable_list = { name = kehillah_library_works target = flag:$F$ } }",
        "\t\t\tkehillah_lib_standing_$F$ > var:kehillah_lib_best_$G$",
        "\t\t}",
        "\t\tset_variable = { name = kehillah_lib_best_$G$ value = kehillah_lib_standing_$F$ }",
        "\t\tset_variable = { name = kehillah_lib_stand_$G$ value = flag:$F$ }",
        "\t}",
        "}",
        "",
        f"# Parameters G and F: put a held book on the next shelf with room ({SHELF_ROW_WIDTH} px).",
        "kehillah_lib_shelf_place_effect = {",
        "\tif = {",
        "\t\tlimit = {",
        "\t\t\tscope:library ?= { is_target_in_variable_list = { name = kehillah_library_works target = flag:$F$ } }",
        "\t\t\tNOT = { var:kehillah_lib_stand_$G$ ?= flag:$F$ }",
        "\t\t}",
        "\t\tchange_variable = { name = kehillah_lib_acc_$G$ add = kehillah_lib_spine_width_$F$ }",
        "\t\tif = {",
        f"\t\t\tlimit = {{ var:kehillah_lib_acc_$G$ > {SHELF_ROW_WIDTH} }}",
        "\t\t\tchange_variable = { name = kehillah_lib_rowc_$G$ add = 1 }",
        "\t\t\tset_variable = { name = kehillah_lib_acc_$G$ value = kehillah_lib_spine_width_$F$ }",
        "\t\t}",
        "\t\tset_variable = { name = kehillah_lib_row_$F$ value = var:kehillah_lib_rowc_$G$ }",
        "\t}",
        "}",
    ]
    write(SHELF_EFFECTS, out)


def short_byline(w):
    """The Author column: one short name. "an anonymous author" -> "Anonymous";
    "the Prophets" -> "The Prophets"; else the composer note."""
    if w.get("byline"):
        return w["byline"]
    n = w.get("composer_name")
    if n:
        if n.startswith(("an ", "a ")):
            return "Anonymous"
        return n[0].upper() + n[1:]
    return w["composer"]


def write_ledger_loc(order, works):
    """Per-work lines of the Sefarim ledger: place, language, author, tenets."""
    lines = ["l_english:"]
    for f in order:
        w = works[f]
        if authored(w):
            lines += [
                f' kehillah_lib_place_{f}:0 "$KEHILLAH_SEFARIM_PLACE_WRITTEN_IN_PLAY$"',
                # 2026-11-10: the language its author chose (Sefer languages).
                f' kehillah_lib_language_{f}:0 "[GetPlayer.Custom(\'KehillahAuthoredLang{int(f.split("_")[-1]):02d}\')]"',
                f' kehillah_lib_lang_vernacular_{f}:0 "[GetGlobalVariable(\'kehillah_wk_{f}_lang_culture\').Culture.GetName] vernacular"',
                f' kehillah_lib_byline_{f}:0 "{written_author_link(f)}"',
                f' kehillah_lib_byline_plain_{f}:0 "$KEHILLAH_SEFARIM_AUTHOR_UNKNOWN$"',
                f' kehillah_lib_tenets_{f}:0 "$KEHILLAH_SEFARIM_TENETS_AUTHORED$"',
                f' kehillah_lib_class_{f}:0 "{w["rank_name"]}"',
            ]
            continue
        if needs_writing(w):
            byline = written_author_link(f)
            # 2026-11-11: the short, capitalised name (short_byline) for the Author column.
            plain = short_byline(w) if w.get("composer_name") else (AUTHOR_NAMES.get(w.get("composer_char") or "", "") or w["composer"])
        elif w.get("composer_char"):
            byline = author_link(w["composer_char"])
            plain = AUTHOR_NAMES[w["composer_char"]]
        else:
            # 2026-11-11 (Daniel: author values simple and consistent): one short
            # name, never the full composer note (that stays on composer_plain_).
            byline = plain = short_byline(w)
        tenets = [f"$" + t + "_name$" for t in (w.get("argues_for") or [])]
        against = [f"#N $" + t + "_name$#!" for t in (w.get("argues_against") or [])]
        text = ", ".join(tenets)
        if against:
            text = (text + "; " if text else "") + "$KEHILLAH_SEFARIM_AGAINST$ " + ", ".join(against)
        lines += [
            f' kehillah_lib_place_{f}:0 "{w.get("place", "")}"',
            f' kehillah_lib_language_{f}:0 "{w.get("language", "")}"',
            f' kehillah_lib_byline_{f}:0 "{byline}"',
            f' kehillah_lib_byline_plain_{f}:0 "{plain}"',
            f' kehillah_lib_tenets_{f}:0 "{text or "$KEHILLAH_SEFARIM_TENETS_NONE$"}"',
            f' kehillah_lib_class_{f}:0 "{w["rank_name"]}"',
        ]
    write(LEDGER_LOC, lines)


def work_language(f, w):
    lang = w.get("lang") or "hebrew"
    if lang not in READING_LANGUAGES:
        raise SystemExit(f"{f}: unknown lang {lang!r}; add it to READING_LANGUAGES")
    return lang


def fluency_lines(lang, ind):
    """Fluency in one language, as vanilla has it: 1 knows it, 0 does not."""
    return [f"{ind}if = {{ limit = {{ knows_language = {READING_LANGUAGES[lang]} }} add = 1 }}"]


def exposure_line(lang, ind):
    """A reading counts toward learning its language; the effect itself counts
    it only when that is the liturgical tongue of the reader's faith."""
    return [f"{ind}kehillah_language_exposure_effect = {{ LANG = {READING_LANGUAGES[lang]} }}"]


def language_term_lines(f, w, ind):
    """The language terms of the mastery chance, for a reader who does not
    know the book's language. A liturgical tongue of his faith costs
    kehillah_study_chance_liturgical_<language> (one term, shrinking with each
    book he masters in it; revision 5), which a yeshiva and a Dayyan who knows
    it each offset, never past zero (revision 6); any other language costs
    kehillah_study_chance_foreign."""
    T = '"KEHILLAH_LIB_CHANCE_TERM_FORMAT"'

    def lit_body(lang, i):
        key = READING_LANGUAGES[lang]
        return [
            f"{i}add = {{ value = kehillah_study_chance_liturgical_{key} desc = KEHILLAH_LIB_CHANCE_LITURGICAL format = {T} }}",
            f"{i}if = {{ limit = {{ kehillah_study_chance_yeshiva_{key} > 0 }} add = {{ value = kehillah_study_chance_yeshiva_{key} desc = KEHILLAH_LIB_CHANCE_YESHIVA format = {T} }} }}",
            f"{i}if = {{ limit = {{ kehillah_study_chance_dayyan_{key} > 0 }} add = {{ value = kehillah_study_chance_dayyan_{key} desc = KEHILLAH_LIB_CHANCE_DAYYAN format = {T} }} }}",
        ]

    def lit_cond(lang):
        return f"kehillah_liturgical_language_trigger = {{ LANG = {READING_LANGUAGES[lang]} }}"
    foreign = f"{ind}else = {{ add = {{ value = kehillah_study_chance_foreign desc = KEHILLAH_LIB_CHANCE_FOREIGN format = {T} }} }}"
    if authored(w):
        g = f"global_var:kehillah_wk_{f}"
        return ([f"{ind}if = {{", f"{ind}\tlimit = {{ {g}_lang ?= flag:aramaic {lit_cond('aramaic')} }}"]
                + lit_body("aramaic", ind + "\t")
                + [f"{ind}}}", f"{ind}else_if = {{",
                   f"{ind}\tlimit = {{ NOT = {{ {g}_lang ?= flag:aramaic }} NOT = {{ {g}_lang ?= flag:vernacular }} {lit_cond('hebrew')} }}"]
                + lit_body("hebrew", ind + "\t") + [f"{ind}}}", foreign])
    lang = work_language(f, w)
    return ([f"{ind}if = {{", f"{ind}\tlimit = {{ {lit_cond(lang)} }}"] + lit_body(lang, ind + "\t")
            + [f"{ind}}}", foreign])


def per_language_value_lines():
    """For each language a sefer can be written in (character scope, the
    reader): the liturgical penalty after the books he has mastered in it, and
    the yeshiva's and the Dayyan's offsets, each capped by what is left of it."""
    out = ["", "# Per language (revision 6): the liturgical penalty, and the yeshiva's and",
           "# Dayyan's offsets, which never take it past zero."]
    for key in READING_LANGUAGES.values():
        out += [
            f"kehillah_study_chance_liturgical_{key} = {{",
            "	value = kehillah_study_chance_liturgical",
            "	if = {",
            f"		limit = {{ has_variable = kehillah_lang_exposure_{key} }}",
            f"		add = {{ value = var:kehillah_lang_exposure_{key} multiply = kehillah_study_chance_liturgical_step }}",
            "	}",
            "	max = 0",
            "}",
            f"kehillah_study_chance_liturgical_gap_{key} = {{",
            f"	value = kehillah_study_chance_liturgical_{key}",
            "	multiply = -1",
            "}",
            f"kehillah_study_chance_yeshiva_{key} = {{",
            "	value = 0",
            "	if = { limit = { kehillah_language_yeshiva_help_trigger = yes } add = kehillah_study_chance_yeshiva_help }",
            f"	max = kehillah_study_chance_liturgical_gap_{key}",
            "}",
            f"kehillah_study_chance_dayyan_room_{key} = {{",
            f"	value = kehillah_study_chance_liturgical_gap_{key}",
            f"	subtract = kehillah_study_chance_yeshiva_{key}",
            "}",
            f"kehillah_study_chance_dayyan_{key} = {{",
            "	value = 0",
            f"	if = {{ limit = {{ kehillah_language_dayyan_help_trigger = {{ LANG = {key} }} }} add = kehillah_study_chance_dayyan_help }}",
            f"	max = kehillah_study_chance_dayyan_room_{key}",
            "}",
        ]
    return out


TRACKS = ("parshanut", "talmudics", "hashkafa")


def depth_lines(track, ind):
    """Depth in the book's field: the Rabbi trait's track, or for a Karaite
    (no clergy) his Scholar experience."""
    t = track
    return [
        f"{ind}if = {{",
        f"{ind}\tlimit = {{ has_trait = kehillah_rabbi_trait has_trait_xp = {{ trait = kehillah_rabbi_trait track = {t} value >= 100 }} }}",
        f"{ind}\tadd = {{ value = kehillah_study_chance_depth_deep desc = KEHILLAH_LIB_CHANCE_DEPTH_{t.upper()} format = \"KEHILLAH_LIB_CHANCE_TERM_FORMAT\" }}",
        f"{ind}}}",
        f"{ind}else_if = {{",
        f"{ind}\tlimit = {{ has_trait = kehillah_rabbi_trait has_trait_xp = {{ trait = kehillah_rabbi_trait track = {t} value >= 50 }} }}",
        f"{ind}\tadd = {{ value = kehillah_study_chance_depth_some desc = KEHILLAH_LIB_CHANCE_DEPTH_{t.upper()} format = \"KEHILLAH_LIB_CHANCE_TERM_FORMAT\" }}",
        f"{ind}}}",
    ]


def mastery_chance_lines(f, w):
    """2026-11-10 (Daniel): Learning makes a book much harder or easier, but
    any book can be tried. kehillah_lib_mastery_chance_<flag> (reader scope)
    is the chance a reading ends in mastery, as a breakdown whose terms the
    book detail and the Learn Torah picker show."""
    T = '"KEHILLAH_LIB_CHANCE_TERM_FORMAT"'
    out = [f"kehillah_lib_tenet_fit_{f} = {{", "\tvalue = 0"]
    if authored(w):
        out += dynamic_tenet_branches(f, lambda cond, t: [
            f"\tif = {{ limit = {{ {cond} has_personal_tenet = {t} }} value = 1 }}"])
    for t in w.get("argues_for", []):
        out += [f"\tif = {{ limit = {{ has_personal_tenet = {t} }} value = 1 }}"]
    for t in w.get("argues_against", []):
        out += [f"\tif = {{ limit = {{ has_personal_tenet = {t} }} value = -1 }}"]
    out += ["}", f"kehillah_lib_mastery_chance_{f} = {{",
            "\tadd = { value = kehillah_study_chance_base desc = KEHILLAH_LIB_CHANCE_BASE }",
            f"\tadd = {{ value = kehillah_study_chance_learning_term desc = KEHILLAH_LIB_CHANCE_LEARNING format = {T} }}",
            "\tif = {",
            f"\t\tlimit = {{ kehillah_lib_fluency_{f} = 0 }}"]
    out += language_term_lines(f, w, "\t\t")
    out += ["\t}"]
    if authored(w):
        for n, t in enumerate(TRACKS, start=1):
            out += [f"\t{'if' if n == 1 else 'else_if'} = {{", f"\t\tlimit = {{ global_var:kehillah_wk_{f}_genre ?= {n} }}"]
            out += depth_lines(t, "\t\t")
            out += ["\t}"]
    else:
        out += depth_lines(w["genre"], "\t")
    out += [
        "\tif = {",
        "\t\tlimit = { NOT = { has_trait = kehillah_rabbi_trait } kehillah_is_karaite_character_trigger = yes has_trait_xp = { trait = lifestyle_scholar value >= 50 } }",
        f"\t\tadd = {{ value = kehillah_study_chance_depth_some desc = KEHILLAH_LIB_CHANCE_DEPTH_KARAITE format = {T} }}",
        "\t}",
        "\tif = {",
        "\t\tlimit = { kehillah_talmud_torah_follower_trigger = yes }",
        f"\t\tadd = {{ value = kehillah_study_chance_talmud_torah desc = KEHILLAH_LIB_CHANCE_TALMUD_TORAH format = {T} }}",
        "\t}",
        "\tif = {",
        f"\t\tlimit = {{ kehillah_lib_tenet_fit_{f} = 1 }}",
        f"\t\tadd = {{ value = kehillah_study_chance_tenet_fit desc = KEHILLAH_LIB_CHANCE_TENET_FOR format = {T} }}",
        "\t}",
        "\telse_if = {",
        f"\t\tlimit = {{ kehillah_lib_tenet_fit_{f} = -1 }}",
        f"\t\tsubtract = {{ value = kehillah_study_chance_tenet_fit desc = KEHILLAH_LIB_CHANCE_TENET_AGAINST format = {T} }}",
        "\t}",
        f"\tif = {{ limit = {{ has_trait = diligent }} add = {{ value = kehillah_study_chance_trait desc = trait_diligent format = {T} }} }}",
        f"\tif = {{ limit = {{ has_trait = lazy }} subtract = {{ value = kehillah_study_chance_trait desc = trait_lazy format = {T} }} }}",
        f"\tif = {{ limit = {{ has_trait = lifestyle_scholar }} add = {{ value = kehillah_study_chance_trait desc = trait_lifestyle_scholar format = {T} }} }}",
        f"\tif = {{ limit = {{ has_trait = theologian }} add = {{ value = kehillah_study_chance_trait_minor desc = trait_theologian format = {T} }} }}",
        "\tif = {",
        f"\t\tlimit = {{ is_target_in_variable_list = {{ name = kehillah_mastered_works target = flag:{f} }} }}",
        f"\t\tadd = {{ value = kehillah_study_chance_reread desc = KEHILLAH_LIB_CHANCE_REREAD format = {T} }}",
        "\t}",
        "\tif = {",
        "\t\tlimit = { has_variable = kehillah_study_torah_mastery_bonus }",
        f"\t\tadd = {{ value = 100 desc = KEHILLAH_LIB_CHANCE_GUIDED format = {T} }}",
        "\t\tmax = 100",
        "\t}",
        "\telse = { max = kehillah_study_chance_max }",
        "\tmin = kehillah_study_chance_min",
        "}",
    ]
    return out


def write_language_files(order, works):
    """2026-11-10: knowing a book's language makes it easier to master.

    One language per work (`lang`). A book written in play takes the language
    its author chose (global_var:kehillah_wk_<slot>_lang: flag:aramaic,
    flag:vernacular with _lang_culture, otherwise Hebrew).
    kehillah_lib_fluency_<flag> (character scope): 1 knows its language, 0
    does not (vanilla's knows_language; no in-between).
    kehillah_lib_learning_needed_<flag> (character scope): the Learning the
    shared study effect asks for a mastery, as a breakdown the book detail's
    tooltip shows. kehillah_lib_read_languages_<flag>_effect: a reading in
    its language counts toward learning it, when that is the liturgical
    tongue of the reader's faith."""
    vals = HEADER + [
        "# 2026-11-10 (docs/spec/2026-11-10-sefer-languages.md). Character scope: the reader.",
        "# Tunables in common/script_values/kehillah_language_values.txt.",
    ]
    effs = HEADER + [
        "# 2026-11-10 (docs/spec/2026-11-10-sefer-languages.md). Character scope: the reader,",
        "# after a reading of the work, from kehillah_study_specific_work_effect.",
    ]
    vals += per_language_value_lines()
    for f in order:
        w = works[f]
        vals += [f"kehillah_lib_fluency_{f} = {{", "	value = 0"]
        effs += [f"kehillah_lib_read_languages_{f}_effect = {{"]
        if authored(w):
            g = f"global_var:kehillah_wk_{f}"
            vals += [f"	if = {{",
                     f"		limit = {{ {g}_lang ?= flag:vernacular }}",
                     f"		if = {{",
                     f"			limit = {{",
                     f"				exists = {g}_lang_culture",
                     f"				knows_language_of_culture = {g}_lang_culture",
                     f"			}}",
                     f"			add = 1",
                     f"		}}",
                     f"	}}",
                     f"	else_if = {{",
                     f"		limit = {{ {g}_lang ?= flag:aramaic }}"]
            vals += fluency_lines("aramaic", "		")
            vals += ["	}", "	else = {"] + fluency_lines("hebrew", "		") + ["	}"]
            effs += [f"	if = {{",
                     f"		limit = {{ {g}_lang ?= flag:aramaic }}"]
            effs += exposure_line("aramaic", "		")
            effs += ["	}",
                     "	else_if = {",
                     f"		limit = {{ NOT = {{ {g}_lang ?= flag:vernacular }} }}"]
            effs += exposure_line("hebrew", "		")
            effs += ["	}"]
        else:
            lang = work_language(f, w)
            vals += fluency_lines(lang, "	")
            effs += exposure_line(lang, "	")
        vals += ["}"]
        vals += mastery_chance_lines(f, w)
        effs += ["}"]
    effs += ["", "# Yearly, from kehillah_sefer_yearly_effect: every written book in its author's",
             "# own tongue takes that tongue's current prestige (vanilla court languages).",
             "kehillah_language_refresh_all_prestige_effect = {"]
    effs += [f"\tkehillah_language_refresh_prestige_effect = {{ SLOT = {f} }}" for f in order if authored(works[f])]
    effs += ["}"]
    write(LANGUAGE_VALUES, vals)
    write(LANGUAGE_EFFECTS, effs)


def write_acquisition_gui(order, works):
    # 2026-11-11 (Daniel: "Why is this seek a copy grayed out?"): the gate checks
    # the work's circulation itself (avail_lines), not the cached candidates
    # list, which only the ledger's opening rebuilt, so a library whose ledger
    # had not been opened could seek nothing. Each condition explains itself.
    out = HEADER + ["# Each action revalidates the named missing work before opening confirmation."]
    for f in order:
        w = works[f]
        if w["corpus"] == "tanakh":
            circ = ["\t\t\talways = no"]
        else:
            circ = avail_lines(f, w, "\t\t\t\t") or ["\t\t\t\talways = yes"]
            circ = ["\t\t\tvar:kehillah_own_library ?= {"] + circ + ["\t\t\t}"]
        out += [
            "",
            f"kehillah_lib_acquire_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = {",
            "\t\tis_adult = yes",
            "\t\tis_imprisoned = no",
            "\t\tkehillah_lib_can_commission_trigger = yes",
            "\t\tcustom_tooltip = {",
            "\t\t\ttext = kehillah_lib_seek_held_tt",
            f"\t\t\tvar:kehillah_own_library ?= {{ NOT = {{ {held(f)} }} }}",
            "\t\t}",
            "\t\tcustom_tooltip = {",
            "\t\t\ttext = kehillah_lib_seek_busy_tt",
            "\t\t\tvar:kehillah_own_library ?= { NOT = { has_variable_list = kehillah_library_commission_work } }",
            "\t\t}",
            "\t\tcustom_tooltip = {",
            "\t\t\ttext = " + ("kehillah_lib_seek_tanakh_tt" if w["corpus"] == "tanakh" else "kehillah_lib_seek_unwritten_tt"),
        ] + circ + [
            "\t\t}",
            "\t}",
            "\teffect = {",
            "\t\t# The commission events check the cached list; rebuild it first.",
            "\t\tkehillah_library_refresh_acquisition_candidates_effect = yes",
            f"\t\tset_variable = {{ name = kehillah_commission_work_loc value = flag:{f} }}",
            f"\t\tsave_scope_value_as = {{ name = kehillah_commission_work value = flag:{f} }}",
            "\t\ttrigger_event = kehillah_library.0002",
            "\t}",
            "}",
        ]
    write(ACQUIRE_GUI, out)


def work_name_custom_loc(order, key, var):
    out = [f"{key} = {{", "\ttype = character"]
    for f in order:
        out += [
            "\ttext = {",
            "\t\ttrigger = {",
            f"\t\t\thas_variable = {var}",
            f"\t\t\tvar:{var} = flag:{f}",
            "\t\t}",
            f"\t\tlocalization_key = kehillah_lib_name_{f}",
            "\t}",
        ]
    out += ["\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = KEHILLAH_LIB_COMMISSION_UNKNOWN_WORK", "\t}", "}"]
    return out


def write_acquisition_custom_loc(order):
    out = HEADER + work_name_custom_loc(order, "KehillahCommissionWorkName", "kehillah_commission_work_loc")
    out += work_name_custom_loc(order, "KehillahSeferWorkName", "kehillah_sefer_named_work")
    for n in (1, 2, 3):
        out += work_name_custom_loc(order, f"KehillahSeferCand{n}Name", f"kehillah_sefer_cand_{n}")
    out += work_name_custom_loc(order, "KehillahSeferLatestWorkName", "kehillah_sefer_my_latest_work")
    write(ACQUIRE_CUSTOM_LOC, out)


def write_journey_gui(order):
    out = HEADER + [
        "# V49: which other libraries hold a selected work, and planning a Yeshiva",
        "# Visit to one of them. Since 2026-11-08 every library in kehillah_libraries",
        "# counts, landed ones included.",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            "",
            f"kehillah_lib_holders_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = { always = yes }",
            "\teffect = {",
            "\t\tclear_variable_list = kehillah_lib_holders",
            f"\t\tset_variable = {{ name = kehillah_lib_holders_work_id value = {i} }}",
            "\t\tsave_scope_as = kehillah_lib_holder_viewer",
            "\t\tevery_in_global_list = {",
            "\t\t\tvariable = kehillah_libraries",
            "\t\t\tlimit = {",
            "\t\t\t\tNOT = { scope:kehillah_lib_holder_viewer.var:kehillah_own_library ?= this }",
            "\t\t\t\texists = holder",
            f"\t\t\t\t{held(f)}",
            "\t\t\t}",
            "\t\t\tsave_scope_as = kehillah_lib_holder_candidate",
            "\t\t\tscope:kehillah_lib_holder_viewer = {",
            "\t\t\t\tadd_to_variable_list = { name = kehillah_lib_holders target = scope:kehillah_lib_holder_candidate }",
            "\t\t\t}",
            "\t\t}",
            "\t}",
            "}",
            "",
            f"kehillah_lib_holders_loaded_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            f"\tis_valid = {{ has_variable = kehillah_lib_holders_work_id var:kehillah_lib_holders_work_id = {i} }}",
            "}",
            "",
            f"kehillah_lib_journey_{f} = {{",
            "\tscope = character",
            "\tsaved_scopes = { target }",
            "\tis_shown = { always = yes }",
            "\tis_valid = {",
            "\t\tkehillah_journey_can_plan_trigger = yes",
            "\t\tscope:target = {",
            "\t\t\tNOT = { this = root.primary_title }",
            "\t\t\texists = holder",
            f"\t\t\t{held(f)}",
            "\t\t}",
            "\t}",
            "\teffect = {",
            f"\t\tkehillah_journey_set_plan_effect = {{ TITLE = scope:target WORK = flag:{f} }}",
            "\t}",
            "}",
        ]
    write(JOURNEY_GUI, out)


def write_journey_effects(order, works):
    out = HEADER + [
        "# V49 Yeshiva Visit helpers that need one branch per catalog work.",
        "",
        "# Study the work chosen before the journey. Scope: the traveller, in the",
        "# arrival event, with scope:kehillah_journey_planned_work saved.",
        "kehillah_journey_study_planned_work_effect = {",
    ]
    for i, f in enumerate(order):
        w = works[f]
        out += [
            f"\t{'if' if i == 0 else 'else_if'} = {{",
            f"\t\tlimit = {{ scope:kehillah_journey_planned_work = flag:{f} }}",
            f"\t\tcustom_tooltip = {study_tt_key(f, w)}",
            f"\t\tkehillah_journey_study_work_effect = {{ WORK = flag:{f} }}",
            "\t}",
        ]
    out += [
        "}",
        "",
        "# Run the study a journey option recorded in kehillah_journey_studied_work.",
        "# Called only from the hidden event kehillah_learn_torah_journey.0007, never",
        "# from an option (see the 2026-10-21 live test). Scope: the traveller.",
        "kehillah_journey_resolve_study_effect = {",
    ]
    for i, f in enumerate(order):
        out += [
            f"\t{'if' if i == 0 else 'else_if'} = {{",
            f"\t\tlimit = {{ var:kehillah_journey_studied_work ?= flag:{f} }}",
        ]
        out += study_call(f, works[f], "\t\t")
        out.append("\t}")
    out += [
        "}",
        "",
        "# Rebuild the traveller's list of works worth a journey: held by another",
        "# library and not yet mastered; works his own library lacks go on the",
        "# priority list. Scope: the traveller.",
        "kehillah_journey_build_offers_effect = {",
        "\tclear_variable_list = kehillah_journey_offer_works",
        "\tclear_variable_list = kehillah_journey_offer_priority",
    ]
    for f in order:
        out += [
            "\tif = {",
            "\t\tlimit = {",
            f"\t\t\tNOT = {{ {held(f, '', 'kehillah_mastered_works')} }}",
            "\t\t\tany_in_global_list = {",
            "\t\t\t\tvariable = kehillah_libraries",
            "\t\t\t\tNOT = { root.var:kehillah_own_library ?= this }",
            "\t\t\t\texists = holder",
            f"\t\t\t\t{held(f)}",
            "\t\t\t}",
            "\t\t}",
            f"\t\tadd_to_variable_list = {{ name = kehillah_journey_offer_works target = flag:{f} }}",
            "\t\tif = {",
            f"\t\t\tlimit = {{ NOT = {{ var:kehillah_own_library ?= {{ {held(f)} }} }} }}",
            f"\t\t\tadd_to_variable_list = {{ name = kehillah_journey_offer_priority target = flag:{f} }}",
            "\t\t}",
            "\t}",
        ]
    out.append("}")
    write(JOURNEY_EFFECTS, out)


def write_journey_custom_loc(order):
    out = HEADER + ["# V49: names of the planned and suggested Yeshiva Visit works."]
    out += work_name_custom_loc(order, "KehillahJourneyWorkName", "kehillah_journey_work_loc")
    for n in (1, 2):
        out += work_name_custom_loc(order, f"KehillahJourneyOffer{n}Name", f"kehillah_journey_offer_{n}_loc")
    write(JOURNEY_CUSTOM_LOC, out)


def write_study_custom_loc(order, works):
    """2026-11-08: the opening text of kehillah_study_torah.0002 for every work.
    The event once listed the first 22 works by ID and fell back to the Kuzari,
    so every work added to the catalog later opened with the Kuzari's text."""
    out = HEADER + ["# kehillah_study_torah.0002: the work the scheme has just opened, by",
                    "# kehillah_study_current_work_id (1..N in catalog order).",
                    "KehillahStudyOpeningDesc = {", "	type = character"]
    for i, f in enumerate(order, start=1):
        key = (f"kehillah_study_torah.0002.{short(f)}_desc" if i <= OPENING_DESC_WORKS
               else study_tt_key(f, works[f]))
        out += ["	text = {", "		trigger = {", "			has_variable = kehillah_study_current_work_id",
                f"			var:kehillah_study_current_work_id = {i}", "		}",
                f"		localization_key = {key}", "	}"]
    out += ["	text = {", "		fallback = yes", "		localization_key = kehillah_study_torah.0002.unknown_desc", "	}", "}"]
    # 2026-11-11: kehillah_study_torah.0008 names the book being read and the
    # one the Study button offers instead, by their catalog numbers.
    for key, var in (("KehillahStudyCurrentWorkName", "kehillah_study_current_work_id"),
                     ("KehillahStudyPendingWorkName", "kehillah_study_pending_work_id")):
        out += ["", f"{key} = {{", "	type = character"]
        for i, f in enumerate(order, start=1):
            out += ["	text = {", "		trigger = {", f"			has_variable = {var}",
                    f"			var:{var} = {i}", "		}",
                    f"		localization_key = kehillah_lib_name_{f}", "	}"]
        out += ["	text = {", "		fallback = yes", "		localization_key = KEHILLAH_LIB_COMMISSION_UNKNOWN_WORK", "	}", "}"]
    # The scheme card itself uses this version. Unlike the switch-event names,
    # its fallback is a player-facing instruction rather than an unknown-work
    # placeholder.
    out += ["", "KehillahStudySchemeWorkName = {", "\ttype = character"]
    for i, f in enumerate(order, start=1):
        out += ["\ttext = {", "\t\ttrigger = {", "\t\t\thas_variable = kehillah_study_current_work_id",
                f"\t\t\tvar:kehillah_study_current_work_id = {i}", "\t\t}",
                f"\t\tlocalization_key = kehillah_lib_name_{f}", "\t}"]
    out += ["\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = kehillah_study_torah.no_target", "\t}", "}"]
    write(STUDY_CUSTOM_LOC, out)


# ---------------------------------------------------------------------------
# The Bet Din docket by order of the Mishnah (2026-11-11,
# docs/spec/2026-11-11-rulings-sermons-and-gates.md section 2)
# ---------------------------------------------------------------------------

SEDARIM = ("zeraim", "moed", "nashim", "nezikin", "kodashim", "tahorot")
# A gloss on a work covering several orders takes the first of these it covers.
SEDER_PREFERENCE = ("nezikin", "nashim", "moed", "kodashim", "zeraim", "tahorot")


def work_sedarim(f, w):
    """The orders a work covers: a Talmud volume its own, others from the catalog."""
    if w["corpus"] in ("bavli", "yerushalmi"):
        return [f.rsplit("_", 1)[1]]
    return list(w.get("sedarim", []))


def covers_cond(f, w, seder):
    """Judge-scope trigger lines: he has mastered f, and f covers seder."""
    m = held(f, "", "kehillah_mastered_works")
    if authored(w):
        return f"global_var:kehillah_wk_{f}_seder ?= flag:{seder} {m}"
    if seder in work_sedarim(f, w):
        return m
    return None


def conviction_cond(f, w):
    """He holds a tenet the work argues for: personally, or his rite holds it."""
    if authored(w):
        return f"kehillah_lib_tenet_fit_{f} = 1"
    ts = w.get("argues_for", [])
    if not ts:
        return None
    rites = " ".join(f"rite_has_tenet = {t}" for t in ts)
    if len(ts) > 1:
        rites = f"OR = {{ {rites} }}"
    return f"OR = {{ kehillah_lib_tenet_fit_{f} = 1 rite ?= {{ {rites} }} }}"


def write_citation_files(order, works):
    trig = HEADER + [
        "# The Bet Din docket by order of the Mishnah (2026-11-11). Scope: a judge.",
        "# He has mastered a work that covers the order (catalog `sedarim`; a Talmud",
        "# volume covers its own; a book written in play, kehillah_wk_<slot>_seder).",
    ]
    for seder in SEDARIM:
        trig += [f"kehillah_din_covers_{seder}_trigger = {{", "\tOR = {"]
        for f in order:
            c = covers_cond(f, works[f], seder)
            if c:
                trig.append(f"\t\tAND = {{ {c} }}" if authored(works[f]) else f"\t\t{c}")
        trig += ["\t}", "}"]
    write(CITE_TRIGGERS, trig)

    eff = HEADER + [
        "# The Bet Din docket by order of the Mishnah (2026-11-11). Scope: the citing",
        "# judge; scope:kehillah_din_cite_activity the Bet Din. Fills up to three",
        "# authorities he could name, among the works he has mastered on the order:",
        "#   kehillah_din_cite_grounded    the highest standing in his rite;",
        "#   kehillah_din_cite_innovative  below Esteemed, not canon, the newest;",
        "#   kehillah_din_cite_conviction  not canon, arguing for a tenet he holds.",
    ]
    for seder in SEDARIM:
        eff += [
            f"kehillah_din_pick_citations_{seder}_effect = {{",
            "\tscope:kehillah_din_cite_activity = {",
            "\t\tremove_variable = kehillah_din_cite_grounded",
            "\t\tremove_variable = kehillah_din_cite_innovative",
            "\t\tremove_variable = kehillah_din_cite_conviction",
            "\t}",
            "\tset_local_variable = { name = kehillah_din_best value = -1 }",
            "\tset_local_variable = { name = kehillah_din_newest value = -1 }",
            "\tset_local_variable = { name = kehillah_din_conviction value = -1 }",
        ]
        for f in order:
            w = works[f]
            c = covers_cond(f, w, seder)
            if not c:
                continue
            st = f"kehillah_lib_standing_{f}"
            eff += [
                "\tif = {",
                f"\t\tlimit = {{ {c} {st} > local_var:kehillah_din_best }}",
                f"\t\tset_local_variable = {{ name = kehillah_din_best value = {st} }}",
                f"\t\tscope:kehillah_din_cite_activity = {{ set_variable = {{ name = kehillah_din_cite_grounded value = flag:{f} }} }}",
                "\t}",
            ]
            if not w.get("canon"):
                yr = f"kehillah_lib_year_{f}"
                eff += [
                    "\tif = {",
                    f"\t\tlimit = {{ {c} {st} <= 6 {yr} > local_var:kehillah_din_newest }}",
                    f"\t\tset_local_variable = {{ name = kehillah_din_newest value = {yr} }}",
                    f"\t\tscope:kehillah_din_cite_activity = {{ set_variable = {{ name = kehillah_din_cite_innovative value = flag:{f} }} }}",
                    "\t}",
                ]
                cc = conviction_cond(f, w)
                if cc:
                    eff += [
                        "\tif = {",
                        f"\t\tlimit = {{ {c} {cc} {st} > local_var:kehillah_din_conviction }}",
                        f"\t\tset_local_variable = {{ name = kehillah_din_conviction value = {st} }}",
                        f"\t\tscope:kehillah_din_cite_activity = {{ set_variable = {{ name = kehillah_din_cite_conviction value = flag:{f} }} }}",
                        "\t}",
                    ]
        eff += ["}"]

    noncanon = [f for f in order if not works[f].get("canon") and works[f]["corpus"] != "tanakh"]

    def dispatch(name, comment, call, keys):
        lines = ["", f"# {comment}", f"{name} = {{"]
        for i, k in enumerate(keys):
            lines += [f"\t{'if' if i == 0 else 'else_if'} = {{",
                      f"\t\tlimit = {{ $SOURCE$ ?= flag:{k} }}",
                      f"\t\t{call.format(k=k)}", "\t}"]
        lines.append("}")
        return lines

    eff += dispatch("kehillah_din_record_citation_dispatch_effect",
                    "Scope: a judge in the Bet Din. The cited work ($SOURCE$, a flag) counts a "
                    "citation, once per community; canon counts nothing.",
                    "kehillah_sefer_record_citation_effect = {{ KEY = {k} }}", noncanon)
    eff += dispatch("kehillah_din_conviction_popularity_dispatch_effect",
                    "Scope: a faith. The tenets of the cited work ($SOURCE$) gain popularity.",
                    "kehillah_sefer_work_popularity_{k}_effect = {{ AMOUNT = 3 }}", noncanon)
    glossable = [f for f in order if not authored(works[f]) and work_sedarim(f, works[f])]
    eff += ["", "# Scope: the author of a Talmudics gloss. The book covers the order of the",
            "# work it glosses ($SLOT$ his authored slot).", "kehillah_sefer_gloss_seder_dispatch_effect = {"]
    for i, f in enumerate(glossable):
        seds = work_sedarim(f, works[f])
        first = next(x for x in SEDER_PREFERENCE if x in seds)
        eff += [f"\t{'if' if i == 0 else 'else_if'} = {{",
                f"\t\tlimit = {{ var:kehillah_book_comment_on ?= flag:{f} }}",
                f"\t\tset_global_variable = {{ name = kehillah_wk_$SLOT$_seder value = flag:{first} }}", "\t}"]
    eff.append("}")
    eff += ["", "# Scope: none. Once, for an older save: a Talmudics book written before",
            "# orders existed covers Nezikin (kehillah_sefer_migrate_save_effect).",
            "kehillah_din_seder_migrate_effect = {"]
    for f in order:
        if authored(works[f]):
            eff += ["\tif = {",
                    f"\t\tlimit = {{ has_global_variable = kehillah_wk_{f}_written global_var:kehillah_wk_{f}_genre ?= 2 "
                    f"NOT = {{ has_global_variable = kehillah_wk_{f}_seder }} }}",
                    f"\t\tset_global_variable = {{ name = kehillah_wk_{f}_seder value = flag:nezikin }}", "\t}"]
    eff.append("}")
    write(CITE_EFFECTS, eff)

    loc = list(HEADER)
    for kind in ("Grounded", "Innovative", "Conviction"):
        var = f"kehillah_din_cite_{kind.lower()}"
        loc += [f"KehillahDinCite{kind} = {{", "\ttype = character"]
        for f in order:
            loc += ["\ttext = {", "\t\ttrigger = {",
                    f"\t\t\tinvolved_activity ?= {{ var:{var} ?= flag:{f} }}",
                    "\t\t}", f"\t\tlocalization_key = kehillah_lib_name_{f}", "\t}"]
        loc += ["\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = KEHILLAH_LIB_COMMISSION_UNKNOWN_WORK", "\t}", "}"]
    write(CITE_CUSTOM_LOC, loc)


# ---------------------------------------------------------------------------
# Sermons cite Parshanut works by kind (2026-11-11,
# docs/spec/2026-11-11-rulings-sermons-and-gates.md section 3)
# ---------------------------------------------------------------------------

# Which kinds of Parshanut fit each sermon topic. A grammar fits any topic.
SERMON_TOPICS = {
    "portion": ("torah", "torah_commentary", "targum", "midrash"),
    "neighbours": ("writings", "midrash"),
    "tzedakah": ("writings", "midrash"),
    "peace": ("prophets", "writings"),
    "trouble": ("prophets", "poetry"),
    "guest": ("torah", "torah_commentary", "targum", "midrash"),
    "appeal": ("writings", "midrash"),
}
# A book written in play: its kind (kehillah_wk_<slot>_kind) as a sermon kind.
AUTHORED_SERMON_KINDS = {1: "torah_commentary", 6: "poetry"}


def sermon_fit_cond(f, w, topic):
    """Preacher-scope trigger lines: he has mastered f, and f fits the topic."""
    m = held(f, "", "kehillah_mastered_works")
    ok = set(SERMON_TOPICS[topic]) | {"grammar"}
    if authored(w):
        kinds = [n for n, k in AUTHORED_SERMON_KINDS.items() if k in ok]
        if not kinds:
            return None
        if len(kinds) == 1:
            return f"global_var:kehillah_wk_{f}_kind ?= {kinds[0]} {m}"
        alts = " ".join(f"global_var:kehillah_wk_{f}_kind ?= {n}" for n in kinds)
        return f"OR = {{ {alts} }} {m}"
    if set(w.get("kinds", [])) & ok:
        return m
    return None


def write_sermon_files(order, works):
    eff = HEADER + [
        "# Sermons cite Parshanut works by kind (2026-11-11). Scope: the preacher;",
        "# scope:kehillah_sermon_holder the character the sermon belongs to (the",
        "# community's leader, or the maggid). Fills up to two texts he could cite,",
        "# among the works he has mastered that fit the topic, leaving out the one",
        "# he has already cited (var:kehillah_sermon_cited_1 on the holder):",
        "#   kehillah_sermon_cand_grounded  the highest standing in his rite;",
        "#   kehillah_sermon_cand_newer     below Esteemed, not canon, the newest.",
    ]
    for topic in SERMON_TOPICS:
        eff += [
            f"kehillah_sermon_pick_{topic}_effect = {{",
            "\tscope:kehillah_sermon_holder = {",
            "\t\tremove_variable = kehillah_sermon_cand_grounded",
            "\t\tremove_variable = kehillah_sermon_cand_newer",
            "\t}",
            "\tset_local_variable = { name = kehillah_sermon_best value = -1 }",
            "\tset_local_variable = { name = kehillah_sermon_newest value = -1 }",
        ]
        for f in order:
            w = works[f]
            c = sermon_fit_cond(f, w, topic)
            if not c:
                continue
            c += f" NOT = {{ scope:kehillah_sermon_holder.var:kehillah_sermon_cited_1 ?= flag:{f} }}"
            st = f"kehillah_lib_standing_{f}"
            eff += [
                "\tif = {",
                f"\t\tlimit = {{ {c} {st} > local_var:kehillah_sermon_best }}",
                f"\t\tset_local_variable = {{ name = kehillah_sermon_best value = {st} }}",
                f"\t\tscope:kehillah_sermon_holder = {{ set_variable = {{ name = kehillah_sermon_cand_grounded value = flag:{f} }} }}",
                "\t}",
            ]
            if not w.get("canon"):
                yr = f"kehillah_lib_year_{f}"
                eff += [
                    "\tif = {",
                    f"\t\tlimit = {{ {c} {st} <= 6 {yr} > local_var:kehillah_sermon_newest }}",
                    f"\t\tset_local_variable = {{ name = kehillah_sermon_newest value = {yr} }}",
                    f"\t\tscope:kehillah_sermon_holder = {{ set_variable = {{ name = kehillah_sermon_cand_newer value = flag:{f} }} }}",
                    "\t}",
                ]
        eff += ["}"]

    # Parshanut works a sermon can count toward their Authoritative gate.
    countable = [f for f in order if not works[f].get("canon")
                 and (authored(works[f]) or works[f].get("kinds"))]
    eff += ["", "# Scope: the preacher; scope:kehillah_sermon_title the community that heard",
            "# him. The cited work ($SOURCE$, a flag) counts a sermon toward its standing,",
            "# once per community; canon counts nothing.",
            "kehillah_sermon_record_preached_dispatch_effect = {"]
    for i, f in enumerate(countable):
        eff += [f"\t{'if' if i == 0 else 'else_if'} = {{",
                f"\t\tlimit = {{ $SOURCE$ ?= flag:{f} }}",
                f"\t\tkehillah_sermon_record_preached_effect = {{ KEY = {f} }}", "\t}"]
    eff.append("}")
    write(SERMON_EFFECTS, eff)

    loc = list(HEADER)
    # 2026-11-11: Cited1/Cited2 name the texts chosen, for the delivery (kehillah_sermon.0004).
    for kind, var in (("Grounded", "kehillah_sermon_cand_grounded"), ("Newer", "kehillah_sermon_cand_newer"),
                      ("Cited1", "kehillah_sermon_cited_1"), ("Cited2", "kehillah_sermon_cited_2")):
        loc += [f"KehillahSermonCand{kind} = {{", "\ttype = character"]
        for f in order:
            loc += ["\ttext = {", "\t\ttrigger = {", f"\t\t\tvar:{var} ?= flag:{f}",
                    "\t\t}", f"\t\tlocalization_key = kehillah_lib_name_{f}", "\t}"]
        loc += ["\ttext = {", "\t\tfallback = yes", "\t\tlocalization_key = KEHILLAH_LIB_COMMISSION_UNKNOWN_WORK", "\t}", "}"]
    write(SERMON_CUSTOM_LOC, loc)


# ---------------------------------------------------------------------------
# Machshavah changes minds (2026-11-11,
# docs/spec/2026-11-11-rulings-sermons-and-gates.md section 4)
# ---------------------------------------------------------------------------

def write_minds_files(order, works):
    eff = HEADER + [
        "# Machshavah changes minds (2026-11-11). kehillah_minds_pick_<work>_effect,",
        "# scope the reader who has just mastered it: var:kehillah_minds_tenet, the",
        "# index (kehillah_sefer_tenet_index order) of the first tenet the work argues",
        "# for that is still open to him (kehillah_minds_index_open_trigger); none set",
        "# when every one is his already. Defined for every work so a caller can pass",
        "# any key; only Machshavah books argue in this way.",
    ]
    for f in order:
        w = works[f]
        eff.append(f"kehillah_minds_pick_{f}_effect = {{")
        eff.append("\tremove_variable = kehillah_minds_tenet")
        if authored(w):
            for which in ("a", "b"):
                g = f"global_var:kehillah_wk_{f}_tenet_{which}"
                eff += ["\tif = {",
                        f"\t\tlimit = {{ NOT = {{ has_variable = kehillah_minds_tenet }} exists = {g} "
                        f"kehillah_minds_index_open_trigger = {{ VALUE = {g} }} }}",
                        f"\t\tset_variable = {{ name = kehillah_minds_tenet value = {g} }}", "\t}"]
        elif w["genre"] == "hashkafa":
            for t in w.get("argues_for", []):
                if t not in TENET_INDEX:
                    continue
                n = TENET_INDEX.index(t) + 1
                eff += ["\tif = {",
                        f"\t\tlimit = {{ NOT = {{ has_variable = kehillah_minds_tenet }} kehillah_minds_tenet_open_trigger = {{ TENET = {t} }} }}",
                        f"\t\tset_variable = {{ name = kehillah_minds_tenet value = {n} }}", "\t}"]
        eff.append("}")
    keys = [f for f in order if authored(works[f]) or works[f]["genre"] == "hashkafa"]
    eff += ["", "# Scope: the reader whose mind a work changed ($SOURCE$, a flag): it counts",
            "# toward the work's Authoritative gate (kehillah_minds_count_effect).",
            "kehillah_minds_count_dispatch_effect = {"]
    for i, f in enumerate(keys):
        eff += [f"\t{'if' if i == 0 else 'else_if'} = {{",
                f"\t\tlimit = {{ $SOURCE$ ?= flag:{f} }}",
                f"\t\tkehillah_minds_count_effect = {{ KEY = {f} }}", "\t}"]
    eff.append("}")
    write(MINDS_EFFECTS, eff)
    write(MINDS_CUSTOM_LOC, list(HEADER) + work_name_custom_loc(order, "KehillahMindsWork", "kehillah_minds_work"))


# ---------------------------------------------------------------------------
# Reviews: haskamah and cherem on books (2026-11-11,
# docs/spec/2026-11-11-reviews-and-cherem.md section 1)
# ---------------------------------------------------------------------------

def reviewable(w):
    return not w.get("canon") and w["corpus"] != "tanakh"


def write_review_files(order, works):
    trig = HEADER + [
        "# Reviews (2026-11-11). Scope: the would-be reviewer. Defined for every work so",
        "# a caller can pass any key; canon and the Tanakh are never reviewed.",
        "#   kehillah_review_can_cherem_<work>_trigger    he may pronounce a cherem on it",
        "#   kehillah_review_can_haskamah_<work>_trigger  ... and give it a haskamah (mastered)",
        "#   kehillah_review_objects_<work>_trigger      it argues against what he holds",
    ]
    for f in order:
        w = works[f]
        if not reviewable(w):
            for t in ("can_cherem", "can_haskamah", "objects", "haskamah_window"):
                trig.append(f"kehillah_review_{t}_{f}_trigger = {{ always = no }}")
            continue
        base = ["\tkehillah_review_reviewer_trigger = yes"]
        base += avail_lines(f, w, "\t")
        base += [f"\tNOT = {{ {held(f, '', 'kehillah_reviewed_works')} }}"]
        if needs_writing(w):
            base += [f"\tNOT = {{ global_var:kehillah_wk_{f}_author ?= this }}"]
        trig += [f"kehillah_review_can_cherem_{f}_trigger = {{"] + base + ["}"]
        trig += [f"kehillah_review_can_haskamah_{f}_trigger = {{",
                 f"\tkehillah_review_can_cherem_{f}_trigger = yes",
                 f"\t{held(f, '', 'kehillah_mastered_works')}",
                 f"\tkehillah_review_haskamah_window_{f}_trigger = yes", "}"]
        trig += [f"kehillah_review_haskamah_window_{f}_trigger = {{",
                 f"\tkehillah_lib_standing_{f} >= 4",
                 f"\tkehillah_lib_standing_{f} <= 7",
                 f"\tcurrent_year <= {{ value = kehillah_lib_year_{f} add = kehillah_review_haskamah_years }}", "}"]
        trig += [f"kehillah_review_objects_{f}_trigger = {{", "\tOR = {",
                 f"\t\tkehillah_lib_tenet_fit_{f} = -1",
                 f"\t\tkehillah_sefer_work_heterodox_{f}_trigger = yes", "\t}", "}"]
    write(REVIEW_TRIGGERS, trig)

    keys = [f for f in order if reviewable(works[f])]
    eff = HEADER + [
        "# Reviews (2026-11-11). Dispatchers from a work flag ($SOURCE$) to the",
        "# review effects (common/scripted_effects/kehillah_review_effects.txt).",
        "kehillah_review_haskamah_dispatch_effect = {",
    ]
    for i, f in enumerate(keys):
        eff += [f"\t{'if' if i == 0 else 'else_if'} = {{", f"\t\tlimit = {{ $SOURCE$ ?= flag:{f} }}",
                f"\t\tkehillah_review_haskamah_effect = {{ KEY = {f} }}", "\t}"]
    eff += ["}", "", "kehillah_review_cherem_dispatch_effect = {"]
    for i, f in enumerate(keys):
        eff += [f"\t{'if' if i == 0 else 'else_if'} = {{", f"\t\tlimit = {{ $SOURCE$ ?= flag:{f} }}",
                f"\t\tkehillah_review_cherem_effect = {{ KEY = {f} READ = $READ$ }}", "\t}"]
    eff += ["}", "",
            "# Scope: a reader in the Learn Torah scheme. var:kehillah_review_work is the",
            "# work he is reading (kehillah_study_current_work_id) when it argues against",
            "# what he holds and he may still pronounce a cherem on it.",
            "kehillah_review_current_objection_effect = {",
            "\tremove_variable = kehillah_review_work"]
    first = True
    for n, f in enumerate(order, start=1):
        if not reviewable(works[f]):
            continue
        eff += [f"\t{'if' if first else 'else_if'} = {{",
                f"\t\tlimit = {{ var:kehillah_study_current_work_id = {n} kehillah_review_can_cherem_{f}_trigger = yes kehillah_review_objects_{f}_trigger = yes }}",
                f"\t\tset_variable = {{ name = kehillah_review_work value = flag:{f} }}", "\t}"]
        first = False
    eff.append("}")
    write(REVIEW_EFFECTS, eff)

    gui = HEADER + [
        "# Reviews (2026-11-11): the work page's Give a Haskamah and Pronounce a Cherem",
        "# buttons (gui/kehillah_domicile_library.gui). Scope: the player.",
    ]
    for f in order:
        w = works[f]
        if not reviewable(w):
            for t in ("haskamah", "cherem"):
                gui += [f"kehillah_review_{t}_{f} = {{", "\tscope = character",
                        "\tis_shown = { always = no }", "\teffect = { }", "}"]
            continue
        gui += [
            f"kehillah_review_haskamah_{f} = {{", "\tscope = character",
            "\tis_shown = { kehillah_review_reviewer_trigger = yes }",
            "\tis_valid = {",
            f"\t\tcustom_description = {{ text = KEHILLAH_REVIEW_REQ_NOT_REVIEWED NOT = {{ {held(f, '', 'kehillah_reviewed_works')} }} }}",
            f"\t\tcustom_description = {{ text = KEHILLAH_REVIEW_REQ_MASTERED {held(f, '', 'kehillah_mastered_works')} }}",
            f"\t\tcustom_description = {{ text = KEHILLAH_REVIEW_REQ_WINDOW kehillah_review_haskamah_window_{f}_trigger = yes }}",
            f"\t\tkehillah_review_can_haskamah_{f}_trigger = yes",
            "\t}",
            "\teffect = {",
            f"\t\tset_variable = {{ name = kehillah_review_work value = flag:{f} }}",
            "\t\ttrigger_event = kehillah_review.0001",
            "\t}",
            "}",
            f"kehillah_review_cherem_{f} = {{", "\tscope = character",
            "\tis_shown = { kehillah_review_reviewer_trigger = yes }",
            "\tis_valid = {",
            f"\t\tcustom_description = {{ text = KEHILLAH_REVIEW_REQ_NOT_REVIEWED NOT = {{ {held(f, '', 'kehillah_reviewed_works')} }} }}",
            f"\t\tkehillah_review_can_cherem_{f}_trigger = yes",
            "\t}",
            "\teffect = {",
            f"\t\tset_variable = {{ name = kehillah_review_work value = flag:{f} }}",
            "\t\ttrigger_event = kehillah_review.0002",
            "\t}",
            "}",
        ]
    write(REVIEW_GUI, gui)
    write(REVIEW_CUSTOM_LOC, list(HEADER) + work_name_custom_loc(order, "KehillahReviewWork", "kehillah_review_work"))


# ---------------------------------------------------------------------------
# A reviewer's stance on a book (2026-11-11, Daniel: "consider using vanilla
# systems for tenet opposition"). Built from vanilla's own measures: his rite's
# status of each tenet the book argues for, his personal tenets, and the 1.20
# spiritual-fulfillment fit of the tenet with his virtues and sins
# (expected_tenet_fulfillment_change), which is how rival tenets clash; then
# faith hostility for a book of the other tradition, and the author.
# ---------------------------------------------------------------------------

def stance_for_lines(t, ind, cond=""):
    c = (cond + " ") if cond else ""
    fit = f'"expected_tenet_fulfillment_change(tenet:{t})"'
    return [
        f"{ind}if = {{ limit = {{ {c}rite ?= {{ has_tenet_status = {{ tenet = {t} status = core }} }} }} add = kehillah_review_stance_core }}",
        f"{ind}else_if = {{ limit = {{ {c}rite ?= {{ has_tenet_status = {{ tenet = {t} status = permitted }} }} }} add = kehillah_review_stance_permitted }}",
        f"{ind}else_if = {{ limit = {{ {c}rite ?= {{ has_tenet_status = {{ tenet = {t} status = prohibited }} }} }} add = kehillah_review_stance_prohibited }}",
        f"{ind}if = {{ limit = {{ {c}has_personal_tenet = {t} }} add = kehillah_review_stance_personal }}",
        f"{ind}else_if = {{ limit = {{ {c}has_variable = kehillah_leaning_{t} }} add = kehillah_review_stance_leaning }}",
        f"{ind}if = {{ limit = {{ {c}{fit} > 10 }} add = kehillah_review_stance_fits_well }}",
        f"{ind}else_if = {{ limit = {{ {c}{fit} > 0 }} add = kehillah_review_stance_fits }}",
        f"{ind}else_if = {{ limit = {{ {c}{fit} < -10 }} add = kehillah_review_stance_clashes_badly }}",
        f"{ind}else_if = {{ limit = {{ {c}{fit} < 0 }} add = kehillah_review_stance_clashes }}",
    ]



def write_cherem_files(order, works):
    """Teshuvah (2026-11-11): the penitent gives up every book in his library
    that his rite has Banned or put under Anathema."""
    keys = [f for f in order if reviewable(works[f])]

    def forbidden(f):
        return (f"{held(f)} scope:kehillah_cherem_penitent = {{ kehillah_lib_standing_{f} <= 1 }}")

    trig = list(HEADER) + [
        "# Title scope: a library; scope:kehillah_cherem_penitent its holder. It",
        "# holds a book his rite has Banned (1) or put under Anathema (0).",
        "kehillah_cherem_library_holds_forbidden_trigger = {",
        "\tOR = {",
    ]
    trig += [f"\t\tAND = {{ {forbidden(f)} }}" for f in keys]
    trig += ["\t}", "}"]
    write(CHEREM_TRIGGERS, trig)

    eff = list(HEADER) + [
        "# Title scope: a library; scope:kehillah_cherem_penitent its holder, who",
        "# does teshuvah. Every book his rite has Banned or put under Anathema leaves",
        "# the library for good (not to the ransom pool).",
        "kehillah_cherem_surrender_forbidden_effect = {",
    ]
    for f in keys:
        eff += ["\tif = {",
                f"\t\tlimit = {{ {forbidden(f)} }}",
                f"\t\tremove_list_variable = {{ name = kehillah_library_works target = flag:{f} }}",
                "\t}"]
    eff.append("}")
    write(CHEREM_EFFECTS, eff)

    # 2026-11-11: a judge of a teshuvah opposes the book that brought the ban
    # (the reviews' stance, at kehillah_teshuvah_zeal_stance or below).
    trig += ["", "# Scope: a judge; scope:kehillah_teshuvah_penitent.var:kehillah_cherem_cause_work",
             "# names the book that brought the ban.",
             "kehillah_cherem_judge_opposes_cause_trigger = {", "	OR = {"]
    for f in keys:
        trig.append(f"		AND = {{ scope:kehillah_teshuvah_penitent.var:kehillah_cherem_cause_work ?= flag:{f} "
                    f"kehillah_review_stance_{f}_value <= kehillah_teshuvah_zeal_stance }}")
    trig += ["	}", "}"]
    write(CHEREM_TRIGGERS, trig)

def write_stance_values(order, works):
    out = HEADER + [
        "# A reviewer's stance on each work (2026-11-11), -100 to 100. Scope: the",
        "# reviewer. Terms in common/script_values/kehillah_review_values.txt.",
    ]
    tradition_faith = {"rabbanite": "faith:rabbinic_faith", "karaite": "faith:karaism"}
    for f in order:
        w = works[f]
        out.append(f"kehillah_review_stance_{f}_value = {{")
        out.append("\tvalue = 0")
        if reviewable(w):
            if authored(w):
                for which in ("a", "b"):
                    for i, t in enumerate(TENET_INDEX, start=1):
                        out += stance_for_lines(t, "\t", f"global_var:kehillah_wk_{f}_tenet_{which} ?= {i}")
            for t in w.get("argues_for", []):
                out += stance_for_lines(t, "\t")
            for t in w.get("argues_against", []):
                out += [f"\tif = {{ limit = {{ rite ?= {{ has_tenet_status = {{ tenet = {t} status = core }} }} }} add = kehillah_review_stance_against_core }}",
                        f"\tif = {{ limit = {{ has_personal_tenet = {t} }} add = kehillah_review_stance_against_personal }}"]
            tf = tradition_faith.get(w.get("tradition", ""))
            if tf and not authored(w):
                out += [f"\tif = {{ limit = {{ faith = {{ faith_hostility_level = {{ target = {tf} value >= 1 }} }} }} add = kehillah_review_stance_hostile_faith }}",
                        f"\tif = {{ limit = {{ faith = {{ faith_hostility_level = {{ target = {tf} value >= 2 }} }} }} add = kehillah_review_stance_hostile_faith }}",
                        f"\tif = {{ limit = {{ faith = {{ faith_hostility_level = {{ target = {tf} value >= 3 }} }} }} add = kehillah_review_stance_hostile_faith }}"]
            if needs_writing(w):
                a = f"global_var:kehillah_wk_{f}_author"
                out += [f"\tif = {{ limit = {{ exists = {a} {a} = {{ is_alive = yes }} NOT = {{ {a} = this }} }}",
                        f"\t\tif = {{ limit = {{ has_relation_rival = {a} }} add = kehillah_review_stance_rival }}",
                        f"\t\telse_if = {{ limit = {{ has_relation_friend = {a} }} add = kehillah_review_stance_friend }}",
                        f"\t\tif = {{ limit = {{ opinion = {{ target = {a} value >= 40 }} }} add = kehillah_review_stance_likes_author }}",
                        f"\t\telse_if = {{ limit = {{ opinion = {{ target = {a} value <= -40 }} }} add = kehillah_review_stance_dislikes_author }}",
                        "\t}"]
            out += ["\tif = { limit = { has_trait = zealous } multiply = kehillah_review_stance_zealous_mult }",
                    "\tmin = -100", "\tmax = 100"]
        out.append("}")
    write(STANCE_VALUES, out)

    # Dispatchers and the yearly pass, appended to the review effects.
    keys = [f for f in order if reviewable(works[f])]
    eff = list(HEADER) + [
        "# AI reviews (2026-11-11). Dispatchers from a work flag ($SOURCE$).",
    ]
    for name, call in (
            ("kehillah_review_pick_approver_dispatch_effect", "kehillah_review_pick_approver_effect = {{ KEY = {k} }}"),
            ("kehillah_review_approver_reads_dispatch_effect", "kehillah_review_approver_reads_effect = {{ KEY = {k} }}"),
            ("kehillah_review_approver_decides_dispatch_effect", "kehillah_review_approver_decides_effect = {{ KEY = {k} }}"),
            ("kehillah_review_ai_reading_dispatch_effect", "kehillah_review_ai_reading_effect = {{ KEY = {k} }}"),
            # 2026-11-11 cherem track: teshuvah renounces the book that caused it.
            ("kehillah_cherem_renounce_dispatch_effect", "kehillah_cherem_renounce_effect = {{ KEY = {k} }}")):
        eff += ["", f"{name} = {{"]
        for i, f in enumerate(keys):
            eff += [f"\t{'if' if i == 0 else 'else_if'} = {{", f"\t\tlimit = {{ $SOURCE$ ?= flag:{f} }}",
                    f"\t\t{call.format(k=f)}", "\t}"]
        eff.append("}")
    eff += ["", "# Scope: none. Yearly: a book written in the last 50 years may draw a cherem",
            "# from a scholar who has not read it but opposes what it argues for",
            "# (kehillah_review_unread_effect), at most kehillah_review_unread_cap a year.",
            "kehillah_review_yearly_unread_effect = {",
            "\tset_global_variable = { name = kehillah_review_unread_this_year value = 0 }"]
    for f in keys:
        if not needs_writing(works[f]):
            continue
        eff += ["\tif = {",
                f"\t\tlimit = {{ has_global_variable = kehillah_wk_{f}_written current_year <= {{ value = kehillah_lib_year_{f} add = kehillah_review_haskamah_years }} "
                "global_var:kehillah_review_unread_this_year < kehillah_review_unread_cap }",
                f"\t\tkehillah_review_unread_effect = {{ KEY = {f} }}", "\t}"]
    eff.append("}")
    write(REVIEW_AI_EFFECTS, eff)


if __name__ == "__main__":
    order, works = load()
    write_values(order, works)
    write_standing_values(order, works)
    write_triggers(order, works)
    write_study_effects(order, works)
    write_study_gui(order, works)
    write_readers_gui(order)
    write_actions_gui(order, works)
    write_loc(order, works)
    write_prose_loc(order, works)
    write_authored_custom_loc(order, works)
    write_acquisition_effects(order, works)
    write_catalog_list_effects(order, works)
    write_acquisition_gui(order, works)
    write_acquisition_custom_loc(order)
    write_journey_gui(order)
    write_journey_effects(order, works)
    write_journey_custom_loc(order)
    write_study_custom_loc(order, works)
    write_shelf_values(order, works)
    write_shelf_effects(order, works)
    write_ledger_loc(order, works)
    write_language_files(order, works)
    write_citation_files(order, works)
    write_sermon_files(order, works)
    write_minds_files(order, works)
    write_review_files(order, works)
    write_stance_values(order, works)
    write_cherem_files(order, works)
    print(f"{len(order)} works -> catalog, standing, study, triggers, GUI and loc")
