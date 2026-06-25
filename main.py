"""
Modern UI shell for PyTask, built on CustomTkinter.
Run: python main.py
Install first: pip install customtkinter

This file shows the PATTERN (tabs, cards, toggle, fade-in, task list)
using a trimmed task list view. Once you're happy with the look, you
migrate the rest of your widgets (calendar popup, rewards section, etc.)
the same way: same logic, swapped widget classes.
"""

import customtkinter as ctk
from ui import theme, home_tab, tasks_tab
import task_manager as tm

theme.apply_appearance("dark")


class PyTaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyTask — To-Do List")

        # ---- Responsive sizing (kept from your original approach) ----
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{int(sw * 0.6)}x{int(sh * 0.65)}")
        self.minsize(640, 480)

        tm.load_tasks()
        tm.load_streak()

        self._build_header()
        self._build_tabs()
        self._fade_in()

    # ---- Header with dark/light toggle ----
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 0))

        ctk.CTkLabel(
            header, text="PyTask", font=theme.font_title()
        ).pack(side="left")

        self.mode_switch = ctk.CTkSwitch(
            header, text="Light mode",
            font=theme.font_body(),
            command=self._toggle_mode,
            progress_color=theme.ACCENT,
        )
        self.mode_switch.pack(side="right")

    def _toggle_mode(self):
        is_light = self.mode_switch.get() == 1
        ctk.set_appearance_mode("light" if is_light else "dark")

    # ---- Tabs ----
    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(
            self, corner_radius=theme.CARD_RADIUS,
            segmented_button_selected_color=theme.ACCENT,
            segmented_button_selected_hover_color=theme.ACCENT_HOVER,
        )
        self.tabs.pack(fill="both", expand=True, padx=24, pady=20)
        self.tabs.add("Today")
        self.tabs.add("Tasks")

        self._build_today_tab(self.tabs.tab("Today"))
        self._build_tasks_tab(self.tabs.tab("Tasks"))

    # ---- "Today" tab: delegated to ui/home_tab.py ----
    def _build_today_tab(self, parent):
        self.home_widgets = home_tab.build(parent)

    # ---- "Tasks" tab: delegated to ui/tasks_tab.py ----
    def _build_tasks_tab(self, parent):
        self.tasks_widgets = tasks_tab.build(parent)
        # Let tasks_tab notify us when data changes, so we can refresh Today
        self.tasks_widgets["on_change"] = lambda: home_tab.refresh(self.home_widgets)

    # (Today tab refresh now handled by home_tab.refresh(self.home_widgets))
    # (Tasks tab rendering/events now handled entirely by ui/tasks_tab.py)

    # ---- Subtle fade-in on launch (CustomTkinter has no real tween engine,
    # so we approximate it via the window's alpha channel) ----
    def _fade_in(self, alpha=0.0):
        self.attributes("-alpha", alpha)
        if alpha < 1.0:
            self.after(15, lambda: self._fade_in(alpha + 0.06))


if __name__ == "__main__":
    app = PyTaskApp()
    app.mainloop()