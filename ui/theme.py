"""
Centralized design tokens for the app.
Keeping colors/fonts here means you change the look in ONE place,
instead of hunting through every widget definition.
"""

import customtkinter as ctk

# ---- Fonts ----
# CustomTkinter respects system fonts. "Segoe UI" is clean and native on
# Windows; swap for "SF Pro Display" on Mac or "Inter" if you bundle it.
FONT_FAMILY = "Segoe UI"

def font_title():
    return ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold")

def font_subtitle():
    return ctk.CTkFont(family=FONT_FAMILY, size=13)

def font_label():
    return ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")

def font_body():
    return ctk.CTkFont(family=FONT_FAMILY, size=12)

def font_button():
    return ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold")


# ---- Accent color (used for buttons, progress bar, highlights) ----
# CustomTkinter widgets natively switch bg/fg between light & dark mode,
# so you mostly only need to define the ACCENT — not every gray shade.
ACCENT = "#7C5CFC"        # purple accent, close to your original PRIMARY
ACCENT_HOVER = "#6645E0"

CARD_RADIUS = 14           # corner radius used everywhere for consistency
BUTTON_RADIUS = 10


def apply_appearance(mode: str = "dark"):
    """Call once at startup. mode = 'dark' | 'light' | 'system'"""
    ctk.set_appearance_mode(mode)
    ctk.set_default_color_theme("dark-blue")  # base theme; we override accent per-widget