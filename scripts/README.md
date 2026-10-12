# Kehillah localization editor

Run `python scripts/kehillah_loc_editor.py` from the repository, or double-click
`kehillah_loc_editor.py` if Windows associates `.py` files with Python. It uses
Python's built-in Tkinter library and needs no package installation.

Search keys, text, or filenames on the left. Select an entry, edit its text on
the right, then press **Ctrl+S**. Text entered on separate lines is saved as
CK3's `\n` sequence. CK3 formatting such as `#italic`, `$other_key$`, and
`[ROOT.Char.GetName]` stays visible for editing.

The editor writes only the selected value. It keeps comments, file order,
header, and UTF-8 BOM intact. It refuses to save if another program has changed
the file since the editor loaded it; use **Reload files** in that case. Check
the resulting Git diff and run `ck3-tiger` after localization work.
