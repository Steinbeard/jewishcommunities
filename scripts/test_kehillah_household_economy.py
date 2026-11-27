"""Income conservation and cross-system regressions; engine/UI probes remain separate."""
from decimal import Decimal
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def block(text, name):
    start = re.search(r"\b" + re.escape(name) + r"\s*=\s*\{", text).end()
    depth = 1
    end = start
    while depth:
        depth += (text[end] == "{") - (text[end] == "}")
        end += 1
    return text[start:end - 1]


VALUES = read("common/script_values/kehillah_household_economy_values.txt")
EFFECTS = read("common/scripted_effects/kehillah_household_economy_effects.txt")


def arithmetic(name, inputs):
    """Evaluate actual flat arithmetic definitions, not a duplicate economic formula."""
    if name in inputs:
        return Decimal(str(inputs[name]))
    try:
        return Decimal(name)
    except Exception:
        pass
    expression = block(VALUES, name)
    if "{" in expression:
        raise ValueError("Conditional/engine scopes require a runtime probe")
    result = Decimal(0)
    for operator, operand in re.findall(r"(value|add|subtract|multiply|divide|min|max)\s*=\s*([\w:.+-]+)", expression):
        value = arithmetic(operand, inputs)
        if operator == "value": result = value
        elif operator == "add": result += value
        elif operator == "subtract": result -= value
        elif operator == "multiply": result *= value
        elif operator == "divide": result /= value
        elif operator == "min": result = max(result, value)
        elif operator == "max": result = min(result, value)
    return result


class HouseholdEconomyTest(unittest.TestCase):
    def test_income_split_conserves_gross_at_every_score_and_assessment(self):
        for wealth in range(101):
            for assessment in range(3):
                inputs = {"var:kehillah_household_wealth": wealth,
                          "kehillah_household_assessment_value": assessment}
                rate = arithmetic("kehillah_household_assessment_rate_value", inputs)
                inputs["var:kehillah_household_of.kehillah_household_assessment_rate_value"] = rate
                gross = arithmetic("kehillah_household_gross_value", inputs)
                due = arithmetic("kehillah_household_due_quarter_value", inputs)
                retained = arithmetic("kehillah_household_retained_quarter_value", inputs)
                self.assertEqual(due + retained, gross * 3)
                self.assertGreater(retained, 0)
                self.assertGreaterEqual(due, 0)
                self.assertLess(due, retained)

    def test_refresh_cannot_pay_or_advance_time(self):
        refresh = block(EFFECTS, "kehillah_household_economy_refresh_effect")
        self.assertNotIn("add_gold", refresh)
        self.assertNotIn("next_wealth", refresh)
        self.assertNotIn("random_list", refresh)
        self.assertNotIn("monthly_income =", read("common/modifiers/kehillah_household_modifiers.txt"))

    def test_settlement_and_ventures_have_independent_duplicate_guards(self):
        settle = block(EFFECTS, "kehillah_household_economy_quarter_effect")
        venture = block(EFFECTS, "kehillah_household_abstract_ventures_effect")
        self.assertIn("NOT = { has_variable = kehillah_household_paid_recently }", settle)
        self.assertIn("NOT = { has_variable = kehillah_household_ventured_recently }", venture)
        self.assertEqual(settle.count("add_gold ="), 2)
        self.assertNotIn("add_gold", block(EFFECTS, "kehillah_household_native_fortune_effect"))
        self.assertIn("NOT = { has_dlc_feature = silk_and_silver }", venture)
        old = read("common/scripted_effects/kehillah_trade_band_effects.txt")
        self.assertNotIn("add_gold", block(old, "kehillah_trade_venture_pulse_effect"))

    def test_actions_recheck_authority_inside_hidden_event(self):
        events = read("events/kehillah_household_economy_events.txt")
        triggers = read("common/scripted_triggers/kehillah_household_economy_triggers.txt")
        for number in range(10, 14):
            action = block(events, f"kehillah_household_economy.{number}")
            self.assertIn("hidden = yes", action)
            self.assertIn("kehillah_household_can_manage_trigger = yes", action)
            self.assertIn("kehillah_household_assignment_cooldown", action)
        self.assertIn("var:kehillah_household_of = root.primary_title", triggers)
        self.assertIn("is_courtier_of", triggers)
        self.assertIn("NOT = { has_variable = kehillah_household_ruling }", triggers)

    def test_wealth_stays_on_house_and_assignments_reset_on_migration(self):
        initialize = block(EFFECTS, "kehillah_household_economy_initialize_effect")
        self.assertIn("NOT = { has_variable = kehillah_household_wealth }", initialize)
        self.assertIn("var:kehillah_household_business_seat ?= scope:kh_ref_title", initialize)
        self.assertIn("name = kehillah_household_assignment value = 0", initialize)
        self.assertNotIn("head.gold", VALUES)
        target = block(VALUES, "kehillah_household_target_value")
        self.assertNotIn("kehillah_var_prosperity", target)

    def test_existing_rewards_are_replaced_not_stacked(self):
        council = read("common/scripted_effects/kehillah_council_task_effects.txt")
        fair = block(council, "kehillah_council_moment_roll_prosperity_effect")
        self.assertIn("kehillah_household_fair_success_effect", fair)
        self.assertNotIn("kehillah_council_moment_set_effect", fair)
        loans = read("common/scripted_effects/kehillah_community_loan_effects.txt")
        repayment = block(loans, "kehillah_community_loan_repaid_effect")
        self.assertIn("kehillah_household_credit_repaid_effect", repayment)
        self.assertNotIn("PILLAR = prosperity", repayment)

    def test_income_updates_precede_pillar_recomputation(self):
        pulse = read("common/on_action/kehillah_on_actions.txt")
        settlement = pulse.index("kehillah_household_economy_quarter_effect = yes")
        self.assertLess(settlement, pulse.index("kehillah_quarterly_pillars_effect = yes", settlement))
        self.assertEqual(pulse.count("kehillah_household_economy_quarter_effect = yes"), 1)

    def test_panel_and_lending_use_existing_systems(self):
        domicile = read("gui/window_domicile.gui")
        self.assertIn("kehillah_household_economy_body", domicile)
        self.assertIn("DomicileBuilding.HasParameter('kehillah_household_management')", domicile)
        self.assertIn("kehillah_economy_view", read("gui/window_my_realm.gui"))
        self.assertIn("add = kehillah_household_credit_terms_rate_value", read("common/script_values/kehillah_banking_values.txt"))
        self.assertNotIn("create_title", EFFECTS)
        self.assertNotIn("set_government", EFFECTS)


if __name__ == "__main__":
    unittest.main()
