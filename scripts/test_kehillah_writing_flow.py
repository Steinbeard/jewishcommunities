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
        events = read("events/kehillah_writing_events.txt")
        triggers = read("common/scripted_triggers/kehillah_writing_triggers.txt")
        loc = read("localization/english/kehillah_writing_l_english.yml")
        forms = re.findall(r"kehillah_writing_choose_project_effect = \{ FORM = (\w+) GENRE = (\w+) \}", events)
        self.assertEqual(len(forms), 14)
        self.assertEqual(len({form for form, _ in forms}), 14)
        for form, _ in forms:
            self.assertIn(f"kehillah_writing_{form}_trigger = {{", triggers)
            self.assertIn(f"kehillah_writing_{form}_near_trigger = {{", triggers)
            self.assertIn(f"kehillah_writing_{form}_trigger = yes", events)
            self.assertIn(f"show_as_unavailable = {{ kehillah_writing_{form}_near_trigger = yes }}", events)
            self.assertIn(f" kehillah_writing.{form}.gate:0", loc)

    def test_landmarks_are_finish_outcomes_and_names_are_unique(self) -> None:
        effects = read("common/scripted_effects/kehillah_writing_effects.txt")
        events = read("events/kehillah_writing_events.txt")
        catalog = json.loads(read("scripts/kehillah_library_catalog.json"))["works"]
        named = set(re.findall(r"set_variable = \{ name = kehillah_book_named_work value = flag:(work_\w+) \}", effects))
        self.assertEqual(len(named), 10)
        self.assertTrue(named <= catalog.keys())
        self.assertNotIn("kehillah_book_named_work value", events)
        self.assertIn("kehillah_writing_select_landmark_effect = yes", effects)
        self.assertIn("kehillah_sefer_finish_composition_effect = yes", effects)
        self.assertNotIn("kehillah_book_complete_effect = yes", effects)

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
