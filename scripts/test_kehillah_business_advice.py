"""Source integration checks for actionable business guidance and navigation."""
import unittest
from test_kehillah_household_economy import read, block
from test_kehillah_business_positions import BUSINESSES

class BusinessAdviceTest(unittest.TestCase):
    def test_staffing_uses_native_eligibility_for_an_actual_vacancy(self):
        tr=read("common/scripted_triggers/kehillah_business_triggers.txt")
        for b in BUSINESSES:
            k=b["key"]
            x=block(tr,f"kehillah_business_{k}_appointment_available_trigger")
            self.assertIn(f"kehillah_business_{k}_built_trigger = yes",x)
            self.assertIn(f"NOT = {{ employs_court_position = kehillah_business_{k}_position }}",x)
            self.assertIn(f"any_courtier = {{ can_be_employed_as = kehillah_business_{k}_position }}",x)
        actions=read("common/important_actions/kehillah_business_actions.txt")
        staff=block(actions,"action_kehillah_staff_business")
        self.assertGreaterEqual(staff.count("kehillah_business_staffing_advice_trigger = yes"),2)
        self.assertNotIn("appoint_court_position",actions)
        self.assertNotIn("add_gold",actions)
        self.assertNotIn("set_variable",actions)
        self.assertNotIn("trigger_event",actions)
        self.assertIn("kehillah_business_alert_open_quarter_effect = yes",actions)
        view=read("common/scripted_effects/kehillah_business_advice_effects.txt")
        self.assertIn("close_view = { view = my_realm player = root }",view)
        self.assertIn("open_view_data = { view = domicile player = root }",view)
        self.assertNotIn("set_variable",view)

    def test_construction_advice_is_conservative_and_suppressed_by_vacancies(self):
        x=block(read("common/scripted_triggers/kehillah_business_advice_triggers.txt"),"kehillah_business_expansion_advice_trigger")
        for gate in ["is_at_war = no","kehillah_charter_allows_new_communal_building_trigger = yes","gold >= kehillah_business_craft_reserve_value","NOT = { kehillah_business_has_vacancy_trigger = yes }","kehillah_business_unassigned_head_trigger = yes","NOT = { has_ongoing_domicile_construction = yes }"]:
            self.assertIn(gate,x)
        for tier in range(1,4):self.assertIn(f"domicile_building_has_free_internal_slot = kehillah_workshops_0{tier}",x)
        for k in ["dyers","goldsmiths","tanners"]:self.assertIn(f"NOT = {{ kehillah_business_{k}_built_trigger = yes }}",x)
        loc=read("localization/english/kehillah_business_advice_l_english.yml")
        self.assertIn("final price and construction conditions",loc)
        self.assertIn("does not start construction or spend gold",loc)

    def test_next_step_prioritizes_staffing_and_preserves_household_limits(self):
        x=read("common/customizable_localization/kehillah_business_advice_custom_loc.txt")
        x=block(x,"KehillahBusinessNextStep")
        self.assertLess(x.index("kehillah_business_staffing_advice_trigger"),x.index("kehillah_business_expansion_advice_trigger"))
        tr=block(read("common/scripted_triggers/kehillah_business_advice_triggers.txt"),"kehillah_business_unassigned_head_trigger")
        self.assertIn("kehillah_household_assignment_cooldown",tr)
        self.assertIn("any_house_member",tr)

    def test_domain_tooltips_are_read_only_and_connect_to_the_businesses_tab(self):
        for path,key in [("localization/english/kehillah_breakdown_l_english.yml","KEHILLAH_BD_PROSPERITY_TOOLTIP"),("localization/english/kehillah_domain_l_english.yml","KEHILLAH_DOM_DRV_PROSPERITY_QUARTER_TT")]:
            line=next(x for x in read(path).splitlines() if x.lstrip().startswith(key+":"))
            self.assertIn("KehillahBusinessDomainDetail",line)
        loc=read("localization/english/kehillah_business_advice_l_english.yml")
        self.assertIn("staffing does not award instant Affluence",loc)
        self.assertNotIn("Execute(",loc)
        realm=read("gui/window_my_realm.gui")
        self.assertIn("kehillah_business_request_open",realm)
        opener=read("gui/kehillah_business_opener.gui")
        self.assertIn("ToggleGameViewData('domicile',GetPlayer.GetDomicile.Self)",opener)
        self.assertIn("Not(IsGameViewOpen('domicile'))",opener)
        self.assertIn("CloseGameView('my_realm')",opener)
        self.assertIn("Not(IsGameViewOpen('my_realm'))",opener)
        self.assertNotIn("OpenGameViewData(",opener)
        self.assertIn("GetVariableSystem.Set('kehillah_businesses_tab','yes')",opener)
        self.assertIn("GetVariableSystem.Clear('kehillah_businesses_tab')",opener)
        consume=block(read("common/scripted_guis/kehillah_business_advice_gui.txt"),"kehillah_business_open_request_consume")
        self.assertIn("is_valid = { always = yes }",consume)
        self.assertIn("remove_variable = kehillah_business_households_request",consume)
        registrations=read("gui/scripted_widgets/kehillah_scripted_widgets.txt")
        self.assertIn("gui/kehillah_business_opener.gui = kehillah_business_open_opener",registrations)
        self.assertIn("gui/kehillah_business_opener.gui = kehillah_business_navigation_ensure",registrations)

if __name__=="__main__":unittest.main()
