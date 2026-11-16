"""Generate gui/kehillah_scheme_widget.gui from vanilla's window_intrigue.gui.

usage: kehillah_make_scheme_widget.py <vanilla window_intrigue.gui> <out .gui>
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8-sig").read().split("\n")
# widget_own_scheme_item through the closing brace of `types IntrigueWindow`
body = "\n".join(lines[167:889])
assert body.startswith("\ttype widget_own_scheme_item"), body[:60]

STUDY = ("And( Scheme.MakeScope.Var( 'kehillah_is_study_scheme' ).IsSet, "
         "GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).IsSet )")
FLAG = "GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).GetFlagName"

# a) header: the study scheme names its book
old = '''					text_single = {
						text = "SCHEME_WINDOW_ITEM_NAME"
						using = Font_Size_Medium
						align = nobaseline
						max_width = 430
						margin_left = 15
					}
'''
assert body.count(old) == 1
new = '''					text_single = {
						visible = "[Not( %(S)s )]"
						text = "SCHEME_WINDOW_ITEM_NAME"
						using = Font_Size_Medium
						align = nobaseline
						max_width = 430
						margin_left = 15
					}

					# Jewish Communities 2026-11-15: the study scheme names its book.
					text_single = {
						visible = "[%(S)s]"
						text = "[Concatenate( Concatenate( Localize( 'kehillah_study_torah' ), ': ' ), Localize( Concatenate( 'kehillah_lib_name_', %(F)s ) ) )]"
						using = Font_Size_Medium
						align = nobaseline
						max_width = 430
						margin_left = 15
					}
''' % {"S": STUDY, "F": FLAG}
body = body.replace(old, new)

# b) the book, as a second portrait-style slot beside the owner's portrait
marker = ("\t\t\t\tvbox  = {\n\t\t\t\t\tlayoutpolicy_horizontal = expanding\n"
          "\t\t\t\t\tlayoutpolicy_vertical = expanding\n\n\t\t\t\t\twidget = {\n"
          "\t\t\t\t\t\tvisible = \"[Not(SchemeItem")
assert body.count(marker) == 1, body.count(marker)
book = '''				# Jewish Communities 2026-11-15: the book being studied, shown like a
				# character target. Hover for its details; click to open the library
				# (the same two steps as the Beit Midrash chip in gui/window_character.gui).
				widget = {
					visible = "[%(S)s]"
					name = "kehillah_study_book_slot"
					size = { 110 120 }

					button = {
						name = "kehillah_study_book_button"
						parentanchor = center
						size = { 96 112 }
						onclick = "[GetScriptedGui( 'kehillah_lib_window_open' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope( 'target', GetPlayer.MakeScope ).End )]"
						onclick = "[GetVariableSystem.Set( 'kehillah_lib_window_open', 'yes' )]"
						using = tooltip_es
						tooltipwidget = { kehillah_study_book_tooltip = {} }

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

''' % {"S": STUDY}
body = body.replace(marker, book + marker)

header = '''##########################################################################
# THE SCHEME PANEL'S ENTRY FOR "STUDYING TORAH" (2026-11-15, Daniel: "include
# more info about the book being studied ... hoverable as if it were a
# portrait ... clicking could open your library"; second pass: keep the
# owner's portrait and show the book beside it like a character target).
# GENERATED from the vanilla 1.20 widget by scripts/kehillah_make_scheme_widget.py:
# a copy of vanilla's widget_own_scheme_item with two changes tagged "Jewish
# Communities 2026-11-15": the header names the book, and a book portrait sits
# beside the owner's. Both are gated on Scheme.MakeScope.Var(
# 'kehillah_is_study_scheme' ) (set by the scheme) and var:kehillah_study_
# current_work (a flag kept in step with the numeric kehillah_study_current_
# work_id by kehillah_study_sync_current_work_effect), so every other scheme
# draws exactly as in vanilla. The pop-out reuses vanilla's
# object_tooltip_pop_out, as SchemeTooltip in gui/shared/cooltip.gui does.
##########################################################################
types KehillahStudyBook
{
	type kehillah_study_book_tooltip = container {
		alwaystransparent = no
		object_tooltip_pop_out = {
			blockoverride "title_text" {
				margin = { 0 8 }
				text = "[Localize( Concatenate( 'kehillah_lib_name_', %(F)s ) )]"
			}
			blockoverride "concept_link" {
				text = "[Localize( Concatenate( 'kehillah_lib_subject_', %(F)s ) )]"
			}
			blockoverride "description_text" {
				text = "KEHILLAH_STUDY_SCHEME_BOOK_TT"
			}
		}
	}
}

types IntrigueWindow
{
''' % {"F": FLAG}
open(dst, "w", encoding="utf-8", newline="\n").write(header + body.rstrip("\n") + "\n")
