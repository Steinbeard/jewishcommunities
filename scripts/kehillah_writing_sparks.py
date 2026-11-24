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
# Upgrade events: kehillah_spark.00(1|2)<n> for Chiddush / Great Work.
DISC_EVENT = {"parshanut": 1, "talmudics": 2, "hashkafa": 3}
# Each discipline's colour on its card (r g b): Scripture blue, Talmud
# crimson, Machshavah green.
DISC_COLOR = {"parshanut": "0.22 0.40 0.66", "talmudics": "0.62 0.20 0.17", "hashkafa": "0.20 0.52 0.42"}
# Learning lifestyle experience for upgrading: an earned, visible reward.
UPGRADE_XP = {2: 100, 3: 300}
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
# 2026-11-24 (Daniel: "a commentary gives you a little bit more Rabbinics xp
# ... and a permanent buff to your scheme success and speed for that genre"):
# mastering one of these sparks nothing; it hones its discipline instead.
COMMENTARIES = {k: WORKS[k]["genre"] for k, v in WORKS.items() if v.get("commentary_on")}
for _k in ("work_yefet_commentary", "work_salmon_ben_jeroham_commentary"):
    if _k in WORKS:
        COMMENTARIES[_k] = WORKS[_k]["genre"]

SCRIPTURE = "kehillah_writing_scripture_language_trigger = yes"
RABBANITE_RITE = "rite ?= { kehillah_rite_rabbanite_trigger = yes }"
# Who may receive a spark in a form: its language, rite and date, plus having
# mastered any book that sparks it (PREFERRED) -- not one named book.
BASE_GATE = {
    "torah": SCRIPTURE, "midrash": SCRIPTURE, "poetry": f"{SCRIPTURE} has_trait = lifestyle_poet",
    "grammar": SCRIPTURE, "chronicle": f"{SCRIPTURE} learning >= 12",
    "talmud": f"{RABBANITE_RITE} knows_language = language_aramaic", "yerushalmi": "knows_language = language_aramaic",
    "law": RABBANITE_RITE, "responsa": f"{RABBANITE_RITE} kehillah_lib_bavli_mastered_count_value >= 1",
    "minhag": SCRIPTURE, "siddur": f"{RABBANITE_RITE} knows_language = language_israelite",
    "tradition_history": RABBANITE_RITE, "scriptural_law": "rite ?= { kehillah_rite_toric_trigger = yes }",
    "dialogue": SCRIPTURE,
    "systematic_dialogue": "current_date >= 933.1.1 OR = { knows_language = language_israelite knows_language = language_arabic }",
    "mystical": SCRIPTURE, "disputation": SCRIPTURE,
    "translation": "knows_language = language_israelite OR = { knows_language = language_greek knows_language = language_arabic }",
    "ethics": SCRIPTURE, "devotion": f"current_date >= 1080.1.1 {SCRIPTURE}",
}

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
    # 2026-11-24: books that fell to a random pick.
    "work_or_zarua": ["law"], "work_arbaah_turim": ["law"], "work_sefer_mitzvot_gadol": ["law"],
    "work_sefer_hachinukh": ["law", "ethics"], "work_teezaza_sanbat": ["minhag"], "work_defter": ["minhag"],
    "work_agron_david_al_fasi": ["grammar"], "work_cochin_copper_plates": ["chronicle"],
}
PREFERRED = {k: v for k, v in PREFERRED.items() if k in WORKS and k not in COMMENTARIES}


def sources_of(form: str) -> list[str]:
    return [w for w, fs in PREFERRED.items() if form in fs]


def hold_gate(form: str) -> str:
    srcs = sources_of(form)
    if not srcs:
        return BASE_GATE[form]
    mastered = " ".join(f"is_target_in_variable_list = {{ name = kehillah_mastered_works target = flag:{w} }}" for w in srcs)
    return f"{BASE_GATE[form]} OR = {{ {mastered} }}" if len(srcs) > 1 else f"{BASE_GATE[form]} {mastered}"


HOLD = {form: hold_gate(form) for form in FORMS}

# Semi-random: a book's own forms weigh PRIMARY each; any other form of its
# discipline the reader could hold weighs SECONDARY.
PRIMARY, SECONDARY = 40, 6

# Deeds that sometimes spark an idea for an empty slot: (chance, forms).
DEEDS = {
    "sermon": (10, ["torah", "midrash", "ethics"]),
    "ruling": (10, ["law", "minhag", "responsa"]),
    "letter": (35, ["responsa"]),
    "debate": (10, ["disputation", "dialogue", "systematic_dialogue"]),
}

# Commentary craft: success per commentary (cap) and monthly scheme progress.
CRAFT_CHANCE, CRAFT_CHANCE_CAP, CRAFT_SPEED, CRAFT_SPEED_CAP, CRAFT_XP = 4, 16, 2, 8, 15

# Chiddush needs this many of the four routes.
ROUTES_NEEDED = 2

# An Original Great Work, for every form, into one of the ledger's authored slots.
ORIGINAL = {
    disc: [("learning >= 16", "Learning 16"),
           (f"kehillah_writing_{apt}_aptitude_value >= 40", f"{name} aptitude 40"),
           (f"has_variable = kehillah_spark_{disc}_base {wv} >= {{ value = var:kehillah_spark_{disc}_base add = 2 }}",
            f"Master 2 more {name} works"),
           ("kehillah_spark_ledger_slot_free_trigger = yes", "A place in the Ledger of Sefarim")]
    for disc, (name, apt), wv in [(d, v, w) for (d, v), w in zip(
        {"parshanut": ("Parshanut", "parshanut"), "talmudics": ("Talmudics", "talmudics"),
         "hashkafa": ("Machshavah", "machshava")}.items(),
        ["kehillah_writing_parshanut_mastered_value", "kehillah_spark_talmudics_mastered_value",
         "kehillah_writing_machshava_mastered_value"])]
}
MAX_PATHS = 3

# Each Great Work path's character, without naming the historical book.
NICHE_HINT = {
    "work_emunot_vedeot": "Belief defended by reason",
    "work_chovot_halevavot": "The inner duties of the heart",
    "work_kuzari": "A king's dialogue on faith",
    "work_seder_rav_amram": "A prayer order for distant communities",
    "work_iggeret_rav_sherira": "A letter tracing the chain of sages",
    "work_rabbenu_hananel": "A concise gloss from the Maghreb",
    "work_mekor_hayyim": "A treatise on the source of being",
    "work_kitab_alanwar": "A survey of sects and their law",
    "work_yefet_commentary": "Scripture read word for word",
    "work_rashi_torah": "Plain sense for every reader",
    "work_rashi_talmud": "A line-by-line Talmud gloss",
    "work_hilkhot_harif": "The Talmud distilled to its law",
    "work_mishneh_torah": "The whole law in one code",
    "work_moreh_nevukhim": "Reason and revelation reconciled",
    "work_sefer_habahir": "Early teaching on the divine emanations",
    "work_sefer_hasidim": "Counsel for the pious of the Rhine",
    "work_tosafot": "Dialectic additions to a classic gloss",
    "work_zohar": "A mystical reading of the Torah",
    "work_sefer_yosippon": "A Hebrew history of the Second Temple",
    "work_toldot_yeshu": "A polemical counter-history",
    "work_diwan_dunash": "Hebrew verse in Arabic metre",
    "work_diwan_samuel_hanagid": "A statesman's poems of war and wine",
    "work_diwan_ibn_gabirol": "Poems of the soul's longing",
    "work_agron_david_al_fasi": "A dictionary of Scripture's Hebrew",
    "work_salmon_ben_jeroham_commentary": "A literalist reading of the Prophets",
    "work_levi_ben_yefet_mitzvot": "The commandments, from Scripture alone",
    "work_teezaza_sanbat": "The Sabbath laws of a distant community",
    "work_cochin_copper_plates": "The record of a royal charter",
    "work_ibn_ezra_torah": "Plain sense by grammar and reason",
    "work_sefer_mitzvot_gadol": "The commandments, numbered and taught",
    "work_or_zarua": "Rulings gathered from the northern academies",
    "work_ramban_torah": "Plain sense with hidden depths",
    "work_sefer_hamivhar": "A late literalist commentary",
    "work_sefer_hachinukh": "The commandments for the young",
    "work_arbaah_turim": "The law arranged in four rows",
    "work_maggid_mishneh": "A defence of the great code",
}
def _author_slugs() -> dict[str, str]:
    import re
    text = (ROOT / "common/scripted_effects/kehillah_library_authors_effects.txt").read_text(encoding="utf-8-sig")
    return dict(re.findall(r"name = kehillah_lib_author_(\w+) value = character:(\w+)", text))


# 2026-11-24 (Daniel: "make it possible and more likely for historical AI
# authors like Rashi and the Rif to write their own historical works"): niche
# -> the character who wrote it historically, where the mod has him.
_SLUGS = _author_slugs()
HIST_AUTHOR = {}
for _k in landmarks.FORMS:
    _w = WORKS[_k]
    _ref = _w.get("historical_author") or _SLUGS.get(_w.get("composer_char") or "")
    if _ref:
        HIST_AUTHOR[_k] = str(_ref)

DEED_NAME = {"sermon": "a sermon", "ruling": "a Bet Din ruling", "letter": "an answered she'elah", "debate": "a machloket"}

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
        ("learning >= 14", "Learning 14", True),
        (xp("parshanut", 65), "Parshanut experience 65", False),
        (landmarks.mastered("work_targum_onkelos"), f"Master {name('work_targum_onkelos')}", True),
        (mastered_any("work_genesis_rabbah", "work_mekhilta"),
         f"Master {name('work_genesis_rabbah')} or {name('work_mekhilta')}", True),
        ("kehillah_writing_parshanut_mastered_value >= 6", "Master 6 Parshanut works", False),
        ("kehillah_lib_tanakh_rounds_value >= 2", "Read the Tanakh twice through", False),
    ],
    "work_rashi_talmud": [
        ("learning >= 15", "Learning 15", True),
        (xp("talmudics", 60), "Talmudics experience 60", True),
        ("kehillah_lib_bavli_mastered_count_value >= 4", "Master 4 Bavli orders", False),
    ],
    "work_hilkhot_harif": [
        ("learning >= 16", "Learning 16", True),
        (xp("talmudics", 70), "Talmudics experience 70", True),
        ("kehillah_has_mastered_shas_trigger = yes", "Master the whole Bavli", True),
        (landmarks.mastered("work_halakhot_gedolot"), f"Master {name('work_halakhot_gedolot')}", True),
    ],
    "work_tosafot": [
        (landmarks.mastered("work_rashi_talmud"), f"Master {name('work_rashi_talmud')}", False),
        ("learning >= 16", "Learning 16", True),
        (xp("talmudics", 70), "Talmudics experience 70", True),
        ("kehillah_lib_bavli_mastered_count_value >= 4", "Master 4 Bavli orders", True),
    ],
    "work_kuzari": [
        ("learning >= 14", "Learning 14", False),
        (landmarks.mastered("work_emunot_vedeot"), f"Master {name('work_emunot_vedeot')}", False),
        (f"{xp('hashkafa', 50)} OR = {{ has_trait = lifestyle_poet {xp('hashkafa', 75)} }}",
         "Machshavah experience 50 as a poet, or 75", False),
    ],
    "work_mishneh_torah": [
        ("kehillah_has_mastered_shas_trigger = yes", "Master the whole Bavli", False),
        ("learning >= 18", "Learning 18", True),
        (xp("talmudics", 80), "Talmudics experience 80", True),
        (landmarks.mastered("work_mishnah"), f"Master {name('work_mishnah')}", True),
        ("kehillah_lib_yerushalmi_mastered_count_value >= 2", "Master 2 Yerushalmi orders", True),
    ],
    "work_moreh_nevukhim": [
        (landmarks.mastered("work_emunot_vedeot"), f"Master {name('work_emunot_vedeot')}", False),
        ("learning >= 18", "Learning 18", True),
        (xp("hashkafa", 80), "Machshavah experience 80", True),
    ],
    "work_sefer_habahir": [
        (xp("hashkafa", 50), "Machshavah experience 50", False),
        (landmarks.mastered("work_sefer_yetzirah"), f"Master {name('work_sefer_yetzirah')}", False),
        (landmarks.mastered("work_hekhalot_rabbati"), f"Master {name('work_hekhalot_rabbati')}", False),
    ],
    "work_sefer_hasidim": [
        (xp("hashkafa", 50), "Machshavah experience 50", False),
        (landmarks.mastered("work_chovot_halevavot"), f"Master {name('work_chovot_halevavot')}", False),
        ("OR = { culture = culture:ashkenazi rite ?= { rite_has_doctrine = doctrine_monogamy } }",
         "Be Ashkenazi, or of a monogamous rite", False),
    ],
    "work_zohar": [
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
    # 2026-11-24: open until written, at any date.
    return [f"NOT = {{ has_global_variable = kehillah_wk_{key}_written }}"]


NICHES = landmarks.FORMS  # work key -> form
HEADER = "# Generated by scripts/kehillah_writing_sparks.py. Do not edit by hand."


def forms_of(disc: str) -> list[str]:
    return [f for f, d in FORMS.items() if d[0] == disc]


def disc_of(form: str) -> str:
    return FORMS[form][0]


# --------------------------------------------------------------------------
def path_keys(disc: str) -> list[str]:
    """Historical niche keys of a discipline, most urgent first."""
    return sorted((k for k, f in NICHES.items() if disc_of(f) == disc), key=lambda k: WORKS[k]["year"])


def path_conditions(key: str) -> list[tuple[str, str]]:
    if key.startswith("original_"):
        return ORIGINAL[key[len("original_"):]]
    return niche_conditions(key)


def all_path_keys() -> list[str]:
    return list(NICHES) + [f"original_{d}" for d in DISCS]


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
    out.append("# One of the ledger's 100 authored slots is free (they recycle yearly).")
    out.append("kehillah_spark_ledger_slot_free_trigger = { OR = { " + " ".join(
        f"NOT = {{ has_global_variable = kehillah_wk_{k}_written }}" for k in sorted(WORKS) if k.startswith("work_authored_")) + " } }")
    out.append("")
    out.append("# A niche worth showing: unwritten, still open, in the viewer's rite.")
    for key in NICHES:
        conds = niche_open(key) + ([niche_rite(key)] if niche_rite(key) else [])
        out.append(f"kehillah_spark_niche_shown_{key}_trigger = {{ {' '.join(conds)} }}")
    out.append("# 2026-11-24 (Daniel): beyond an Insight, a Rabbanite scholar must be a Rabbi.")
    out.append("kehillah_spark_rabbi_gate_trigger = { OR = { NOT = { rite ?= { kehillah_rite_rabbanite_trigger = yes } } has_trait = kehillah_rabbi_trait } }")
    out.append("# Historical authors of open niches (Rashi, the Rif, the Ri, Maimonides, ...).")
    for key, ref in HIST_AUTHOR.items():
        out.append(f"kehillah_spark_is_author_of_{key}_trigger = {{ character:{ref} ?= this }}")
    out.append("kehillah_spark_is_historical_author_trigger = { OR = { " +
               " ".join(f"kehillah_spark_is_author_of_{k}_trigger = yes" for k in HIST_AUTHOR) + " } }")
    for disc in DISCS:
        conds = " ".join(c for c, _ in ORIGINAL[disc])
        out.append(f"kehillah_spark_original_ready_{disc}_trigger = {{ {conds} }}")
    out.append("# A form still has a historical landmark the viewer could reach.")
    for form in FORMS:
        keys = [k for k, f in NICHES.items() if f == form]
        shown = [f"kehillah_spark_niche_shown_{k}_trigger = yes" for k in keys]
        body = ("OR = { " + " ".join(shown) + " }" if len(shown) > 1 else shown[0]) if shown else "always = no"
        out.append(f"kehillah_spark_form_has_history_{form}_trigger = {{ {body} }}")
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
        out.append(f"kehillah_spark_can_deepen_{disc}_trigger = {{ kehillah_spark_{disc}_routes_met_value >= {ROUTES_NEEDED} }}")
        great = [f for f in forms_of(disc) if f in set(NICHES.values())]
        ready = " ".join(f"AND = {{ kehillah_spark_holds_{f}_trigger = yes kehillah_writing_landmark_ready_{f}_trigger = yes }}"
                         for f in great)
        out.append(f"kehillah_spark_can_be_great_{disc}_trigger = {{ OR = {{ {ready} kehillah_spark_original_ready_{disc}_trigger = yes }} }}")
        out.append("# The Upgrade button: the held spark's next tier is earned.")
        out.append(f"kehillah_spark_can_upgrade_{disc}_trigger = {{ kehillah_spark_rabbi_gate_trigger = yes OR = {{ "
                   f"AND = {{ var:kehillah_spark_{disc}_tier ?= 1 kehillah_spark_can_deepen_{disc}_trigger = yes }} "
                   f"AND = {{ var:kehillah_spark_{disc}_tier ?= 2 kehillah_spark_can_be_great_{disc}_trigger = yes }} }} }}")
    out.append("")
    out.append("# The book being studied, by discipline (commentary craft in the study scheme).")
    for disc in DISCS:
        ws = [k for k in sorted(WORKS) if WORKS[k].get("genre") == disc]
        out.append(f"kehillah_spark_studying_{disc}_trigger = {{ OR = {{ " +
                   " ".join(f"var:kehillah_study_current_work ?= flag:{w}" for w in ws) + " } }")
    return "\n".join(out) + "\n"


def values() -> str:
    out = [HEADER, "# Checklists, counts and craft for the Learning window and the schemes.",
           "# Evaluated on the character shown."]
    for disc in DISCS:
        out.append(f"kehillah_spark_{disc}_apt_target_value = {{ value = 0 if = {{ limit = {{ has_variable = kehillah_spark_{disc}_apt }} "
                   f"value = var:kehillah_spark_{disc}_apt add = {APT_STEP} }} }}")
        out.append(f"kehillah_spark_{disc}_tier_value = {{ value = 0 if = {{ limit = {{ has_variable = kehillah_spark_{disc}_tier }} value = var:kehillah_spark_{disc}_tier }} }}")
        out.append(f"kehillah_spark_{disc}_ready_value = {{ value = 0 if = {{ limit = {{ kehillah_spark_can_upgrade_{disc}_trigger = yes }} value = 1 }} }}")
        for route in ROUTES[disc]:
            out.append(f"kehillah_spark_route_{disc}_{route}_value = {{ value = 0 if = {{ limit = {{ kehillah_spark_route_{disc}_{route}_trigger = yes }} value = 1 }} }}")
        out.append(f"kehillah_spark_{disc}_routes_met_value = {{ value = 0 " +
                   " ".join(f"add = kehillah_spark_route_{disc}_{r}_value" for r in ROUTES[disc]) + " }")
        out.append(f"kehillah_spark_{disc}_routes_needed_value = {{ value = {ROUTES_NEEDED} }}")
        # Potential: 2 a historical landmark is open for the held form, 1 an
        # original Great Work only, 0 none.
        hist = " ".join(f"AND = {{ kehillah_spark_holds_{f}_trigger = yes kehillah_spark_form_has_history_{f}_trigger = yes }}"
                        for f in forms_of(disc))
        out.append(f"kehillah_spark_{disc}_potential_value = {{ value = 0 "
                   f"if = {{ limit = {{ OR = {{ {hist} }} }} value = 2 }} "
                   f"else_if = {{ limit = {{ kehillah_spark_ledger_slot_free_trigger = yes }} value = 1 }} }}")
        known = " ".join(f"if = {{ limit = {{ is_target_in_variable_list = {{ name = kehillah_spark_known target = flag:{f} }} }} add = 1 }}"
                         for f in forms_of(disc))
        out.append(f"kehillah_spark_{disc}_known_value = {{ value = 0 {known} }}")
        out.append(f"kehillah_spark_{disc}_kinds_value = {{ value = {len(forms_of(disc))} }}")
        if disc == "parshanut":
            out.append("kehillah_spark_held_count_value = { value = 0 " + " ".join(
                f"if = {{ limit = {{ has_variable = kehillah_spark_{d}_form }} add = 1 }}" for d in DISCS) + " }")
            out.append("# -1 not Rabbanite (no gate), 0 not yet a Rabbi, 1 a Rabbi.")
            out.append("kehillah_spark_rabbi_gate_value = { value = -1 if = { limit = { rite ?= { kehillah_rite_rabbanite_trigger = yes } } "
                       "value = 0 if = { limit = { has_trait = kehillah_rabbi_trait } value = 1 } } }")
        out.append(f"kehillah_spark_{disc}_commentaries_value = {{ value = 0 if = {{ limit = {{ has_variable = kehillah_commentaries_{disc} }} value = var:kehillah_commentaries_{disc} }} }}")
        out.append(f"kehillah_spark_{disc}_craft_chance_value = {{ value = kehillah_spark_{disc}_commentaries_value multiply = {CRAFT_CHANCE} max = {CRAFT_CHANCE_CAP} }}")
        out.append(f"kehillah_spark_{disc}_craft_speed_value = {{ value = kehillah_spark_{disc}_commentaries_value multiply = {CRAFT_SPEED} max = {CRAFT_SPEED_CAP} }}")
    for key in all_path_keys():
        conds = path_conditions(key)
        for n in range(1, MAX_CONDITIONS + 1):
            name = f"kehillah_spark_nc_{key}_{n}"
            if n <= len(conds):
                out.append(f"{name} = {{ value = 0 if = {{ limit = {{ {conds[n - 1][0]} }} value = 1 }} }}")
            else:
                out.append(f"{name} = {{ value = -1 }}")
        out.append(f"kehillah_spark_nc_{key}_met_value = {{ value = 0 " +
                   " ".join(f"add = kehillah_spark_nc_{key}_{n}" for n in range(1, len(conds) + 1)) + " }")
        out.append(f"kehillah_spark_nc_{key}_total_value = {{ value = {len(conds)} }}")
    # Commentary craft for the writing scheme's genre and the study scheme's book.
    out.append("kehillah_spark_writing_craft_chance_value = { value = 0 "
               "if = { limit = { OR = { var:kehillah_book_genre ?= flag:parshanut var:kehillah_book_genre ?= flag:poetry } } add = kehillah_spark_parshanut_craft_chance_value } "
               "else_if = { limit = { var:kehillah_book_genre ?= flag:talmudics } add = kehillah_spark_talmudics_craft_chance_value } "
               "else_if = { limit = { var:kehillah_book_genre ?= flag:hashkafa } add = kehillah_spark_hashkafa_craft_chance_value } }")
    out.append("kehillah_spark_writing_craft_speed_value = { value = 0 "
               "if = { limit = { OR = { var:kehillah_book_genre ?= flag:parshanut var:kehillah_book_genre ?= flag:poetry } } add = kehillah_spark_parshanut_craft_speed_value } "
               "else_if = { limit = { var:kehillah_book_genre ?= flag:talmudics } add = kehillah_spark_talmudics_craft_speed_value } "
               "else_if = { limit = { var:kehillah_book_genre ?= flag:hashkafa } add = kehillah_spark_hashkafa_craft_speed_value } }")
    for kind in ("chance", "speed"):
        body = " ".join(f"{'if' if i == 0 else 'else_if'} = {{ limit = {{ kehillah_spark_studying_{d}_trigger = yes }} add = kehillah_spark_{d}_craft_{kind}_value }}"
                        for i, d in enumerate(DISCS))
        out.append(f"kehillah_spark_study_craft_{kind}_value = {{ value = 0 {body} }}")
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
                f"\tremove_variable = kehillah_spark_{disc}_ready_told",
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
                f"\tif = {{ limit = {{ NOT = {{ is_target_in_variable_list = {{ name = kehillah_spark_known target = flag:{form} }} }} }} "
                f"add_to_variable_list = {{ name = kehillah_spark_known target = flag:{form} }} }}",
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
        # The most urgent open niches (earliest year first), at most MAX_PATHS,
        # then the Original Great Work, always last.
        out += [f"kehillah_spark_refresh_paths_{disc}_effect = {{",
                f"\tclear_variable_list = kehillah_spark_{disc}_paths",
                "\tset_local_variable = { name = kehillah_spark_paths_n value = 0 }"]
        for key in path_keys(disc):
            form = NICHES[key]
            out.append(f"\tif = {{ limit = {{ local_var:kehillah_spark_paths_n < {MAX_PATHS} kehillah_spark_holds_{form}_trigger = yes "
                       f"kehillah_spark_niche_shown_{key}_trigger = yes }} "
                       f"add_to_variable_list = {{ name = kehillah_spark_{disc}_paths target = flag:{key} }} "
                       "change_local_variable = { name = kehillah_spark_paths_n add = 1 } }")
        out.append(f"\tif = {{ limit = {{ has_variable = kehillah_spark_{disc}_form }} "
                   f"add_to_variable_list = {{ name = kehillah_spark_{disc}_paths target = flag:original_{disc} }} }}")
        out.append("}")
        # 2026-11-24 (Daniel: "upgrading the spark should be an active choice
        # that feels good"): ripening only tells the player once that the
        # Upgrade button is ready. The AI upgrades at once.
        out += [f"kehillah_spark_ripen_{disc}_effect = {{",
                f"\tif = {{ limit = {{ has_variable = kehillah_spark_{disc}_form }} kehillah_spark_refresh_paths_{disc}_effect = yes }}",
                "\tif = {",
                f"\t\tlimit = {{ kehillah_spark_can_upgrade_{disc}_trigger = yes }}",
                "\t\tif = {",
                "\t\t\tlimit = { is_ai = yes }",
                f"\t\t\tkehillah_spark_upgrade_{disc}_effect = yes",
                "\t\t}",
                "\t\telse_if = {",
                f"\t\t\tlimit = {{ NOT = {{ has_variable = kehillah_spark_{disc}_ready_told }} }}",
                f"\t\t\tset_variable = {{ name = kehillah_spark_{disc}_ready_told value = yes }}",
                "\t\t\t" + toast("ready", disc),
                "\t\t}",
                "\t}",
                "}"]
        out += [f"# The Upgrade button (scripted gui kehillah_spark_upgrade_{disc}).",
                f"kehillah_spark_upgrade_{disc}_effect = {{",
                "\tif = {",
                f"\t\tlimit = {{ var:kehillah_spark_{disc}_tier ?= 1 kehillah_spark_can_deepen_{disc}_trigger = yes }}",
                f"\t\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 2 }}",
                f"\t\tif = {{ limit = {{ is_ai = no }} trigger_event = kehillah_spark.{DISC_EVENT[disc] + 10:04d} }}",
                "\t}",
                "\telse_if = {",
                f"\t\tlimit = {{ var:kehillah_spark_{disc}_tier ?= 2 kehillah_spark_can_be_great_{disc}_trigger = yes }}",
                f"\t\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 3 }}",
                f"\t\tif = {{ limit = {{ is_ai = no }} trigger_event = kehillah_spark.{DISC_EVENT[disc] + 20:04d} }}",
                "\t}",
                f"\tremove_variable = kehillah_spark_{disc}_ready_told",
                f"\tkehillah_spark_refresh_paths_{disc}_effect = yes",
                "}"]
        out += [f"# The card's discard button asks first (kehillah_spark.{DISC_EVENT[disc] + 30:04d}).",
                f"kehillah_spark_discard_{disc}_effect = {{ kehillah_spark_clear_{disc}_effect = yes }}"]
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
    out.append("# Scope: a writer. A deed sometimes sparks an idea, into an empty slot only.")
    for deed, (chance, forms) in DEEDS.items():
        open_ = [f"NOT = {{ has_variable = kehillah_spark_{disc_of(f)}_form }} kehillah_spark_can_hold_{f}_trigger = yes" for f in forms]
        cond = "OR = { " + " ".join(f"AND = {{ {c} }}" for c in open_) + " }" if len(open_) > 1 else open_[0]
        out += [f"kehillah_spark_from_deed_{deed}_effect = {{",
                "\tif = {",
                f"\t\tlimit = {{ kehillah_sefer_can_write_trigger = yes {cond} }}",
                f"\t\trandom = {{ chance = {chance}",
                "\t\t\trandom_list = {"]
        out += [f"\t\t\t\t10 = {{ trigger = {{ NOT = {{ has_variable = kehillah_spark_{disc_of(f)}_form }} kehillah_spark_can_hold_{f}_trigger = yes }} "
                f"kehillah_spark_set_{f}_effect = {{ WORK = flag:deed_{deed} }} }}" for f in forms]
        out += ["\t\t\t}", "\t\t}", "\t}", "}"]

    # Study: a commentary hones its discipline; any other book sparks an idea,
    # semi-randomly: its own forms are likely, others of its discipline possible.
    out += ["", "# Scope: the reader, after a first mastery. WORK: flag; TRACK: its discipline.",
            "kehillah_spark_from_study_effect = {",
            "\tset_local_variable = { name = kehillah_spark_src value = $WORK$ }",
            "\tif = {",
            "\t\tlimit = { OR = { " + " ".join(f"local_var:kehillah_spark_src ?= flag:{w}" for w in COMMENTARIES) + " } }",
            "\t\tkehillah_spark_commentary_$TRACK$_effect = yes",
            "\t}",
            "\telse_if = {",
            "\t\tlimit = { kehillah_sefer_can_write_trigger = yes }",
            "\t\t# A held slot only sometimes yields a competing idea.",
            "\t\tif = {",
            "\t\t\tlimit = { has_variable = kehillah_spark_$TRACK$_form }",
            "\t\t\trandom = { chance = 65 set_local_variable = { name = kehillah_spark_done value = yes } }",
            "\t\t}"]
    for work, forms in PREFERRED.items():
        disc = WORKS[work].get("genre")
        pool = list(forms) + [f for f in FORMS if disc_of(f) == disc and f not in forms]
        out += ["\t\tif = {",
                f"\t\t\tlimit = {{ NOT = {{ exists = local_var:kehillah_spark_done }} local_var:kehillah_spark_src ?= flag:{work} "
                "OR = { " + " ".join(f"kehillah_spark_can_hold_{f}_trigger = yes" for f in pool) + " } }",
                "\t\t\tset_local_variable = { name = kehillah_spark_done value = yes }",
                "\t\t\trandom_list = {"]
        out += [f"\t\t\t\t{PRIMARY if f in forms else SECONDARY} = {{ trigger = {{ kehillah_spark_can_hold_{f}_trigger = yes }} "
                f"kehillah_spark_offer_{f}_effect = {{ WORK = $WORK$ }} }}" for f in pool]
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
        # A mastered commentary: craft for the discipline, a little more Rabbi
        # experience, and a popup naming both.
        out += [f"kehillah_spark_commentary_{disc}_effect = {{",
                f"\tchange_variable = {{ name = kehillah_commentaries_{disc} add = 1 }}",
                f"\tif = {{ limit = {{ has_trait = kehillah_rabbi_trait }} add_trait_xp = {{ trait = kehillah_rabbi_trait track = {disc} value = {CRAFT_XP} }} }}",
                "\t" + toast("craft", disc),
                "}"]

    # AI writers, who rarely study, find an idea in an empty slot.
    out += ["", "kehillah_spark_ai_find_effect = {", "\trandom_list = {"]
    out += [f"\t\t10 = {{ trigger = {{ NOT = {{ has_variable = kehillah_spark_{disc_of(f)}_form }} kehillah_spark_can_hold_{f}_trigger = yes }} "
            f"kehillah_spark_set_{f}_effect = {{ WORK = flag:none }} }}" for f in FORMS]
    out += ["\t\t1 = { }", "\t}", "}"]

    # Historical AI authors: their own idea, already a Chiddush, each year
    # their niche is open; on finishing, they fill their own niche first.
    out += ["", "# Scope: an AI writer, yearly. A historical author takes up his own work.",
            "kehillah_spark_ai_author_effect = {"]
    for key, ref in HIST_AUTHOR.items():
        form = NICHES[key]
        disc = disc_of(form)
        out += ["\tif = {",
                f"\t\tlimit = {{ kehillah_spark_is_author_of_{key}_trigger = yes "
                f"NOT = {{ has_global_variable = kehillah_wk_{key}_written }} "
                f"kehillah_spark_can_hold_{form}_trigger = yes kehillah_spark_rabbi_gate_trigger = yes "
                f"NOT = {{ AND = {{ kehillah_spark_holds_{form}_trigger = yes var:kehillah_spark_{disc}_tier >= 2 }} }} }}",
                f"\t\tkehillah_spark_set_{form}_effect = {{ WORK = flag:none }}",
                f"\t\tset_variable = {{ name = kehillah_spark_{disc}_tier value = 2 }}",
                "\t}"]
    out.append("}")
    out += ["# Scope: the author finishing a manuscript. A historical author who meets",
            "# his own niche's conditions writes that work, without the quality roll.",
            "kehillah_spark_author_claim_effect = {"]
    for i, (key, ref) in enumerate(HIST_AUTHOR.items()):
        kw = "if" if i == 0 else "else_if"
        out += [f"\t{kw} = {{",
                f"\t\tlimit = {{ kehillah_spark_is_author_of_{key}_trigger = yes " + " ".join(landmarks.eligibility(key)) + " }",
                f"\t\tset_variable = {{ name = kehillah_book_named_work value = flag:{key} }}",
                "\t\tset_variable = { name = kehillah_writing_landmark value = yes }",
                "\t}"]
    out.append("}")

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
                # The AI writes its ripest idea.
                "\t\tai_chance = {",
                "\t\t\tbase = 10",
                f"\t\t\tmodifier = {{ add = 30 var:kehillah_spark_{disc}_tier ?= 2 }}",
                f"\t\t\tmodifier = {{ add = 90 var:kehillah_spark_{disc}_tier ?= 3 }}",
                "\t\t}",
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
    # Discard, from the card's corner button: confirm first.
    for disc, n in DISC_EVENT.items():
        out += ["", f"kehillah_spark.{30 + n:04d} = {{",
                "\ttype = character_event",
                "\ttitle = kehillah_spark.discard.t",
                f"\tdesc = kehillah_spark.discard_{disc}.desc",
                "\ttheme = learning",
                "\tleft_portrait = { character = root animation = thinking }",
                f"\ttrigger = {{ has_variable = kehillah_spark_{disc}_form }}",
                "\toption = {",
                "\t\tname = kehillah_spark.discard.yes",
                "\t\tcustom_tooltip = kehillah_spark.discard.yes.tt",
                f"\t\thidden_effect = {{ kehillah_spark_discard_{disc}_effect = yes }}",
                "\t}",
                "\toption = { name = kehillah_spark.discard.no }",
                "}"]
    # The upgrade moment: a short scene and a visible reward.
    for disc, n in DISC_EVENT.items():
        for tier, base, anim in ((2, 10, "personality_rational"), (3, 20, "happiness")):
            eid = f"kehillah_spark.{base + n:04d}"
            out += ["", f"{eid} = {{",
                    "\ttype = character_event",
                    f"\ttitle = kehillah_spark.upgrade_{tier}.t",
                    f"\tdesc = kehillah_spark.upgrade_{tier}_{disc}.desc",
                    "\ttheme = learning",
                    f"\tleft_portrait = {{ character = root animation = {anim} }}",
                    "\toption = {",
                    f"\t\tname = kehillah_spark.upgrade_{tier}.a",
                    f"\t\tadd_learning_lifestyle_xp = {UPGRADE_XP[tier]}",
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
    # The whole study-icon sentence, commentaries included.
    out.append("KehillahSparkStudyLine = {")
    out.append("\ttype = character")
    for work in sorted(WORKS):
        if work.startswith("work_authored_"):
            continue
        out.append(f"\ttext = {{ trigger = {{ var:kehillah_study_current_work ?= flag:{work} }} localization_key = kehillah_spark_bookline_{work} }}")
    out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_form_unknown fallback = yes }")
    out.append("}")
    # A discovered kind, or ??? (the card's kinds-found tooltip).
    for form in FORMS:
        out.append(f"KehillahSparkKnown_{form} = {{")
        out.append("\ttype = character")
        out.append(f"\ttext = {{ trigger = {{ is_target_in_variable_list = {{ name = kehillah_spark_known target = flag:{form} }} }} localization_key = kehillah_spark_known_{form} }}")
        out.append("\ttext = { trigger = { always = yes } localization_key = kehillah_spark_unknown fallback = yes }")
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
        out.append(f' kehillah_spark_ready_{disc}_toast:0 "{name}: my idea for {held} is ready to grow. #weak Upgrade it from the Learning window.#!"')
        root = f"[ROOT.Char.Custom('KehillahSparkForm_{disc}')]"
        chiddush = {
            "parshanut": f"I read the verses again with my idea beside them, and this time they answered. My idea for {root} is no longer a passing thought.\\n\\nIt is a #high chiddush#!: a reading no one has set down before.",
            "talmudics": f"The sugya that would not close has closed. Turning the argument once more, I see where my idea for {root} must stand.\\n\\nIt is a #high chiddush#! now, reasoned through to its end.",
            "hashkafa": f"What began as a question has found its answer. My idea for {root} holds together now, from its first principle to its last.\\n\\nIt is a #high chiddush#! of my own.",
        }[disc]
        out.append(f' kehillah_spark.upgrade_2_{disc}.desc:0 "{chiddush}"')
        out.append(f' kehillah_spark.upgrade_3_{disc}.desc:0 "Late in the night it came to me whole. My idea for {root} could become one of the books that generations copy, cite and argue over.\\n\\nFew scholars are given such an idea. Fewer still finish it."')
        out.append(f' kehillah_spark_empty_{disc}:0 "Master a work of {name} to spark an idea."')
        for route in ROUTES[disc]:
            if route == "apt":
                label = f"Grow in {name} aptitude"
            elif route == "works":
                label = f"Master another {name} work"
            else:
                label = ROUTE_LABEL[route]
            out.append(f' kehillah_spark_route_{disc}_{route}:0 "{label}"')
        out.append(f' kehillah_spark_craft_{disc}_toast:0 "{name}: a commentary mastered. My {name} study and writing grow surer and quicker."')
        out.append(f' kehillah_spark.discard_{disc}.desc:0 "Shall I set aside my idea for {root}? Once let go, it will not come back unless my studies spark it again."')
        known = "\\n".join(f"[GetPlayer.MakeScope.Var('kehillah_learning_view').Char.Custom('KehillahSparkKnown_{f}')]" for f in forms_of(disc))
        out.append(f' kehillah_spark_known_tt_{disc}:0 "#T {name}: forms discovered#!\\nEvery kind of {name} book you have ever held a spark for.\\n{known}"')
        out.append(f' kehillah_spark_craft_tt_{disc}:0 "#T Commentaries mastered: [GetPlayer.MakeScope.Var(\'kehillah_learning_view\').Char.MakeScope.ScriptValue(\'kehillah_spark_{disc}_commentaries_value\')|0]#!\\nEach commentary of {name} studied raises the success chance of {name} study and writing, and speeds them.\\nNow: [GetPlayer.MakeScope.Var(\'kehillah_learning_view\').Char.MakeScope.ScriptValue(\'kehillah_spark_{disc}_craft_chance_value\')|0]% success, [GetPlayer.MakeScope.Var(\'kehillah_learning_view\').Char.MakeScope.ScriptValue(\'kehillah_spark_{disc}_craft_speed_value\')|0] progress a month."')
        out.append(f' kehillah_spark_original_title_{disc}:0 "An original {name} work of my own"')
    for form in FORMS:
        out.append(f' kehillah_spark_known_{form}:0 "#P $kehillah_spark_title_{form}$#!"')
    out.append(' kehillah_spark_unknown:0 "#weak ???#!"')
    for deed, label in DEED_NAME.items():
        out.append(f' kehillah_lib_name_deed_{deed}:0 "{label}"')
    for work, forms in PREFERRED.items():
        out.append(f' kehillah_spark_preview_{work}:0 "{" or ".join(FORMS[f][2] for f in forms)}"')
    # One line per book, for the Beit Midrash card and the study scheme icon.
    for work in sorted(WORKS):
        disc = WORKS[work].get("genre")
        dname = DISCS.get(disc, ("a new", ""))[0]
        if work in COMMENTARIES:
            line = f"#P A commentary.#! Mastering it hones your {dname} study and writing instead of sparking an idea."
        elif work in PREFERRED:
            line = f"On first mastery, likely sparks an idea for {' or '.join(FORMS[f][2] for f in PREFERRED[work])}."
        else:
            line = f"On first mastery, sparks a {dname} idea."
        out.append(f' kehillah_spark_bookline_{work}:0 "{line}"')
    for key, form in NICHES.items():
        out.append(f' kehillah_spark_path_{key}:0 "{NICHE_HINT[key]}"')
        for n, (_, label) in enumerate(niche_conditions(key), 1):
            out.append(f' kehillah_spark_nc_{key}_{n}:0 "{label}"')
    for disc in DISCS:
        out.append(f' kehillah_spark_path_original_{disc}:0 "$kehillah_spark_original_title_{disc}$ #weak · into the Ledger#!"')
        for n, (_, label) in enumerate(ORIGINAL[disc], 1):
            out.append(f' kehillah_spark_nc_original_{disc}_{n}:0 "{label}"')
    return "﻿" + "\n".join(out) + "\n"


# --------------------------------------------------------------------------
VIEW = "GetPlayer.MakeScope.Var( 'kehillah_learning_view' ).Char"


def sv(name_expr: str) -> str:
    return f"{VIEW}.MakeScope.ScriptValue( {name_expr} )"


def check_line(value_expr: str, text_expr: str, indent: int, visible: str | None = None) -> str:
    """One check/cross requirement line, for a dark tooltip background."""
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
{t}\t\talpha = 0.6
{t}\t}}
{t}\ttext_single = {{
{t}\t\ttext = "{text_expr}"
{t}\t\talign = left|nobaseline
{t}\t\tmax_width = 380
{t}\t}}
{t}\texpand = {{}}
{t}}}"""


def upgrade_tooltip(disc: str) -> str:
    """The Upgrade button's tooltip: the next rung only."""
    name, apt = DISCS[disc]
    tier = sv(f"'kehillah_spark_{disc}_tier_value'")
    routes = []
    for route in ROUTES[disc]:
        value = sv(f"'kehillah_spark_route_{disc}_{route}_value'")
        if route == "apt":
            cur = sv(f"'kehillah_writing_{apt}_aptitude_value'")
            target = sv(f"'kehillah_spark_{disc}_apt_target_value'")
            text = (f"[Concatenate( Localize( 'kehillah_spark_route_{disc}_apt' ), Concatenate( '  ', Concatenate( "
                    f"IntToString( FixedPointToInt( {cur} ) ), Concatenate( ' / ', IntToString( FixedPointToInt( {target} ) ) ) ) ) )]")
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
    return f"""		tooltipwidget = {{
			widget = {{
				using = GeneralTooltipSetup
				using = DefaultTooltipBackground
				vbox = {{
					margin = {{ 16 12 }}
					spacing = 4
					min_width = 300
					text_single = {{
						layoutpolicy_horizontal = expanding
						text = "kehillah_spark_upgrade_tt_title"
						using = Font_Size_Medium
						align = left|nobaseline
					}}
					### Rabbanite scholars: beyond an Insight, a Rabbi.
{check_line(sv("'kehillah_spark_rabbi_gate_value'"), "[Localize( 'kehillah_spark_rabbi_gate' )]", 5, visible="[GreaterThanOrEqualTo_CFixedPoint( " + sv("'kehillah_spark_rabbi_gate_value'") + ", '(CFixedPoint)0' )]")}
					### Insight: any one route.
					vbox = {{
						visible = "[EqualTo_CFixedPoint( {tier}, '(CFixedPoint)1' )]"
						layoutpolicy_horizontal = expanding
						spacing = 2
						text_single = {{
							layoutpolicy_horizontal = expanding
							text = "kehillah_spark_routes_header"
							default_format = "#weak"
							align = left|nobaseline
						}}
{routes_s}
					}}
					### Chiddush: every open Great Work path.
					vbox = {{
						visible = "[EqualTo_CFixedPoint( {tier}, '(CFixedPoint)2' )]"
						layoutpolicy_horizontal = expanding
						spacing = 4
						text_single = {{
							layoutpolicy_horizontal = expanding
							text = "kehillah_spark_paths_header"
							default_format = "#weak"
							align = left|nobaseline
						}}
						text_single = {{
							visible = "[IsDataModelEmpty( {VIEW}.MakeScope.GetList( 'kehillah_spark_{disc}_paths' ) )]"
							layoutpolicy_horizontal = expanding
							text = "kehillah_spark_no_paths"
							default_format = "#weak"
							align = left|nobaseline
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
										text = "[Concatenate( Localize( Concatenate( 'kehillah_spark_path_', Scope.GetFlagName ) ), Concatenate( '   ', Concatenate( IntToString( FixedPointToInt( {sv("Concatenate( Concatenate( 'kehillah_spark_nc_', Scope.GetFlagName ), '_met_value' )")} ) ), Concatenate( '/', IntToString( FixedPointToInt( {sv("Concatenate( Concatenate( 'kehillah_spark_nc_', Scope.GetFlagName ), '_total_value' )")} ) ) ) ) ) )]"
										default_format = "#high"
										align = left|nobaseline
										max_width = 380
									}}
									vbox = {{
										layoutpolicy_horizontal = expanding
										margin_left = 6
										spacing = 1
{conds_s}
									}}
								}}
							}}
						}}
					}}
					text_single = {{
						visible = "[EqualTo_CFixedPoint( {sv(f"'kehillah_spark_{disc}_ready_value'")}, '(CFixedPoint)1' )]"
						layoutpolicy_horizontal = expanding
						text = "kehillah_spark_upgrade_tt_ready"
						align = left|nobaseline
					}}
				}}
			}}
		}}"""


def card(disc: str) -> str:
    name, _ = DISCS[disc]
    color = DISC_COLOR[disc]
    tier = sv(f"'kehillah_spark_{disc}_tier_value'")
    ready = sv(f"'kehillah_spark_{disc}_ready_value'")
    held = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_form' ).IsSet"
    form = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_form' ).GetFlagName"
    work = f"{VIEW}.MakeScope.Var( 'kehillah_spark_{disc}_work' )"
    mine = f"{VIEW}.IsLocalPlayer"
    potential = sv(f"'kehillah_spark_{disc}_potential_value'")
    stars = "\n".join(f"""				widget = {{
					size = {{ 22 22 }}
					icon = {{
						visible = "[GreaterThanOrEqualTo_CFixedPoint( {tier}, '(CFixedPoint){n}' )]"
						size = {{ 22 22 }}
						texture = "gfx/interface/icons/flat_icons/star.dds"
					}}
					icon = {{
						visible = "[LessThan_CFixedPoint( {tier}, '(CFixedPoint){n}' )]"
						size = {{ 22 22 }}
						texture = "gfx/interface/icons/flat_icons/star.dds"
						alpha = 0.2
					}}
				}}""" for n in (1, 2, 3))
    return f"""	### {name}: a card in its own colour.
	type kehillah_spark_card_{disc} = widget {{
		size = {{ 186 350 }}

		### Drop shadow, offset down and right.
		widget = {{
			position = {{ 5 6 }}
			size = {{ 182 344 }}
			alpha = 0.35
			background = {{
				texture = "gfx/interface/colors/white.dds"
				color = {{ 0.08 0.05 0.03 1 }}
			}}
		}}

		### The card.
		widget = {{
			size = {{ 182 344 }}
			background = {{ using = Background_Area_Dark }}
			background = {{
				texture = "gfx/interface/colors/white.dds"
				color = {{ {color} 0.16 }}
			}}
			background = {{ using = Background_Frame }}

			vbox = {{
				size = {{ 100% 100% }}
				margin_bottom = 10
				spacing = 6

				### Band: the discipline, in its colour.
				widget = {{
					layoutpolicy_horizontal = expanding
					size = {{ 0 30 }}
					background = {{
						texture = "gfx/interface/colors/white.dds"
						color = {{ {color} 0.9 }}
					}}
					text_single = {{
						parentanchor = center
						text = "kehillah_spark_disc_{disc}"
						align = nobaseline
					}}
					### Set the idea aside (asks first: kehillah_spark.{30 + DISC_EVENT[disc]:04d}).
					button_close = {{
						visible = "[And( {held}, {mine} )]"
						parentanchor = right|vcenter
						position = {{ -4 0 }}
						size = {{ 22 22 }}
						onclick = "[GetScriptedGui( 'kehillah_spark_discard_{disc}' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
						tooltip = "kehillah_spark_discard_tt"
					}}
				}}

				widget = {{
					size = {{ 64 64 }}
					icon = {{
						visible = "[{held}]"
						size = {{ 64 64 }}
						texture = "gfx/interface/icons/inspirations/book_inspiration.dds"
					}}
					icon = {{
						visible = "[Not( {held} )]"
						size = {{ 64 64 }}
						texture = "gfx/interface/icons/inspirations/book_inspiration.dds"
						alpha = 0.18
					}}
				}}

				### A held spark: its name, tier and source.
				vbox = {{
					visible = "[{held}]"
					layoutpolicy_horizontal = expanding
					spacing = 4
					text_multi = {{
						layoutpolicy_horizontal = expanding
						autoresize = yes
						max_width = 166
						min_width = 166
						text = "[Localize( Concatenate( 'kehillah_spark_title_', {form} ) )]"
						using = Font_Size_Medium
						align = hcenter|nobaseline
					}}
					hbox = {{
						spacing = 2
						tooltip = "[Concatenate( Localize( 'kehillah_spark_tier_tt_prefix' ), {VIEW}.Custom( 'KehillahSparkTier_{disc}' ) )]"
{stars}
						### Great Work potential: bright for a historical landmark,
						### dimmer for an original work only, faint for none.
						widget = {{
							visible = "[LessThan_CFixedPoint( {tier}, '(CFixedPoint)3' )]"
							size = {{ 26 22 }}
							icon = {{
								visible = "[EqualTo_CFixedPoint( {potential}, '(CFixedPoint)2' )]"
								size = {{ 22 22 }}
								position = {{ 4 0 }}
								texture = "gfx/interface/icons/artifact/artifact_book.dds"
								tooltip = "kehillah_spark_potential_2"
							}}
							icon = {{
								visible = "[EqualTo_CFixedPoint( {potential}, '(CFixedPoint)1' )]"
								size = {{ 22 22 }}
								position = {{ 4 0 }}
								texture = "gfx/interface/icons/artifact/artifact_book.dds"
								alpha = 0.55
								tooltip = "kehillah_spark_potential_1"
							}}
							icon = {{
								visible = "[EqualTo_CFixedPoint( {potential}, '(CFixedPoint)0' )]"
								size = {{ 22 22 }}
								position = {{ 4 0 }}
								texture = "gfx/interface/icons/artifact/artifact_book.dds"
								alpha = 0.15
								tooltip = "kehillah_spark_potential_0"
							}}
						}}
					}}
					text_single = {{
						text = "[{VIEW}.Custom( 'KehillahSparkTier_{disc}' )]"
						default_format = "#weak"
						align = nobaseline
					}}
					text_multi = {{
						visible = "[And( {work}.IsSet, Not( EqualTo_string( {work}.GetFlagName, 'none' ) ) )]"
						layoutpolicy_horizontal = expanding
						autoresize = yes
						max_width = 166
						min_width = 166
						text = "[Concatenate( Localize( 'kehillah_spark_from' ), Localize( Concatenate( 'kehillah_lib_name_', {work}.GetFlagName ) ) )]"
						default_format = "#weak"
						align = hcenter|nobaseline
					}}
				}}

				### An empty slot.
				vbox = {{
					visible = "[Not( {held} )]"
					layoutpolicy_horizontal = expanding
					spacing = 6
					text_single = {{
						text = "kehillah_spark_empty_slot"
						using = Font_Size_Medium
						default_format = "#weak"
						align = nobaseline
					}}
					text_multi = {{
						layoutpolicy_horizontal = expanding
						autoresize = yes
						max_width = 160
						min_width = 160
						text = "kehillah_spark_empty_{disc}"
						default_format = "#weak"
						align = hcenter|nobaseline
					}}
				}}

				expand = {{}}

				### Discovery and craft: kinds found in this discipline, commentaries mastered.
				text_single = {{
					text = "[Concatenate( Localize( 'kehillah_spark_kinds_found' ), Concatenate( IntToString( FixedPointToInt( {sv(f"'kehillah_spark_{disc}_known_value'")} ) ), Concatenate( ' / ', IntToString( FixedPointToInt( {sv(f"'kehillah_spark_{disc}_kinds_value'")} ) ) ) ) )]"
					tooltip = "kehillah_spark_known_tt_{disc}"
					default_format = "#weak"
					align = nobaseline
				}}
				text_single = {{
					visible = "[GreaterThan_CFixedPoint( {sv(f"'kehillah_spark_{disc}_commentaries_value'")}, '(CFixedPoint)0' )]"
					text = "[Concatenate( Localize( 'kehillah_spark_commentaries' ), IntToString( FixedPointToInt( {sv(f"'kehillah_spark_{disc}_commentaries_value'")} ) ) )]"
					tooltip = "kehillah_spark_craft_tt_{disc}"
					default_format = "#weak"
					align = nobaseline
				}}

				### Actions, on the player's own cards.
				button_standard = {{
					visible = "[And( {held}, And( {mine}, LessThan_CFixedPoint( {tier}, '(CFixedPoint)3' ) ) )]"
					size = {{ 156 32 }}
					text = "[Concatenate( Localize( 'kehillah_spark_upgrade_button' ), Select_CString( EqualTo_CFixedPoint( {tier}, '(CFixedPoint)1' ), Concatenate( Localize( 'KEHILLAH_SPARK_COUNT_OPEN' ), Concatenate( IntToString( FixedPointToInt( {sv(f"'kehillah_spark_{disc}_routes_met_value'")} ) ), Concatenate( '/', Concatenate( IntToString( FixedPointToInt( {sv(f"'kehillah_spark_{disc}_routes_needed_value'")} ) ), Localize( 'KEHILLAH_SPARK_COUNT_CLOSE' ) ) ) ) ), Localize( 'KEHILLAH_SPARK_NOTHING' ) ) )]"
					enabled = "[GetScriptedGui( 'kehillah_spark_upgrade_{disc}' ).IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
					onclick = "[GetScriptedGui( 'kehillah_spark_upgrade_{disc}' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
					using = tooltip_es
					glow = {{
						visible = "[EqualTo_CFixedPoint( {ready}, '(CFixedPoint)1' )]"
						glow_radius = 8
						using = Glow_Standard
						using = Color_Bright_Yellow
					}}
{upgrade_tooltip(disc)}
				}}
				### A Great Work's place in the action row, and a viewer's read-only tooltip.
				text_single = {{
					visible = "[And( {held}, GreaterThanOrEqualTo_CFixedPoint( {tier}, '(CFixedPoint)3' ) )]"
					text = "kehillah_spark_great_badge"
					align = nobaseline
				}}
				button_standard = {{
					visible = "[And( {held}, {mine} )]"
					size = {{ 156 32 }}
					text = "kehillah_spark_write_button"
					enabled = "[GetScriptedGui( 'kehillah_spark_write' ).IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
					onclick = "[GetScriptedGui( 'kehillah_spark_write' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
					tooltip = "kehillah_spark_write_button_tt"
				}}
			}}
		}}
	}}
"""


def gui() -> str:
    head = """##########################################################################
# SPARK CARDS for the Learning window (2026-11-24, Daniel: "sparks like cards
# in three columns, with a shadow and 'empty slot' ... color code the three
# genres ... upgrading the spark should be an active choice that feels good").
# GENERATED by scripts/kehillah_writing_sparks.py -- edit the script, not this.
# One card per discipline, for the character the Learning window shows
# (var:kehillah_learning_view): a coloured band, the inspiration icon, the
# spark's name, tier stars and source; on the player's own cards an Upgrade
# button (its tooltip lists the next rung's requirements; it glows when they
# are met) and Write.
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
