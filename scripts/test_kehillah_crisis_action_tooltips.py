"""Style contracts for crisis action tooltips (Daniel, 2026-11-06).

Run: python scripts/test_kehillah_crisis_action_tooltips.py
Sizes are hand-written because the outcomes sit in a later scene, so this checks the prose
limits and the size each push should show against the point values in the measure effects.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOC = ROOT / "localization/english"
KEY = re.compile(r'^ ((?:kehillah_crisis_phase_actions|kehillah_crisis_recommend)\.\d+(?:\.\w+)*\.(?:tt|flavor)):0 "(.*)"\s*$', re.M)
EFFECTS = ROOT / "common/scripted_effects/kehillah_crisis_phase_measure_effects.txt"
MEASURE_KEYS = {
    "aid": "0001", "mediate": "0001", "lord": "0002", "scholars": "0002", "overlord": "0002",
    "evidence": "0003", "neighbors": "0003", "refuge": "0004", "patrol": "0004", "escort": "0004",
    "guards": "0005", "retreat": "0005", "terms": "0006", "delay": "0006", "divide": "0006",
    "obligations": "0006",
}


def tooltips():
    found = {}
    for path in LOC.glob("kehillah_crisis*_l_english.yml"):
        found.update(KEY.findall(path.read_text(encoding="utf-8-sig")))
    return found


def size(points):
    return "small" if points <= 8 else "moderate" if points <= 14 else "large"


def effect_points(block):
    points = {}
    for line in block.splitlines():
        match = re.search(r"kehillah_crisis_measure \?= flag:(\w+) \}", line)
        pushed = re.search(r"POINTS = (\d+)", line)
        if match and pushed:
            points[match.group(1)] = int(pushed.group(1))
    return points


class CrisisActionTooltips(unittest.TestCase):
    def test_tooltips_stay_short_and_free_of_numbers_and_scene_narration(self):
        # An option's flavor and effect lines are separate keys, read as one tooltip.
        options = {}
        for key, text in tooltips().items():
            option = re.sub(r"\.(?:fail\.tt|last\.tt|odds\.tt|tt|flavor)$", "", key)
            options.setdefault(option, []).append(text)
        self.assertGreaterEqual(len(options), 31)
        for option, parts in options.items():
            with self.subTest(option=option):
                plain = re.sub(r"\[[^\]]*\]|\$[^$]*\$|#[A-Za-z]+ |#!", "", " ".join(parts))
                self.assertNotIn("next scene", plain.lower())
                self.assertNotRegex(plain, r"\d")
                self.assertLessEqual(len(plain), 170)

    def test_option_flavor_is_not_an_effect_line(self):
        # Vanilla keeps flavor apart from effects; a blank line inside a tooltip reads as a mistake.
        for key, tip in tooltips().items():
            with self.subTest(key=key):
                self.assertNotIn("\\n", tip)

    def test_measure_tooltips_show_the_size_of_their_real_pushes(self):
        text = EFFECTS.read_text(encoding="utf-8-sig")
        success, failure = text.split("kehillah_crisis_phase_failure_effect = {")
        wins, losses = effect_points(success), effect_points(failure)
        found = tooltips()
        for measure, event in MEASURE_KEYS.items():
            tip = found[f"kehillah_crisis_phase_actions.{event}.{measure}.tt"]
            with self.subTest(measure=measure):
                won = re.search(r"#P Success:#! \$kehillah_crisis_tt_\w+?_(small|moderate|large)\$", tip)
                self.assertEqual(won.group(1), size(wins[measure]))
                if measure in losses:
                    fail = found[f"kehillah_crisis_phase_actions.{event}.{measure}.fail.tt"]
                    lost = re.search(r"#N Failure:#! \$kehillah_crisis_tt_\w+?_(small|moderate|large)\$", fail)
                    self.assertEqual(lost.group(1), size(losses[measure]))

    def test_tooltips_do_not_read_root_which_is_empty_in_an_option_tooltip(self):
        # CK3 logged a data error and printed blanks for ROOT here (live, 2026-11-06).
        for key, tip in tooltips().items():
            with self.subTest(key=key):
                self.assertNotIn("[ROOT.", tip)

    def test_granada_opening_keeps_its_pushes_out_of_the_preview(self):
        # A preview never sets the points variable, so a visible push shows the default size.
        events = (ROOT / "events/kehillah_granada_events.txt").read_text(encoding="utf-8-sig")
        effects = events[:events.index("namespace = kehillah_granada")]
        visible = re.sub(r"hidden_effect = \{.*?\n\t+\}\r?\n", "", effects, flags=re.S)
        self.assertEqual(effects.count("kehillah_crisis_race_add_effect"), 5)
        self.assertNotIn("kehillah_crisis_race_add_effect", visible)

    def test_crisis_action_pushes_stay_out_of_the_preview(self):
        for name in ("recommendation", "phase_measure"):
            text = (ROOT / f"common/scripted_effects/kehillah_crisis_{name}_effects.txt").read_text(encoding="utf-8-sig")
            bare = re.sub(r"hidden_effect = \{ kehillah_crisis_(armed_)?race_add_effect = \{[^}]*\} \}", "", text)
            self.assertNotRegex(bare, r"kehillah_crisis_(armed_)?race_add_effect = \{ CATALYST")


    def test_rolled_outcomes_report_their_result(self):
        # An unseen roll left the player not knowing what had happened (Daniel, 2026-11-06).
        events = (ROOT / "events/kehillah_granada_events.txt").read_text(encoding="utf-8-sig")
        effects = events[:events.index("namespace = kehillah_granada")]
        self.assertEqual(effects.count("send_interface_toast"), 5)
        measures = (ROOT / "common/scripted_effects/kehillah_crisis_phase_measure_effects.txt").read_text(encoding="utf-8-sig")
        self.assertEqual(measures.count("send_interface_toast"), 32)
        loc = (LOC / "kehillah_crisis_toast_l_english.yml").read_text(encoding="utf-8-sig")
        for title in re.findall(r"title = (kehillah_crisis_toast_\w+)", measures):
            self.assertIn(f" {title}:0 ", loc)


    def test_warning_events_report_every_roll(self):
        events = (ROOT / "events/kehillah_crisis_events.txt").read_text(encoding="utf-8-sig")
        rolls = len(re.findall(r"^\s*\d+ = \{\s*$", events, re.M))
        self.assertEqual(events.count("send_interface_toast"), rolls)

    def test_warning_pressure_stays_out_of_the_preview(self):
        effects = (ROOT / "common/scripted_effects/kehillah_crisis_effects.txt").read_text(encoding="utf-8-sig")
        pressure = effects[effects.index("kehillah_crisis_agitation_pressure_effect = {"):effects.index("kehillah_crisis_development_effect = {")]
        self.assertIn("hidden_effect = { kehillah_crisis_race_add_effect", pressure)
        self.assertIn("custom_tooltip = kehillah_crisis_tt_armed_small", pressure)


if __name__ == "__main__":
    unittest.main(verbosity=2)
