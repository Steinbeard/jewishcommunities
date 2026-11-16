"""Generate gui/kehillah_scheme_widget.gui from vanilla's window_intrigue.gui.

usage: kehillah_make_scheme_widget.py <vanilla window_intrigue.gui> <out .gui>
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8-sig").read().split("\n")
# widget_own_scheme_item through the closing brace of `types IntrigueWindow`
body = "\n".join(lines[167:889])
assert body.startswith("\ttype widget_own_scheme_item"), body[:60]

T = "\t"
STUDY = ("And( Scheme.MakeScope.Var( 'kehillah_is_study_scheme' ).IsSet, "
         "GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).IsSet )")
FLAG = "GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).GetFlagName"


def tabs(block, n):
    """Indent every non-empty line of block by n tabs."""
    return "\n".join((T * n + l) if l.strip() else l for l in block.split("\n"))


# a) header: the study scheme names its book
old = (T * 5 + 'text_single = {\n' +
       T * 6 + 'text = "SCHEME_WINDOW_ITEM_NAME"\n' +
       T * 6 + 'using = Font_Size_Medium\n' +
       T * 6 + 'align = nobaseline\n' +
       T * 6 + 'max_width = 430\n' +
       T * 6 + 'margin_left = 15\n' +
       T * 5 + '}\n')
assert body.count(old) == 1
new = old.replace(T * 6 + 'text = "SCHEME_WINDOW_ITEM_NAME"',
                  T * 6 + 'visible = "[Not( %s )]"\n' % STUDY + T * 6 + 'text = "SCHEME_WINDOW_ITEM_NAME"')
new += "\n" + T * 5 + "# Jewish Communities 2026-11-15: the study scheme names its book.\n"
new += (T * 5 + 'text_single = {\n' +
        T * 6 + 'visible = "[%s]"\n' % STUDY +
        T * 6 + 'text = "[Concatenate( Concatenate( Localize( \'kehillah_study_torah\' ), \': \' ), '
        'Localize( Concatenate( \'kehillah_lib_name_\', %s ) ) )]"\n' % FLAG +
        T * 6 + 'using = Font_Size_Medium\n' +
        T * 6 + 'align = nobaseline\n' +
        T * 6 + 'max_width = 430\n' +
        T * 6 + 'margin_left = 15\n' +
        T * 5 + '}\n')
body = body.replace(old, new)

# b) the book, as a second portrait-style slot beside the owner's portrait
marker = (T * 4 + "vbox  = {\n" + T * 5 + "layoutpolicy_horizontal = expanding\n" +
          T * 5 + "layoutpolicy_vertical = expanding\n\n" + T * 5 + "widget = {\n" +
          T * 6 + 'visible = "[Not(SchemeItem')
assert body.count(marker) == 1, body.count(marker)
book = """# Jewish Communities 2026-11-15: the book being studied, shown like a
# character target. Hover for the Beit Midrash's own book card; click to open
# the library the course is read in (var:kehillah_study_library, kept current
# monthly by kehillah_study_torah_resolve_library_effect) -- not the player's
# own, since an adventurer has none.
widget = {
	visible = "[STUDY]"
	name = "kehillah_study_book_slot"
	size = { 110 120 }

	button = {
		name = "kehillah_study_book_button"
		parentanchor = center
		size = { 96 112 }
		enabled = "[GetScriptedGui( 'kehillah_lib_window_open_title' ).IsValid( GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope( 'library', GetPlayer.MakeScope.Var( 'kehillah_study_library' ).Title.MakeScope ).End )]"
		onclick = "[GetScriptedGui( 'kehillah_lib_window_open_title' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope( 'library', GetPlayer.MakeScope.Var( 'kehillah_study_library' ).Title.MakeScope ).End )]"
		onclick = "[GetVariableSystem.Set( 'kehillah_lib_window_open', 'yes' )]"
		using = tooltip_es
		state = { name = _mouse_hierarchy_enter on_start = "[GetVariableSystem.Set( 'kehillah_lib_hover_work', FLAG )]" }
		tooltipwidget = { kehillah_library_work_tooltip_hovered = {} }

		background = { using = Background_Area }
		background = { using = Background_Frame }

		icon = {
			parentanchor = center
			size = { 80 80 }
			texture = "gfx/interface/icons/artifact/artifact_chronicle.dds"
			alwaystransparent = yes
		}
	}
}

""".replace("STUDY", STUDY).replace("FLAG", FLAG)
body = body.replace(marker, tabs(book, 4) + marker)

# c) the success-chance row: for the study scheme, the Beit Midrash's own
# breakdown of the book's mastery chance (every term) in place of vanilla's
# tooltip, which cannot expand the nested script value.
start = (T * 7 + "hbox = {\n" + T * 8 + 'datacontext = "[SchemeItem.GetScheme]"\n' +
         T * 8 + 'visible = "[Scheme.GetSchemeType.IsBasic]"\n')
assert body.count(start) == 1
i = body.index(start)
end_token = T * 8 + "expand = {}\n" + T * 7 + "}\n"
j = body.index(end_token, i) + len(end_token)
row = body[i:j]
old_tt = 'tooltip = "SCHEME_WINDOW_SUCCESS_BASIC_TOOLTIP"'
assert old_tt in row
vis = 'visible = "[Scheme.GetSchemeType.IsBasic]"'
plain = row.replace(vis, 'visible = "[And( Scheme.GetSchemeType.IsBasic, Not( %s ) )]"' % STUDY)
chance = "GetPlayer.MakeScope.ScriptValue( Concatenate( 'kehillah_lib_mastery_chance_', %s ) )" % FLAG
tip = """# Jewish Communities 2026-11-15: the same breakdown the Beit Midrash's
# Study button shows, so it cannot drift from the roll.
tooltipwidget = {
	kehillah_mastery_chance_breakdown_tooltip = {
		datacontext = "[GuiScope.SetRoot( GetPlayer.MakeScope ).GetScriptValueBreakdown( Concatenate( 'kehillah_lib_mastery_chance_', FLAG ) )]"

		blockoverride "total" {
			text_single = {
				layoutpolicy_horizontal = expanding
				text = "[Concatenate( IntToString( FixedPointToInt( CHANCE ) ), '%' )]"
				default_format = "#T"
			}
		}
	}
}""".replace("FLAG", FLAG).replace("CHANCE", chance)
tip = tip.split("\n")
tip = tip[0] + "\n" + "\n".join(T * 8 + l if l.strip() else l for l in tip[1:])
study = row.replace(vis, 'visible = "[And( Scheme.GetSchemeType.IsBasic, %s )]"' % STUDY)
study = study.replace(old_tt, tip)
body = body[:i] + plain + "\n" + study + body[j:]

header = """##########################################################################
# THE SCHEME PANEL'S ENTRY FOR "STUDYING TORAH" (2026-11-15, Daniel: "include
# more info about the book being studied ... hoverable as if it were a
# portrait ... clicking could open your library"; second pass: keep the
# owner's portrait and show the book beside it like a character target;
# third: open the library being studied, and list the factors).
# GENERATED from the vanilla 1.20 widget by scripts/kehillah_make_scheme_widget.py:
# a copy of vanilla's widget_own_scheme_item with three changes tagged "Jewish
# Communities 2026-11-15": the header names the book, a book portrait sits
# beside the owner's, and the success row's hover lists the mastery factors.
# All are gated on Scheme.MakeScope.Var( 'kehillah_is_study_scheme' ) (set by
# the scheme) and var:kehillah_study_current_work (a flag kept in step with the
# numeric kehillah_study_current_work_id by kehillah_study_sync_current_work_
# effect), so every other scheme draws exactly as in vanilla. The book hover is
# the Beit Midrash's own card (kehillah_library_work_tooltip_hovered); the
# success hover is kehillah_mastery_chance_breakdown_tooltip.
##########################################################################
types IntrigueWindow
{
"""
open(dst, "w", encoding="utf-8", newline="\n").write(header + body.rstrip("\n") + "\n")
