"""
AutoEverGreen GUI — Settings Panel
Application preferences (appearance, behavior).
"""
import tkinter as tk
import customtkinter as ctk
from .theme import *
from .components import Card, Divider, PrimaryButton, SectionLabel

class SettingsPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, service, **kw):
        super().__init__(parent, fg_color=BG_BASE, corner_radius=0, **kw)
        self._svc = service
        self._build()
        self.refresh()

    def _build(self):
        # ── Header ──────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(40, 20))

        ctk.CTkLabel(
            hdr, text="Settings",
            font=(FONT_FAMILY, 24, "bold"), text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")

        Divider(self).pack(fill="x", padx=40, pady=10)

        # ── Appearance ──────────────────────────────────────────
        app_card = Card(self)
        app_card.pack(fill="x", padx=40, pady=(10, 20))
        
        inner1 = ctk.CTkFrame(app_card, fg_color="transparent")
        inner1.pack(fill="both", padx=20, pady=20)
        
        SectionLabel(inner1, text="Appearance").pack(anchor="w", pady=(0, 10))

        # Theme Switch
        theme_row = ctk.CTkFrame(inner1, fg_color="transparent")
        theme_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(theme_row, text="Theme", font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left")
        
        self._theme_var = tk.StringVar(value="Dark")
        self._theme_opt = ctk.CTkOptionMenu(
            theme_row, values=["Dark", "Light", "System"],
            variable=self._theme_var,
            font=FONT_BODY, fg_color=BG_SURFACE2,
            button_color=BG_SURFACE2, button_hover_color=BG_HOVER,
            command=self._on_theme_change
        )
        self._theme_opt.pack(side="right")

        # ── Application Behavior ─────────────────────────────────
        behav_card = Card(self)
        behav_card.pack(fill="x", padx=40, pady=10)
        
        inner2 = ctk.CTkFrame(behav_card, fg_color="transparent")
        inner2.pack(fill="both", padx=20, pady=20)
        
        SectionLabel(inner2, text="Application Behavior").pack(anchor="w", pady=(0, 10))

        # Start with Windows
        startup_row = ctk.CTkFrame(inner2, fg_color="transparent")
        startup_row.pack(fill="x", pady=10)
        
        ctk.CTkLabel(startup_row, text="Start with Windows", font=FONT_BODY, text_color=TEXT_PRIMARY).pack(side="left")
        
        self._startup_var = tk.BooleanVar(value=False)
        self._startup_sw = ctk.CTkSwitch(
            startup_row, text="", variable=self._startup_var,
            progress_color=ACCENT, command=self._on_startup_change
        )
        self._startup_sw.pack(side="right")

        # Dry Run
        dry_row = ctk.CTkFrame(inner2, fg_color="transparent")
        dry_row.pack(fill="x", pady=10)
        
        text_frame = ctk.CTkFrame(dry_row, fg_color="transparent")
        text_frame.pack(side="left")
        ctk.CTkLabel(text_frame, text="Dry Run Mode", font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Simulate execution without modifying files or pushing.", font=FONT_SMALL, text_color=TEXT_MUTED, anchor="w").pack(anchor="w")
        
        self._dryrun_var = tk.BooleanVar(value=False)
        self._dryrun_sw = ctk.CTkSwitch(
            dry_row, text="", variable=self._dryrun_var,
            progress_color=ACCENT, command=self._on_dryrun_change
        )
        self._dryrun_sw.pack(side="right", pady=5)

    def _on_theme_change(self, value):
        ctk.set_appearance_mode(value)

    def _on_startup_change(self):
        enabled = self._startup_var.get()
        success = self._svc.set_startup_enabled(enabled)
        if not success:
            # Revert if it failed
            self._startup_var.set(not enabled)

    def _on_dryrun_change(self):
        dry = self._dryrun_var.get()
        try:
            self._svc.save_settings(dry_run=dry, log_enabled=True)
        except Exception:
            self._dryrun_var.set(not dry)

    def refresh(self):
        # Refresh config values
        self._svc.reload()
        if self._svc.is_config_loaded:
            self._dryrun_var.set(self._svc.config.settings.dry_run)
            
        # Refresh startup state
        self._startup_var.set(self._svc.get_startup_enabled())
