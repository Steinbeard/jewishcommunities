"""Check that catalyst feedback matches the native situation's actual scoring bindings."""

from pathlib import Path
import re
import unittest

from test_kehillah_crisis_intro import block as first_block

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def block(text, key):
    """Select an immediate child, ignoring invocations and nested phase bindings."""
    masked = re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*', lambda match: re.sub(r"[^\n]", " ", match[0]), text)
    for match in re.finditer(r"(?m)^\s*" + re.escape(key) + r"\s*=\s*\{", masked):
        prefix = masked[:match.start()]
        if prefix.count("{") == prefix.count("}"):
            return first_block(text[match.start():], key)
    raise AssertionError(f"Missing immediate child {key}")


class CatalystNotices(unittest.TestCase):
    def test_notice_destinations_and_values_match_native_scoring(self):
        situation = source("common/situation/situations/kehillah_crisis_situation.txt")
        notices = source("common/scripted_effects/kehillah_catalyst_notice_effects.txt")
        phases = block(block(situation, "kehillah_community_crisis"), "phases")
        expected = set()
        for current, targets in (("warning", ("armed", "spared")), ("armed", ("held", "struck"))):
            future = block(block(phases, f"kehillah_crisis_{current}"), "future_phases")
            for target in targets:
                catalysts = block(block(future, f"kehillah_crisis_{target}"), "catalysts")
                for catalyst, points in re.findall(r"(kehillah_\w+_catalyst)\s*=\s*(kehillah_\w+_points_value)", catalysts):
                    expected.add((catalyst, current, target, points))
        actual = set()
        for catalyst in re.findall(r"(?m)^(kehillah_\w+_catalyst)_trigger_effect =", notices):
            dispatch = block(notices, catalyst + "_trigger_effect")
            for current, found, points, target in re.findall(
                r"situation_current_phase = kehillah_crisis_(\w+).*?"
                r"CATALYST = (\w+) POINTS = (\w+) TRACK = (\w+)", dispatch, re.S
            ):
                self.assertEqual(catalyst, found)
                actual.add((catalyst, current, target, points))
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 14)

    def test_one_native_award_and_snapshot_precedes_transition(self):
        effects = source("common/scripted_effects/kehillah_catalyst_notice_effects.txt")
        apply = block(effects, "kehillah_crisis_apply_catalyst_effect")
        self.assertEqual(apply.count("trigger_situation_catalyst ="), 1)
        self.assertLess(apply.index("save_scope_value_as"), apply.index("trigger_situation_catalyst"))
        self.assertLess(apply.index("trigger_situation_catalyst"), apply.index("kehillah_crisis_catalyst_notice_effect"))
        notice = block(effects, "kehillah_crisis_catalyst_notice_effect")
        self.assertNotIn("trigger_situation_catalyst", notice)
        self.assertNotIn("change_variable", notice)
        self.assertIn("is_ai = no", notice)
        self.assertIn("NOT = { has_variable = kehillah_crisis_intro_pending }", notice)
        self.assertIn("scope:kehillah_notice_points > 0", notice)

    def test_event_actions_notify_and_recurring_reports_do_not_duplicate(self):
        effects = source("common/scripted_effects/kehillah_crisis_situation_effects.txt")
        for helper in ("kehillah_crisis_race_add_effect", "kehillah_crisis_armed_race_add_effect"):
            self.assertIn("$CATALYST$_trigger_effect = { NOTICE = yes }", block(effects, helper))
        tick = block(effects, "kehillah_crisis_struck_tick_effect")
        self.assertIn("$CATALYST$_trigger_effect = { NOTICE = no }", tick)
        self.assertIn("var:kehillah_crisis_armed_ticks >= 2", tick)
        monthly = block(effects, "kehillah_crisis_race_monthly_effect")
        self.assertIn("kehillah_crisis_agitator_catalyst_trigger_effect = { NOTICE = no }", monthly)
        self.assertEqual(monthly.count("kehillah_crisis_pressure_toast_effect = yes"), 1)
        report = block(effects, "kehillah_crisis_send_pressure_effect")
        self.assertIn("PROGRESS = month", report)
        self.assertIn("PROGRESS = interval", report)
        self.assertNotIn("kehillah_flavor_toast_effect =", report)

    def test_flavor_preview_is_a_report_not_another_award(self):
        effects = source("common/scripted_effects/kehillah_catalyst_notice_effects.txt")
        report = block(effects, "kehillah_crisis_flavor_catalyst_send_effect")
        self.assertNotIn("trigger_situation_catalyst", report)
        self.assertIn("desc = $KEY$_d$N$", report)
        self.assertIn("title = $KEY$_t$N$", report)
        self.assertIn("desc = kehillah_crisis_catalyst_report_$PROGRESS$", report)
        self.assertIn("msg_kehillah_crisis_catalyst", report)

    def test_revised_prose_identifies_threat_and_active_mobilization(self):
        toasts = source("localization/english/kehillah_crisis_toasts_l_english.yml")
        warning = next(line for line in toasts.splitlines() if "kehillah_crisis_pressure_vizier_d4:" in line)
        self.assertIn("calling for the Jews to be killed", warning)
        self.assertNotIn("GetFirstName", warning)
        granada = source("localization/english/kehillah_granada_l_english.yml")
        scene = next(line for line in granada.splitlines() if "kehillah_granada.0021.desc:" in line)
        self.assertIn("Sanhaja commanders", scene)
        self.assertIn("kehillah_granada_emir.GetTitledFirstName", scene)
        self.assertIn("quarter's defenses", scene)
        self.assertNotIn("They are not ready yet", scene)


if __name__ == "__main__":
    unittest.main(verbosity=2)
