"""Add an auditable roll call and enact-before-result synod resolution.

Run after kehillah_synod_agenda_build.py. Preserves the existing vote weights.
"""
import re
from kehillah_synod_agenda_build import read, write, replace_block


def build():
    path = 'events/kehillah_synod_events.txt'
    text = read(path)
    for side, counter in (('for', 'for'), ('against', 'against')):
        old = f'involved_activity ?= {{ change_variable = {{ name = kehillah_synod_votes_{counter} add = 1 }} }}'
        text = text.replace(old, f'kehillah_synod_record_vote_effect = {{ SIDE = {side} }}')
    # A delegate can vote once. The host's supporting vote is explicit and already recorded.
    vote = re.search(r'(?ms)^kehillah_synod\.0102 = \{.*?^\}', text)[0]
    guard = '''
        NOT = { involved_activity = { is_target_in_variable_list = { name = kehillah_synod_voted target = root } } }
'''
    if 'name = kehillah_synod_voted target = root' not in vote:
        vote = vote.replace('involved_activity = { has_variable = kehillah_synod_takkanah }', 'involved_activity = { has_variable = kehillah_synod_takkanah }' + guard, 1)
        text = re.sub(r'(?ms)^kehillah_synod\.0102 = \{.*?^\}', lambda _: vote, text, count=1)
    # Save who was actually asked to vote, so missing votes are not described as opposition.
    old = 'trigger_event = { id = kehillah_synod.0102 days = kehillah_synod_vote_delay_days }'
    new = 'involved_activity = { add_to_variable_list = { name = kehillah_synod_electorate target = prev } }\n\t\t\t\t\t' + old
    if new not in text:
        text = text.replace(old, new, 1)
    text = replace_block(text, 'kehillah_synod.0103', r'''
    type = character_event
    title = kehillah_synod.0103.t
    desc = {
        first_valid = {
            triggered_desc = { trigger = { scope:kehillah_synod_outcome = flag:no_quorum } desc = kehillah_synod.0103.desc.no_quorum }
            triggered_desc = { trigger = { scope:kehillah_synod_outcome = flag:failed } desc = kehillah_synod.0103.desc.failed }
            triggered_desc = {
                trigger = { scope:kehillah_synod_takkanah = flag:head_of_rite scope:kehillah_synod_applied ?= yes }
                desc = kehillah_synod_result_head_appointed
            }
            triggered_desc = {
                trigger = { scope:kehillah_synod_takkanah = flag:head_of_rite scope:kehillah_synod_nominee ?= { has_title = title:d_kehillah_gaonate exists = rite.head_of_rite rite.head_of_rite = this } }
                desc = kehillah_synod_result_head_already
            }
            triggered_desc = {
                trigger = { scope:kehillah_synod_takkanah = flag:head_of_rite scope:kehillah_synod_nominee ?= { has_title = title:d_kehillah_gaonate } }
                desc = kehillah_synod_result_head_unconfirmed
            }
            triggered_desc = { trigger = { scope:kehillah_synod_applied ?= yes } desc = kehillah_synod_result_enacted }
            desc = kehillah_synod_result_lapsed
        }
        desc = kehillah_synod_result_tally
    }
    theme = faith
    left_portrait = { character = root animation = personality_bold }
    right_portrait = { trigger = { exists = scope:kehillah_synod_nominee } character = scope:kehillah_synod_nominee animation = personality_bold }
    trigger = { exists = scope:kehillah_synod_outcome }
    # Apply first. The popup describes the actual result, not an unexecuted promise.
    immediate = {
        if = {
            limit = { scope:kehillah_synod_outcome = flag:passed }
            kehillah_synod_enact_takkanah_effect = yes
        }
        else_if = {
            limit = { scope:kehillah_synod_outcome = flag:failed }
            kehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_failed_greatness }
        }
    }
    option = {
        name = kehillah_synod.0103.a
        custom_tooltip = kehillah_synod_result_recorded_tt
        kehillah_synod_rollcall_tooltip_effect = yes
    }
    after = {
        if = {
            limit = { scope:kehillah_synod_applied ?= yes }
            kehillah_notify_rite_players_effect = { TYPE = msg_kehillah_community_news TITLE = kehillah_news_synod_t DESC = kehillah_news_synod_passed_d }
        }
    }
''')
    write(path, text)

    path = 'common/scripted_effects/kehillah_synod_effects.txt'
    text = read(path)
    seed = '''
        clear_variable_list = kehillah_synod_voted
        clear_variable_list = kehillah_synod_voted_for
        clear_variable_list = kehillah_synod_voted_against
        clear_variable_list = kehillah_synod_electorate
        add_to_variable_list = { name = kehillah_synod_voted target = root }
        add_to_variable_list = { name = kehillah_synod_voted_for target = root }
        add_to_variable_list = { name = kehillah_synod_electorate target = root }
'''
    opening = re.search(r'(?ms)^kehillah_synod_open_session_effect = \{.*?^\}', text)[0]
    if 'clear_variable_list = kehillah_synod_voted' not in opening:
        updated = opening.replace('scope:activity = {', 'scope:activity = {' + seed, 1)
        text = text.replace(opening, updated, 1)
    # Capture the full roll call while the activity object still exists.
    snapshot = '''
    set_variable = { name = kehillah_synod_result_for value = scope:activity.var:kehillah_synod_votes_for }
    set_variable = { name = kehillah_synod_result_against value = scope:activity.var:kehillah_synod_votes_against }
    set_variable = { name = kehillah_synod_result_uncast value = 0 }
    clear_variable_list = kehillah_synod_roll_for
    clear_variable_list = kehillah_synod_roll_against
    clear_variable_list = kehillah_synod_roll_uncast
    scope:activity = {
        every_in_list = {
            variable = kehillah_synod_voted_for
            root = { add_to_variable_list = { name = kehillah_synod_roll_for target = prev } }
        }
        every_in_list = {
            variable = kehillah_synod_voted_against
            root = { add_to_variable_list = { name = kehillah_synod_roll_against target = prev } }
        }
        every_in_list = {
            variable = kehillah_synod_electorate
            limit = { NOT = { scope:activity = { is_target_in_variable_list = { name = kehillah_synod_voted target = prev } } } }
            root = {
                add_to_variable_list = { name = kehillah_synod_roll_uncast target = prev }
                change_variable = { name = kehillah_synod_result_uncast add = 1 }
            }
        }
    }
'''
    marker = '\tdebug_log = "KEHILLAH_SYNOD: closing ruling captured"'
    if 'name = kehillah_synod_result_for' not in text:
        text = text.replace(marker, snapshot + marker, 1)
    # Confirm both actual title ownership and native head-of-rite recognition.
    head_old = '''\t\t\tscope:kehillah_synod_nominee = {
\t\t\t\tcustom_tooltip = kehillah_synod_head_named_tt
\t\t\t\tsave_scope_value_as = { name = kehillah_synod_applied value = yes }
\t\t\t\thidden_effect = { kehillah_gaonate_grant_effect = yes }
\t\t\t}
\t\t\tkehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_passed_greatness }'''
    head_new = r'''
            scope:kehillah_synod_nominee = {
                hidden_effect = { kehillah_gaonate_grant_effect = yes }
                if = {
                    limit = { has_title = title:d_kehillah_gaonate exists = rite.head_of_rite rite.head_of_rite = this }
                    save_scope_value_as = { name = kehillah_synod_applied value = yes }
                    custom_tooltip = kehillah_synod_head_named_tt
                    debug_log = "KEHILLAH_SYNOD: title and engine headship confirmed"
                }
                else = { custom_tooltip = kehillah_synod_head_unconfirmed_tt debug_log = "KEHILLAH_SYNOD: headship grant not confirmed" }
            }
            if = {
                limit = { scope:kehillah_synod_applied ?= yes }
                kehillah_change_pillar_effect = { PILLAR = greatness AMOUNT = kehillah_synod_passed_greatness }
            }'''
    text = text.replace(head_old, head_new, 1)
    text = text.replace('has_title = title:d_kehillah_gaonate rite.head_of_rite ?= this',
                        'has_title = title:d_kehillah_gaonate exists = rite.head_of_rite rite.head_of_rite = this')
    # The sponsor's already-counted supporting vote also belongs in the activity log.
    sponsor = 'involved_activity ?= { set_variable = { name = kehillah_synod_takkanah value = $MOTION$ } }'
    text = text.replace(sponsor, '''involved_activity ?= {
        set_variable = { name = kehillah_synod_takkanah value = $MOTION$ }
        add_activity_log_entry = { key = kehillah_synod_vote_for_log character = root tags = { completed } show_in_conclusion = yes }
    }''')
    write(path, text)

    effects = '''# Vote ledger; called by a delegate in the actual vote option.\n'''
    effects += r'''
kehillah_synod_record_vote_effect = {
    if = {
        limit = {
            exists = involved_activity
            NOT = { involved_activity = { is_target_in_variable_list = { name = kehillah_synod_voted target = root } } }
        }
        save_scope_as = kehillah_synod_voter
        involved_activity = {
            change_variable = { name = kehillah_synod_votes_$SIDE$ add = 1 }
            add_to_variable_list = { name = kehillah_synod_voted target = scope:kehillah_synod_voter }
            add_to_variable_list = { name = kehillah_synod_voted_$SIDE$ target = scope:kehillah_synod_voter }
            add_activity_log_entry = {
                key = kehillah_synod_vote_$SIDE$_log
                character = scope:kehillah_synod_voter
                tags = { completed }
                show_in_conclusion = yes
            }
            activity_host = {
                if = {
                    limit = { is_ai = no }
                    send_interface_toast = { type = event_toast_text_and_effect_neutral title = kehillah_synod_vote_$SIDE$_toast left_icon = scope:kehillah_synod_voter }
                }
            }
        }
    }
}
kehillah_synod_rollcall_tooltip_effect = {
    custom_tooltip = kehillah_synod_roll_for_header
    every_in_list = { variable = kehillah_synod_roll_for save_scope_as = kehillah_synod_voter custom_tooltip = kehillah_synod_roll_name }
    custom_tooltip = kehillah_synod_roll_against_header
    every_in_list = { variable = kehillah_synod_roll_against save_scope_as = kehillah_synod_voter custom_tooltip = kehillah_synod_roll_name }
    custom_tooltip = kehillah_synod_roll_uncast_header
    every_in_list = { variable = kehillah_synod_roll_uncast save_scope_as = kehillah_synod_voter custom_tooltip = kehillah_synod_roll_name }
}
'''
    write('common/scripted_effects/kehillah_synod_vote_effects.txt', effects)
    loc = {
        'kehillah_synod_vote_for_log': '[CHARACTER.GetTitledFirstName] voted for the synod’s proposal.',
        'kehillah_synod_vote_against_log': '[CHARACTER.GetTitledFirstName] voted against the synod’s proposal.',
        'kehillah_synod_vote_for_log_title': 'A Vote in Favour',
        'kehillah_synod_vote_against_log_title': 'A Vote Against',
        'kehillah_synod_vote_for_toast': '[kehillah_synod_voter.GetTitledFirstName] votes for the proposal',
        'kehillah_synod_vote_against_toast': '[kehillah_synod_voter.GetTitledFirstName] votes against the proposal',
        'kehillah_synod_result_head_appointed': 'The motion carried. [kehillah_synod_nominee.GetTitledFirstName] has received the Gaonate and is now recognised as head of the rite. The appointment is already in effect. Open the rite’s page to see its Head of Rite; this is distinct from the faith’s religious head.',
        'kehillah_synod_result_head_unconfirmed': 'The motion carried and [kehillah_synod_nominee.GetTitledFirstName] holds the Gaonate, but the game has not registered the nominee as head of the rite. The appointment could not be confirmed.',
        'kehillah_synod_result_head_already': 'The motion carried. [kehillah_synod_nominee.GetTitledFirstName] already holds the Gaonate and is recognised as head of the rite, so no new appointment was needed.',
        'kehillah_synod_result_enacted': 'The motion carried and the ruling is already in effect.',
        'kehillah_synod_result_lapsed': 'The motion carried, but the proposal no longer met its requirements when the sitting closed. It was not enacted.',
        'kehillah_synod_result_tally': '\\n\\nFor: [ROOT.Char.MakeScope.Var(\'kehillah_synod_result_for\').GetValue|0]   Against: [ROOT.Char.MakeScope.Var(\'kehillah_synod_result_against\').GetValue|0]   Not cast: [ROOT.Char.MakeScope.Var(\'kehillah_synod_result_uncast\').GetValue|0]\\n\\nHover Record the ruling for the named roll call. Individual votes are also recorded in the activity log. As sponsor, the host’s vote supports the proposal.',
        'kehillah_synod.0103.a': 'Record the ruling.',
        'kehillah_synod_result_recorded_tt': 'Acknowledges the result. Valid rulings have already taken effect; this button does not grant the office.',
        'kehillah_synod_roll_for_header': 'Voted for:',
        'kehillah_synod_roll_against_header': 'Voted against:',
        'kehillah_synod_roll_uncast_header': 'Did not cast a vote:',
        'kehillah_synod_roll_name': '[kehillah_synod_voter.GetTitledFirstName]',
        'kehillah_synod_head_unconfirmed_tt': 'The game did not confirm both title ownership and recognition as head of rite.',
    }
    write('localization/english/kehillah_synod_votes_l_english.yml', 'l_english:\n' + '\n'.join(f' {key}:0 "{value}"' for key, value in loc.items()) + '\n')
    # Keep the pre-existing key in one file, avoiding duplicate localization IDs.
    path = 'localization/english/kehillah_synod_l_english.yml'
    text = read(path)
    text = re.sub(r'(?m)^ kehillah_synod\.0103\.a:.*$', ' kehillah_synod.0103.a:0 "Record the ruling."', text)
    write(path, text)
    path = 'localization/english/kehillah_synod_votes_l_english.yml'
    text = read(path)
    write(path, re.sub(r'(?m)^ kehillah_synod\.0103\.a:.*\n', '', text))


if __name__ == '__main__':
    build()
