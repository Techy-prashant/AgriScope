"""
AutoEverGreen GUI — Reusable Components
Premium dark-theme widget building blocks.
"""
from __future__ import annotations
import tkinter as tk
import customtkinter as ctk
from typing import Optional, Callable
from .theme import *


# ──────────────────────────────────────────────────────────────────────
# CARD / PANEL
# ──────────────────────────────────────────────────────────────────────

class Card(ctk.CTkFrame):
    """Styled panel with optional title header."""
    def __init__(self, parent, title: Optional[str] = None, **kw):
        kw.setdefault("fg_color", BG_SURFACE)
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("border_width", BORDER_WIDTH)
        kw.setdefault("border_color", BORDER)
        super().__init__(parent, **kw)
        if title:
            lbl = ctk.CTkLabel(
                self, text=title.upper(),
                font=FONT_TINY, text_color=TEXT_MUTED,
                anchor="w"
            )
            lbl.pack(anchor="w", padx=PAD_INNER, pady=(PAD_INNER, 4))
            sep = ctk.CTkFrame(self, height=1, fg_color=BORDER, corner_radius=0)
            sep.pack(fill="x", padx=0)


class SectionLabel(ctk.CTkLabel):
    """Small all-caps section header."""
    def __init__(self, parent, text: str, **kw):
        kw.setdefault("font", FONT_TINY)
        kw.setdefault("text_color", TEXT_MUTED)
        kw.setdefault("anchor", "w")
        super().__init__(parent, text=text.upper(), **kw)


class Divider(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        kw.setdefault("height", 1)
        kw.setdefault("fg_color", BORDER)
        kw.setdefault("corner_radius", 0)
        super().__init__(parent, **kw)


# ──────────────────────────────────────────────────────────────────────
# STAT BOX
# ──────────────────────────────────────────────────────────────────────

class StatBox(ctk.CTkFrame):
    """Single numeric KPI block."""
    def __init__(self, parent, label: str, value: str = "—",
                 color: str = TEXT_PRIMARY, **kw):
        kw.setdefault("fg_color", BG_SURFACE2)
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("border_width", BORDER_WIDTH)
        kw.setdefault("border_color", BORDER)
        super().__init__(parent, **kw)
        self._num_var = tk.StringVar(value=value)
        self._lbl_color = color

        num_lbl = ctk.CTkLabel(
            self, textvariable=self._num_var,
            font=FONT_STAT_NUM, text_color=color
        )
        num_lbl.pack(padx=PAD_INNER, pady=(PAD_INNER, 2))

        desc = ctk.CTkLabel(
            self, text=label,
            font=FONT_STAT_LBL, text_color=TEXT_MUTED
        )
        desc.pack(padx=PAD_INNER, pady=(0, PAD_INNER))

    def set(self, value: str):
        self._num_var.set(value)


# ──────────────────────────────────────────────────────────────────────
# STATUS BADGE
# ──────────────────────────────────────────────────────────────────────

class StatusBadge(ctk.CTkLabel):
    """Colored text badge for job status."""
    def __init__(self, parent, status: str = "pending", **kw):
        label, color = get_status_display(status)
        kw.setdefault("font", FONT_SMALL)
        kw.setdefault("text_color", color)
        kw.setdefault("anchor", "w")
        super().__init__(parent, text=label, **kw)
        self._current = status

    def set_status(self, status: str):
        if status != self._current:
            label, color = get_status_display(status)
            self.configure(text=label, text_color=color)
            self._current = status


# ──────────────────────────────────────────────────────────────────────
# PRIMARY BUTTON
# ──────────────────────────────────────────────────────────────────────

class PrimaryButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("fg_color", ACCENT)
        kw.setdefault("hover_color", ACCENT_DIM)
        kw.setdefault("text_color", "#0d0f0e")
        kw.setdefault("font", (FONT_FAMILY, 12, "bold"))
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("height", 36)
        super().__init__(parent, text=text, command=command, **kw)


class SecondaryButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("fg_color", BG_SURFACE2)
        kw.setdefault("hover_color", BG_HOVER)
        kw.setdefault("text_color", TEXT_SECONDARY)
        kw.setdefault("border_width", BORDER_WIDTH)
        kw.setdefault("border_color", BORDER)
        kw.setdefault("font", FONT_BODY)
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("height", 32)
        super().__init__(parent, text=text, command=command, **kw)


class DangerButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("fg_color", "#3d1a1a")
        kw.setdefault("hover_color", "#5a2222")
        kw.setdefault("text_color", STATUS_FAILED)
        kw.setdefault("border_width", BORDER_WIDTH)
        kw.setdefault("border_color", "#5a2222")
        kw.setdefault("font", FONT_BODY)
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("height", 32)
        super().__init__(parent, text=text, command=command, **kw)


# ──────────────────────────────────────────────────────────────────────
# PROGRESS BAR CARD
# ──────────────────────────────────────────────────────────────────────

class ProgressCard(Card):
    def __init__(self, parent, **kw):
        super().__init__(parent, title="Progress", **kw)
        self._bar = ctk.CTkProgressBar(
            self, progress_color=ACCENT,
            fg_color=BG_SURFACE2,
            corner_radius=4, height=10
        )
        self._bar.set(0)
        self._bar.pack(fill="x", padx=PAD_INNER, pady=(PAD_INNER, 4))

        self._lbl_var = tk.StringVar(value="0 / 0 completed")
        lbl = ctk.CTkLabel(
            self, textvariable=self._lbl_var,
            font=FONT_SMALL, text_color=TEXT_SECONDARY, anchor="w"
        )
        lbl.pack(anchor="w", padx=PAD_INNER, pady=(0, PAD_INNER))

    def set_progress(self, completed: int, total: int):
        if total > 0:
            self._bar.set(completed / total)
        else:
            self._bar.set(0)
        self._lbl_var.set(f"{completed} / {total} completed")


# ──────────────────────────────────────────────────────────────────────
# CONNECTION DOT
# ──────────────────────────────────────────────────────────────────────

class ConnectionDot(ctk.CTkLabel):
    def __init__(self, parent, **kw):
        kw.setdefault("font", FONT_SMALL)
        kw.setdefault("text_color", TEXT_MUTED)
        super().__init__(parent, text="● Checking...", **kw)

    def set_connected(self, ok: bool):
        if ok:
            self.configure(text="● Connected", text_color=STATUS_SUCCESS)
        else:
            self.configure(text="● Unreachable", text_color=STATUS_FAILED)

    def set_checking(self):
        self.configure(text="● Checking...", text_color=STATUS_PENDING)


# ──────────────────────────────────────────────────────────────────────
# LOG LINE
# ──────────────────────────────────────────────────────────────────────

def log_line_color(line: str) -> str:
    if " - ERROR - " in line or "ERROR" in line[:20]:
        return STATUS_FAILED
    if " - WARNING - " in line or "WARN" in line[:20]:
        return STATUS_PENDING
    if "✓" in line or "SUCCESS" in line:
        return STATUS_SUCCESS
    return TEXT_SECONDARY


# ──────────────────────────────────────────────────────────────────────
# SCROLLABLE TABLE ROW
# ──────────────────────────────────────────────────────────────────────

class TableRow(ctk.CTkFrame):
    """A single row in a table-like list."""
    def __init__(self, parent, columns: list, widths: list,
                 on_click: Optional[Callable] = None,
                 is_header: bool = False, **kw):
        bg = BG_SURFACE2 if is_header else BG_SURFACE
        kw.setdefault("fg_color", bg)
        kw.setdefault("corner_radius", 0)
        kw.setdefault("border_width", 0)
        super().__init__(parent, **kw)
        self.configure(cursor="hand2" if on_click else "arrow")

        for col, w in zip(columns, widths):
            font = FONT_SUBHEAD if is_header else FONT_SMALL
            color = TEXT_MUTED if is_header else TEXT_SECONDARY
            lbl = ctk.CTkLabel(
                self, text=str(col), font=font, text_color=color,
                anchor="w", width=w
            )
            lbl.pack(side="left", padx=(6, 0), pady=4)

        if on_click:
            self.bind("<Button-1>", lambda e: on_click())
            for child in self.winfo_children():
                child.bind("<Button-1>", lambda e: on_click())

        # hover effect
        if not is_header and on_click:
            self.bind("<Enter>", lambda e: self.configure(fg_color=BG_HOVER))
            self.bind("<Leave>", lambda e: self.configure(fg_color=BG_SURFACE))


# ──────────────────────────────────────────────────────────────────────
# NAV BUTTON
# ──────────────────────────────────────────────────────────────────────

class NavButton(ctk.CTkButton):
    def __init__(self, parent, text: str, command=None, **kw):
        kw.setdefault("fg_color", "transparent")
        kw.setdefault("hover_color", BG_HOVER)
        kw.setdefault("text_color", TEXT_SECONDARY)
        kw.setdefault("anchor", "w")
        kw.setdefault("font", FONT_NAV)
        kw.setdefault("corner_radius", CORNER_RADIUS)
        kw.setdefault("height", 38)
        super().__init__(parent, text=text, command=command, **kw)
        self._active = False

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.configure(
                fg_color=ACCENT_MUTED, text_color=TEXT_ACCENT,
                hover_color=ACCENT_MUTED
            )
        else:
            self.configure(
                fg_color="transparent", text_color=TEXT_SECONDARY,
                hover_color=BG_HOVER
            )


# ──────────────────────────────────────────────────────────────────────
# EXECUTION LOG STREAM PANEL
# ──────────────────────────────────────────────────────────────────────

class ExecutionPanel(ctk.CTkToplevel):
    """
    Modal-style overlay showing live execution progress lines.
    Stays on top, non-blocking (uses after() callbacks to refresh).
    """
    def __init__(self, parent, title="Execution Progress"):
        super().__init__(parent)
        self.title(title)
        self.geometry("640x420")
        self.resizable(False, False)
        self.configure(fg_color=BG_BASE)
        self.grab_set()

        hdr = ctk.CTkLabel(
            self, text="● EXECUTING",
            font=(FONT_FAMILY, 14, "bold"), text_color=STATUS_PENDING
        )
        hdr.pack(padx=20, pady=(18, 8), anchor="w")
        self._hdr = hdr

        self._text = ctk.CTkTextbox(
            self, fg_color=BG_SURFACE, text_color=TEXT_SECONDARY,
            font=FONT_MONO_SM, corner_radius=CORNER_RADIUS,
            border_width=BORDER_WIDTH, border_color=BORDER,
            state="disabled", wrap="word"
        )
        self._text.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self._close_btn = SecondaryButton(self, text="Close", command=self.destroy)
        self._close_btn.configure(state="disabled")
        self._close_btn.pack(padx=20, pady=(0, 16), anchor="e")

    def append(self, line: str):
        self._text.configure(state="normal")
        self._text.insert("end", line + "\n")
        self._text.see("end")
        self._text.configure(state="disabled")

    def finish(self, success: bool, summary: str):
        self._hdr.configure(
            text=f"{'✓ COMPLETE' if success else '✗ FAILED'} — {summary}",
            text_color=STATUS_SUCCESS if success else STATUS_FAILED
        )
        self._close_btn.configure(state="normal")
