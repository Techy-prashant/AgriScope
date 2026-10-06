"""
AutoEverGreen GUI — About Panel
Simplified about page.
"""
import customtkinter as ctk
from .theme import *
from .service import AppService
from .components import Divider

class AboutPanel(ctk.CTkFrame):
    def __init__(self, parent, service, **kw):
        super().__init__(parent, fg_color=BG_BASE, corner_radius=0, **kw)
        self._svc = service
        self._build()

    def _build(self):
        # ── Header ──────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=40, pady=(40, 20))

        ctk.CTkLabel(
            hdr, text="AutoEverGreen",
            font=(FONT_FAMILY, 28, "bold"), text_color=TEXT_PRIMARY, anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            hdr, text="Automated GitHub publishing utility.",
            font=FONT_BODY, text_color=TEXT_MUTED, anchor="w"
        ).pack(anchor="w")
        
        Divider(self).pack(fill="x", padx=40, pady=20)
        
        # ── Info ────────────────────────────────────────────────
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(fill="x", padx=40)
        
        def add_row(label, value):
            row = ctk.CTkFrame(info, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=label, font=FONT_BODY, text_color=TEXT_MUTED, width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=value, font=FONT_BODY, text_color=TEXT_PRIMARY, anchor="w").pack(side="left")
            
        add_row("Version", AppService.APP_VERSION)
        add_row("Technology", "Python + CustomTkinter")

    def refresh(self):
        pass
