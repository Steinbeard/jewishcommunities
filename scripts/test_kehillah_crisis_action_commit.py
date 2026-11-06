"""Source contracts for choosing a crisis action (Daniel, 2026-11-06).

Run: python scripts/test_kehillah_crisis_action_commit.py
An option in a category scene is only considered. The final choice commits the category, and
every scene behind that menu can go back. These tests do not emulate CK3.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "kehillah_crisis_commit_action_effect = yes"
BACK = "kehillah_crisis_return_to_options_effect = yes"


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def events(text):
    found = {}
    for match in re.finditer(r"(?m)^(kehillah_[\w.]+) = \{\n(.*?)^\}", text, re.S):
        found[match.group(1)] = match.group(2)
    return found


class CrisisActionCommit(unittest.TestCase):
    def test_category_scenes_spend_nothing_when_an_option_is_clicked(self):
        scenes = source("events/kehillah_crisis_phase_action_events.txt")
        for spent in ("kehillah_crisis_used_", "kehillah_crisis_story_", "name = kehillah_crisis_answered", "name = kehillah_crisis_pleaded"):
            self.assertNotIn(spent, scenes.replace("NOT = { has_variable = kehillah_crisis_used_", ""))
        self.assertEqual(scenes.count("kehillah_crisis_consider_action_effect"), 24)

    def test_every_measure_scene_commits_on_a_choice_and_can_go_back(self):
        scenes = events(source("events/kehillah_crisis_phase_measure_events.txt"))
        self.assertEqual(len(scenes), 6)
        for key, body in scenes.items():
            with self.subTest(event=key):
                self.assertEqual(body.count(COMMIT), 2)
                self.assertEqual(body.count(BACK), 1)

    def test_every_confirmation_commits_and_can_go_back(self):
        scenes = events(source("events/kehillah_crisis_recommendation_action_events.txt"))
        self.assertEqual(len(scenes), 7)
        for key, body in scenes.items():
            with self.subTest(event=key):
                self.assertLess(body.index(COMMIT), body.index("_effect = yes\n }\n option"))
                self.assertEqual(body.count(BACK), 1)

    def test_both_duels_commit_and_offer_back_only_from_a_category(self):
        scenes = events(source("events/kehillah_crisis_race_events.txt"))
        for key in ("kehillah_crisis_race.0100", "kehillah_crisis_race.0200"):
            with self.subTest(event=key):
                self.assertEqual(scenes[key].count(COMMIT), 2)
                self.assertEqual(scenes[key].count(BACK), 1)
                self.assertIn("trigger = { primary_title = { has_variable = kehillah_crisis_pending_category } }", scenes[key])

    def test_commit_covers_every_category_and_back_reopens_it(self):
        effects = source("common/scripted_effects/kehillah_crisis_phase_measure_effects.txt")
        self.assertNotIn("﻿", effects)
        for event, category in enumerate(("steady", "restraint", "case", "armed_protect", "armed_defend", "armed_parley"), 1):
            with self.subTest(category=category):
                self.assertIn(f"name = kehillah_crisis_used_{category} value = yes", effects)
                self.assertIn(f"name = kehillah_crisis_story_{category} value = var:kehillah_crisis_pending_story", effects)
                self.assertIn(f"flag:{category} }} kehillah_crisis_clear_considered_action_effect = yes trigger_event = kehillah_crisis_phase_actions.000{event}", effects)


if __name__ == "__main__":
    unittest.main(verbosity=2)
