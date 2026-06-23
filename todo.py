import tkinter as tk
import tkinter.messagebox 
from tkinter import ttk
import time
import os
from datetime import datetime, timedelta
import calendar
from datetime import datetime
import json

# ---- (Time Settings) ----
OFFSET_HOURS = -5

# ---- Settings ----
# --- Storage for all tasks ----
tasks = []
STREAK_FILE = "streak.txt" # file where streaks are saved

# functions for our times
def get_local_datetime():
    return datetime.now() + timedelta(hours=OFFSET_HOURS)

def get_local_date():
    return get_local_datetime().date()
    
# ---- Colors & Fonts ----
BG_MAIN   = "#121212"   # main window background (near-black)
BG_CARD   = "#1E1E1E"   # card / list background (dark gray)
PRIMARY   = "#BB86FC"   # accent color (purple like Android dark theme)
PRIMARY_D = "#9858E6"   # darker accent for hover / active
TEXT_MAIN = "#FFFFFF"   # main text color
TEXT_MUTED= "#B3B3B3"   # secondary text color
BORDER    = "#333333"   # subtle border color

TITLE_FONT  = ("Times New Roman", 25, "bold")
LABEL_FONT  = ("Times New Roman", 11)
BUTTON_FONT = ("Times New Roman", 10, "bold")
ENTRY_FONT  = ("Times New Roman", 11)

# ---- Main Frame ----
root = tk.Tk()

# ---- Style for Progress Bar ----
style = ttk.Style(root)
style.theme_use("clam")

style.configure("ProgressTracker.Horizontal.TProgressbar",
troughcolor=BG_CARD, #background behind the bar
background=PRIMARY, #bar fill color
bordercolor=BG_MAIN, 
lightcolor=PRIMARY,
darkcolor=PRIMARY
)

# Customizing the Combobox 
style.configure("Custom.TCombobox", 
fieldbackground=BG_CARD,
background=BG_CARD,
foreground=PRIMARY,
bordercolor="black",
lightcolor="black",
darkcolor="black",
arrowcolor= "white",
font=("Times New Roman", 11),
padding=4)

style.map(
    "Custom.TCombobox",
    fieldbackground=[("readonly", BG_CARD), ("focus", BG_CARD), ("active", BG_CARD)],
    background=[("readonly", BG_CARD), ("active", BG_CARD)],
    foreground=[("readonly", PRIMARY)],
    selectbackground=[("readonly", BG_CARD)],
    selectforeground=[("readonly", PRIMARY)],
    bordercolor=[("focus", PRIMARY), ("readonly", PRIMARY)],
    lightcolor=[("focus", PRIMARY)],
    darkcolor=[("focus", PRIMARY)]
)

root.option_add("*TCombobox*Listbox.background", BG_MAIN)
root.option_add("*TCombobox*Listbox.foreground", TEXT_MAIN)
root.option_add("*TCombobox*Listbox.selectBackground", BG_CARD)
root.option_add("*TCombobox*Listbox.selectForeground", PRIMARY)
root.option_add("*TCombobox*Listbox.font", ("Times New Roman", 11))

"""
TOGGLE THEME INCOMPLETE 
# ---- Colors & Fonts ----
# ---- Theme Definitions ----
LIGHT_THEME = {
    "BG_MAIN":   "#F8FAFC",
    "BG_CARD":   "#FFFFFF",
    "PRIMARY":   "#3B82F6",
    "PRIMARY_D": "#2563EB",
    "TEXT_MAIN": "#0F172A",
    "TEXT_MUTED":"#64748B",
    "BORDER":    "#E2E8F0",
    "PROGRESS":  "#22C55E",
    "TROUGH":    "#E5E7EB",  # progress bar track
}

DARK_THEME = {
    "BG_MAIN":   "#121212",
    "BG_CARD":   "#1E1E1E",
    "PRIMARY":   "#BB86FC",
    "PRIMARY_D": "#9858E6",
    "TEXT_MAIN": "#FFFFFF",
    "TEXT_MUTED":"#B3B3B3",
    "BORDER":    "#333333",
    "PROGRESS":  "#04AF2F",
    "TROUGH":    "#121212",  # same as BG_MAIN
}

current_theme = LIGHT_THEME

TITLE_FONT  = ("Times New Roman", 25, "bold")
LABEL_FONT  = ("Times New Roman", 11)
BUTTON_FONT = ("Times New Roman", 10, "bold")
ENTRY_FONT  = ("Times New Roman", 11)

# ---- Main Frame ----
root = tk.Tk()

# ---- Style for Progress Bar ----
style = ttk.Style(root)
style.theme_use("clam")


card_frames = [] # append your task list/card frames to this list

def apply_themes(theme):
    global BG_MAIN, BG_CARD, PRIMARY, PRIMARY_D, TEXT_MAIN, TEXT_MUTED, BORDER
    # Depedning on the user selects it chooses the 
    BG_MAIN   = theme["BG_MAIN"] 
    BG_CARD   = theme["BG_CARD"]
    PRIMARY   = theme["PRIMARY"]
    PRIMARY_D = theme["PRIMARY_D"]
    TEXT_MAIN = theme["TEXT_MAIN"]
    TEXT_MUTED= theme["TEXT_MUTED"]
    BORDER    = theme["BORDER"]
    
    #Window background
    root.configure(bg=BG_MAIN)
    
    #Progress bar style
    style.configure("ProgressTracker.Horizontal.TProgressbar",
troughcolor=theme["TROUGH"], 
#background behind the progress bar
background=theme["PROGRESS"], 
#bar fill color
bordercolor=BORDER
)
    
    # Update card frames (if you store them)
    for frame in card_frames:
        frame.configure(bg=BG_CARD, highlightbackground=BORDER, highlightcolor=BORDER)
        
    #Optionally walk through all widgets and recolor labels/buttons/entries
    for widget in root.winfo_children():
        recolor_widget(widget, theme)
    
def recolor_widget(widget, theme):
    #For containers, recurse
    for child in widget.winfor_children():
        recolor_widget(child, theme)
        
    if isinstance(widget, tk.Label):
        widget.configure(bg=theme["BG_MAIN"], fg=theme["TEXT_MAIN"])
    elif isinstance(widget, tk.Button):
        widget.configure(bg=theme["PRIMARY"],
        fg="#FFFFFF",
        activebackground=theme["PRIMARY_D"],
        activeforeground="#FFFFFF",
        highlightbackground=theme["BORDER"])
    elif isinstance(widget, tk.Entry):
        widget.configure(bg=theme["BG_CARD"], 
        fg=theme["TEXT_MAIN"], 
        insertbackground=theme["TEXT_MAIN"])
    elif isinstance(widget, ttk.Progressbar):
        widget.configure(bg=theme["BG_MAIN"])
        
        #Only change if it doesn't already have a special bg
        if not isinstance(widget, ttk.Progressbar):
            widget.configure(bg=theme["BG_MAIN"])


# ---- Define a Toggle Button ----
def toggle_theme():
    global current_theme
    if current_theme is LIGHT_THEME:
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    apply_theme(current_theme)


toggle_button = tk.Button(frame_get_started, 
text="Toggle Theme", font=("Times New Roman", 15), bg=BG_MAIN, fg=PRIMARY, command=toggle_theme)
toggle_button.pack(padx=10, pady=10)
"""
# --- Styled Buttons Function ----
def styled_button(master, text=None, command=None, width=None, **kwargs):
    return tk.Button(
        master,
        text=text,
        command=command,
        width=width,
        font=BUTTON_FONT,
        bg=PRIMARY,
        fg="#000000",
        activebackground=PRIMARY_D,
        activeforeground="#000000",
        bd=0,
        cursor="hand2",
        relief="flat",
        highlightthickness=0,
        **kwargs
        )
        
# ---- Notebook (2 tabs) ----
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)
#Tab 1: Get Started 
frame_get_started = tk.Frame(notebook, bg=BG_MAIN)
notebook.add(frame_get_started, text="Get Started")

#Tab 2: To-Do List Frame
frame_todo = tk.Frame(notebook, bg=BG_MAIN)
notebook.add(frame_todo, text="To-Do List")
    
# ----------------------------------------------------------------------
# ---- Code below provides a framework for the Get Started Mini-App ----
header_row = tk.Frame(frame_get_started, bg=BG_MAIN)
header_row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

# Today label (left)
get_started = tk.Label(header_row, font=("Times New Roman", 20, "bold"),
text="Today", bg=BG_MAIN, fg=PRIMARY)
get_started.pack(side=tk.TOP, anchor="nw")

# ---- Time label at top ----
time_label= tk.Label(header_row,
font=("Times New Roman", 12),
bg=BG_MAIN,
fg=TEXT_MAIN)

# ---- Time -----
def update_time():

    #apply manual offset
    local = get_local_datetime()
    
    current_time = f"{local.strftime('%A, %B')} {local.day}"
    time_label.config(text=current_time)
    root.after(1000, update_time)
    # update every 1000 ms
    
# --- Pack top labels & start time updates ----
time_label.pack(side=tk.LEFT, pady=(4,0))
update_time()

my_project_label = tk.Label(frame_get_started, text="My Projects (top 3)",
font=("Times New Roman", 15, "bold"), 
bg=BG_MAIN,
fg=PRIMARY)
my_project_label.pack(side=tk.TOP, anchor="nw", padx=10, pady=20)

listbox_top3 = tk.Listbox(frame_get_started, 
height=3, 
width=10,
bg=BG_CARD,
fg=TEXT_MAIN,
activestyle="none",
bd=0,
highlightthickness=0)    

listbox_top3.pack(side=tk.TOP, fill="x", padx=10)

# --- Mini progress bar in home screen ---

home_progress_frame = tk.Frame(frame_get_started, bg=BG_MAIN)
home_progress_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

# ---- Progress Bar ----
my_project_label = tk.Label(home_progress_frame, text="My Progress",
font=("Times New Roman", 15, "bold"), 
bg=BG_MAIN,
fg=PRIMARY)
my_project_label.pack(side=tk.TOP ,fill=tk.X, anchor="e")

progress_bar = ttk.Progressbar(home_progress_frame, 
orient="horizontal", 
length=50,
mode="determinate",
style="ProgressTracker.Horizontal.TProgressbar",
maximum=100)
progress_bar.pack(side=tk.TOP,fill=tk.X, pady=5)

# ---- Label under progress bar ----
progress_label = tk.Label(home_progress_frame, text="0% completed",
font=("Times New Roman", 12, "bold"),
bg=BG_MAIN,
fg=PRIMARY)
progress_label.pack(side=tk.TOP, padx=10, pady=5)


# ---- Code below provides a framework for the To-Do List Mini-App ----

# ---- Title & Subtitle----
title_label = tk.Label(frame_todo, text="My Tasks",
font=TITLE_FONT,
pady=5, #space between the text and border vertically)
bg=BG_MAIN,
fg=PRIMARY) 
title_label.pack(pady=(4,0))

subtitle_label = tk.Label(frame_todo, text="Stay organized - add, save, and manage your tasks",
font=("Times New Roman", 11),
bg=BG_MAIN,
fg=TEXT_MUTED)
subtitle_label.pack(pady=(0,4))


# ---- Search Filter (Combobox)  ---- 
search_frame = tk.Frame(frame_todo, bg=BG_CARD, bd=1, relief="solid", highlightthickness=0)
search_frame.pack(padx=16, pady=10, fill="both", expand=True)

my_list = ["All", "School", "Sports", "Work", "Urgent", "Personal", "Completed", "Uncompleted"]
filter_box = ttk.Combobox(search_frame, values=my_list,
state="readonly", style="Custom.TCombobox")

filter_box.pack(padx=16, pady=10, anchor="w")

# Set default
filter_box.set("All")

# Bind
filter_box.bind("<<ComboboxSelected>>", lambda: refresh_listbox())

# This removes the internal "highlight" state of the text
def clear_selection(event):
    event.widget.selection_clear()

# Bind to selection and focus event
filter_box.bind("<<ComboboxSelected>>", clear_selection)
filter_box.bind("<FocusIn>", clear_selection)

# ---- Listbox (tasks) ----
listbox_tasks = tk.Listbox(frame_todo, 
height=15, 
width=50,
bg=BG_CARD,
fg=TEXT_MAIN,
selectbackground=PRIMARY,
selectforeground="#000000", #black text on purple
selectmode=tk.EXTENDED,     #easier multi-select
activestyle="none",
bd=0,
highlightthickness=0)     
listbox_tasks.pack(side=tk.LEFT, fill="both", expand=True)

#Scrollbar vertical
scrollbar_tasks = tk.Scrollbar(frame_todo,
troughcolor=BG_CARD,
bg=BG_CARD,
activebackground=PRIMARY,
highlightthickness=0)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set) #Allows to go up and down in the y directions
scrollbar_tasks.config(command=listbox_tasks.yview)

#Scrollbar horizontal (x-axis)
horizontal_scrollbar_tasks = tk.Scrollbar(frame_todo,
troughcolor=BG_CARD,
bg=BG_CARD,
activebackground=PRIMARY,
highlightthickness=0,
orient=tk.HORIZONTAL)

listbox_tasks.config(xscrollcommand=horizontal_scrollbar_tasks.set) #Allows to go up and down in the y directions
horizontal_scrollbar_tasks.config(command=listbox_tasks.xview)

horizontal_scrollbar_tasks.pack(side=tk.BOTTOM, fill=tk.X)

# ---- Entry + Deadline Entry (Month + Day) + Calendar + Add button row ----
input_frame = tk.Frame(frame_todo, bg=BG_MAIN)
input_frame.pack(padx=16, pady=(0,10), fill="x")

entry_tasks = tk.Entry(input_frame, font=ENTRY_FONT,
width=30, bg="#262626", fg="gray",
insertbackground=TEXT_MAIN,
bd=1,
relief="solid",
highlightthickness=0)

entry_tasks.insert(0, "Add Task")

entry_tasks.grid(row=0, column=0, padx=(0,6),pady=4, sticky="we")

placeholder_text = "Add Task"

def on_entry_click(event):
    #when user clicks in the entry
    if entry_tasks.get() == placeholder_text:
        entry_tasks.delete(0, "end") #deletes all the text in the entry
        entry_tasks.config(fg=TEXT_MAIN) #set to the main text
        
def on_focusout(event):
    #when entry loses focus
    if entry_tasks.get() == "":
        entry_tasks.insert(0, placeholder_text)
        entry_tasks.config(fg="gray")
        
entry_tasks.bind("<FocusIn>", on_entry_click)
entry_tasks.bind("<FocusOut>", on_focusout)

# --- Categories (using tk.Menu) ----

def show_menu(button, menu):
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height()
    menu.tk_popup(x, y)

priority_var = tk.StringVar(value="Category ▼")

priority_button = styled_button(input_frame, 
textvariable=priority_var,
width=12,
command=lambda: show_menu(priority_button, priority_menu))
priority_button.grid(row=0, column=1, padx=10, pady=4)

priority_menu = tk.Menu(input_frame, 
tearoff=0, 
bg=BG_CARD,
fg=TEXT_MAIN,
activebackground=PRIMARY,
activeforeground="#000000",
bd=0,
font=ENTRY_FONT)

def set_priority(value):
    priority_var.set(f"{value}  ▼")
    
# Define categories
categories = {
    "School",
    "Sports",
    "Work",
    "Urgent",
    "Personal"
}

for option in categories:
    priority_menu.add_command(label=option,
    command= lambda value=option: set_priority(value))


# --- Deadline Entry ----
# Frame for Month entry and Day entry
deadline_frame = tk.Frame(frame_todo, bg=BG_MAIN)
deadline_frame.pack(padx=16, pady=(0,10), fill="x")

# --- Deadline Entry ----
# Month entry
month_placeholder = "Month (1-12)"

month_entry = tk.Entry(deadline_frame, font=ENTRY_FONT,
width=15, bg="#262626",fg="gray",
insertbackground=TEXT_MAIN,
bd=1,
relief="solid",
highlightthickness=0)

month_entry.insert(0, month_placeholder)

month_entry.grid(row=0, column=1, padx=(0,6), pady=4)

def on_month_click(event):
    #when user clicks in the entry
    if month_entry.get() == month_placeholder:
        month_entry.delete(0, "end") #deletes all the text in the entry
        month_entry.config(fg=TEXT_MAIN) #set to the main text
        
def on_month_focusout(event):
    #when entry loses focus
    if month_entry.get() == "":
        month_entry.insert(0, month_placeholder)
        month_entry.config(fg="gray")
        
month_entry.bind("<FocusIn>", on_month_click)
month_entry.bind("<FocusOut>", on_month_focusout)

#Day entry
day_placeholder = "Day (1-31)"

day_entry = tk.Entry(deadline_frame, font=ENTRY_FONT,
width=10, bg="#262626",fg="gray",
insertbackground=TEXT_MAIN,
bd=1,
relief="solid",
highlightthickness=0)

day_entry.insert(0, day_placeholder)

day_entry.grid(row=0, column=2, padx=(0,6), pady=4)

def on_day_click(event):
    #when user clicks in the entry
    if day_entry.get() == day_placeholder:
        day_entry.delete(0, "end") #deletes all the text in the entry
        day_entry.config(fg=TEXT_MAIN) #set to the main text
        
def on_day_focusout(event):
    #when entry loses focus
    if day_entry.get() == "":
        day_entry.insert(0, day_placeholder)
        day_entry.config(fg="gray")
        
day_entry.bind("<FocusIn>", on_day_click)
day_entry.bind("<FocusOut>", on_day_focusout)

# ---- CALENDAR ----- 
def open_calendar(event=None):
    # Create popup window
    cal_win = tk.Toplevel(root)
    cal_win.configure(bg=BG_MAIN)
    #Get current date
    today = get_local_date()
    year = today.year
    month = today.month
    
    month_name = calendar.month_name[month]
    
    #Define what happens when a day is clicked
    def select_day(d):
        month_entry.delete(0, tk.END)
        day_entry.delete(0, tk.END)

        month_entry.insert(0, str(month))
        day_entry.insert(0, str(d))

        cal_win.destroy()  # closes calendar
        
    cal_label = tk.Label(cal_win, 
    font=("Times New Roman", 15, "bold"), 
    text=(f"{month_name} {year}"),
    bg=BG_MAIN,
    fg=PRIMARY)
    
    cal_label.pack(padx=5, pady=5)
    
    # BUILD CALENDAR GRID HERE
    btn_frame = tk.Frame(cal_win, bg=BG_MAIN)
    btn_frame.pack()
    
    #Calendar Buttons
    for i in range(31):
        row = i // 7
        col = i % 7

        btn = styled_button(
        btn_frame,
        text=str(i + 1),
        width=4,
        command=lambda d=i+1: select_day(d)
    )
        btn.grid(row=row, column=col, padx=2, pady=2)
    
# --- Rewards Section below Progress Bar -----

streak = 0

last_completed_day = None

rewards_title = tk.Label(frame_get_started,
text="Rewards",
font=("Times New Roman", 14, "bold"),
bg=BG_MAIN,
fg=PRIMARY)
rewards_title.pack(padx=10, pady=(10,2), anchor="w")

streak_label = tk.Label(
    frame_get_started,
    text="Productivity Streak: 0 days",
    font=("Times New Roman", 12),
    bg=BG_MAIN,
    fg=TEXT_MAIN
)
streak_label.pack(padx=10, anchor="w")


def save_streak():
    try:
        with open(STREAK_FILE, "w") as f:
            f.write(f"{streak}\n")
            f.write(f"{last_completed_day}\n")
    except:
        pass

def check_streak():
    global streak, last_completed_day
    
    total = listbox_tasks.size()
    
    if total == 0:
        return
    
    completed = 0
    
    for i in range(total):
        if listbox_tasks.itemcget(i, "fg") == "#888888":
            completed += 1
    
    if completed == total:
        today = get_local_date()
        
        if last_completed_day != today:
            
            if last_completed_day == today - timedelta(days=1):
                streak += 1
            else:
                streak = 1
                
            last_completed_day = today
            
            save_streak()
            update_streak_ui()
            
            tkinter.messagebox.showinfo(
                "Streak!",
                f"Productivity Streak: {streak} day(s)!")

def load_streak():
    global streak, last_completed_day 
    
    if not os.path.exists(STREAK_FILE):
        return
    
    try:
        with open(STREAK_FILE, "r") as f:
            lines = f.readlines()
            
            streak = int(lines[0].strip())
            
            date_str = lines[1].strip()
            if date_str != "None":
                last_completed_day = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                last_completed_day = None
    except:
        streak = 0
        last_completed_day = None

            
streak_message = tk.Label(
    frame_get_started,font=("Times New Roman", 12, "bold"),
    text="Start your streak today!",
    bg=BG_MAIN,
    fg=TEXT_MUTED)
streak_message.pack(padx=10, pady=10, anchor="w")

def update_streak_ui():
    streak_label.config(text=f"Productivity Streak: {streak} day(s)")
    
    if streak >= 5:
        streak_message.config(text="You're on fire!")
    elif streak >= 1:
        streak_message.config(text="Keep your streak going!")
    else:
        streak_message.config(text="Start your streak!")
        

# ---- Functions (TAB 1)----
def refresh_top3():
    #clear existing preview
    listbox_top3.delete(0, tk.END)
    
    #Build a list of (display_text, is_completed) from the main listbox
    uncompleted = []
    
    for task in tasks:
        if task["completed"] == False:
            uncompleted.append(task)
        
    if len(uncompleted) == 0:
        listbox_top3.insert(tk.END, "You are all caught up, no work due soon!")
    else:
        for task in uncompleted[:3]:
            listbox_top3.insert(tk.END, f"• {task['title']} ({task['month']}/{task['day']})")
            
# Month Function
def month_name(month):
    month = month_entry.get().strip()
 
    if month == "1":
        return "January"
    elif month == "2":
        return "February"
    elif month == "3":
        return "March"
    elif month == "4":
        return "April"
    elif month == "5":
        return "May"
    elif month == "6":
        return "June"
    elif month == "7":
        return "July"
    elif month == "8":
        return "August"
    elif month == "9":
        return "September"
    elif month == "10":
        return "October"
    elif month == "11":
        return "November"
    elif month == "12":
        return "December"
    else:
        return "Invalid Month"

# Function required for display of items in the listbox (add, delete, cross, uncross)
displayed_task_indexes = []

def refresh_listbox(event=None):
    global displayed_task_indexes
    displayed_task_indexes = []
    
    listbox_tasks.delete(0, tk.END)
    
    selected_category = filter_box.get()

    for i, task in enumerate(tasks):
        show_task = False
        
        if selected_category == "All":
            show_task = True
        elif selected_category == "Completed" and task["completed"]:
            show_task = True
        elif selected_category == "Uncompleted" and not task["completed"]:
            show_task = True
        elif task["category"] == selected_category:
            show_task = True
            
        if show_task:
            displayed_task_indexes.append(i)
            text = f"{task['category']} | {task['title']} | {task['month']}/{task['day']}"
            listbox_tasks.insert(tk.END, text)
                
            if task["completed"]:
                index = listbox_tasks.size() - 1
                listbox_tasks.itemconfig(index, fg="#888888")
            
# Add task function
def add_task():
    
    title = entry_tasks.get().strip() #Gets the user's task and stores in var task
    month = month_entry.get().strip()
    day = day_entry.get().strip()
    category = priority_var.get().replace(" ▼", "").strip() 

    
    if (title == "" or title == placeholder_text or month == "" or month == month_placeholder or day == "" or day == day_placeholder):
        tkinter.messagebox.showwarning(title="Warning!", message="Enter the task and due date!")
        return 
    
    if category == "Category":
        tkinter.messagebox.showwarning(title="Warning!", message="Select a category!")
        return
    
    # Try to converty month/day to integers
    try:
        month = int(month)
        day = int(day)
    except ValueError:
        tkinter.messagebox.showwarning(title="Warning!", message="Month and day must be numbers!")
        return

    # Basic range checks
    if month < 1 or month > 12:
        tkinter.messagebox.showwarning(title="Warning!", message="Enter a valid month number (1-12)!")
        return
    
    if day < 1 or day > 31:
        tkinter.messagebox.showwarning(title="Warning!", message="Enter a valid day (1-31)")
        return 
    # Handle February + leap year 
    if month == 2 and day > 29:
        tkinter.messagebox.showwarning(title="Warning!", message="February has at most 29 days!")
        return
    
    # Months with 30 days
    if month in (4, 6, 9, 11) and day > 30:        
        tkinter.messagebox.showwarning(title="Warning!", message="That month has only 30 days!")
        return
    
    tasks.append({
        "title": title,
        "category": category,
        "month": month,
        "day": day,
        "completed": False
    })
    
    refresh_listbox()
    update_progress()
    refresh_top3()
    
    entry_tasks.delete(0, tk.END) #Clears the entry bar to allow the user to enter more tasks
    month_entry.delete(0, tk.END)
    day_entry.delete(0, tk.END)
    priority_var.set("Category ▼")
    
    
    
    
# Delete Task Function
def delete_task(): 
    selection = list(listbox_tasks.curselection())
    if not selection:
        tkinter.messagebox.showwarning(title="Warning!", message="You must select at least one task.")
        return
    
    real_indexes = [displayed_task_indexes[i] for i in selection]
    
    for real_index in sorted(real_indexes, reverse=True):
        del tasks[real_index]
    
    refresh_listbox()    
    update_progress()
    refresh_top3()
    


# save task function
def save_task(show_popup=False):
    # Get all tasks from the listbox
    if listbox_tasks.size() == 0:
        return
    try:
        # Write one task per line
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)
        if show_popup:        
            tkinter.messagebox.showinfo("Saved", "Tasks saved successfully.")
    except Exception as e:
        tkinter.messagebox.showwarning(
            title="Error",
            message=f"Could not save tasks: {e}"
        )
 
# load task function
def load_task():
    global tasks

    try:
        with open("tasks.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)

        update_progress()
        refresh_top3()

    except FileNotFoundError:
        tasks = []
        
    refresh_listbox()


def cross_item(): #New Change: Mark dictionary as True for ["completed"]
    selected_indices = listbox_tasks.curselection() # a tuple of indices from a list selected
    
    if not selected_indices:
        tkinter.messagebox.showwarning(
        title="Warning!",
        message="Select some tasks first."
       )
        return
    
    for visible_index in selected_indices:
        real_index = displayed_task_indexes[visible_index]
        tasks[real_index]["completed"] = True
    
    refresh_listbox()
    update_progress()
    refresh_top3()
    check_streak()
    save_task()
   
def uncross_item(): #New change: Mark dictionary as False for ["completed"]
    selected_indices = listbox_tasks.curselection() # a tuple of indices from a list selected
    
    if not selected_indices:
        tkinter.messagebox.showwarning(
        title="Warning!",
        message="Select some tasks first."
       )
        return #stop the function here
       
    for visible_index in selected_indices:
        real_index = displayed_task_indexes[visible_index]
        tasks[real_index]["completed"] = False
    
    refresh_listbox()
    update_progress()
    refresh_top3()
    check_streak()
    save_task()
    
    
def delete_crossed_item():
    global tasks
    tasks = [task for task in tasks if isinstance(task, dict) and not task["completed"]]
    refresh_listbox()
    update_progress()
    refresh_top3
    save_task()
   
    
# ---- Button wiring (AFTER functions so names exist) ----
# create the clickable label (OPEN CALENDAR)
calendar_button = styled_button(
    deadline_frame,
    text="Open Calendar",
    command=open_calendar,
    width=15
)

calendar_button.grid(row=0, column=3, padx=10, pady=10, sticky="we")

#To add tasks using a button
button_add_tasks = styled_button(input_frame, text="Add Task", command=add_task, width=12)
button_add_tasks.grid(row=0, column=2, pady=4, padx=5)

input_frame.columnconfigure(0, weight=1)

# ---- Bottom Buttons (Delete/Load/Save) ----

buttons_frame = tk.Frame(frame_todo, bg=BG_MAIN)
buttons_frame.pack(padx=16, pady=(0,16), fill="x")

#To delete using a button
button_delete_tasks = styled_button(buttons_frame, text="Delete Selected", command=delete_task)
button_delete_tasks.grid(row=0, column=0, padx=(0,6), pady=4, sticky="we")

#To load using a button
button_load_tasks = styled_button(buttons_frame, text="Load Task", command=load_task)
button_load_tasks.grid(row=0, column=1, padx=(0,6), pady=4, sticky="we")

#To save using a button
button_save_tasks = styled_button(buttons_frame, text="Save Task", command=lambda: save_task(True))
button_save_tasks.grid(row=0, column=2, padx=(0,6), pady=4, sticky="we")

for i in range(3):
    buttons_frame.columnconfigure(i, weight=1)
    
# ----- Buttons below (Delete/Load/Save) are (Cross/Uncross/Delete Crossed Item) -----

below_buttons_frame = tk.Frame(frame_todo, bg=BG_MAIN)
below_buttons_frame.pack(padx=16, pady=(0,16), fill="x")

#To cross item using a button 
cross_item_tasks = styled_button(below_buttons_frame, text="Check Item", command=cross_item)
cross_item_tasks.grid(row =1, column=0, padx=(0,6), pady=4, sticky="we")

#To uncross item
uncross_item_tasks = styled_button(below_buttons_frame, text="Uncheck Item", command=uncross_item)
uncross_item_tasks.grid(row =1, column=1, padx=(0,6), pady=4, sticky="we")

#To delete crossed items
delete_crossed_tasks = styled_button(below_buttons_frame, text="Clear Checked Items", command=delete_crossed_item)
delete_crossed_tasks.grid(row =1, column=2, padx=(0,6), pady=4, sticky="we")

# ---- Label Hint for Tasks Completed ----
label_hint = tk.Label(frame_todo, text="\"To do two things at once is to do neither.\"", 
bg=BG_MAIN, fg="#999999", font=LABEL_FONT)
label_hint.pack(padx=5, pady=5)

for i in range(3):
    below_buttons_frame.columnconfigure(i, weight=1)
    

# ---- Code below provides a framework for the Progress Tracker -----
# ---- Functions (TAB 2) ----

def update_progress():
    #Total number of tasks in the dictionary
    total_tasks = len(tasks)
    completed_tasks = 0
    
    for task in tasks:
        if task["completed"]:
            completed_tasks +=1
            
    if total_tasks == 0: #if there are no tasks in tasks dictionary then 0% completed
        percent = 0
    else:
        percent = (completed_tasks/ total_tasks) * 100
    

    progress_bar["value"] = percent
    progress_label.config(text=f"{completed_tasks}/{total_tasks} completed ({percent:.0f}%)")

    
# --- These functions are called after all widgets/functions are defined ----
load_streak()
update_streak_ui()
load_task()
refresh_top3()
update_progress()

root.mainloop()