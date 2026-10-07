"""
AutoEverGreen GUI — Main Application Window
Sidebar navigation + content area.
"""
from __future__ import annotations
import sys
import tkinter as tk
import customtkinter as ctk
from pathlib import Path

from .theme import *
from .components import NavButton, Divider
from .service import AppService
from .dashboard import DashboardPanel
from .json_editor import JsonEditorPanel
from .settings import SettingsPanel
from .about import AboutPanel

ctk.set_appearance_mode(CTK_DEFAULTS["appearance_mode"])
ctk.set_default_color_theme(CTK_DEFAULTS["color_theme"])


NAV_ITEMS = [
    ("HOME",         "dashboard"),
    ("JSON EDITOR",  "json_editor"),
    ("SETTINGS",     "settings"),
    ("ABOUT",        "about"),
]


class AutoEverGreenApp(ctk.CTk):
    def __init__(self, service: AppService):
        super().__init__()
        self._svc = service
        self._panels: dict[str, ctk.CTkFrame] = {}
        self._active_page = ""

        self.title("AutoEverGreen")
        self.geometry("1100x720")
        self.minsize(900, 580)
        self.configure(fg_color=BG_BASE)

        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception:
            pass

        self._build()
        self._navigate("dashboard")

    # ── LAYOUT ────────────────────────────────────────────────────────

    def _build(self):
        # Outer container
        outer = ctk.CTkFrame(self, fg_color=BG_BASE, corner_radius=0)
        outer.pack(fill="both", expand=True)

        # ── Sidebar ──────────────────────────────────────────────────
        sidebar = ctk.CTkFrame(
            outer, width=200, fg_color=BG_SURFACE,
            corner_radius=0,
            border_width=BORDER_WIDTH, border_color=BORDER
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo area
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent", height=80)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame, text="AEG",
            font=(FONT_FAMILY, 20, "bold"), text_color=ACCENT
        ).place(relx=0.1, rely=0.4, anchor="w")

        ctk.CTkLabel(
            logo_frame, text="AutoEverGreen",
            font=(FONT_FAMILY, 12, "bold"), text_color=TEXT_PRIMARY
        ).place(relx=0.1, rely=0.7, anchor="w")

        Divider(sidebar).pack(fill="x")

        # Nav section
        nav_section = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_section.pack(fill="x", padx=PAD_SMALL, pady=(15, 0))

        self._nav_btns: dict[str, NavButton] = {}
        for label, page in NAV_ITEMS:
            btn = NavButton(
                nav_section, text=label,
                command=lambda p=page: self._navigate(p)
            )
            btn.pack(fill="x", pady=2)
            self._nav_btns[page] = btn

        # Bottom sidebar info
        Divider(sidebar).pack(fill="x", side="bottom")
        self._sidebar_footer(sidebar)

        # ── Content area ─────────────────────────────────────────────
        self._content = ctk.CTkFrame(outer, fg_color=BG_BASE, corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

        # Pre-build panels
        self._panels["dashboard"]   = DashboardPanel(
            self._content, self._svc,
            on_run_complete=lambda: self._on_run_complete()
        )
        self._panels["json_editor"] = JsonEditorPanel(self._content, self._svc)
        self._panels["settings"]    = SettingsPanel(self._content, self._svc)
        self._panels["about"]       = AboutPanel(self._content, self._svc)

    def _sidebar_footer(self, parent):
        foot = ctk.CTkFrame(parent, fg_color="transparent")
        foot.pack(side="bottom", fill="x", padx=PAD_SMALL, pady=PAD_SMALL)

        ctk.CTkLabel(
            foot, text=f"Version {AppService.APP_VERSION}",
            font=FONT_TINY, text_color=TEXT_MUTED
        ).pack(anchor="w", padx=6)

    # ── NAVIGATION ────────────────────────────────────────────────────

    def _navigate(self, page: str):
        if self._active_page == page:
            return

        for panel in self._panels.values():
            panel.pack_forget()

        self._panels[page].pack(fill="both", expand=True)

        for p, btn in self._nav_btns.items():
            btn.set_active(p == page)

        self._active_page = page

        panel = self._panels[page]
        if hasattr(panel, "refresh"):
            panel.refresh()

    def _on_run_complete(self):
        """Called by dashboard after an execution finishes."""
        pass
