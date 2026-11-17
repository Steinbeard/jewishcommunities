"""Focused source regressions for the leadership prototype; no engine simulation."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')
class LeadershipStyles(unittest.TestCase):
    def test_specialists_win_their_skill_component(self):
        source = read('common/script_values/kehillah_leadership_style_values.txt')
        skills = ['learning', 'stewardship', 'diplomacy']
        styles = ['scholarly', 'commercial', 'political']
        specialists = [[20, 8, 8], [8, 20, 8], [8, 8, 20]]
        matrix = {}
        for skill in skills:
            block = source.split(f'kehillah_leadership_{skill}_weight = {{', 1)[1].split('\n}\n', 1)[0]
            matrix[skill] = [float(v) for v in re.findall(r'\bvalue = ([0-9.]+)', block)]
            self.assertIn('scope:title =', block)
        # Source order is scholarly, political, commercial.
        for expected, index in [(0, 0), (1, 2), (2, 1)]:
            scores = [sum(candidate[k] * matrix[skill][index] for k, skill in enumerate(skills)) for candidate in specialists]
            self.assertEqual(scores.index(max(scores)), expected)
        self.assertEqual([matrix[k][0] for k in skills], [3, 2, 0.5])
    def test_mutation_is_guarded_and_seat_owned(self):
        source = read('common/scripted_effects/kehillah_leadership_style_effects.txt')
        self.assertEqual(source.count('kehillah_leadership_style_available_trigger = yes'), 3)
        self.assertEqual(source.count('name = kehillah_leadership_style_lock value = yes years = 10'), 3)
        self.assertEqual(source.count('primary_title = {\n   set_variable'), 3)
        self.assertEqual(source.count('NOT = { primary_title = { has_variable = kehillah_leadership_style kehillah_leadership_is_'), 3)
        self.assertNotRegex(source, r'add_gold|change_title_holder|change_variable.*kehillah_var_')
    def test_ui_and_ai_use_same_guarded_effects(self):
        gui = read('common/scripted_guis/kehillah_leadership_style_gui.txt')
        ai = read('common/on_action/kehillah_leadership_style_on_actions.txt')
        panel = read('gui/kehillah_leadership_style.gui')
        for style in ['scholarly', 'political', 'commercial']:
            effect = f'kehillah_leadership_choose_{style}_effect = yes'
            self.assertIn(effect, gui)
            self.assertIn(effect, ai)
            self.assertIn(f"kehillah_leadership_choose_{style}').IsValid", panel)
            self.assertIn(f"kehillah_leadership_active_{style}').IsShown", panel)
        self.assertIn('kehillah_leadership_style_available_trigger = yes', ai)
    def test_every_bonus_is_explained_and_connected(self):
        values = read('common/script_values/kehillah_script_values.txt')
        tooltips = read('localization/english/kehillah_breakdown_l_english.yml')
        for pillar in ['greatness', 'stability', 'prosperity']:
            self.assertEqual(values.count(f'add = kehillah_leadership_{pillar}_bonus'), 1)
            self.assertIn(f"Custom('KehillahLeadership{pillar.capitalize()}')", tooltips)
    def test_default_and_localization_scopes(self):
        triggers = read('common/scripted_triggers/kehillah_leadership_style_triggers.txt')
        self.assertIn('NOT = { has_variable = kehillah_leadership_style }', triggers)
        loc = read('localization/english/kehillah_leadership_style_l_english.yml')
        self.assertNotIn('CHARACTER.', loc)
        self.assertIn("ROOT.Title.MakeScope.Var('kehillah_leadership_style_until')", loc)
        self.assertIn('is_imprisoned = no', triggers)
        self.assertIn('is_incapable = no', triggers)
    def test_initial_scholarly_choice_is_not_blocked_by_legacy_fallback(self):
        effects = read('common/scripted_effects/kehillah_leadership_style_effects.txt')
        gui = read('common/scripted_guis/kehillah_leadership_style_gui.txt')
        explicit = 'has_variable = kehillah_leadership_style kehillah_leadership_is_scholarly_trigger = yes'
        self.assertIn(explicit, effects)
        self.assertIn(explicit, gui)
        action = read('common/important_actions/kehillah_leadership_style_actions.txt')
        self.assertIn('NOT = { has_variable = kehillah_leadership_style }', action)
        self.assertIn('view = my_realm data = flag:bookmark_domain', action)
    def test_current_effects_and_selection_are_visible_without_hover(self):
        panel = read('gui/kehillah_leadership_style.gui')
        self.assertIn("Custom('KehillahLeadershipStyleEffects')", panel)
        self.assertNotIn('text = "kehillah_leadership_active"', panel)
        self.assertIn("kehillah_leadership_unselected').IsShown", panel)
        self.assertEqual(panel.count('0.42 }'), 3)
        self.assertEqual(panel.count('enabled = "[Or('), 3)
if __name__ == '__main__':
    unittest.main()
