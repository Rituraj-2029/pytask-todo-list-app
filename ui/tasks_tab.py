"""
The 'Tasks' tab: everything for creating, filtering, completing, and
deleting tasks — entry field, category dropdown, deadline (month/day)
inputs with a calendar picker, a search/filter combobox, and the
scrollable task-card list.

Like home_tab.py, this exposes build(parent) -> widgets dict and
refresh(widgets) -> None. All validation/business logic stays in
task_manager.py; this file only handles layout and wiring callbacks.
"""

import calendar
import customtkinter as ctk
from . import theme
import task_manager as tm


def build(parent):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(3, weight=1)

    widgets = {}

    _build_entry_row(parent, widgets)
    _build_deadline_row(parent, widgets)
    _build_filter_row(parent, widgets)
    _build_task_list(parent, widgets)
    _build_action_row(parent, widgets)

    refresh(widgets)
    return widgets


# ---------------------------------------------------------------- entry row
def _build_entry_row(parent, widgets):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.grid(row=0, column=0, sticky="ew", pady=(10, 8))
    row.grid_columnconfigure(0, weight=1)

    task_entry = ctk.CTkEntry(
        row, placeholder_text="Add a task...",
        font=theme.font_body(), height=40,
        corner_radius=theme.BUTTON_RADIUS,
    )
    task_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

    category_var = ctk.StringVar(value="Category")
    category_menu = ctk.CTkOptionMenu(
        row, values=tm.CATEGORIES, variable=category_var,
        width=130, height=40, corner_radius=theme.BUTTON_RADIUS,
        fg_color=theme.ACCENT, button_color=theme.ACCENT,
        button_hover_color=theme.ACCENT_HOVER,
        font=theme.font_body(),
    )
    category_menu.grid(row=0, column=1, padx=(0, 10))

    add_btn = ctk.CTkButton(
        row, text="Add Task", width=110, height=40,
        corner_radius=theme.BUTTON_RADIUS,
        fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
        font=theme.font_button(),
        command=lambda: _on_add_task(widgets),
    )
    add_btn.grid(row=0, column=2)

    widgets["task_entry"] = task_entry
    widgets["category_var"] = category_var


# ------------------------------------------------------------- deadline row
def _build_deadline_row(parent, widgets):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.grid(row=1, column=0, sticky="ew", pady=(0, 8))

    month_entry = ctk.CTkEntry(
        row, placeholder_text="Month (1-12)", width=130,
        font=theme.font_body(), height=36, corner_radius=theme.BUTTON_RADIUS,
    )
    month_entry.grid(row=0, column=0, padx=(0, 8))

    day_entry = ctk.CTkEntry(
        row, placeholder_text="Day (1-31)", width=110,
        font=theme.font_body(), height=36, corner_radius=theme.BUTTON_RADIUS,
    )
    day_entry.grid(row=0, column=1, padx=(0, 8))

    calendar_btn = ctk.CTkButton(
        row, text="Open Calendar", width=140, height=36,
        corner_radius=theme.BUTTON_RADIUS,
        fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
        font=theme.font_button(),
        command=lambda: _open_calendar(parent, widgets),
    )
    calendar_btn.grid(row=0, column=2)

    widgets["month_entry"] = month_entry
    widgets["day_entry"] = day_entry


# --------------------------------------------------------------- filter row
def _build_filter_row(parent, widgets):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.grid(row=2, column=0, sticky="ew", pady=(0, 12))

    ctk.CTkLabel(row, text="Filter:", font=theme.font_body()).pack(side="left", padx=(0, 8))

    filter_var = ctk.StringVar(value="All")
    filter_menu = ctk.CTkOptionMenu(
        row, values=tm.FILTERS, variable=filter_var,
        width=150, height=34, corner_radius=theme.BUTTON_RADIUS,
        fg_color=theme.ACCENT, button_color=theme.ACCENT,
        button_hover_color=theme.ACCENT_HOVER,
        font=theme.font_body(),
        command=lambda _: _refresh_task_list(widgets),
    )
    filter_menu.pack(side="left")

    widgets["filter_var"] = filter_var


# --------------------------------------------------------------- task list
def _build_task_list(parent, widgets):
    list_frame = ctk.CTkScrollableFrame(parent, corner_radius=theme.CARD_RADIUS)
    list_frame.grid(row=3, column=0, sticky="nsew")
    list_frame.grid_columnconfigure(0, weight=1)
    widgets["list_frame"] = list_frame


# ------------------------------------------------------------- action row
def _build_action_row(parent, widgets):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.grid(row=4, column=0, sticky="ew", pady=(12, 4))
    row.grid_columnconfigure((0, 1, 2), weight=1)

    ctk.CTkButton(
        row, text="Delete Selected", height=38, corner_radius=theme.BUTTON_RADIUS,
        font=theme.font_button(),
        command=lambda: _on_delete_selected(widgets),
    ).grid(row=0, column=0, padx=4, sticky="ew")

    ctk.CTkButton(
        row, text="Clear Checked Items", height=38, corner_radius=theme.BUTTON_RADIUS,
        font=theme.font_button(),
        command=lambda: _on_clear_checked(widgets),
    ).grid(row=0, column=1, padx=4, sticky="ew")

    ctk.CTkButton(
        row, text="Save Tasks", height=38, corner_radius=theme.BUTTON_RADIUS,
        fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
        font=theme.font_button(),
        command=lambda: _on_save(widgets),
    ).grid(row=0, column=2, padx=4, sticky="ew")


# ---------------------------------------------------------------- calendar
def _open_calendar(parent, widgets):
    today = tm.get_local_date()
    month_name = calendar.month_name[today.month]

    popup = ctk.CTkToplevel(parent)
    popup.title("Select a day")
    popup.geometry("300x320")
    popup.grab_set()  # modal-ish: keeps focus on the popup

    ctk.CTkLabel(
        popup, text=f"{month_name} {today.year}", font=theme.font_label(),
    ).pack(pady=(16, 10))

    grid_frame = ctk.CTkFrame(popup, fg_color="transparent")
    grid_frame.pack(padx=10)

    days_in_month = calendar.monthrange(today.year, today.month)[1]

    def select_day(d):
        widgets["month_entry"].delete(0, "end")
        widgets["month_entry"].insert(0, str(today.month))
        widgets["day_entry"].delete(0, "end")
        widgets["day_entry"].insert(0, str(d))
        popup.destroy()

    for i in range(days_in_month):
        r, c = divmod(i, 7)
        ctk.CTkButton(
            grid_frame, text=str(i + 1), width=34, height=30,
            corner_radius=theme.BUTTON_RADIUS,
            fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
            font=theme.font_body(),
            command=lambda d=i + 1: select_day(d),
        ).grid(row=r, column=c, padx=2, pady=2)


# ----------------------------------------------------------------- render
def refresh(widgets):
    _refresh_task_list(widgets)


def _refresh_task_list(widgets):
    frame = widgets["list_frame"]
    for child in frame.winfo_children():
        child.destroy()

    # Any previously selected (checked for deletion) indexes are now stale,
    # since the checkboxes that tracked them were just destroyed above.
    widgets["_selected_indexes"] = set()

    selected_filter = widgets["filter_var"].get()
    indexes = tm.filtered_indexes(selected_filter)

    if not indexes:
        ctk.CTkLabel(
            frame, text="No tasks match this filter.", font=theme.font_body(),
        ).grid(row=0, column=0, pady=20)
        return

    for row_pos, real_index in enumerate(indexes):
        task = tm.tasks[real_index]
        card = ctk.CTkFrame(frame, corner_radius=theme.BUTTON_RADIUS)
        card.grid(row=row_pos, column=0, sticky="ew", pady=4, padx=2)
        card.grid_columnconfigure(1, weight=1)

        checked = ctk.BooleanVar(value=task["completed"])
        ctk.CTkCheckBox(
            card, text="", variable=checked, width=24,
            fg_color=theme.ACCENT, hover_color=theme.ACCENT_HOVER,
            command=lambda idx=real_index, var=checked: _on_toggle(widgets, idx, var),
        ).grid(row=0, column=0, padx=(12, 6), pady=10)

        text_color = "gray50" if task["completed"] else None
        month_label = tm.month_name(task["month"])[:3]
        ctk.CTkLabel(
            card,
            text=f"{task['title']}   ·   {task['category']}   ·   {month_label} {task['day']}",
            font=theme.font_body(), text_color=text_color, anchor="w",
        ).grid(row=0, column=1, sticky="ew", padx=6)

        # selection checkbox for "Delete Selected" (separate from completed-check)
        selected = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            card, text="Select", variable=selected, width=24,
            font=theme.font_body(),
            command=lambda idx=real_index, var=selected: _on_select(widgets, idx, var),
        ).grid(row=0, column=2, padx=(6, 12), pady=10)


# -------------------------------------------------------------- callbacks
def _on_add_task(widgets):
    try:
        tm.add_task(
            widgets["task_entry"].get(),
            widgets["month_entry"].get(),
            widgets["day_entry"].get(),
            widgets["category_var"].get(),
        )
    except tm.TaskError as e:
        _toast(widgets, str(e))
        return

    widgets["task_entry"].delete(0, "end")
    widgets["month_entry"].delete(0, "end")
    widgets["day_entry"].delete(0, "end")
    widgets["category_var"].set("Category")

    tm.save_tasks()
    _refresh_task_list(widgets)
    _notify_home(widgets)


def _on_toggle(widgets, idx, var):
    tm.set_completed([idx], var.get())
    tm.save_tasks()
    new_streak = tm.check_streak_increment()
    if new_streak:
        _toast(widgets, f"Streak! {new_streak} day(s)")
    _refresh_task_list(widgets)
    _notify_home(widgets)


def _on_select(widgets, idx, var):
    selected_set = widgets.setdefault("_selected_indexes", set())
    if var.get():
        selected_set.add(idx)
    else:
        selected_set.discard(idx)


def _on_delete_selected(widgets):
    selected_set = widgets.get("_selected_indexes", set())
    if not selected_set:
        _toast(widgets, "Select at least one task first.")
        return
    tm.delete_tasks(list(selected_set))
    widgets["_selected_indexes"] = set()
    tm.save_tasks()
    _refresh_task_list(widgets)
    _notify_home(widgets)


def _on_clear_checked(widgets):
    tm.delete_completed_tasks()
    tm.save_tasks()
    _refresh_task_list(widgets)
    _notify_home(widgets)


def _on_save(widgets):
    tm.save_tasks()
    _toast(widgets, "Tasks saved successfully.")


def _toast(widgets, message):
    """Non-blocking notice. Looks for a root window to attach to."""
    root = widgets["list_frame"].winfo_toplevel()
    toast = ctk.CTkLabel(
        root, text=message, font=theme.font_body(),
        fg_color=theme.ACCENT, text_color="white",
        corner_radius=8, padx=14, pady=8,
    )
    toast.place(relx=0.5, rely=0.95, anchor="s")
    root.after(2200, toast.destroy)


def _notify_home(widgets):
    """
    The Tasks tab doesn't own the Today tab's widgets, so it stores an
    optional callback (set by main.py) to trigger a Today-tab refresh
    after any change here. This keeps the two tabs decoupled.
    """
    callback = widgets.get("on_change")
    if callback:
        callback()
