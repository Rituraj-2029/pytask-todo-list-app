"""
The 'Today' tab: progress card, streak/rewards card, and a top-3 preview
of upcoming uncompleted tasks.

This is a self-contained component — main.py just calls build() and gets
back a dict of widget references it needs to refresh later (progress bar,
labels, preview list), without needing to know HOW any of it is built.
"""

import customtkinter as ctk
from . import theme
import task_manager as tm


def build(parent):
    """
    Builds the Today tab inside `parent` (a CTkFrame from the tabview).
    Returns a dict of widgets that need to be refreshed externally
    (e.g. after a task is added/completed elsewhere in the app).
    """
    parent.grid_columnconfigure((0, 1), weight=1, uniform="col")
    parent.grid_rowconfigure(1, weight=1)

    # ---- Top row: Progress card + Streak card ----
    progress_card = _card(parent)
    progress_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(10, 10))

    ctk.CTkLabel(progress_card, text="My Progress", font=theme.font_label()).pack(
        anchor="w", padx=18, pady=(18, 6)
    )
    progress_bar = ctk.CTkProgressBar(
        progress_card, progress_color=theme.ACCENT, height=14, corner_radius=7,
    )
    progress_bar.set(0)
    progress_bar.pack(fill="x", padx=18, pady=4)

    progress_label = ctk.CTkLabel(
        progress_card, text="0/0 completed (0%)", font=theme.font_body()
    )
    progress_label.pack(anchor="w", padx=18, pady=(4, 18))

    streak_card = _card(parent)
    streak_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=(10, 10))

    ctk.CTkLabel(streak_card, text="Rewards", font=theme.font_label()).pack(
        anchor="w", padx=18, pady=(18, 6)
    )
    streak_label = ctk.CTkLabel(streak_card, text="Streak: 0 day(s)", font=theme.font_body())
    streak_label.pack(anchor="w", padx=18, pady=4)

    streak_message = ctk.CTkLabel(
        streak_card, text="Start your streak today!",
        font=theme.font_body(), text_color=theme.ACCENT,
    )
    streak_message.pack(anchor="w", padx=18, pady=(0, 18))

    # ---- Bottom row: "My Tasks (top 3)" preview card ----
    preview_card = _card(parent)
    preview_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
    preview_card.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(preview_card, text="My Tasks (top 3)", font=theme.font_label()).pack(
        anchor="w", padx=18, pady=(18, 6)
    )
    preview_list_frame = ctk.CTkFrame(preview_card, fg_color="transparent")
    preview_list_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    widgets = {
        "progress_bar": progress_bar,
        "progress_label": progress_label,
        "streak_label": streak_label,
        "streak_message": streak_message,
        "preview_list_frame": preview_list_frame,
    }

    refresh(widgets)
    return widgets


def refresh(widgets):
    """Call this any time tasks/streak data changes elsewhere in the app."""
    completed, total, percent = tm.progress_stats()
    widgets["progress_bar"].set(percent / 100)
    widgets["progress_label"].configure(text=f"{completed}/{total} completed ({percent:.0f}%)")

    widgets["streak_label"].configure(text=f"Streak: {tm.streak} day(s)")
    if tm.streak >= 5:
        msg = "You're on fire!"
    elif tm.streak >= 1:
        msg = "Keep your streak going!"
    else:
        msg = "Start your streak today!"
    widgets["streak_message"].configure(text=msg)

    _refresh_preview(widgets["preview_list_frame"])


def _refresh_preview(frame):
    for child in frame.winfo_children():
        child.destroy()

    top3 = tm.get_top_uncompleted(limit=3)
    if not top3:
        ctk.CTkLabel(
            frame, text="You're all caught up, no work due soon!",
            font=theme.font_body(),
        ).pack(anchor="w", pady=4)
        return

    for task in top3:
        ctk.CTkLabel(
            frame,
            text=f"•  {task['title']}  ({task['month']}/{task['day']})",
            font=theme.font_body(), anchor="w",
        ).pack(anchor="w", pady=3, fill="x")


def _card(parent):
    return ctk.CTkFrame(parent, corner_radius=theme.CARD_RADIUS)