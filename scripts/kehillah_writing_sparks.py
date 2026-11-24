"""Generate the writing-spark system: triggers, values, effects, events,
custom localization, localization and the Learning window's spark cards.

A writer holds at most one spark per discipline (Parshanut, Talmudics,
Machshavah). Slot variables, in character scope:
  kehillah_spark_<disc>_form   flag:<form>
  kehillah_spark_<disc>_tier   1 Insight, 2 Chiddush, 3 Great Work
  kehillah_spark_<disc>_work   flag:<work> the study it came from
  kehillah_spark_<disc>_base   discipline works mastered when it came
  kehillah_spark_<disc>_apt    discipline aptitude when it came
  kehillah_spark_<disc>_did_<route>   an action taken with this idea
  kehillah_spark_<disc>_paths  list of open Great Work niches (for the GUI)
Mastering a sefer sparks an Insight. Any one route deepens it into a
Chiddush. A landmark niche's conditions make a Chiddush a Great Work.
Writing a Sefer uses the spark up. See docs/spec/2026-11-24-writing-sparks-v2.md.
"""

import json
from pathlib import Path

import kehillah_writing_landmarks as landmarks


ROOT = Path(__file__).resolve().parents[1]
OUT = {
    "triggers": ROOT / "common/scripted_triggers/kehillah_writing_spark_generated_triggers.txt",
    "values": ROOT / "common/script_values/kehillah_writing_spark_generated_values.txt",
    "effects": ROOT / "common/scripted_effects/kehillah_writing_spark_generated_effects.txt",
    "events": ROOT / "events/kehillah_spark_events.txt",
    "custom": ROOT / "common/customizable_localization/kehillah_spark_custom_loc.txt",
    "loc": ROOT / "localization/english/kehillah_writing_spark_generated_l_english.yml",
    "gui": ROOT / "gui/kehillah_spark_cards.gui",
}
WORKS = json.loads((ROOT / "scripts/kehillah_library_catalog.json").read_text(encoding="utf-8"))["works"]

DISCS = {
    # key (= Rabbi trait track): (display name, aptitude value key, book genre)
    "parshanut": ("Parshanut", "parshanut"),
    "talmudics": ("Talmudics", "talmudics"),
    "hashkafa": ("Machshavah", "machshava"),
}
# form: (discipline, book genre for the scheme, noun phrase, title case)
FORMS = {
    "torah": ("parshanut", "parshanut", "a Torah commentary", "Torah Commentary"),
    "midrash": ("parshanut", "parshanut", "a midrashic exposition", "Midrashic Exposition"),
    "poetry": ("parshanut", "poetry", "a cycle of sacred poems", "Sacred Poems"),
    "grammar": ("parshanut", "parshanut", "a grammar of the holy tongue", "Grammar of the Holy Tongue"),
    "chronicle": ("parshanut", "parshanut", "a chronicle of our people", "Chronicle"),
    "talmud": ("talmudics", "talmudics", "a Talmud commentary", "Talmud Commentary"),
    "yerushalmi": ("talmudics", "talmudics", "a Yerushalmi commentary", "Yerushalmi Commentary"),
    "law": ("talmudics", "talmudics", "a halakhic treatise", "Halakhic Treatise"),
    "responsa": ("talmudics", "talmudics", "a collection of responsa", "Responsa"),
    "minhag": ("talmudics", "talmudics", "a book of customs", "Book of Customs"),
    "siddur": ("talmudics", "talmudics", "an order of prayer", "Order of Prayer"),
    "tradition_history": ("talmudics", "talmudics", "a chain of the sages", "Chain of the Sages"),
    "scriptural_law": ("talmudics", "talmudics", "a book of Scripture's commandments", "Book of Commandments"),
    "dialogue": ("hashkafa", "hashkafa", "a dialogue on Scripture and law", "Dialogue"),
    "systematic_dialogue": ("hashkafa", "hashkafa", "a dialogue on faith and reason", "Faith and Reason"),
    "mystical": ("hashkafa", "hashkafa", "a work on the hidden order of creation", "Hidden Order of Creation"),
    "disputation": ("hashkafa", "hashkafa", "a disputation for our tradition", "Disputation"),
    "translation": ("hashkafa", "hashkafa", "a glossed translation", "Glossed Translation"),
    "ethics": ("hashkafa", "hashkafa", "an exhortation on righteous conduct", "Ethical Exhortation"),
    "devotion": ("hashkafa", "hashkafa", "a work on the duties of the heart", "Duties of the Heart"),
}
# Who may receive a spark in a form: the former project gate, so language,
# source, rite and date stay part of the idea. Responsa needs only the law
# gate; answering letters is one of its routes.
HOLD = {form: f"kehillah_writing_{form}_trigger = yes" for form in FORMS}
HOLD["responsa"] = "kehillah_writing_law_trigger = yes"

# The book a spark grows from. A work not listed sparks a random form of its
# own discipline.
PREFERRED = {
    "work_tanakh_torah": ["torah"], "work_samaritan_pentateuch": ["torah"], "work_orit": ["torah", "minhag"],
    "work_tanakh_neviim": ["torah", "chronicle", "ethics"], "work_tanakh_ketuvim": ["poetry", "ethics", "chronicle"],
    "work_genesis_rabbah": ["midrash"], "work_leviticus_rabbah": ["midrash"], "work_lamentations_rabbah": ["midrash"],
    "work_pesikta_derav_kahana": ["midrash"], "work_tanhuma": ["midrash"], "work_mekhilta": ["midrash", "law"],
    "work_sifra": ["midrash", "law"], "work_sifre_numbers": ["midrash"], "work_sifre_deuteronomy": ["midrash"],
    "work_pirkei_derabbi_eliezer": ["midrash"],
    "work_targum_onkelos": ["grammar"], "work_targum_jonathan": ["grammar"], "work_targum_pseudo_jonathan": ["grammar"],
    "work_samaritan_targum": ["grammar"],
    "work_josephus_jewish_war": ["chronicle"], "work_seder_olam_rabbah": ["chronicle", "tradition_history"],
    "work_sefer_yosippon": ["chronicle"],
    "work_diwan_dunash": ["poetry"], "work_diwan_samuel_hanagid": ["poetry"], "work_diwan_ibn_gabirol": ["poetry"],
    "work_bavli_zeraim": ["talmud", "law"], "work_bavli_moed": ["talmud", "law"], "work_bavli_nashim": ["talmud", "law"],
    "work_bavli_nezikin": ["talmud", "law"], "work_bavli_kodashim": ["talmud"], "work_bavli_tahorot": ["talmud"],
    "work_yerushalmi_zeraim": ["yerushalmi"], "work_yerushalmi_moed": ["yerushalmi"],
    "work_yerushalmi_nashim": ["yerushalmi"], "work_yerushalmi_nezikin": ["yerushalmi"],
    "work_mishnah": ["minhag", "siddur", "tradition_history"], "work_tosefta": ["law", "minhag"],
    "work_halakhot_gedolot": ["law"], "work_hilkhot_harif": ["law"], "work_mishneh_torah": ["law"],
    "work_seder_rav_amram": ["siddur"], "work_iggeret_rav_sherira": ["tradition_history"],
    "work_avot_derabbi_natan": ["ethics", "tradition_history"],
    "work_anan_sefer_hamitzvot": ["scriptural_law"], "work_levi_ben_yefet_mitzvot": ["scriptural_law"],
    "work_sefer_yetzirah": ["mystical"], "work_hekhalot_rabbati": ["mystical"], "work_shiur_qomah": ["mystical"],
    "work_sefer_harazim": ["mystical"], "work_sefer_habahir": ["mystical"], "work_zohar": ["mystical"],
    "work_emunot_vedeot": ["systematic_dialogue", "disputation"], "work_kuzari": ["systematic_dialogue", "disputation"],
    "work_moreh_nevukhim": ["systematic_dialogue"], "work_mekor_hayyim": ["systematic_dialogue"],
    "work_chovot_halevavot": ["devotion", "ethics"], "work_sefer_hasidim": ["devotion", "ethics"],
    "work_philo_allegorical": ["dialogue", "ethics"], "work_memar_marqah": ["dialogue", "ethics"],
    "work_theology_of_aristotle": ["translation"], "work_galen_de_usu_partium": ["translation"],
    "work_kitab_alanwar": ["disputation"], "work_toldot_yeshu": ["disputation"],
}
PREFERRED = {k: v for k, v in PREFERRED.items() if k in WORKS}

APT_STEP = "kehillah_spark_aptitude_step_value"
WORKS_VALUE = {
    "parshanut": "kehillah_writing_parshanut_mastered_value",
    "talmudics": "kehillah_spark_talmudics_mastered_value",
    "hashkafa": "kehillah_writing_machshava_mastered_value",
}
# Routes from Insight to Chiddush; any one is enough.
ROUTES = {
    "parshanut": ["apt", "works", "preached", "chavrusa"],
    "talmudics": ["apt", "works", "ruled", "answered"],
    "hashkafa": ["apt", "works", "debated", "chavrusa"],
}
ACTION_ROUTES = ["preached", "chavrusa", "ruled", "answered", "debated"]
ROUTE_LABEL = {
    "preached": "Preach a sermon",
    "chavrusa": "Study with a chavrusa",
    "ruled": "Preside over a Bet Din ruling",
    "answered": "Answer a she'elah",
    "debated": "Take a side in a machloket",
}

# Readable labels for the landmark conditions in kehillah_writing_landmarks.py.
RITE_LABEL = {
    landmarks.RABBANITE: "Rabbanite rite",
    landmarks.KARAITE: "Karaite rite",
    landmarks.HAYMANOT: "Haymanot rite",
}
MAX_CONDITIONS = 8


# The ten historical ambitions (common/scripted_triggers/kehillah_sefer_
# ambition_triggers.txt), spelled out as their general path. Each line marked
# True also accepts the historical author's shorter path (SHORTCUT), so that
# author sees every line ticked when he qualifies. Keep in step with the
# triggers; the landmark itself is still decided by them.
def xp(track: str, n: int) -> str:
    return f"has_trait_xp = {{ trait = kehillah_rabbi_trait track = {track} value >= {n} }}"


def mastered_any(*works: str) -> str:
    return "OR = { " + " ".join(landmarks.mastered(w) for w in works) + " }"


def name(work: str) -> str:
    return f"$kehillah_lib_name_{work}$"


RABBI = ("has_trait = kehillah_rabbi_trait", "Be a Rabbi", False)
SHORTCUT = {
    "work_rashi_torah": f"AND = {{ character:9000201 ?= this {xp('parshanut', 30)} }}",
    "work_rashi_talmud": "AND = { character:9000201 ?= this kehillah_lib_bavli_mastered_count_value >= 2 }",
    "work_hilkhot_harif": "AND = { character:9001101 ?= this kehillah_lib_bavli_mastered_count_value >= 3 }",
    "work_tosafot": "AND = { character:9001123 ?= this kehillah_lib_bavli_mastered_count_value >= 3 }",
    "work_mishneh_torah": "character:maimonides_1 ?= this",
    "work_moreh_nevukhim": "character:maimonides_1 ?= this",
}
NAMED = {
    "work_rashi_torah": [
        RABBI,
        (landmarks.mastered("work_tanakh_torah"), f"Master {name('work_tanakh_torah')}", False),
        ("learning >= 14", "Learning 14", True),
        (xp("parshanut", 65), "Parshanut experience 65", False),
        (landmarks.mastered("work_targum_onkelos"), f"Master {name('work_targum_onkelos')}", True),
        (mastered_any("work_genesis_rabbah", "work_mekhilta"),
         f"Master {name('work_genesis_rabbah')} or {name('work_mekhilta')}", True),
        ("kehillah_writing_parshanut_mastered_value >= 6", "Master 6 Parshanut works", False),
        ("kehillah_lib_tanakh_rounds_value >= 2", "Read the Tanakh twice through", False),
    ],
    "work_rashi_talmud": [
        RABBI,
        ("learning >= 15", "Learning 15", True),
        (xp("talmudics", 60), "Talmudics experience 60", True),
        ("kehillah_lib_bavli_mastered_count_value >= 4", "Master 4 Bavli orders", False),
    ],
    "work_hilkhot_harif": [
        RABBI,
        ("learning >= 16", "Learning 16", True),
        (xp("talmudics", 70), "Talmudics experience 70", True),
        ("kehillah_has_mastered_shas_trigger = yes", "Master the whole Bavli", True),
        (landmarks.mastered("work_halakhot_gedolot"), f"Master {name('work_halakhot_gedolot')}", True),
    ],
    "work_tosafot": [
        RABBI,
        (landmarks.mastered("work_rashi_talmud"), f"Master {name('work_rashi_talmud')}", False),
        ("learning >= 16", "Learning 16", True),
        (xp("talmudics", 70), "Talmudics experience 70", True),
        ("kehillah_lib_bavli_mastered_count_value >= 4", "Master 4 Bavli orders", True),
    ],
    "work_kuzari": [
        RABBI,
        ("learning >= 14", "Learning 14", False),
        (landmarks.mastered("work_emunot_vedeot"), f"Master {name('work_emunot_vedeot')}", False),
        (xp("hashkafa", 50), "Machshavah experience 50", False),
        (f"OR = {{ has_trait = lifestyle_poet {xp('hashkafa', 75)} }}", "Be a poet, or Machshavah experience 75", False),
    ],
    "work_mishneh_torah": [
        RABBI,
        ("kehillah_has_mastered_shas_trigger = yes", "Master the whole Bavli", False),
        ("learning >= 18", "Learning 18", True),
        (xp("talmudics", 80), "Talmudics experience 80", True),
        (landmarks.mastered("work_mishnah"), f"Master {name('work_mishnah')}", True),
        ("kehillah_lib_yerushalmi_mastered_count_value >= 2", "Master 2 Yerushalmi orders", True),
    ],
    "work_moreh_nevukhim": [
        RABBI,
        (landmarks.mastered("work_emunot_vedeot"), f"Master {name('work_emunot_vedeot')}", False),
        ("learning >= 18", "Learning 18", True),
        (xp("hashkafa", 80), "Machshavah experience 80", True),
    ],
    "work_sefer_habahir": [
        RABBI,
        (xp("hashkafa", 50), "Machshavah experience 50", False),
        (landmarks.mastered("work_sefer_yetzirah"), f"Master {name('work_sefer_yetzirah')}", False),
        (landmarks.mastered("work_hekhalot_rabbati"), f"Master {name('work_hekhalot_rabbati')}", False),
    ],
    "work_sefer_hasidim": [
        RABBI,
        (xp("hashkafa", 50), "Machshavah experience 50", False),
        (landmarks.mastered("work_chovot_halevavot"), f"Master {name('work_chovot_halevavot')}", False),
        ("OR = { culture = culture:ashkenazi rite ?= { rite_has_doctrine = doctrine_monogamy } }",
         "Be Ashkenazi, or of a monogamous rite", False),
    ],
    "work_zohar": [
        RABBI,
        ("learning >= 16", "Learning 16", False),
        (xp("hashkafa", 80), "Machshavah experience 80", False),
        (landmarks.mastered("work_sefer_habahir"), f"Master {name('work_sefer_habahir')}", False),
        (landmarks.mastered("work_sefer_yetzirah"), f"Master {name('work_sefer_yetzirah')}", False),
    ],
}
# Ambitions that also require knowing a tenet: folded into the thesis line,
# which then needs both.
KNOWS = {"work_moreh_nevukhim": "tenet_kehillah_hokhmah", "work_sefer_habahir": "tenet_esotericism"}


def condition_label(cond: str) -> str:
    if cond in RITE_LABEL:
        return RITE_LABEL[cond]
    if cond.startswith("learning >= "):
        return f"Learning {cond.split()[-1]}"
    if cond == "knows_language = language_arabic":
        return "Knows Arabic"
    if cond.startswith("kehillah_lib_bavli_mastered_count_value >= "):
        n = cond.split()[-1]
        return f"Master {n} Bavli orders"
    if cond.startswith("is_target_in_variable_list"):
        work = cond.split("flag:")[1].split()[0]
        return f"Master $kehillah_lib_name_{work}$"
    raise ValueError(cond)


def niche_conditions(key: str) -> list[tuple[str, str]]:
    """(trigger, label) pairs shown for one landmark niche."""
    work = WORKS[key]
    out = []
    if work.get("named"):
        for cond, label, shortcut in NAMED[key]:
            if shortcut:
                cond = f"OR = {{ {SHORTCUT[key]} {cond} }}"
            out.append((cond, label))
    else:
        for cond in landmarks.EXTRA[key]:
            if cond not in RITE_LABEL:  # shown niches already match the viewer's rite
                out.append((cond, condition_label(cond)))
    thesis = work.get("writing_thesis_tenet")
    if thesis:
        cond = f"kehillah_writing_believes_thesis_trigger = {{ TENET = {thesis} }}"
        if key in KNOWS:
            cond += f" kehillah_sefer_author_knows_tenet_trigger = {{ TENET = {KNOWS[key]} }}"
        out.append((cond, f"Hold ${thesis}_name$"))
    elif key in KNOWS:
        out.append((f"kehillah_sefer_author_knows_tenet_trigger = {{ TENET = {KNOWS[key]} }}", f"Hold ${KNOWS[key]}_name$"))
    assert len(out) <= MAX_CONDITIONS, key
    return out


def niche_rite(key: str) -> str | None:
    if WORKS[key].get("named"):
        return landmarks.RABBANITE  # every historical ambition is Rabbanite
    for cond in landmarks.EXTRA[key]:
        if cond in RITE_LABEL:
            return cond
    return None


def niche_open(key: str) -> list[str]:
    conds = [f"NOT = {{ has_global_variable = kehillah_wk_{key}_written }}"]
    if not WORKS[key].get("named"):
        conds.append(f"current_date < {WORKS[key]['year']}.1.1")
    return conds


NICHES = landmarks.FORMS  # work key -> form
HEADER = "# Generated by scripts/kehillah_writing_sparks.py. Do not edit by hand."


def forms_of(disc: str) -> list[str]:
    return [f for f, d in FORMS.items() if d[0] == disc]


def disc_of(form: str) -> str:
    return FORMS[form][0]


# --------------------------------------------------------------------------
def triggers() -> str:
    out = [HEADER]
    for form in FORMS:
        disc = disc_of(form)
        out.append(f"kehillah_spark_can_hold_{form}_trigger = {{ {HOLD[form]} }}")
        out.append(f"kehillah_spark_holds_{form}_trigger = {{ var:kehillah_spark_{disc}_form ?= flag:{form} }}")
    for disc in DISCS:
        out.append(f"kehillah_has_spark_{disc}_trigger = {{ has_variable = kehillah_spark_{disc}_form }}")
    out.append("kehillah_has_any_spark_trigger = { OR = { " +
               " ".join(f"has_variable = kehillah_spark_{d}_form" for d in DISCS) + " } }")
    out.append("")
    for disc, (_, apt) in DISCS.items():
        for route in ROUTES[disc]:
            if route == "apt":
                body = (f"has_variable = kehillah_spark_{disc}_apt "
                        f"kehillah_writing_{apt}_aptitude_value >= kehillah_spark_{disc}_apt_target_value")
            elif route == "works":
                body = (f"has_variable = kehillah_spark_{disc}_base "
                        f"{WORKS_VALUE[disc]} > var:kehillah_spark_{disc}_base")
            else:
                body = f"has_variable = kehillah_spark_{disc}_did_{route}"
            out.append(f"kehillah_spark_route_{disc}_{route}_trigger = {{ {body} }}")
        out.append(f"kehillah_spark_can_deepen_{disc}_trigger = {{ OR = {{ " +
                   " ".join(f"kehillah_spark_route_{disc}_{r}_trigger = yes" for r in ROUTES[disc]) + " } }")
    out.append("")
    out.append("# A niche worth showing: unwritten, still open and, where it names one, in the viewer's rite.")
    for key in NICHES:
        conds = niche_open(key) + ([niche_rite(key)] if niche_rite(key) else [])
        out.append(f"kehillah_spark_niche_shown_{key}_trigger = {{ {' '.join(conds)} }}")
    return "\n".join(out) + "\n"


def values() -> str:
    out = [HEADER, "# 0/1 per Chiddush route and -1/0/1 per Great Work condition, for the",
           "# Learning window's checklists. Evaluated on the character shown."]
    for disc in DISCS:
        out.append(f"kehillah_spark_{disc}_apt_target_value = {{ value = 0 if = {{ limit = {{ has_variable = kehillah_spark_{disc}_apt }} "
                   f"value = var:kehillah_spark_{disc}_apt add = {APT_STEP} }} }}")
        out.append(f"kehillah_spark_{disc}_tier_value = {{ value = 0 if = {{ limit = {{ has_variable = kehillah_spark_{disc}_tier }} value = var:kehillah_spark_{disc}_tier }} }}")
        for route in ROUTES[disc]:
            out.append(f"kehillah_spark_route_{disc}_{route}_value = {{ value = 0 if = {{ limit = {{ kehillah_spark_route_{disc}_{route}_trigger = yes }} value = 1 }} }}")
    for key in NICHES:
        conds = niche_conditions(key)
        for n in range(1, MAX_CONDITIONS + 1):
            name = f"kehillah_spark_nc_{key}_{n}"
            if n <= len(conds):
                out.append(f"{name} = {{ value = 0 if = {{ limit = {{ {conds[n - 1][0]} }} value = 1 }} }}")
            else:
                out.append(f"{name} = {{ value = -1 }}")
    return "\n".join(out) + "\n"


def toast(kind: str, disc: str) -> str:
    return (f"if = {{ limit = {{ is_ai = no }} send_interface_toast = {{ type = event_toast_text_good "
            f"title = kehillah_spark_{kind}_toast_t desc = kehillah_spark_{kind}_{disc}_toast left_icon = this }} }}")


def effects() -> str:
    out = [HEADER, ""]
    # Slot lifecycle.
    for disc in DISCS:
        out += [f"kehillah_spark_clear_{disc}_effect = {{",
                f"\tremove_variable = kehillah_spark_{disc}_form",
                f"\tremove_variable = kehillah_spark_{disc}_tier",
                f"\tremove_variable = kehillah_spark_{disc}_work",
                f"\tremove_variable = kehillah_spark_{disc}_base",
                f"\tremove_variable = kehillah_spark_{disc}_apt",
                f"\tclear_variable_list = kehillah_spark_{disc}_paths"]
        out += [f"\tremove_variable = kehillah_spark_{disc}_did_{r}" for r in ACTION_ROUTES]
        out.append("}")
    out.append("")
    out.append("# Scope: a writer. FORM's slot takes a fresh Insight; WORK is its source or flag:none.")
    for form in FORMS:
        disc = disc_of(form)
        out += [f"kehillah_spark_set_{form}_effect = {{",
                f"\tkehillah_spark_clear_{disc}_effect = yes",
                f"\tset_variable = {{ name = kehillah_spark_{disc}_form value = flag:{form} }}",
                f"\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 1 }}",
                f"\tset_variable = {{ name = kehillah_spark_{disc}_work value = $WORK$ }}",
                f"\tset_variable = {{ name = kehillah_spark_{disc}_base value = {WORKS_VALUE[disc]} }}",
                f"\tset_variable = {{ name = kehillah_spark_{disc}_apt value = kehillah_writing_{DISCS[disc][1]}_aptitude_value }}",
                "\t" + toast("new", disc),
                "}"]
    out.append("")
    out.append("# Scope: a writer. Offer an Insight in FORM: an empty slot takes it; a slot")
    out.append("# holding another form asks the player (AI keeps what it has).")
    for form in FORMS:
        disc = disc_of(form)
        out += [f"kehillah_spark_offer_{form}_effect = {{",
                "\tif = {",
                f"\t\tlimit = {{ kehillah_spark_can_hold_{form}_trigger = yes }}",
                "\t\tif = {",
                f"\t\t\tlimit = {{ NOT = {{ has_variable = kehillah_spark_{disc}_form }} }}",
                f"\t\t\tkehillah_spark_set_{form}_effect = {{ WORK = $WORK$ }}",
                "\t\t}",
                "\t\telse_if = {",
                f"\t\t\tlimit = {{ is_ai = no NOT = {{ kehillah_spark_holds_{form}_trigger = yes }} NOT = {{ has_variable = kehillah_spark_pending_form }} }}",
                f"\t\t\tset_variable = {{ name = kehillah_spark_pending_form value = flag:{form} days = 60 }}",
                f"\t\t\tset_variable = {{ name = kehillah_spark_pending_work value = $WORK$ days = 60 }}",
                "\t\t\ttrigger_event = { id = kehillah_spark.0002 days = 1 }",
                "\t\t}",
                "\t}",
                "}"]
    out += ["", "# The player takes up the pending idea (kehillah_spark.0002).",
            "kehillah_spark_take_pending_effect = {"]
    for i, form in enumerate(FORMS):
        kw = "if" if i == 0 else "else_if"
        out.append(f"\t{kw} = {{ limit = {{ var:kehillah_spark_pending_form ?= flag:{form} }} "
                   f"kehillah_spark_set_{form}_effect = {{ WORK = var:kehillah_spark_pending_work }} }}")
    out += ["\tremove_variable = kehillah_spark_pending_form", "\tremove_variable = kehillah_spark_pending_work", "}"]

    # Paths list and ripening.
    out.append("")
    for disc in DISCS:
        out += [f"kehillah_spark_refresh_paths_{disc}_effect = {{",
                f"\tclear_variable_list = kehillah_spark_{disc}_paths"]
        for key, form in NICHES.items():
            if disc_of(form) != disc:
                continue
            out.append(f"\tif = {{ limit = {{ kehillah_spark_holds_{form}_trigger = yes "
                       f"kehillah_spark_niche_shown_{key}_trigger = yes }} "
                       f"add_to_variable_list = {{ name = kehillah_spark_{disc}_paths target = flag:{key} }} }}")
        out.append("}")
        great = [f for f in forms_of(disc) if f in set(NICHES.values())]
        ready = " ".join(f"AND = {{ kehillah_spark_holds_{f}_trigger = yes kehillah_writing_landmark_ready_{f}_trigger = yes }}"
                         for f in great)
        out += [f"kehillah_spark_ripen_{disc}_effect = {{",
                "\tif = {",
                f"\t\tlimit = {{ var:kehillah_spark_{disc}_tier ?= 1 kehillah_spark_can_deepen_{disc}_trigger = yes }}",
                f"\t\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 2 }}",
                "\t\t" + toast("deepen", disc),
                "\t}",
                "\tif = {",
                f"\t\tlimit = {{ var:kehillah_spark_{disc}_tier ?= 2 OR = {{ {ready} }} }}",
                f"\t\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 3 }}",
                "\t\t" + toast("great", disc),
                "\t}",
                f"\tif = {{ limit = {{ has_variable = kehillah_spark_{disc}_form }} kehillah_spark_refresh_paths_{disc}_effect = yes }}",
                "}"]
    out += ["kehillah_spark_ripen_all_effect = {"] + \
           [f"\tkehillah_spark_ripen_{d}_effect = yes" for d in DISCS] + ["}"]

    # Action routes.
    out.append("")
    out.append("# Scope: a writer. An action taken while holding a spark of DISC.")
    out += ["kehillah_spark_mark_route_effect = {",
            "\tif = {",
            "\t\tlimit = { has_variable = kehillah_spark_$DISC$_form }",
            "\t\tset_variable = { name = kehillah_spark_$DISC$_did_$ROUTE$ value = yes }",
            "\t\tkehillah_spark_ripen_$DISC$_effect = yes",
            "\t}",
            "}"]

    # Study: the book read chooses the form.
    out += ["", "# Scope: the reader, after a first mastery. WORK: flag; TRACK: its discipline.",
            "kehillah_spark_from_study_effect = {",
            "\tif = {",
            "\t\tlimit = { kehillah_sefer_can_write_trigger = yes }",
            "\t\tset_local_variable = { name = kehillah_spark_src value = $WORK$ }",
            "\t\t# A held slot only sometimes yields a competing idea.",
            "\t\tif = {",
            "\t\t\tlimit = { has_variable = kehillah_spark_$TRACK$_form }",
            "\t\t\trandom = { chance = 65 set_local_variable = { name = kehillah_spark_done value = yes } }",
            "\t\t}"]
    for work, forms in PREFERRED.items():
        options = [f for f in forms]
        holds = " ".join(f"kehillah_spark_can_hold_{f}_trigger = yes" for f in options)
        if len(options) > 1:
            holds = f"OR = {{ {holds} }}"
        out += ["\t\tif = {",
                f"\t\t\tlimit = {{ NOT = {{ exists = local_var:kehillah_spark_done }} local_var:kehillah_spark_src ?= flag:{work} {holds} }}",
                "\t\t\tset_local_variable = { name = kehillah_spark_done value = yes }",
                "\t\t\trandom_list = {"]
        out += [f"\t\t\t\t10 = {{ trigger = {{ kehillah_spark_can_hold_{f}_trigger = yes }} kehillah_spark_offer_{f}_effect = {{ WORK = $WORK$ }} }}"
                for f in options]
        out += ["\t\t\t}", "\t\t}"]
    out += ["\t\tif = {", "\t\t\tlimit = { NOT = { exists = local_var:kehillah_spark_done } }",
            "\t\t\tkehillah_spark_from_$TRACK$_pool_effect = { WORK = $WORK$ }", "\t\t}",
            "\t\tkehillah_spark_ripen_$TRACK$_effect = yes", "\t}", "}"]
    for disc in DISCS:
        forms = forms_of(disc)
        out += [f"kehillah_spark_from_{disc}_pool_effect = {{",
                "\tif = {",
                "\t\tlimit = { OR = { " + " ".join(f"kehillah_spark_can_hold_{f}_trigger = yes" for f in forms) + " } }",
                "\t\trandom_list = {"]
        out += [f"\t\t\t10 = {{ trigger = {{ kehillah_spark_can_hold_{f}_trigger = yes }} kehillah_spark_offer_{f}_effect = {{ WORK = $WORK$ }} }}"
                for f in forms]
        out += ["\t\t}", "\t}", "}"]

    # AI writers, who rarely study, find an idea in an empty slot.
    out += ["", "kehillah_spark_ai_find_effect = {", "\trandom_list = {"]
    out += [f"\t\t10 = {{ trigger = {{ NOT = {{ has_variable = kehillah_spark_{disc_of(f)}_form }} kehillah_spark_can_hold_{f}_trigger = yes }} "
            f"kehillah_spark_set_{f}_effect = {{ WORK = flag:none }} }}" for f in FORMS]
    out += ["\t\t1 = { }", "\t}", "}"]

    # Writing.
    out += ["", "# Scope: the author starting a project. Uses up the chosen form's spark.",
            "kehillah_spark_consume_current_effect = {"]
    for i, form in enumerate(FORMS):
        kw = "if" if i == 0 else "else_if"
        out.append(f"\t{kw} = {{ limit = {{ var:kehillah_writing_form ?= flag:{form} }} kehillah_spark_clear_{disc_of(form)}_effect = yes }}")
    out.append("}")
    return "\n".join(out) + "\n"


def events() -> str:
    out = ["﻿" + HEADER, "namespace = kehillah_spark", "",
           "# What shall I write? One option per held spark (at most one per discipline).",
           "kehillah_spark.0001 = {",
           "\ttype = character_event",
           "\ttitle = kehillah_spark.0001.t",
           "\tdesc = kehillah_spark.0001.desc",
           "\ttheme = learning",
           "\tleft_portrait = { character = root animation = thinking }",
           "\timmediate = {",
           "\t\tkehillah_writing_clear_draft_effect = yes",
           "\t\tkehillah_spark_ripen_all_effect = yes",
           "\t}"]
    for form, (disc, genre, _, _) in FORMS.items():
        out += ["\toption = {"]
        for tier in (1, 2, 3):
            out.append(f"\t\tname = {{ trigger = {{ var:kehillah_spark_{disc}_tier ?= {tier} }} text = kehillah_spark.0001.{form}.{tier} }}")
        out += [f"\t\ttrigger = {{ kehillah_spark_holds_{form}_trigger = yes }}",
                f"\t\tkehillah_spark_option_hint_effect = {{ FORM = {form} DISC = {disc} }}",
                f"\t\tkehillah_writing_choose_project_effect = {{ FORM = {form} GENRE = {genre} DISC = {disc} }}",
                "\t\ttrigger_event = { id = kehillah_writing.0010 days = 1 }",
                "\t}"]
    out += ["\toption = { name = kehillah_writing.close }", "}", "",
            "# A new idea arrives while the discipline's slot holds another.",
            "kehillah_spark.0002 = {",
            "\ttype = character_event",
            "\ttitle = kehillah_spark.0002.t",
            "\tdesc = kehillah_spark.0002.desc",
            "\ttheme = learning",
            "\tleft_portrait = { character = root animation = thinking }",
            "\ttrigger = { has_variable = kehillah_spark_pending_form }",
            "\toption = {",
            "\t\tname = kehillah_spark.0002.keep",
            "\t\tremove_variable = kehillah_spark_pending_form",
            "\t\tremove_variable = kehillah_spark_pending_work",
            "\t}",
            "\toption = {",
            "\t\tname = kehillah_spark.0002.take",
            "\t\tcustom_tooltip = kehillah_spark.0002.take.tt",
            "\t\thidden_effect = { kehillah_spark_take_pending_effect = yes }",
            "\t}",
            "}"]
    return "\n".join(out) + "\n"


def custom() -> str:
    out = [HEADER]

    def block(name: str, var: str, keyfmt: str, items, fallback_key: str) -> None:
        out.append(f"{name} = {{")
        out.append("\ttype = character")
        for item in items:
            out.append(f"\ttext = {{ trigger = {{ var:{var} ?= flag:{item} }} localization_key = {keyfmt.format(item)} }}")
        out.append(f"\ttext = {{ trigger = {{ always = yes }} localization_key = {fallback_key} fallback = yes }}")
        out.append("}")

    block("KehillahSparkPendingForm", "kehillah_spark_pending_form", "kehillah_spark_form_{}", FORMS, "kehillah_spark_form_unknown")
    block("KehillahSparkPendingSource", "kehillah_spark_pending_work", "kehillah_lib_name_{}", PREFERRED_SOURCES(), "kehillah_spark_form_unknown")
    # The spark the pending idea would replace: the slot of its discipline.
    out.append("KehillahSparkPendingHeld = {")
    out.append("\ttype = character")
    for disc in DISCS:
        cond = " ".join(f"var:kehillah_spark_pending_form ?= flag:{f}" for f in forms_of(disc))
        out.append(f"\ttext = {{ trigger = {{ OR = {{ {cond} }} }} localization_key = kehillah_spark_held_{disc} }}")
    out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_form_unknown fallback = yes }")
    out.append("}")
    # The scheme panel: what the book being studied can spark, and the tier
    # a project was written from.
    out.append("KehillahSparkStudyPreview = {")
    out.append("\ttype = character")
    for work in PREFERRED:
        out.append(f"\ttext = {{ trigger = {{ var:kehillah_study_current_work ?= flag:{work} }} localization_key = kehillah_spark_preview_{work} }}")
    out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_form_unknown fallback = yes }")
    out.append("}")
    out.append("KehillahSparkWritingTier = {")
    out.append("\ttype = character")
    for tier in (1, 2, 3):
        out.append(f"\ttext = {{ trigger = {{ var:kehillah_writing_spark_tier ?= {tier} }} localization_key = kehillah_spark_tier_{tier}_name }}")
    out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_form_unknown fallback = yes }")
    out.append("}")
    for disc in DISCS:
        block(f"KehillahSparkForm_{disc}", f"kehillah_spark_{disc}_form", "kehillah_spark_form_{}", forms_of(disc), "kehillah_spark_form_unknown")
        out.append(f"KehillahSparkTier_{disc} = {{")
        out.append("\ttype = character")
        for tier in (1, 2, 3):
            out.append(f"\ttext = {{ trigger = {{ var:kehillah_spark_{disc}_tier ?= {tier} }} localization_key = kehillah_spark_tier_{tier}_name }}")
        out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_form_unknown fallback = yes }")
        out.append("}")
    return "\n".join(out) + "\n"


def PREFERRED_SOURCES() -> list[str]:
    return [k for k in WORKS if not k.startswith("work_authored_")]


def loc() -> str:
    out = ["l_english:"]
    out.append(' kehillah_spark_form_unknown:0 "a new work"')
    for form, (disc, _, noun, title) in FORMS.items():
        out.append(f' kehillah_spark_form_{form}:0 "{noun}"')
        out.append(f' kehillah_spark_title_{form}:0 "{title}"')
        for tier in (1, 2, 3):
            out.append(f' kehillah_spark.0001.{form}.{tier}:0 "$kehillah_spark_title_{form}$ #weak ($kehillah_spark_tier_{tier}_name$)#!"')
    for disc, (name, _) in DISCS.items():
        held = f"[GetPlayer.Custom('KehillahSparkForm_{disc}')]"
        out.append(f' kehillah_spark_disc_{disc}:0 "{name}"')
        out.append(f' kehillah_spark_held_{disc}:0 "[ROOT.Char.Custom(\'KehillahSparkForm_{disc}\')] #weak ([ROOT.Char.Custom(\'KehillahSparkTier_{disc}\')])#!"')
        out.append(f' kehillah_spark_new_{disc}_toast:0 "{name}: an idea for {held}."')
        out.append(f' kehillah_spark_deepen_{disc}_toast:0 "{name}: my idea for {held} has become a #high Chiddush#!."')
        out.append(f' kehillah_spark_great_{disc}_toast:0 "{name}: my idea for {held} could become a #high Great Work#!."')
        out.append(f' kehillah_spark_empty_{disc}:0 "Master a work of {name} to spark an idea."')
        for route in ROUTES[disc]:
            if route == "apt":
                label = f"Grow in {name} aptitude"
            elif route == "works":
                label = f"Master another {name} work"
            else:
                label = ROUTE_LABEL[route]
            out.append(f' kehillah_spark_route_{disc}_{route}:0 "{label}"')
    for work, forms in PREFERRED.items():
        out.append(f' kehillah_spark_preview_{work}:0 "{" or ".join(FORMS[f][2] for f in forms)}"')
    for key, form in NICHES.items():
        noun = FORMS[form][2]
        when = "" if WORKS[key].get("named") else f" #weak · before {WORKS[key]['year']}#!"
        out.append(f' kehillah_spark_path_{key}:0 "An unwritten {noun[2:] if noun.startswith("a ") else noun[3:]}{when}"')
        for n, (_, label) in enumerate(niche_conditions(key), 1):
            out.append(f' kehillah_spark_nc_{key}_{n}:0 "{label}"')
    return "﻿" + "\n".join(out) + "\n"


# --------------------------------------------------------------------------
VIEW = "GetPlayer.MakeScope.Var( 'kehillah_learning_view' ).Char"


def sv(name_expr: str) -> str:
    return f"{VIEW}.MakeScope.ScriptValue( {name_expr} )"


def check_line(value_expr: str, text_expr: str, indent: int, visible: str | None = None) -> str:
    t = "\t" * indent
    vis = f'\n{t}\tvisible = "{visible}"' if visible else ""
    return f"""{t}hbox = {{{vis}
{t}\tlayoutpolicy_horizontal = expanding
{t}\tspacing = 6
{t}\ticon = {{
{t}\t\tvisible = "[EqualTo_CFixedPoint( {value_expr}, '(CFixedPoint)1' )]"
{t}\t\tsize = {{ 18 18 }}
{t}\t\ttexture = "gfx/interface/icons/symbols/icon_check.dds"
{t}\t}}
{t}\ticon = {{
{t}\t\tvisible = "[EqualTo_CFixedPoint( {value_expr}, '(CFixedPoint)0' )]"
{t}\t\tsize = {{ 18 18 }}
{t}\t\ttexture = "gfx/interface/icons/symbols/icon_cross.dds"
{t}\t\talpha = 0.55
{t}\t}}
{t}\ttext_single = {{
{t}\t\ttext = "{text_expr}"
{t}\t\tdefault_format = "#light_background"
{t}\t\tusing = Text_Light_Background_Overrides
{t}\t\talign = left|nobaseline
{t}\t\tmax_width = 440
{t}\t}}
{t}\texpand = {{}}
{t}}}"""


def card(disc: str) -> str:
    name, apt = DISCS[disc]
    tier = sv(f"'kehillah_spark_{disc}_tier_value'")
    held = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_form' ).IsSet"
    form = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_form' ).GetFlagName"
    work = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_work' )"
    stars = "\n".join(f"""\t\t\t\twidget = {{
\t\t\t\t\tsize = {{ 20 20 }}
\t\t\t\t\ticon = {{
\t\t\t\t\t\tvisible = "[GreaterThanOrEqualTo_CFixedPoint( {tier}, '(CFixedPoint){n}' )]"
\t\t\t\t\t\tsize = {{ 20 20 }}
\t\t\t\t\t\ttexture = "gfx/interface/icons/flat_icons/star.dds"
\t\t\t\t\t}}
\t\t\t\t\ticon = {{
\t\t\t\t\t\tvisible = "[LessThan_CFixedPoint( {tier}, '(CFixedPoint){n}' )]"
\t\t\t\t\t\tsize = {{ 20 20 }}
\t\t\t\t\t\ttexture = "gfx/interface/icons/flat_icons/star.dds"
\t\t\t\t\t\talpha = 0.2
\t\t\t\t\t}}
\t\t\t\t}}""" for n in (1, 2, 3))
    routes = []
    for route in ROUTES[disc]:
        value = sv(f"'kehillah_spark_route_{disc}_{route}_value'")
        if route == "apt":
            text = (f"[Concatenate( Localize( 'kehillah_spark_route_{disc}_apt' ), Concatenate( ' ', Concatenate( "
                    f"IntToString( FixedPointToInt( {sv(f'{chr(39)}kehillah_writing_{apt}_aptitude_value{chr(39)}')} ) ), Concatenate( ' / ', "
                    f"IntToString( FixedPointToInt( {sv(f'{chr(39)}kehillah_spark_{disc}_apt_target_value{chr(39)}')} ) ) ) ) ) )]")
        else:
            text = f"[Localize( 'kehillah_spark_route_{disc}_{route}' )]"
        routes.append(check_line(value, text, 5))
    conds = []
    for n in range(1, MAX_CONDITIONS + 1):
        name_expr = f"Concatenate( Concatenate( 'kehillah_spark_nc_', Scope.GetFlagName ), '_{n}' )"
        value = sv(name_expr)
        conds.append(check_line(value, f"[Localize( {name_expr} )]", 9,
                                visible=f"[GreaterThanOrEqualTo_CFixedPoint( {value}, '(CFixedPoint)0' )]"))
    routes_s = "\n".join(routes)
    conds_s = "\n".join(conds)
    return f"""	### {name}
	type kehillah_spark_card_{disc} = vbox {{
		layoutpolicy_horizontal = expanding
		margin = {{ 12 8 }}
		spacing = 4
		background = {{
			using = Background_Area
			alpha = 0.4
		}}

		### Header: the spark, its discipline and its tier.
		hbox = {{
			layoutpolicy_horizontal = expanding
			spacing = 10
			widget = {{
				size = {{ 44 44 }}
				icon = {{
					visible = "[{held}]"
					size = {{ 44 44 }}
					texture = "gfx/interface/icons/inspirations/book_inspiration.dds"
				}}
				icon = {{
					visible = "[Not( {held} )]"
					size = {{ 44 44 }}
					texture = "gfx/interface/icons/inspirations/book_inspiration.dds"
					alpha = 0.3
				}}
			}}
			vbox = {{
				layoutpolicy_horizontal = expanding
				text_single = {{
					layoutpolicy_horizontal = expanding
					text = "kehillah_spark_disc_{disc}"
					default_format = "#light_background;weak"
					using = Text_Light_Background_Overrides
					align = left|nobaseline
				}}
				text_single = {{
					visible = "[{held}]"
					layoutpolicy_horizontal = expanding
					text = "[Localize( Concatenate( 'kehillah_spark_title_', {form} ) )]"
					default_format = "#light_background;bold"
					using = Text_Light_Background_Overrides
					using = Font_Size_Medium
					align = left|nobaseline
					max_width = 330
				}}
				text_single = {{
					visible = "[Not( {held} )]"
					layoutpolicy_horizontal = expanding
					text = "kehillah_spark_empty_{disc}"
					default_format = "#light_background;weak"
					using = Text_Light_Background_Overrides
					align = left|nobaseline
					max_width = 330
				}}
			}}
			hbox = {{
				visible = "[{held}]"
				spacing = 2
				tooltip = "[Concatenate( Localize( 'kehillah_spark_tier_tt_prefix' ), {VIEW}.Custom( 'KehillahSparkTier_{disc}' ) )]"
{stars}
			}}
			button_standard = {{
				visible = "[And( {held}, {VIEW}.IsLocalPlayer )]"
				size = {{ 110 32 }}
				text = "kehillah_spark_write_button"
				enabled = "[GetScriptedGui( 'kehillah_spark_write' ).IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
				onclick = "[GetScriptedGui( 'kehillah_spark_write' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
				tooltip = "kehillah_spark_write_button_tt"
			}}
		}}

		### Where it came from.
		text_single = {{
			visible = "[And( {work}.IsSet, Not( EqualTo_string( {work}.GetFlagName, 'none' ) ) )]"
			layoutpolicy_horizontal = expanding
			margin_left = 54
			text = "[Concatenate( Localize( 'kehillah_spark_from' ), Localize( Concatenate( 'kehillah_lib_name_', {work}.GetFlagName ) ) )]"
			default_format = "#light_background;weak"
			using = Text_Light_Background_Overrides
			align = left|nobaseline
			max_width = 460
		}}

		### Insight: any one route deepens it.
		vbox = {{
			visible = "[EqualTo_CFixedPoint( {tier}, '(CFixedPoint)1' )]"
			layoutpolicy_horizontal = expanding
			margin_left = 54
			margin_top = 4
			spacing = 2
			text_single = {{
				layoutpolicy_horizontal = expanding
				text = "kehillah_spark_routes_header"
				default_format = "#light_background;weak"
				using = Text_Light_Background_Overrides
				align = left|nobaseline
			}}
{routes_s}
		}}

		### Chiddush and Great Work: the open landmark paths for this form.
		vbox = {{
			visible = "[GreaterThanOrEqualTo_CFixedPoint( {tier}, '(CFixedPoint)2' )]"
			layoutpolicy_horizontal = expanding
			margin_left = 54
			margin_top = 4
			spacing = 4
			text_single = {{
				visible = "[EqualTo_CFixedPoint( {tier}, '(CFixedPoint)2' )]"
				layoutpolicy_horizontal = expanding
				text = "kehillah_spark_paths_header"
				default_format = "#light_background;weak"
				using = Text_Light_Background_Overrides
				align = left|nobaseline
			}}
			text_single = {{
				visible = "[EqualTo_CFixedPoint( {tier}, '(CFixedPoint)3' )]"
				layoutpolicy_horizontal = expanding
				text = "kehillah_spark_great_header"
				default_format = "#light_background"
				using = Text_Light_Background_Overrides
				align = left|nobaseline
			}}
			text_single = {{
				visible = "[IsDataModelEmpty( {VIEW}.MakeScope.GetList( 'kehillah_spark_{disc}_paths' ) )]"
				layoutpolicy_horizontal = expanding
				text = "kehillah_spark_no_paths"
				default_format = "#light_background;weak"
				using = Text_Light_Background_Overrides
				align = left|nobaseline
				max_width = 460
			}}
			vbox = {{
				layoutpolicy_horizontal = expanding
				spacing = 6
				datamodel = "[{VIEW}.MakeScope.GetList( 'kehillah_spark_{disc}_paths' )]"
				item = {{
					vbox = {{
						layoutpolicy_horizontal = expanding
						spacing = 1
						text_single = {{
							layoutpolicy_horizontal = expanding
							text = "[Localize( Concatenate( 'kehillah_spark_path_', Scope.GetFlagName ) )]"
							default_format = "#light_background;bold"
							using = Text_Light_Background_Overrides
							align = left|nobaseline
							max_width = 460
						}}
						vbox = {{
							layoutpolicy_horizontal = expanding
							margin_left = 8
							spacing = 1
{conds_s}
						}}
					}}
				}}
			}}
		}}
	}}
"""


def gui() -> str:
    head = """##########################################################################
# SPARK CARDS for the Learning window (2026-11-24, Daniel: "a very clean and
# vanilla-like UI experience that cleanly communicates without overexplaining,
# using icons, colors and smart visual hierarchies").
# GENERATED by scripts/kehillah_writing_sparks.py -- edit the script, not this.
# One card per discipline, for the character the Learning window shows
# (var:kehillah_learning_view). Header: inspiration icon, discipline, the
# spark's name, three tier stars, and Write for the player. Below: the source
# book, then the next rung only -- the Insight's routes, or the Chiddush's
# open landmark paths -- as check/cross lines.
##########################################################################
types KehillahSparkCards
{
"""
    return head + "\n".join(card(d) for d in DISCS) + "}\n"


def main() -> None:
    OUT["triggers"].write_text("﻿" + triggers(), encoding="utf-8", newline="\n")
    OUT["values"].write_text("﻿" + values(), encoding="utf-8", newline="\n")
    OUT["effects"].write_text("﻿" + effects(), encoding="utf-8", newline="\n")
    OUT["events"].write_text(events(), encoding="utf-8", newline="\n")
    OUT["custom"].write_text("﻿" + custom(), encoding="utf-8", newline="\n")
    OUT["loc"].write_text(loc(), encoding="utf-8", newline="\n")
    OUT["gui"].write_text(gui(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
