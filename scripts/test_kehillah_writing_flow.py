"""Source-level integration checks for the writing flow and generated catalog links."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


class WritingFlowTest(unittest.TestCase):
    def test_project_choices_have_gates_and_localization(self) -> None:
        # 2026-11-24: the project is chosen from held sparks (one per discipline)
        # in the generated kehillah_spark.0001; the old per-form gate decides who
        # may receive a spark in that form.
        events = read("events/kehillah_spark_events.txt")
        triggers = read("common/scripted_triggers/kehillah_writing_triggers.txt")
        sparks = read("common/scripted_triggers/kehillah_writing_spark_generated_triggers.txt")
        loc = read("localization/english/kehillah_writing_l_english.yml")
        spark_loc = read("localization/english/kehillah_writing_spark_generated_l_english.yml")
        forms = re.findall(r"kehillah_writing_choose_project_effect = \{ FORM = (\w+) GENRE = (\w+) DISC = (\w+) \}", events)
        self.assertEqual(len(forms), 20)
        self.assertEqual(len({form for form, _, _ in forms}), 20)
        for form, _, disc in forms:
            self.assertIn(f"kehillah_writing_{form}_trigger = {{", triggers)
            self.assertIn(f"kehillah_spark_can_hold_{form}_trigger = {{", sparks)
            self.assertIn(f"trigger = {{ kehillah_spark_holds_{form}_trigger = yes NOT = {{ kehillah_writing_busy_trigger = yes }} }}", events)
            self.assertIn(f" kehillah_writing.{form}.tt:0", loc)
            for tier in (1, 2, 3):
                self.assertIn(f" kehillah_spark.0001.{form}.{tier}:0", spark_loc)
        self.assertNotIn("kehillah_writing.0001 = {", read("events/kehillah_writing_events.txt"))

    def test_sparks_gate_and_are_used_up(self) -> None:
        decision = read("common/decisions/kehillah_rabbi_book_decisions.txt")
        effects = read("common/scripted_effects/kehillah_writing_effects.txt")
        scheme = read("common/schemes/scheme_types/kehillah_writing_scheme.txt")
        self.assertIn("kehillah_has_any_spark_trigger = yes", decision)
        self.assertIn("trigger_event = kehillah_spark.0001", decision)
        start = effects[effects.index("kehillah_writing_start_effect = {"):]
        self.assertLess(start.index("kehillah_spark_consume_current_effect = yes"),
                        start.index("		start_scheme = { type = kehillah_writing"))
        self.assertIn("var:kehillah_writing_spark_tier ?= 3", effects)
        self.assertIn("NOT = { var:kehillah_writing_spark_tier ?= 1 }", scheme)
        self.assertNotIn("kehillah_spark_seed_effect", read("common/on_action/kehillah_writing_spark_on_actions.txt"))
        hooks = {
            "common/scripted_effects/kehillah_library_effects.txt": "kehillah_spark_from_study_effect = { WORK = $WORK$ TRACK = $TRACK$ }",
            "common/scripted_effects/kehillah_bet_din_scripted_effects.txt": "DISC = talmudics ROUTE = ruled",
            "common/scripted_effects/kehillah_sheelah_effects.txt": "DISC = talmudics ROUTE = answered",
            "common/scripted_effects/kehillah_machloket_effects.txt": "DISC = hashkafa ROUTE = debated",
            "events/kehillah_sermon_events.txt": "DISC = parshanut ROUTE = preached",
        }
        for path, call in hooks.items():
            self.assertIn(call, read(path), path)

    def test_spark_ui_is_wired(self) -> None:
        window = read("gui/kehillah_learning_window.gui")
        cards = read("gui/kehillah_spark_cards.gui")
        widget = read("gui/kehillah_scheme_widget.gui")
        for disc in ("parshanut", "talmudics", "hashkafa"):
            self.assertIn(f"kehillah_spark_card_{disc} = {{}}", window)
            self.assertIn(f"type kehillah_spark_card_{disc} = widget", cards)
            self.assertIn(f"kehillah_spark_upgrade_{disc} = {{", read("common/scripted_guis/kehillah_learning_gui.txt"))
        self.assertIn("kehillah_spark_scheme_study_tt", widget)
        self.assertIn("kehillah_is_writing_scheme", read("common/schemes/scheme_types/kehillah_writing_scheme.txt"))
        self.assertIn("kehillah_spark_write = {", read("common/scripted_guis/kehillah_learning_gui.txt"))
        self.assertEqual(cards.count("{"), cards.count("}"))
        # 2026-11-24: historical ambitions list their real requirements.
        spark_loc = read("localization/english/kehillah_writing_spark_generated_l_english.yml")
        self.assertNotIn("A life given to this study", spark_loc)
        self.assertIn(" kehillah_spark_nc_work_rashi_torah_6:0", spark_loc)
        self.assertNotIn("Be a Rabbi", spark_loc)
        self.assertNotIn(" kehillah_spark_bookline_work_rashi_torah:0 \"On first", spark_loc)
        for disc in ("parshanut", "talmudics", "hashkafa"):
            self.assertIn(f" kehillah_spark_path_original_{disc}:0", spark_loc)

    def test_landmarks_are_finish_outcomes_and_names_are_unique(self) -> None:
        effects = read("common/scripted_effects/kehillah_writing_effects.txt")
        generated = read("common/scripted_effects/kehillah_writing_landmark_generated_effects.txt")
        events = read("events/kehillah_writing_events.txt")
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        named = set(re.findall(r"set_variable = \{ name = kehillah_book_named_work value = flag:(work_\w+) \}", generated))
        future = {key for key, work in catalog.items()
                  if not key.startswith("work_authored_") and work.get("year", 0) > 867}
        self.assertEqual(named, future)
        self.assertEqual(len(named), 50)  # 2026-11-25: +14 historical Great Works
        for year, expected in ((867, 50), (1066, 34), (1178, 20)):
            self.assertEqual(sum(catalog[key]["year"] > year for key in named), expected)
        self.assertNotIn("kehillah_book_named_work value", events)
        self.assertIn("kehillah_writing_select_landmark_effect = yes", effects)
        self.assertIn("kehillah_sefer_finish_composition_effect = yes", effects)
        self.assertIn("kehillah_book_complete_effect = yes", effects)
        self.assertIn("limit = { has_variable = kehillah_book_named_work }", effects)
        self.assertIn("kehillah_writing_create_manuscript_effect = yes", effects)
        self.assertRegex(generated, r"flag:systematic_dialogue[^\n]*kehillah_sefer_ambition_kuzari_trigger")
        self.assertRegex(generated, r"flag:systematic_dialogue[^\n]*kehillah_sefer_ambition_moreh_trigger")
        self.assertLess(effects.index("remove_variable = kehillah_sefer_my_latest_work"),
                        effects.index("kehillah_book_complete_effect = yes"))

    def test_landmark_artifacts_use_direct_work_titles(self) -> None:
        effects = read("common/scripted_effects/kehillah_writing_effects.txt")
        identity = read("common/scripted_effects/kehillah_writing_landmark_artifact_generated_effects.txt")
        identity_loc = read("localization/english/kehillah_writing_landmark_artifact_l_english.yml")
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        future = {key for key, work in catalog.items()
                  if not key.startswith("work_authored_") and work.get("year", 0) > 867}
        self.assertIn("kehillah_writing_set_landmark_artifact_identity_effect = yes", effects)
        self.assertNotIn("set_artifact_name = kehillah_writing_manuscript_name", effects)
        for key in future:
            self.assertIn(f"var:kehillah_sefer_my_latest_work ?= flag:{key}", identity)
            self.assertIn(f"set_artifact_description = kehillah_writing_landmark_artifact_desc_{key}", identity)
            self.assertIn(f" kehillah_writing_landmark_artifact_desc_{key}:0", identity_loc)

    def test_ordinary_artifact_and_news_use_the_chosen_form(self) -> None:
        effects = read("common/scripted_effects/kehillah_writing_effects.txt")
        titles = read("common/customizable_localization/kehillah_writing_ordinary_titles_custom_loc.txt")
        artifact_identity = read("common/scripted_effects/kehillah_writing_ordinary_titles_generated_effects.txt")
        news = read("localization/english/kehillah_community_news_l_english.yml")
        events = read("events/kehillah_writing_events.txt")
        forms = set(re.findall(r"kehillah_writing_choose_project_effect = \{ FORM = (\w+) GENRE = \w+ \}", events))
        for form in forms:
            self.assertIn(f"var:kehillah_writing_ordinary_form ?= flag:{form}", titles)
            self.assertIn(f"set_artifact_name = kehillah_writing_ordinary_title_{form}", artifact_identity)
            self.assertIn(f"set_artifact_description = kehillah_writing_ordinary_desc_{form}", artifact_identity)
        self.assertIn("kehillah_writing_set_ordinary_artifact_identity_effect = yes", effects)
        self.assertIn("KehillahWritingOrdinaryTitle", news)

    def test_authored_future_work_is_visible_before_historical_date(self) -> None:
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        future_fixed = {key for key, work in catalog.items()
                        if not work.get("named") and not key.startswith("work_authored_")
                        and work.get("year", 0) > 867}
        available = read("common/scripted_triggers/kehillah_library_generated_triggers.txt")
        dispatch = read("common/scripted_effects/kehillah_library_study_generated_effects.txt")
        titles = read("common/customizable_localization/kehillah_writing_future_titles_custom_loc.txt")
        artifact = read("common/customizable_localization/kehillah_writing_artifact_custom_loc.txt")
        ledger = read("localization/english/kehillah_library_ledger_catalog_l_english.yml")
        catalog_loc = read("localization/english/kehillah_library_catalog_l_english.yml")
        self.assertEqual(len(future_fixed), 40)
        for key in future_fixed:
            self.assertIn(f"has_global_variable = kehillah_wk_{key}_written", available)
            self.assertIn(f"kehillah_sefer_write_named_work_effect = {{ KEY = {key} }}", dispatch)
            self.assertIn(f"KehillahFutureTitle_{key}", titles)
            self.assertIn(f"KehillahFutureComposer_{key}", ledger)
            self.assertIn(f"KehillahFutureComposer_{key}", catalog_loc)
            self.assertIn(f"flag:{key}", artifact)
            self.assertTrue(catalog[key].get("writing_title"))

    def test_landmark_belief_and_commentary_links(self) -> None:
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        selector = read("common/scripted_effects/kehillah_writing_landmark_generated_effects.txt")
        writing_triggers = read("common/scripted_triggers/kehillah_writing_triggers.txt")
        study = read("common/scripted_effects/kehillah_library_study_generated_effects.txt")
        authorship = read("common/scripted_effects/kehillah_sefer_authorship_effects.txt")
        commentary_index = read("common/customizable_localization/kehillah_library_commentary_custom_loc.txt")
        future = {key: work for key, work in catalog.items()
                  if not key.startswith("work_authored_") and work.get("year", 0) > 867}
        for key, work in future.items():
            thesis = work.get("writing_thesis_tenet")
            self.assertEqual(bool(thesis), bool(work.get("argues_for")), key)
            if thesis:
                self.assertIn(thesis, work["argues_for"])
                self.assertIn(f"kehillah_writing_believes_thesis_trigger = {{ TENET = {thesis} }}", selector)
            if work.get("commentary_on"):
                self.assertIn(f"kehillah_sefer_commentary_authority_{key}_effect", study)
                self.assertIn(f"KehillahCommentaryItem_{key}", commentary_index)
        self.assertIn("kehillah_sefer_commentary_authority_$KEY$_effect = yes", authorship)
        belief = writing_triggers.split("kehillah_writing_believes_thesis_trigger = {", 1)[1].split("}", 2)[0]
        self.assertIn("has_personal_tenet = $TENET$", belief)
        self.assertIn("rite_has_tenet = $TENET$", belief)
        self.assertNotIn("knows_tenet", belief)
        self.assertIn("AMOUNT = kehillah_reception_commentary_value", study)
        self.assertEqual(catalog["work_maggid_mishneh"]["commentary_on"], "work_mishneh_torah")
        self.assertIn("KEY = work_mishneh_torah AMOUNT = kehillah_reception_commentary_value", study)

    def test_writing_localization_has_ck3_encoding(self) -> None:
        for path in (ROOT / "localization/english").glob("kehillah_writing*.yml"):
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"), path.name)

    def test_early_thought_has_sources_before_later_forms_open(self) -> None:
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        triggers = read("common/scripted_triggers/kehillah_writing_triggers.txt")
        self.assertEqual(catalog["work_emunot_vedeot"]["year"], 933)
        self.assertEqual(catalog["work_chovot_halevavot"]["year"], 1080)
        for key in ("work_mishnah", "work_philo_allegorical", "work_memar_marqah"):
            self.assertLessEqual(catalog[key]["year"], 867)
        early_dialogue = triggers.split("kehillah_writing_dialogue_trigger = {", 1)[1].split("kehillah_writing_systematic_dialogue_trigger = {", 1)[0]
        self.assertNotIn("work_emunot_vedeot", early_dialogue)
        self.assertNotIn("work_chovot_halevavot", early_dialogue)
        self.assertIn("current_date >= 933.1.1", triggers)
        self.assertIn("current_date >= 1080.1.1", triggers)

    def test_artifact_dispatch_and_recycling_cover_every_authored_slot(self) -> None:
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        slots = {key for key in catalog if key.startswith("work_authored_")}
        artifact = read("common/customizable_localization/kehillah_writing_artifact_custom_loc.txt")
        refs = read("common/scripted_effects/kehillah_writing_artifact_refs_effects.txt")
        recycling = read("common/scripted_effects/kehillah_library_study_generated_effects.txt")
        authored = read("common/scripted_effects/kehillah_sefer_authorship_effects.txt")
        self.assertEqual(slots, set(re.findall(r"var:kehillah_artifact_work \?= flag:(work_authored_\d+)", artifact)))
        self.assertEqual(slots, set(re.findall(r"name = kehillah_wk_(work_authored_\d+)_manuscript", refs)))
        for key in slots:
            self.assertIn(f"kehillah_wk_{key}_manuscript", recycling)
        self.assertIn("remove_global_variable = kehillah_wk_$SLOT$_manuscript", authored)
        self.assertIn("add_to_variable_list = { name = kehillah_mastered_works", authored)


if __name__ == "__main__":
    unittest.main()
