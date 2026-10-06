"""
AutoEverGreen GUI — JSON Editor Panel
A simple built-in text editor for configuration files.
"""
from __future__ import annotations
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from pathlib import Path
from .theme import *
from .components import Divider, PrimaryButton, SecondaryButton, SectionLabel

class JsonEditorPanel(ctk.CTkFrame):
    def __init__(self, parent, service, **kw):
        super().__init__(parent, fg_color=BG_BASE, corner_radius=0, **kw)
        self._svc = service
        self._current_file: Path | None = None
        self._build()
        self.refresh()

    def _build(self):
        # ── Header ──────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(40, 20))

        title_col = ctk.CTkFrame(hdr, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_col, text="JSON Editor",
            font=(FONT_FAMILY, 24, "bold"), text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")

        self._file_lbl = ctk.CTkLabel(
            title_col, text="No file loaded",
            font=FONT_BODY, text_color=TEXT_MUTED, anchor="w"
        )
        self._file_lbl.pack(anchor="w")
        
        btn_col = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_col.pack(side="right")
        
        SecondaryButton(
            btn_col, text="Upload JSON File",
            command=self._upload_file
        ).pack(anchor="e")

        Divider(self).pack(fill="x", padx=40, pady=10)

        # ── Text Editor ──────────────────────────────────────────────
        self._editor = ctk.CTkTextbox(
            self, font=FONT_MONO, fg_color=BG_SURFACE, text_color=TEXT_PRIMARY,
            border_width=BORDER_WIDTH, border_color=BORDER, corner_radius=CORNER_RADIUS,
            wrap="none"
        )
        self._editor.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # ── Buttons ──────────────────────────────────────────────
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=40, pady=(0, 40))

        PrimaryButton(
            btn_row, text="Save Changes",
            command=self._save_changes
        ).pack(side="left", ipadx=10)
        
        SecondaryButton(
            btn_row, text="Format JSON",
            command=self._format_json
        ).pack(side="left", padx=(10, 0))
        
        SecondaryButton(
            btn_row, text="Validate",
            command=self._validate_json
        ).pack(side="left", padx=(10, 0))

        self._status_lbl = ctk.CTkLabel(
            btn_row, text="", font=FONT_BODY, text_color=TEXT_MUTED
        )
        self._status_lbl.pack(side="left", padx=16)

    def refresh(self):
        # Only load the active config if no file is currently loaded
        if self._current_file is None:
            config_path = self._svc.config_path
            if config_path and config_path.exists():
                self._load_file(config_path)

    def _load_file(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self._editor.delete("1.0", "end")
            self._editor.insert("end", content)
            self._current_file = path
            
            # Show if it's the active config or another file
            is_active = (path.resolve() == self._svc.config_path.resolve())
            if is_active:
                self._file_lbl.configure(text=f"Current file: {path.name}", text_color=STATUS_SUCCESS)
            else:
                self._file_lbl.configure(text=f"Loaded: {path}", text_color=STATUS_PENDING)
                
            self._status_lbl.configure(text="")
        except Exception as e:
            self._status_lbl.configure(text=f"✗ Failed to load: {e}", text_color=STATUS_FAILED)

    def _upload_file(self):
        filetypes = [("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        path = filedialog.askopenfilename(title="Select JSON File", filetypes=filetypes)
        if path:
            self._load_file(Path(path))

    def _validate_json(self):
        content = self._editor.get("1.0", "end-1c")
        if not content.strip():
            self._status_lbl.configure(text="✕ Empty content", text_color=STATUS_FAILED)
            return False
            
        try:
            json.loads(content)
            self._status_lbl.configure(text="✓ Valid JSON", text_color=STATUS_SUCCESS)
            return True
        except json.JSONDecodeError as e:
            self._status_lbl.configure(text=f"✕ Invalid JSON: {e}", text_color=STATUS_FAILED)
            return False

    def _format_json(self):
        content = self._editor.get("1.0", "end-1c")
        try:
            parsed = json.loads(content)
            formatted = json.dumps(parsed, indent=2)
            self._editor.delete("1.0", "end")
            self._editor.insert("end", formatted)
            self._status_lbl.configure(text="✓ JSON Formatted", text_color=STATUS_SUCCESS)
        except json.JSONDecodeError as e:
            self._status_lbl.configure(text=f"✕ Cannot format invalid JSON: {e}", text_color=STATUS_FAILED)

    def _save_changes(self):
        if not self._current_file:
            self._status_lbl.configure(text="✕ No file loaded to save", text_color=STATUS_FAILED)
            return

        if not self._validate_json():
            messagebox.showerror("Validation Error", "The JSON is invalid and cannot be saved.")
            return

        is_active = (self._current_file.resolve() == self._svc.config_path.resolve())
        if not is_active:
            confirm = messagebox.askyesno(
                "Confirm Save", 
                f"You are saving a file that is not the active configuration:\n{self._current_file}\n\nContinue?"
            )
            if not confirm:
                return

        content = self._editor.get("1.0", "end-1c")
        try:
            with open(self._current_file, "w", encoding="utf-8") as f:
                f.write(content)
            self._status_lbl.configure(text=f"✓ Saved {self._current_file.name}", text_color=STATUS_SUCCESS)
            
            # If we saved the active config, tell the service to reload it
            if is_active:
                self._svc.reload()
                
        except Exception as e:
            self._status_lbl.configure(text=f"✕ Failed to save: {e}", text_color=STATUS_FAILED)
            messagebox.showerror("Save Error", f"Failed to save file:\n{e}")
