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
}


def mastered(key: str) -> str:
    return f"is_target_in_variable_list = {{ name = kehillah_mastered_works target = flag:{key} }}"


RABBANITE = "rite ?= { kehillah_rite_rabbanite_trigger = yes }"
KARAITE = "rite ?= { kehillah_rite_toric_trigger = yes }"
HAYMANOT = "rite ?= { kehillah_rite_haymanot_trigger = yes }"

EXTRA = {
    "work_emunot_vedeot": [RABBANITE, "learning >= 15"],
    "work_chovot_halevavot": [RABBANITE, "learning >= 15"],
    "work_seder_rav_amram": ["learning >= 15"],
    "work_iggeret_rav_sherira": ["learning >= 15", "kehillah_lib_bavli_mastered_count_value >= 2"],
    "work_rabbenu_hananel": ["learning >= 15", "kehillah_lib_bavli_mastered_count_value >= 2"],
    "work_mekor_hayyim": [RABBANITE, "learning >= 16", "knows_language = language_arabic"],
    "work_kitab_alanwar": [KARAITE, "learning >= 15"],
    "work_yefet_commentary": [KARAITE, "learning >= 15"],
    "work_sefer_yosippon": ["learning >= 15", mastered("work_josephus_jewish_war")],
    "work_toldot_yeshu": ["learning >= 15", mastered("work_mishnah")],  # 2026-11-24 floor: two requirements
    "work_diwan_dunash": [RABBANITE, "learning >= 15", "knows_language = language_arabic"],
    "work_diwan_samuel_hanagid": [RABBANITE, "learning >= 15", mastered("work_diwan_dunash")],
    "work_diwan_ibn_gabirol": [RABBANITE, "learning >= 15", mastered("work_diwan_dunash")],
    "work_agron_david_al_fasi": [KARAITE, "learning >= 15", "knows_language = language_arabic"],  # 2026-11-24 floor
    "work_salmon_ben_jeroham_commentary": [KARAITE, "learning >= 15", mastered("work_tanakh_neviim")],
    "work_levi_ben_yefet_mitzvot": [KARAITE, "learning >= 15"],
    "work_teezaza_sanbat": [HAYMANOT, "learning >= 15", mastered("work_orit")],
    "work_cochin_copper_plates": ["learning >= 15", mastered("work_tanakh_neviim")],  # 2026-11-24 floor
    "work_ibn_ezra_torah": [RABBANITE, "learning >= 15", mastered("work_targum_onkelos")],
    "work_sefer_mitzvot_gadol": [RABBANITE, "learning >= 16", mastered("work_mishneh_torah")],
    "work_or_zarua": [RABBANITE, "learning >= 16", "kehillah_lib_bavli_mastered_count_value >= 3"],
    "work_ramban_torah": [RABBANITE, "learning >= 16", mastered("work_rashi_torah")],
    "work_sefer_hamivhar": [KARAITE, "learning >= 15", mastered("work_yefet_commentary")],
    "work_sefer_hachinukh": [RABBANITE, "learning >= 15", mastered("work_tanakh_torah")],
    "work_arbaah_turim": [RABBANITE, "learning >= 17", mastered("work_mishneh_torah")],
    "work_maggid_mishneh": [RABBANITE, "learning >= 16", mastered("work_mishneh_torah")],
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
        # Fixed historical works circulate automatically at their catalog date.
        # Until then, a scholar can fill the same niche in an alternate history.
        parts.append(f"current_date < {work['year']}.1.1")
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
                        if not work.get("named"):
                            conditions.append(f"current_date < {work['year']}.1.1")
                    else:
                        conditions = eligibility(key)[1:]
                    if len(keys) == 1:
                        status.extend("\t" + condition for condition in conditions)
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
