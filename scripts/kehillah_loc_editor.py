"""Small, dependency-free editor for this mod's CK3 localization.

Run from any directory: python scripts/kehillah_loc_editor.py
Only an edited value is replaced; comments, order, headers and encoding survive.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk


ROOT = Path(__file__).resolve().parents[1]
LOC_ROOT = ROOT / "localization" / "english"
ENTRY_START = re.compile(r'(?m)^[ \t]*([A-Za-z0-9_.-]+):(\d+)[ \t]+"')


def decode_value(raw: str) -> str:
    """Show CK3's common escapes as text, keeping unknown escapes unchanged."""
    return re.sub(r'\\([\\"n])', lambda m: {"n": "\n", '"': '"', "\\": "\\"}[m[1]], raw)


def encode_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def parse_entries(source: str):
    """Return (key, version, value, start, end) with offsets for quoted content."""
    entries = []
    for match in ENTRY_START.finditer(source):
        start = match.end()
        pos = start
        while pos < len(source):
            if source[pos] == "\\":
                pos += 2
            elif source[pos] == '"':
                tail = source[pos + 1:source.find("\n", pos + 1) if "\n" in source[pos + 1:] else len(source)]
                if not tail.strip() or tail.lstrip().startswith("#"):
                    entries.append((match[1], match[2], decode_value(source[start:pos]), start, pos))
                break
            else:
                pos += 1
    return entries


class Editor:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Kehillah localization editor")
        root.geometry("1150x740")
        self.files = {}
        self.rows = []
        self.visible = []
        self.selected = None
        self.original = ""

        bar = ttk.Frame(root, padding=8)
        bar.pack(fill="x")
        ttk.Label(bar, text="Search key or text:").pack(side="left")
        self.query = tk.StringVar()
        search = ttk.Entry(bar, textvariable=self.query)
        search.pack(side="left", fill="x", expand=True, padx=8)
        self.query.trace_add("write", lambda *_: self.filter_rows())
        ttk.Button(bar, text="Reload files", command=self.reload).pack(side="left")

        pane = ttk.Panedwindow(root, orient="horizontal")
        pane.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        left = ttk.Frame(pane)
        right = ttk.Frame(pane, padding=(12, 4))
        pane.add(left, weight=2)
        pane.add(right, weight=3)

        self.listbox = tk.Listbox(left, exportselection=False, font=("Consolas", 10))
        scroll = ttk.Scrollbar(left, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self.select_row)

        self.key_label = ttk.Label(right, text="Select an entry", font=("Segoe UI", 13, "bold"))
        self.key_label.pack(anchor="w")
        self.file_label = ttk.Label(right, text="")
        self.file_label.pack(anchor="w", pady=(4, 12))
        ttk.Label(right, text="Text (line breaks here save as \\n):").pack(anchor="w")
        self.text = tk.Text(right, wrap="word", undo=True, font=("Segoe UI", 11))
        self.text.pack(fill="both", expand=True, pady=(4, 8))
        self.text.bind("<<Modified>>", self.on_modified)
        actions = ttk.Frame(right)
        actions.pack(fill="x")
        self.save_button = ttk.Button(actions, text="Save value  (Ctrl+S)", command=self.save)
        self.save_button.pack(side="left")
        ttk.Button(actions, text="Revert", command=self.revert).pack(side="left", padx=8)
        self.status = ttk.Label(root, text="", padding=(8, 0, 8, 8))
        self.status.pack(anchor="w")
        root.bind("<Control-s>", lambda _: self.save())
        self.reload()
        search.focus_set()

    def on_modified(self, _=None):
        if self.text.edit_modified():
            self.text.edit_modified(False)
            if self.selected is not None:
                self.status.configure(text="Unsaved change" if self.current_text() != self.original else "")

    def current_text(self):
        return self.text.get("1.0", "end-1c")

    def confirm_discard(self):
        return self.selected is None or self.current_text() == self.original or messagebox.askyesno(
            "Unsaved edit", "Discard the current unsaved edit?"
        )

    def reload(self):
        if not self.confirm_discard():
            return
        self.files.clear()
        self.rows.clear()
        for path in sorted(LOC_ROOT.rglob("*_l_english.yml")):
            data = path.read_bytes()
            try:
                source = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            digest = hashlib.sha256(data).digest()
            self.files[path] = (source, digest, data.startswith(b"\xef\xbb\xbf"))
            for key, version, value, start, end in parse_entries(source):
                self.rows.append((path, key, version, value, start, end))
        self.selected = None
        self.original = ""
        self.text.delete("1.0", "end")
        self.key_label.configure(text="Select an entry")
        self.file_label.configure(text="")
        self.filter_rows()

    def filter_rows(self):
        needle = self.query.get().casefold().strip()
        self.visible = [r for r in self.rows if needle in r[1].casefold() or needle in r[3].casefold() or needle in str(r[0].relative_to(ROOT)).casefold()]
        self.listbox.delete(0, "end")
        for path, key, _, value, _, _ in self.visible:
            excerpt = " ".join(value.split())[:70]
            self.listbox.insert("end", f"{key}   —   {excerpt}")
        self.status.configure(text=f"{len(self.visible)} of {len(self.rows)} entries")

    def select_row(self, _=None):
        indices = self.listbox.curselection()
        if not indices:
            return
        row = self.visible[indices[0]]
        if row == self.selected:
            return
        if not self.confirm_discard():
            self.listbox.selection_clear(0, "end")
            return
        self.selected = row
        path, key, version, value, _, _ = row
        self.original = value
        self.key_label.configure(text=f"{key}:{version}")
        self.file_label.configure(text=str(path.relative_to(ROOT)))
        self.text.delete("1.0", "end")
        self.text.insert("1.0", value)
        self.text.edit_modified(False)
        self.status.configure(text="")

    def revert(self):
        if self.selected is None:
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", self.original)
        self.text.edit_modified(False)
        self.status.configure(text="Reverted")

    def save(self):
        if self.selected is None:
            return
        value = self.current_text()
        if value == self.original:
            self.status.configure(text="No changes to save")
            return
        path, key, version, _, start, end = self.selected
        source, digest, bom = self.files[path]
        if hashlib.sha256(path.read_bytes()).digest() != digest:
            messagebox.showerror("File changed", "This file changed outside the editor. Reload before saving so no edits are lost.")
            return
        updated = source[:start] + encode_value(value) + source[end:]
        data = (b"\xef\xbb\xbf" if bom else b"") + updated.encode("utf-8")
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".kehillah_loc_", suffix=".tmp", delete=False) as tmp:
                temp_path = Path(tmp.name)
                tmp.write(data)
            os.replace(temp_path, path)
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))
            return
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
        self.original = value
        self.reload()
        self.query.set(key)
        if self.visible:
            self.listbox.selection_set(0)
            self.select_row()
        self.status.configure(text=f"Saved {key} in {path.name}")


if __name__ == "__main__":
    window = tk.Tk()
    Editor(window)
    window.mainloop()
