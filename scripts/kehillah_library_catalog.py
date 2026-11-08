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
  plus, as before, the acquisition and V49 journey files listed below.

The authors the hover card links to are NOT generated: they are real
characters written by hand in history/characters/kehillah_library_authors.txt.
"""

import json
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
JOURNEY_GUI = ROOT / "common/scripted_guis/kehillah_library_journey_gui.txt"
JOURNEY_EFFECTS = ROOT / "common/scripted_effects/kehillah_library_journey_generated_effects.txt"
JOURNEY_CUSTOM_LOC = ROOT / "common/customizable_localization/kehillah_library_journey_custom_loc.txt"

GENRES = {"parshanut": 1, "talmudics": 2, "hashkafa": 3}
GENRE_BY_N = {v: k for k, v in GENRES.items()}
# rank name -> (shelf band, frame in the rank-frame strip). The band only orders
# the shelf; a work's standing is per rite (kehillah_lib_standing_<flag>).
RANKS = {"Foundational": (1, 1), "Essential": (2, 1), "Celebrated": (3, 2), "Popular": (4, 3), "Obscure": (5, 4)}
CORPORA = {"": 0, "bavli": 1, "yerushalmi": 2, "tanakh": 3}
CANON = {"": 0, "oral_torah": 11, "neviim_ketuvim": 12, "torah": 13}
TRADITIONS = {"rabbanite": 1, "karaite": 2, "shared": 3}
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
        "# Classic or higher 2, Respected or Esteemed 3, lower 4.",
    ]
    for f in order:
        out += [
            f"kehillah_lib_frame_{f} = {{",
            "\tvalue = 4",
            f"\tif = {{ limit = {{ kehillah_lib_standing_{f} >= 11 }} value = 1 }}",
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
    out += ["", "# canon tier, fixed by doctrine: 0 none, 11 Oral Torah, 12 Prophets and Writings, 13 Torah"]
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
            f"# Shelf entries of this genre the title's library holds ({genre}); scope: title.",
            "# A corpus volume does not count on its own: each corpus held counts once (its card).",
            f"kehillah_lib_genre_{n}_held_count_value = {{",
            "\tvalue = 0",
        ]
        for f in order:
            w = works[f]
            if CORPORA[w["corpus"]]:
                continue
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
        corpora = {"talmudics": ("bavli", "yerushalmi"), "parshanut": ("tanakh",)}.get(genre, ())
        for corpus in corpora:
            out += [
                "\tif = {",
                f"\t\tlimit = {{ kehillah_lib_{corpus}_held_count_value > 0 }}",
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
        "# Ladder: 1 Banned .. 10 Venerated. Canon (11-13) is fixed by doctrine and",
        "# never stored; 0 means outside this rite's canon (e.g. the Talmud for a Karaite).",
        "",
        "# ---- ceilings (rite scope): the least favourable status among the tenets a",
        "# work argues for sets how high it may climb in this rite; a core tenet it",
        "# argues against takes two tiers off.",
    ]
    for f in order:
        w = works[f]
        if w.get("canon"):
            continue
        out += [f"kehillah_lib_ceiling_{f} = {{", "\tvalue = 10"]
        if authored(w):
            # Compact form (one line per status): 100 slots x 2 tenets x 12.
            out += dynamic_tenet_branches(f, lambda cond, t: [
                f"\tif = {{ limit = {{ {cond} }}",
                f"\t\tif = {{ limit = {{ has_tenet_status = {{ tenet = {t} status = prohibited }} }} max = 3 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = known }} }} }} max = 5 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = permitted }} }} }} max = 7 }}",
                f"\t\telse_if = {{ limit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = core }} }} }} max = 9 }}",
                "\t}",
            ])
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
                "\t\tmax = 7",
                "\t}",
                "\telse_if = {",
                f"\t\tlimit = {{ NOT = {{ has_at_least_tenet_status = {{ tenet = {t} status = core }} }} }}",
                "\t\tmax = 9",
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
                "\t\tlimit = { rite_has_doctrine = temple_authority_rabbinic_doctrine }",
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
        other = max(1, min(b["rabbinic"], b["karaite"]) - 1)
        out += [
            f"kehillah_lib_baseline_{f} = {{",
            f"\tvalue = {other}",
            "\tif = {",
            "\t\tlimit = { rite_has_doctrine = temple_authority_rabbinic_doctrine }",
            f"\t\tvalue = {b['rabbinic']}",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { rite_has_doctrine = temple_authority_toric_doctrine }",
            f"\t\tvalue = {b['karaite']}",
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
            out += ["\tvalue = 13"]
        elif canon == "neviim_ketuvim":
            out += [
                "\tvalue = 12",
                "\tif = {",
                "\t\tlimit = { rite ?= { rite_has_doctrine = temple_authority_samaritan_torah_doctrine } }",
                "\t\tvalue = 0",
                "\t}",
            ]
        elif canon == "oral_torah":
            out += [
                "\tvalue = 0",
                "\tif = {",
                "\t\tlimit = { rite ?= { rite_has_doctrine = temple_authority_rabbinic_doctrine } }",
                "\t\tvalue = 11",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { NOT = { faith.religion = religion:judaism_religion } }",
                "\t\tvalue = 11",
                "\t}",
            ]
        else:
            b = w.get("baseline", {"rabbinic": 4, "karaite": 4})
            out += [
                f"\tvalue = {b['rabbinic']}",
                "\tif = {",
                f"\t\tlimit = {{ rite ?= {{ has_variable = kehillah_standing_{f} }} }}",
                f"\t\tvalue = rite.var:kehillah_standing_{f}",
                "\t}",
                "\telse_if = {",
                "\t\tlimit = { rite ?= { rite_has_doctrine = temple_authority_toric_doctrine } }",
                f"\t\tvalue = {b['karaite']}",
                "\t}",
            ]
        out.append("}")
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
            "\tvalue = 10",
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
    out += ["\t}", "}", "", "# Scope: the studying character. Resolve the work the numeric ID names.",
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
        "# its standing in his rite makes Classic or better twice as likely.",
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
        "# Scope: the Av Beit Din of a good ruling (kehillah_bet_din_reward_judges_",
        "# for_ruling_effect). He cites one non-canon work he has mastered -- one",
        "# that stands high in his rite more often -- and the court's citation counts",
        "# toward the work's standing once per community (spec section 3.4).",
        "kehillah_sefer_cite_in_ruling_effect = {",
        "\tif = {",
        "\t\tlimit = {",
        "\t\t\tOR = {",
    ]
    citable = [f for f in order if not works[f].get("canon") and works[f]["corpus"] != "tanakh"]
    out += [f"\t\t\t\t{held(f, '', 'kehillah_mastered_works')}" for f in citable]
    out += ["\t\t\t}", "\t\t}", "\t\trandom_list = {"]
    for f in citable:
        out += [
            "\t\t\t1 = {",
            f"\t\t\t\ttrigger = {{ {held(f, '', 'kehillah_mastered_works')} }}",
            f"\t\t\t\tmodifier = {{ add = 2 kehillah_lib_standing_{f} >= 7 }}",
            f"\t\t\t\tmodifier = {{ add = 1 kehillah_lib_genre_{f} = 2 }}",
            f"\t\t\t\tkehillah_sefer_record_citation_effect = {{ KEY = {f} }}",
            "\t\t\t}",
        ]
    out += ["\t\t}", "\t}", "}"]
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
        "# non-canon, held somewhere, Respected or better (to endorse) in his rite.",
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
            f"\t\tclamp_variable = {{ name = kehillah_standing_{f} min = kehillah_lib_floor_{f} max = kehillah_lib_ceiling_{f} }}",
            "\t}",
        ]
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
        "# Selected-book starters for the Learn Torah personal scheme. Kehillah leaders",
        "# read their own Kehillah's library; landed Jewish rulers read the library",
        "# they hold or that serves them (var:kehillah_own_library). 10 Piety, as the",
        "# decision costs.",
    ]
    for i, f in enumerate(order, start=1):
        out += [
            "",
            f"kehillah_lib_study_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = {",
            "\t\tkehillah_lib_can_start_selected_study_trigger = yes",
            f"\t\tkehillah_lib_own_library_has_trigger = {{ WORK = flag:{f} }}",
            "\t}",
            "\teffect = {",
            "\t\tadd_piety = -10",
            "\t\tstart_scheme = { type = kehillah_study_torah target_character = root }",
            "\t\tkehillah_study_torah_resolve_library_effect = { CHARACTER = root }",
            f"\t\tset_variable = {{ name = kehillah_study_current_work_id value = {i} }}",
            "\t\ttrigger_event = kehillah_study_torah.0002",
            "\t}",
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
        ' KEHILLAH_LIB_ROW_RANK:0 "Standing"',
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


def write_acquisition_gui(order):
    out = HEADER + ["# Each action revalidates the named missing work before opening confirmation."]
    for f in order:
        out += [
            "",
            f"kehillah_lib_acquire_{f} = {{",
            "\tscope = character",
            "\tis_shown = { always = yes }",
            "\tis_valid = {",
            "\t\tis_adult = yes",
            "\t\tis_imprisoned = no",
            "\t\tkehillah_lib_can_commission_trigger = yes",
            "\t\tvar:kehillah_own_library ?= {",
            "\t\t\tNOT = { has_variable_list = kehillah_library_commission_work }",
            f"\t\t\tis_target_in_variable_list = {{ name = kehillah_library_acquisition_candidates target = flag:{f} }}",
            f"\t\t\tNOT = {{ {held(f)} }}",
            "\t\t}",
            "\t}",
            "\teffect = {",
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
    write_acquisition_gui(order)
    write_acquisition_custom_loc(order)
    write_journey_gui(order)
    write_journey_effects(order, works)
    write_journey_custom_loc(order)
    print(f"{len(order)} works -> catalog, standing, study, triggers, GUI and loc")
