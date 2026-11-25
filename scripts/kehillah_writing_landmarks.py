"""Generate writing niches for every fixed work dated after the 867 bookmark."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKS = json.loads((ROOT / "scripts/kehillah_library_catalog.json").read_text(encoding="utf-8"))["works"]
EFFECT = ROOT / "common/scripted_effects/kehillah_writing_landmark_generated_effects.txt"
CUSTOM = ROOT / "common/customizable_localization/kehillah_writing_future_titles_custom_loc.txt"
LOC = ROOT / "localization/english/kehillah_writing_future_titles_l_english.yml"
STATUS = ROOT / "common/scripted_triggers/kehillah_writing_landmark_generated_triggers.txt"


FORMS = {
    "work_emunot_vedeot": "disputation",
    "work_chovot_halevavot": "ethics",
    "work_kuzari": "systematic_dialogue",
    "work_seder_rav_amram": "siddur",
    "work_iggeret_rav_sherira": "tradition_history",
    "work_rabbenu_hananel": "talmud",
    "work_mekor_hayyim": "systematic_dialogue",
    "work_kitab_alanwar": "disputation",
    "work_yefet_commentary": "torah",
    "work_rashi_torah": "torah",
    "work_rashi_talmud": "talmud",
    "work_hilkhot_harif": "law",
    "work_mishneh_torah": "law",
    "work_moreh_nevukhim": "systematic_dialogue",
    "work_sefer_habahir": "mystical",
    "work_sefer_hasidim": "devotion",
    "work_tosafot": "talmud",
    "work_zohar": "mystical",
    "work_sefer_yosippon": "chronicle",
    "work_toldot_yeshu": "disputation",
    "work_diwan_dunash": "poetry",
    "work_diwan_samuel_hanagid": "poetry",
    "work_diwan_ibn_gabirol": "poetry",
    "work_agron_david_al_fasi": "grammar",
    "work_salmon_ben_jeroham_commentary": "torah",
    "work_levi_ben_yefet_mitzvot": "scriptural_law",
    "work_teezaza_sanbat": "minhag",
    "work_cochin_copper_plates": "chronicle",
    "work_ibn_ezra_torah": "torah",
    "work_sefer_mitzvot_gadol": "law",
    "work_or_zarua": "law",
    "work_ramban_torah": "torah",
    "work_sefer_hamivhar": "torah",
    "work_sefer_hachinukh": "law",
    "work_arbaah_turim": "law",
    "work_maggid_mishneh": "law",
    # 2026-11-25 (Daniel: "add some additional historical Great Work sparks"):
    # these also give midrash, Yerushalmi, responsa, dialogue and translation
    # sparks their first historical Great Works.
    "work_lekach_tov": "midrash",
    "work_machzor_vitry": "siddur",
    "work_eshkol_hakofer": "scriptural_law",
    "work_siponto_zeraim": "yerushalmi",
    "work_sefer_haqabbalah": "tradition_history",
    "work_sefer_haberit": "dialogue",
    "work_ibn_tibbon_moreh": "translation",
    "work_sefer_hamanhig": "minhag",
    "work_radak_shorashim": "grammar",
    "work_responsa_maharam": "responsa",
    "work_maalot_hamiddot": "ethics",
    "work_responsa_rashba": "responsa",
    "work_milhamot_hashem": "systematic_dialogue",
    "work_etz_hayyim_karaite": "systematic_dialogue",
}


def mastered(key: str) -> str:
    return f"is_target_in_variable_list = {{ name = kehillah_mastered_works target = flag:{key} }}"


RABBANITE = "rite ?= { kehillah_rite_rabbanite_trigger = yes }"
KARAITE = "rite ?= { kehillah_rite_toric_trigger = yes }"
HAYMANOT = "rite ?= { kehillah_rite_haymanot_trigger = yes }"

# Conditions that are not a learning floor, a language, a Bavli count or a
# mastered book carry their own card label here (read by
# kehillah_writing_sparks.py's condition_label).
LABELS: dict[str, str] = {}


def labelled(cond: str, label: str) -> str:
    LABELS[cond] = label
    return cond


DEED_LABEL = {"sermon": "Preach {n} sermons", "ruling": "Preside over {n} Bet Din rulings",
              "letter": "Answer {n} she'elot", "debate": "Take a side in {n} machlokot"}


def deeds(kind: str, n: int) -> str:
    """Lifetime deeds, counted by kehillah_spark_from_deed_<kind>_effect.
    AI scholars rarely reach these deeds, so they are spared them: otherwise
    historical authors (HIST_AUTHOR in the sparks generator) could never
    write their own works."""
    return labelled(f"kehillah_deed_{kind}_ok_value >= {n}", DEED_LABEL[kind].format(n=n))


APT = {"parshanut": ("parshanut", "Parshanut"), "talmudics": ("talmudics", "Talmudics"),
       "hashkafa": ("machshava", "Machshavah")}


def aptitude(disc: str, n: int) -> str:
    key, label = APT[disc]
    return labelled(f"kehillah_writing_{key}_aptitude_value >= {n}", f"{label} aptitude {n}")


def lang_or_region(lang: str, region: str, label: str) -> str:
    return labelled(f"OR = {{ knows_language = language_{lang} location ?= {{ geographical_region = {region} }} }}", label)


def either(a: str, b: str) -> str:
    return labelled(f"OR = {{ {mastered(a)} {mastered(b)} }}", f"Master $kehillah_lib_name_{a}$ or $kehillah_lib_name_{b}$")


ARABIC = "knows_language = language_arabic"
GREEK_OR_BALKANS = lang_or_region("greek", "world_europe_south_east", "Know Greek or live in the Balkans")
GREEK_OR_ITALY = lang_or_region("greek", "world_europe_south_italy", "Know Greek or live in Italy")
ARABIC_OR_IBERIA = lang_or_region("arabic", "world_europe_west_iberia", "Know Arabic or live in Iberia")
ARABIC_OR_MAGHREB = lang_or_region("arabic", "world_africa_north", "Know Arabic or live in North Africa")
TAMIL_OR_INDIA = lang_or_region("tamil", "world_india", "Know Tamil or live in India")
POLYGLOT = labelled("num_of_known_languages >= 3", "Know 3 languages")
SHAS = labelled("kehillah_has_mastered_shas_trigger = yes", "Master the whole Bavli")
TANAKH_TWICE = labelled("kehillah_lib_tanakh_rounds_value >= 2", "Read the Tanakh twice through")
YERUSHALMI_1 = labelled("kehillah_lib_yerushalmi_mastered_count_value >= 1", "Master a Yerushalmi order")
GENTLE = labelled("OR = { has_trait = humble has_trait = patient has_trait = temperate }",
                  "Be humble, patient or temperate")
STATESMAN = labelled("OR = { diplomacy >= 14 martial >= 14 }", "Diplomacy or Martial 14")


def bavli(n: int) -> str:
    return f"kehillah_lib_bavli_mastered_count_value >= {n}"


# 2026-11-25 audit (Daniel: "assess if they're fun (a challenge), flavorful,
# and unique. Improve on them if they're too easy or bland"): every niche was
# "Learning 15 and one book", easier than an original Great Work (Learning
# 16, aptitude 40, two more works). Each now asks for four or five things:
# a Learning floor of 15-18, the books its author stood on, and one deed,
# place, language or temperament that was his. Karaite and Haymanot niches
# avoid deeds, which their communities rarely reach, and use aptitude instead.
EXTRA = {
    "work_emunot_vedeot": [RABBANITE, "learning >= 16", ARABIC, aptitude("hashkafa", 40), deeds("debate", 3)],
    "work_chovot_halevavot": [RABBANITE, "learning >= 16", ARABIC, mastered("work_avot_derabbi_natan"), GENTLE],
    "work_seder_rav_amram": ["learning >= 16", mastered("work_mishnah"), deeds("letter", 3)],
    "work_iggeret_rav_sherira": ["learning >= 16", bavli(3), mastered("work_seder_olam_rabbah"), deeds("letter", 5)],
    "work_rabbenu_hananel": ["learning >= 16", bavli(4), YERUSHALMI_1, ARABIC_OR_MAGHREB],
    "work_mekor_hayyim": [RABBANITE, "learning >= 17", ARABIC, mastered("work_theology_of_aristotle"), aptitude("hashkafa", 45)],
    "work_kitab_alanwar": [KARAITE, "learning >= 16", ARABIC, mastered("work_anan_sefer_hamitzvot"), aptitude("talmudics", 40)],
    "work_yefet_commentary": [KARAITE, "learning >= 16", ARABIC, TANAKH_TWICE],
    "work_sefer_yosippon": ["learning >= 16", mastered("work_josephus_jewish_war"), GREEK_OR_ITALY],
    "work_toldot_yeshu": ["learning >= 15", mastered("work_mishnah"), deeds("debate", 3)],
    "work_diwan_dunash": [RABBANITE, "learning >= 15", ARABIC, mastered("work_tanakh_ketuvim")],
    "work_diwan_samuel_hanagid": [RABBANITE, "learning >= 15", mastered("work_diwan_dunash"), STATESMAN],
    "work_diwan_ibn_gabirol": [RABBANITE, "learning >= 16", ARABIC, mastered("work_diwan_dunash"), mastered("work_sefer_yetzirah")],
    "work_agron_david_al_fasi": [KARAITE, "learning >= 15", ARABIC, TANAKH_TWICE],
    "work_salmon_ben_jeroham_commentary": [KARAITE, "learning >= 15", mastered("work_tanakh_neviim"), aptitude("parshanut", 35)],
    "work_levi_ben_yefet_mitzvot": [KARAITE, "learning >= 16", mastered("work_anan_sefer_hamitzvot"), mastered("work_kitab_alanwar")],
    "work_teezaza_sanbat": [HAYMANOT, "learning >= 15", mastered("work_orit"), aptitude("talmudics", 30)],
    "work_cochin_copper_plates": ["learning >= 15", mastered("work_tanakh_neviim"), TAMIL_OR_INDIA],
    "work_ibn_ezra_torah": [RABBANITE, "learning >= 17", mastered("work_targum_onkelos"), POLYGLOT, aptitude("parshanut", 45)],
    "work_sefer_mitzvot_gadol": [RABBANITE, "learning >= 16", mastered("work_mishneh_torah"), deeds("sermon", 5)],
    "work_or_zarua": [RABBANITE, "learning >= 16", bavli(3), mastered("work_tosafot"), deeds("ruling", 5)],
    "work_ramban_torah": [RABBANITE, "learning >= 17", mastered("work_rashi_torah"), mastered("work_ibn_ezra_torah"), aptitude("parshanut", 50)],
    "work_sefer_hamivhar": [KARAITE, "learning >= 16", mastered("work_yefet_commentary"), TANAKH_TWICE],
    "work_sefer_hachinukh": [RABBANITE, "learning >= 15", mastered("work_tanakh_torah"), mastered("work_mishneh_torah")],
    "work_arbaah_turim": [RABBANITE, "learning >= 17", mastered("work_mishneh_torah"), SHAS, aptitude("talmudics", 60)],
    "work_maggid_mishneh": [RABBANITE, "learning >= 16", mastered("work_mishneh_torah"), bavli(4), deeds("ruling", 8)],
    # 2026-11-25 new niches.
    "work_lekach_tov": [RABBANITE, "learning >= 16", mastered("work_genesis_rabbah"), mastered("work_pesikta_derav_kahana"),
                        GREEK_OR_BALKANS, deeds("sermon", 5)],
    "work_machzor_vitry": [RABBANITE, "learning >= 16", mastered("work_seder_rav_amram"), mastered("work_rashi_talmud")],
    "work_eshkol_hakofer": [KARAITE, "learning >= 16", mastered("work_levi_ben_yefet_mitzvot"), mastered("work_agron_david_al_fasi"),
                            GREEK_OR_BALKANS],
    "work_siponto_zeraim": [RABBANITE, "learning >= 16", mastered("work_yerushalmi_zeraim"), mastered("work_tosefta"), GREEK_OR_ITALY],
    "work_sefer_haqabbalah": [RABBANITE, "learning >= 16", mastered("work_iggeret_rav_sherira"), ARABIC_OR_IBERIA, deeds("debate", 3)],
    "work_sefer_haberit": [RABBANITE, "learning >= 16", mastered("work_tanakh_neviim"), mastered("work_emunot_vedeot"), deeds("debate", 6)],
    "work_ibn_tibbon_moreh": [RABBANITE, "learning >= 17", ARABIC, mastered("work_moreh_nevukhim"), aptitude("hashkafa", 50)],
    "work_sefer_hamanhig": [RABBANITE, "learning >= 16", mastered("work_seder_rav_amram"), POLYGLOT, deeds("ruling", 3)],
    "work_radak_shorashim": [RABBANITE, "learning >= 16", mastered("work_targum_onkelos"), TANAKH_TWICE, aptitude("parshanut", 45)],
    "work_responsa_maharam": [RABBANITE, "learning >= 17", mastered("work_tosafot"), bavli(4), deeds("letter", 12)],
    "work_maalot_hamiddot": [RABBANITE, "learning >= 15", mastered("work_chovot_halevavot"), GENTLE, deeds("sermon", 8)],
    "work_responsa_rashba": [RABBANITE, "learning >= 17", mastered("work_ramban_torah"), deeds("letter", 20), deeds("ruling", 5)],
    "work_milhamot_hashem": [RABBANITE, "learning >= 18", mastered("work_ibn_tibbon_moreh"), aptitude("hashkafa", 60)],
    "work_etz_hayyim_karaite": [KARAITE, "learning >= 17", mastered("work_kitab_alanwar"),
                                either("work_moreh_nevukhim", "work_ibn_tibbon_moreh"), aptitude("hashkafa", 50)],
}

LEGACY_TITLES = {
    "work_emunot_vedeot": "Emunot ve-Deot",
    "work_chovot_halevavot": "Chovot ha-Levavot",
}
LEGACY_DESCS = {
    "work_emunot_vedeot": "Saadia Gaon's Book of Beliefs and Opinions, the first systematic Jewish philosophy.",
    "work_chovot_halevavot": "Bahya ibn Paquda's Duties of the Heart sets inward devotion beside the outward law.",
}
LEGACY_DETAILS = {
    "work_emunot_vedeot": "Saadia Gaon wrote this tenth-century work to defend Jewish belief through reasoned argument. Its subjects include creation, revelation, human choice, and the relation between inherited teaching and philosophy.",
    "work_chovot_halevavot": "Bahya ibn Paquda's Andalusian ethical work asks what intention and trust in God add to outward observance. Written in the later eleventh century, it moves from public duties toward the inward life of the worshipper.",
}


def eligibility(key: str) -> list[str]:
    work = WORKS[key]
    parts = [f"var:kehillah_writing_form ?= flag:{FORMS[key]}",
             f"kehillah_writing_{FORMS[key]}_trigger = yes",
             f"NOT = {{ has_global_variable = kehillah_wk_{key}_written }}"]
    if work.get("named"):
        if key == "work_rashi_torah":
            parts.append("kehillah_writing_rashi_torah_ready_trigger = yes")
        elif key == "work_rashi_talmud":
            parts.append("kehillah_writing_rashi_talmud_ready_trigger = yes")
        else:
            parts.append(f"kehillah_sefer_ambition_{work['ambition']}_trigger = yes")
    else:
        # 2026-11-24 (Daniel): a fixed work dated after the game's start stays
        # open until someone writes it (kehillah_library_catalog.py marks the
        # earlier ones written at the start); no closing year.
        parts.extend(EXTRA[key])
    thesis = work.get("writing_thesis_tenet")
    if thesis:
        parts.append(f"kehillah_writing_believes_thesis_trigger = {{ TENET = {thesis} }}")
    return parts


def quoted(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    expected = {key for key, work in WORKS.items()
                if not key.startswith("work_authored_") and work.get("year", 0) > 867}
    assert set(FORMS) == expected, f"unmapped future works: {sorted(expected ^ set(FORMS))}"
    assert set(EXTRA) == {key for key in expected if not WORKS[key].get("named")}
    for key, conds in EXTRA.items():
        for ref in re.findall(r"flag:(\w+)", " ".join(conds)):
            assert ref in WORKS, f"{key} needs unknown work {ref}"
    for key in expected:
        thesis = WORKS[key].get("writing_thesis_tenet")
        assert bool(thesis) == bool(WORKS[key].get("argues_for")), key
        if thesis:
            assert thesis in WORKS[key]["argues_for"], key
        if not WORKS[key].get("named"):
            assert WORKS[key].get("writing_title"), key

    effect = ["# Generated by scripts/kehillah_writing_landmarks.py.",
              "# Every dated catalog work after 867 is a possible future niche.",
              "kehillah_writing_select_landmark_effect = {",
              "\tif = {", "\t\tlimit = {", "\t\t\tOR = {"]
    for key in FORMS:
        effect.append("\t\t\t\tAND = { " + " ".join(eligibility(key)) + " }")
    effect += ["\t\t\t}", "\t\t}", "\t\trandom_list = {"]
    for key in FORMS:
        effect += ["\t\t\t100 = {", "\t\t\t\ttrigger = { " + " ".join(eligibility(key)) + " }",
                   f"\t\t\t\tset_variable = {{ name = kehillah_book_named_work value = flag:{key} }}",
                   "\t\t\t}"]
    effect += ["\t\t}", "\t}",
               "\tif = { limit = { has_variable = kehillah_book_named_work } set_variable = { name = kehillah_writing_landmark value = yes } }",
               "}"]
    effect += ["", "# In a project-option preview. $FORM$ is the option's form key.",
               "kehillah_writing_landmark_hint_effect = {",
               "\tif = { limit = { NOT = { kehillah_writing_landmark_has_$FORM$_trigger = yes } } custom_tooltip = kehillah_writing.landmark_none }",
               "\telse_if = { limit = { kehillah_writing_landmark_ready_$FORM$_trigger = yes } custom_tooltip = kehillah_writing.landmark_ready }",
               "\telse_if = { limit = { kehillah_writing_landmark_open_$FORM$_trigger = yes } custom_tooltip = kehillah_writing.landmark_open }",
               "\telse = { custom_tooltip = kehillah_writing.landmark_filled }",
               "\tkehillah_writing_landmark_belief_hint_$FORM$_effect = yes",
               "}"]
    EFFECT.write_text("\n".join(effect) + "\n", encoding="utf-8-sig")

    # 2026-11-24: project options moved to the generated spark event.
    events = (ROOT / "events/kehillah_spark_events.txt").read_text(encoding="utf-8")
    forms = set(re.findall(r"kehillah_writing_choose_project_effect = \{ FORM = (\w+) GENRE = \w+ DISC = \w+ \}", events))
    assert len(forms) == 20, sorted(forms)
    for form in sorted(forms):
        effect = [f"kehillah_writing_landmark_belief_hint_{form}_effect = {{"]
        for key, candidate_form in FORMS.items():
            if candidate_form != form or not WORKS[key].get("writing_thesis_tenet"):
                continue
            thesis = WORKS[key]["writing_thesis_tenet"]
            other_conditions = eligibility(key)[1:-1]
            effect += ["\tif = {", "\t\tlimit = { " + " ".join(other_conditions) +
                       f" NOT = {{ kehillah_writing_believes_thesis_trigger = {{ TENET = {thesis} }} }} }}",
                       f"\t\tcustom_tooltip = kehillah_writing.landmark_thesis_{key}", "\t}"]
        effect.append("}")
        with EFFECT.open("a", encoding="utf-8") as handle:
            handle.write("\n" + "\n".join(effect) + "\n")
    status = ["# Generated by scripts/kehillah_writing_landmarks.py."]
    for form in sorted(forms):
        keys = [key for key, candidate_form in FORMS.items() if candidate_form == form]
        status += [f"kehillah_writing_landmark_has_{form}_trigger = {{ always = {'yes' if keys else 'no'} }}"]
        for kind in ("open", "ready"):
            status += [f"kehillah_writing_landmark_{kind}_{form}_trigger = {{"]
            if keys:
                if len(keys) > 1:
                    status.append("\tOR = {")
                for key in keys:
                    work = WORKS[key]
                    if kind == "open":
                        conditions = [f"NOT = {{ has_global_variable = kehillah_wk_{key}_written }}"]
                    else:
                        conditions = eligibility(key)[1:]
                    if len(keys) == 1:
                        status.extend("\t" + condition for condition in conditions)
                    elif len(conditions) == 1:
                        status.append("\t\t" + conditions[0])
                    else:
                        status.append("\t\tAND = { " + " ".join(conditions) + " }")
                if len(keys) > 1:
                    status.append("\t}")
            else:
                status.append("\talways = no")
            status.append("}")
    STATUS.write_text("\n".join(status) + "\n", encoding="utf-8-sig")

    custom = ["# Generated by scripts/kehillah_writing_landmarks.py."]
    loc = ["l_english:"]
    for key in FORMS:
        work = WORKS[key]
        thesis = work.get("writing_thesis_tenet")
        if thesis:
            title = work.get("writing_title") or work.get("prose", {}).get("name") or key
            loc.append(f' kehillah_writing.landmark_thesis_{key}:0 "A landmark {quoted(title)} needs conviction in ${thesis}_name$, held personally or by your rite."')
        if work.get("named"):
            continue
        global_author = f"kehillah_wk_{key}_author"
        for kind in ("Title", "Composer", "Desc", "Detail"):
            custom += [f"KehillahFuture{kind}_{key} = {{", "\ttype = character",
                       f"\ttext = {{ trigger = {{ exists = global_var:{global_author} }} localization_key = kehillah_future_{kind.lower()}_{key}_written }}",
                       f"\ttext = {{ trigger = {{ always = no }} localization_key = kehillah_future_{kind.lower()}_{key}_historical fallback = yes }}",
                       "}"]
        author = f"[GetGlobalVariable('{global_author}').GetCharacter.GetFirstNamePossessiveNoTooltip]"
        author_link = f"[GetGlobalVariable('{global_author}').GetCharacter.GetShortUIName]"
        loc += [f' kehillah_future_title_{key}_written:0 "{author} {quoted(work["writing_title"])}"',
                f' kehillah_future_title_{key}_historical:0 "{quoted(work.get("prose", {}).get("name") or LEGACY_TITLES[key])}"',
                f' kehillah_future_composer_{key}_written:0 "{author_link}"',
                f' kehillah_future_composer_{key}_historical:0 "{quoted(work["composer"])}"',
                f' kehillah_future_desc_{key}_written:0 "A new work on {quoted(work["writing_title"])} by {author_link}."',
                f' kehillah_future_desc_{key}_historical:0 "{quoted(work.get("prose", {}).get("desc") or LEGACY_DESCS[key])}"',
                f' kehillah_future_detail_{key}_written:0 "{author_link} has given this subject a new form in this campaign. Copies, readers and debate will determine its standing in each rite."',
                f' kehillah_future_detail_{key}_historical:0 "{quoted(work.get("prose", {}).get("detail") or LEGACY_DETAILS[key])}"']
    CUSTOM.write_text("\n".join(custom) + "\n", encoding="utf-8-sig")
    LOC.write_text("\n".join(loc) + "\n", encoding="utf-8-sig")


if __name__ == "__main__":
    main()
