"""
AutoEverGreen GUI — Theme and Color System
Dark charcoal developer-tool aesthetic with evergreen accent.
"""

# ──────────────────────────────────────────────
# PALETTE
# ──────────────────────────────────────────────
BG_BASE      = "#0d0f0e"   # near-black, slight green tint
BG_SURFACE   = "#141917"   # card / panel background
BG_SURFACE2  = "#1c2220"   # raised elements inside panels
BG_HOVER     = "#1f2826"   # hover state on nav items

ACCENT       = "#2ecc71"   # evergreen main accent (buttons, active)
ACCENT_DIM   = "#1a7d44"   # dimmed accent (inactive indicators)
ACCENT_MUTED = "#1d4d2e"   # very muted accent for highlights

BORDER       = "#252e28"   # subtle panel border
BORDER_LIGHT = "#2e3d35"   # slightly lighter dividers

TEXT_PRIMARY   = "#e8f0eb"  # main readable text
TEXT_SECONDARY = "#7a9685"  # secondary / metadata
TEXT_MUTED     = "#45574d"  # placeholder, disabled
TEXT_ACCENT    = "#2ecc71"  # accent-colored text

STATUS_SUCCESS = "#2ecc71"
STATUS_PENDING = "#f0a500"
STATUS_FAILED  = "#e74c3c"
STATUS_SKIPPED = "#45574d"
STATUS_DISABLED= "#2e3d35"

# ──────────────────────────────────────────────
# TYPOGRAPHY
# ──────────────────────────────────────────────
FONT_FAMILY  = "Segoe UI"
FONT_MONO_BASE = "Consolas"
FONT_MONO      = (FONT_MONO_BASE, 12)

FONT_TITLE    = (FONT_FAMILY, 22, "bold")
FONT_HEADING  = (FONT_FAMILY, 13, "bold")
FONT_SUBHEAD  = (FONT_FAMILY, 11, "bold")
FONT_BODY     = (FONT_FAMILY, 11)
FONT_SMALL    = (FONT_FAMILY, 10)
FONT_TINY     = (FONT_FAMILY, 9)
FONT_MONO_SM  = (FONT_MONO_BASE, 10)
FONT_MONO_XS  = (FONT_MONO_BASE, 9)
FONT_NAV      = (FONT_FAMILY, 12, "bold")
FONT_STAT_NUM = (FONT_FAMILY, 28, "bold")
FONT_STAT_LBL = (FONT_FAMILY, 10)

# ──────────────────────────────────────────────
# SIZING
# ──────────────────────────────────────────────
SIDEBAR_WIDTH    = 200
CORNER_RADIUS    = 6
BORDER_WIDTH     = 1
PAD_SECTION      = 20
PAD_INNER        = 12
PAD_SMALL        = 6

# ──────────────────────────────────────────────
# STATUS LABELS
# ──────────────────────────────────────────────
STATUS_LABELS = {
    "success":  ("✓ Completed", STATUS_SUCCESS),
    "error":    ("✗ Failed",    STATUS_FAILED),
    "pending":  ("◷ Pending",   STATUS_PENDING),
    "skipped":  ("→ Skipped",   STATUS_SKIPPED),
    "disabled": ("○ Disabled",  STATUS_DISABLED),
}

def get_status_display(status: str):
    return STATUS_LABELS.get(status, (f"? {status}", TEXT_MUTED))

# ──────────────────────────────────────────────
# CTK APPEARANCE DEFAULTS
# ──────────────────────────────────────────────
CTK_DEFAULTS = {
    "appearance_mode": "dark",
    "color_theme": "green",
}
