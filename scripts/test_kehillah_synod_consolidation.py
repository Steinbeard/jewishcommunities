"""Regression checks at synod scope, save-payload and UI integration boundaries.

These are source checks, not a substitute for the engine probe or a rendered UI test.
"""
import re
import unittest
from test_kehillah_faith_revision import source, parse, child
from kehillah_holiday_revision_build import block


def walk(tree):
    for key, op, value in tree:
        yield key, op, value
        if isinstance(value, list):
            yield from walk(value)


class SynodConsolidation(unittest.TestCase):
    def test_small_agenda_cannot_reach_retired_menus(self):
        text = source('events/kehillah_synod_events.txt')
        agenda = child(parse(block(text, 'kehillah_synod.0100')), 'kehillah_synod.0100')
        options = [value for key, _, value in agenda if key == 'option']
        self.assertEqual(len(options), 4)  # three kinds and the free exit
        self.assertEqual({v for key, _, v in walk(agenda) if key == 'trigger_event'},
                         {'kehillah_reform.0001', 'kehillah_synod.0109', 'kehillah_synod.0110'})
        for number in ('0105', '0106', '0107'):
            old = block(text, 'kehillah_synod.' + number)
            self.assertIn('hidden = yes', old)
            self.assertNotIn('kehillah_synod_put_motion_effect', old)

    def test_picker_is_native_known_data_and_has_bounded_pages(self):
        text = source('common/scripted_effects/kehillah_reform_effects.txt')
        picker = block(text, 'kehillah_reform_pick_pressing_effect')
        self.assertIn('ordered_character_tenet', picker)
        self.assertIn('knowledge_filter = known', picker)
        self.assertIn('max = 3', picker)
        self.assertIn('is_target_in_variable_list', picker)
        self.assertIn('add_to_variable_list', picker)
        # Catalogue compatibility is allowed in a separate bridge, never in enumeration.
        self.assertNotRegex(picker, r'tenet:tenet_\w+')
        events = source('events/kehillah_reform_events.txt')
        page = child(parse(block(events, 'kehillah_reform.0001')), 'kehillah_reform.0001')
        self.assertEqual(sum(key == 'option' for key, _, _ in page), 5)
        self.assertIn('ordered_rite_tenet', block(events, 'kehillah_reform.0003'))

    def test_faith_scope_actions_require_sanhedrin_but_core_does_not(self):
        text = source('common/scripted_triggers/kehillah_reform_triggers.txt')
        for action in ('permit', 'ban', 'lift'):
            self.assertIn('kehillah_is_sanhedrin_head_trigger = yes', block(text, f'kehillah_reform_can_{action}_trigger'))
        core = block(text, 'kehillah_reform_can_core_trigger')
        self.assertNotIn('kehillah_is_sanhedrin_head_trigger', core)
        self.assertIn('knows_tenet = $TENET$', core)
        self.assertIn('rite_can_choose_tenet', core)
        self.assertIn('kehillah_temple_service_available_trigger', core)
        self.assertIn('has_character_flag = kehillah_prophetic_calling', core)

    def test_complete_payload_survives_activity_teardown(self):
        put = block(source('common/scripted_effects/kehillah_reform_effects.txt'), 'kehillah_reform_put_motion_effect')
        close = block(source('common/scripted_effects/kehillah_synod_effects.txt'), 'kehillah_synod_prepare_closing_ruling_effect')
        for name in ('topic', 'rite', 'action', 'replacement'):
            self.assertIn('name = kehillah_reform_' + name, put)
            self.assertIn('scope:activity.var:kehillah_reform_' + name, close)
        self.assertNotIn('involved_activity', close)
        ruling = block(source('events/kehillah_synod_events.txt'), 'kehillah_synod.0103')
        self.assertNotIn('exists = involved_activity', ruling)

    def test_stale_core_vote_cannot_remove_a_tenet(self):
        effect = block(source('common/scripted_effects/kehillah_reform_effects.txt'), 'kehillah_reform_enact_effect')
        data = child(parse(effect), 'kehillah_reform_enact_effect')
        branch = child(data, 'if')
        self.assertIn(('kehillah_reform_choice_valid_trigger', '=', 'yes'), child(branch, 'limit'))
        self.assertNotIn('remove_rite_tenet', {k for k, _, _ in walk(child(data, 'else'))})
        trigger = block(source('common/scripted_triggers/kehillah_reform_triggers.txt'), 'kehillah_reform_choice_valid_trigger')
        self.assertIn('rite ?= var:kehillah_reform_rite', trigger)
        self.assertIn('kehillah_reform_pair_valid_trigger', trigger)
        # Macro parameters must remain tenet objects after entering rite/tenet scopes.
        self.assertIn('NEW = scope:kehillah_reform_chosen_topic DROP = scope:kehillah_reform_chosen_drop', trigger)
        for action in ('core', 'permit', 'ban', 'lift'):
            chosen = block(source('common/scripted_triggers/kehillah_reform_triggers.txt'), f'kehillah_reform_chosen_can_{action}_trigger')
            self.assertIn('TENET = scope:kehillah_reform_chosen_topic', chosen)
            self.assertNotIn('TENET = var:', chosen)

    def test_practice_and_headship_are_bounded_real_choices(self):
        text = source('events/kehillah_synod_events.txt')
        for event in ('0108', '0109'):
            tree = child(parse(block(text, 'kehillah_synod.' + event)), 'kehillah_synod.' + event)
            self.assertEqual(sum(k == 'option' for k, _, _ in tree), 4)
        self.assertIn('primary_title = { add = kehillah_head_of_rite_title_score_value }', block(text, 'kehillah_synod.0108'))
        practice = block(text, 'kehillah_synod.0109')
        self.assertNotIn('doctrine_divorce_approval', practice)
        self.assertNotIn('doctrine_funeral_', practice)
        self.assertIn('name = kehillah_synod_proposal_rite', practice)
        self.assertIn('name = kehillah_synod_previous_doctrine', practice)

    def test_native_names_replace_stale_literal_tenet_labels(self):
        text = source('localization/english/kehillah_reform_l_english.yml')
        for i in range(1, 4):
            self.assertIn(f'kehillah_reform_pick_{i}.GetName( ROOT.Char.GetRite )', text)
            self.assertIn(f'kehillah_reform_drop_{i}.GetName( ROOT.Char.GetRite )', text)
        self.assertNotIn('$EFFECT_LIST_BULLET$', text)
        self.assertNotIn('active debate', text.lower())

    def test_each_delegate_vote_is_named_and_recorded_once(self):
        effects = source('common/scripted_effects/kehillah_synod_vote_effects.txt')
        record = block(effects, 'kehillah_synod_record_vote_effect')
        self.assertIn('name = kehillah_synod_voted target = root', record)
        self.assertIn('name = kehillah_synod_voted_$SIDE$ target = scope:kehillah_synod_voter', record)
        self.assertIn('key = kehillah_synod_vote_$SIDE$_log', record)
        self.assertIn('show_in_conclusion = yes', record)
        self.assertIn('left_icon = scope:kehillah_synod_voter', record)
        vote = block(source('events/kehillah_synod_events.txt'), 'kehillah_synod.0102')
        self.assertEqual(vote.count('kehillah_synod_record_vote_effect'), 2)
        self.assertNotIn('change_variable = { name = kehillah_synod_votes_', vote)

    def test_resolution_applies_before_display_and_acknowledgement_does_not_grant(self):
        event = child(parse(block(source('events/kehillah_synod_events.txt'), 'kehillah_synod.0103')), 'kehillah_synod.0103')
        self.assertIn('kehillah_synod_enact_takkanah_effect', {k for k, _, _ in walk(child(event, 'immediate'))})
        self.assertNotIn('kehillah_synod_enact_takkanah_effect', {k for k, _, _ in walk(child(event, 'option'))})
        self.assertIn('kehillah_synod_rollcall_tooltip_effect', {k for k, _, _ in walk(child(event, 'option'))})
        effects = source('common/scripted_effects/kehillah_synod_effects.txt')
        head = effects[effects.index('limit = { scope:kehillah_synod_takkanah = flag:head_of_rite }'):]
        head = head[:head.index('# 2026-11-25 dynamic agenda: common undertakings')]
        check = 'has_title = title:d_kehillah_gaonate exists = rite.head_of_rite rite.head_of_rite = this'
        self.assertLess(head.index('kehillah_gaonate_grant_effect'), head.index(check))
        self.assertLess(head.index(check), head.index('name = kehillah_synod_applied value = yes'))

    def test_rollcall_survives_activity_teardown_with_uncast_separate(self):
        close = block(source('common/scripted_effects/kehillah_synod_effects.txt'), 'kehillah_synod_prepare_closing_ruling_effect')
        for side in ('for', 'against', 'uncast'):
            self.assertIn('name = kehillah_synod_result_' + side, close)
            self.assertIn('name = kehillah_synod_roll_' + side, close)
        self.assertIn('variable = kehillah_synod_electorate', close)
        loc = source('localization/english/kehillah_synod_votes_l_english.yml')
        self.assertIn('kehillah_synod_result_head_unconfirmed', loc)
        self.assertIn('kehillah_synod_result_head_appointed', loc)
        self.assertIn('Not cast:', loc)


if __name__ == '__main__':
    unittest.main()
