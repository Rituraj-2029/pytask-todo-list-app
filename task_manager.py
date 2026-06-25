"""
Pure data/logic layer — NO Tkinter imports allowed in this file.
This is the big architectural win of the migration: this file works
identically no matter what GUI (or no GUI / a future web version) sits on top.

UI code calls these functions and handles displaying results/errors itself.
"""

import json
import os
from datetime import datetime, timedelta

OFFSET_HOURS = -5
STREAK_FILE = "streak.json"
TASKS_FILE = "tasks.json"

CATEGORIES = ["School", "Sports", "Work", "Urgent", "Personal"]
FILTERS = ["All", "School", "Sports", "Work", "Urgent", "Personal", "Completed", "Uncompleted"]

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

tasks = []
streak = 0
last_completed_day = None


class TaskError(Exception):
    """Raised for invalid task input. UI layer catches this and shows a popup."""
    pass


def get_local_datetime():
    return datetime.now() + timedelta(hours=OFFSET_HOURS)


def get_local_date():
    return get_local_datetime().date()


def add_task(title, month_str, day_str, category):
    title = title.strip()
    month_str = month_str.strip()
    day_str = day_str.strip()

    if not title or not month_str or not day_str:
        raise TaskError("Enter the task and due date!")
    if not category or category == "Category":
        raise TaskError("Select a category!")

    try:
        month, day = int(month_str), int(day_str)
    except ValueError:
        raise TaskError("Month and day must be numbers!")

    if not (1 <= month <= 12):
        raise TaskError("Enter a valid month number (1-12)!")
    if not (1 <= day <= 31):
        raise TaskError("Enter a valid day (1-31)!")
    if month == 2 and day > 29:
        raise TaskError("February has at most 29 days!")
    if month in (4, 6, 9, 11) and day > 30:
        raise TaskError("That month has only 30 days!")

    tasks.append({
        "title": title, "category": category,
        "month": month, "day": day, "completed": False,
    })


def delete_tasks(indexes):
    """Deletes tasks at the given indexes. Silently skips any index that's
    out of range (e.g. stale from a UI selection made before the list changed),
    rather than crashing — deletion should always be safe to call."""
    for i in sorted(indexes, reverse=True):
        if 0 <= i < len(tasks):
            del tasks[i]


def delete_completed_tasks():
    """Removes every task marked completed=True. Matches old delete_crossed_item()."""
    global tasks
    tasks = [t for t in tasks if not t["completed"]]


def set_completed(indexes, value: bool):
    for i in indexes:
        tasks[i]["completed"] = value


def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def load_tasks():
    global tasks
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []


def save_streak():
    data = {
        "streak": streak,
        "last_completed_day": str(last_completed_day) if last_completed_day else None,
    }
    with open(STREAK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_streak():
    global streak, last_completed_day
    if not os.path.exists(STREAK_FILE):
        return
    try:
        with open(STREAK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        streak = data.get("streak", 0)
        date_str = data.get("last_completed_day")
        last_completed_day = (
            datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        )
    except Exception:
        streak, last_completed_day = 0, None


def month_name(month) -> str:
    """Accepts an int or numeric string (1-12) and returns the month name."""
    try:
        idx = int(month)
    except (TypeError, ValueError):
        return "Invalid Month"
    if 1 <= idx <= 12:
        return MONTH_NAMES[idx - 1]
    return "Invalid Month"


def filtered_indexes(selected_filter: str):
    """
    Returns the list of indexes into `tasks` that match the selected filter,
    e.g. 'All', 'Completed', 'Uncompleted', or a category name.
    This replaces the filtering logic that used to live inside refresh_listbox().
    """
    result = []
    for i, task in enumerate(tasks):
        if selected_filter == "All":
            match = True
        elif selected_filter == "Completed":
            match = task["completed"]
        elif selected_filter == "Uncompleted":
            match = not task["completed"]
        else:
            match = task["category"] == selected_filter
        if match:
            result.append(i)
    return result


def get_top_uncompleted(limit=3):
    """Used by the 'Today' tab preview list."""
    uncompleted = [t for t in tasks if not t["completed"]]
    return uncompleted[:limit]


def progress_stats():
    """Returns (completed_count, total_count, percent) for the progress bar/label."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    percent = (completed / total * 100) if total else 0
    return completed, total, percent



def check_streak_increment():
    """Call after marking tasks complete. Returns new streak count, or None if unchanged."""
    global streak, last_completed_day
    if not tasks or not all(t["completed"] for t in tasks):
        return None

    today = get_local_date()
    if last_completed_day == today:
        return None  # already counted today

    streak = streak + 1 if last_completed_day == today - timedelta(days=1) else 1
    last_completed_day = today
    save_streak()
    return streak
