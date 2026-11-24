"""Add writing sparks to gui/kehillah_scheme_widget.gui (run after
kehillah_make_scheme_widget.py; safe to run twice).

Studying Torah: a small inspiration icon beside the book's name, shown when
mastering this book would be a first mastery for a writer; its tooltip names
what it can spark. Writing a Sefer: the header names the form, and the same
icon's tooltip names the spark's tier.
"""

from pathlib import Path

GUI = Path(__file__).resolve().parents[1] / "gui/kehillah_scheme_widget.gui"
MARK = "# Jewish Communities 2026-11-24: writing sparks."
T = "\t"

STUDY = ("And( Scheme.MakeScope.Var( 'kehillah_is_study_scheme' ).IsSet, "
         "GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).IsSet )")
WRITING = ("And( Scheme.MakeScope.Var( 'kehillah_is_writing_scheme' ).IsSet, "
           "GetPlayer.MakeScope.Var( 'kehillah_writing_form' ).IsSet )")


def main() -> None:
    text = GUI.read_text(encoding="utf-8-sig")
    if MARK in text:
        return
    plain = (T * 6 + f'visible = "[Not( {STUDY} )]"\n' + T * 6 + 'text = "SCHEME_WINDOW_ITEM_NAME"')
    assert text.count(plain) == 1
    text = text.replace(plain, T * 6 + f'visible = "[Not( Or( {STUDY}, {WRITING} ) )]"\n' +
                        T * 6 + 'text = "SCHEME_WINDOW_ITEM_NAME"')

    study_header_end = ("Localize( Concatenate( 'kehillah_lib_name_', GetPlayer.MakeScope.Var( 'kehillah_study_current_work' ).GetFlagName ) ) )]\"\n"
                        + T * 6 + "using = Font_Size_Medium\n" + T * 6 + "align = nobaseline\n"
                        + T * 6 + "max_width = 430\n" + T * 6 + "margin_left = 15\n" + T * 5 + "}\n")
    assert text.count(study_header_end) == 1
    form = "GetPlayer.MakeScope.Var( 'kehillah_writing_form' ).GetFlagName"
    spark_icon = "gfx/interface/icons/inspirations/book_inspiration.dds"
    insert = f"""
{T*5}{MARK}
{T*5}# The writing scheme names its form, as the study scheme names its book.
{T*5}text_single = {{
{T*6}visible = "[{WRITING}]"
{T*6}text = "[Concatenate( Concatenate( Localize( 'kehillah_writing' ), ': ' ), Localize( Concatenate( 'kehillah_spark_title_', {form} ) ) )]"
{T*6}using = Font_Size_Medium
{T*6}align = nobaseline
{T*6}max_width = 400
{T*6}margin_left = 15
{T*5}}}
{T*5}# A spark icon: what this reading can spark, or the tier being written.
{T*5}icon = {{
{T*6}visible = "[And( {STUDY}, EqualTo_CFixedPoint( GetPlayer.MakeScope.ScriptValue( 'kehillah_spark_study_new_value' ), '(CFixedPoint)1' ) )]"
{T*6}size = {{ 28 28 }}
{T*6}margin_left = 6
{T*6}texture = "{spark_icon}"
{T*6}tooltip = "kehillah_spark_scheme_study_tt"
{T*5}}}
{T*5}icon = {{
{T*6}visible = "[{WRITING}]"
{T*6}size = {{ 28 28 }}
{T*6}margin_left = 6
{T*6}texture = "{spark_icon}"
{T*6}tooltip = "kehillah_spark_scheme_writing_tt"
{T*5}}}
"""
    text = text.replace(study_header_end, study_header_end + insert)
    GUI.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
