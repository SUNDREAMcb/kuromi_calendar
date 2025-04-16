import tkinter as tk
import pyautogui 
from tkinter import ttk, PhotoImage
from tkcalendar import Calendar
from PIL import ImageGrab
from datetime import date, timedelta, datetime



root = tk.Tk()
root.resizable(width=False, height=False)
root.title("Leah Calendar")

style = ttk.Style(root)
style.theme_use('clam') 

# --- Canvas to hold background image ---
canvas = tk.Canvas(root, width=570, height=690)
canvas.pack(fill="both", expand=True)

# --- Load image (adjust path as needed) ---
bg_image = PhotoImage(file="kuromi_bg2.png") 
canvas.create_image(0, 0, image=bg_image, anchor="nw")



# --- Place calendar on top of the image ---
background_color ="#9e7ca8"

def go_to_today(calendar_widget):
    today = datetime.today()
    calendar_widget.selection_set(today)
    calendar_widget.see(today)

def save_window_screenshot(window, filename='calendar_screenshot.png'):
    window.update()
    window.lift()
    window.attributes('-topmost', True)
    window.after(100, lambda: window.attributes('-topmost', False))  # remove topmost after

    x = window.winfo_rootx()
    y = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()

    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

myCal = Calendar(root,font = "Arial 18",
                 selectmode= "none",
                 showweeknumbers = False,
                 showothermonthdays = False, 
                 date_pattern="dd/mm/yyyy",
                 firstweekday="sunday",
                 tooltipdelay = 150,
                 

                 # text colors
                
                 foreground = "gold", #month + year selector
                 headersforeground="old lace", # days of the week
                 normalforeground="black", # week day numbers
                 weekendforeground="black", # weekend colors
                 selectforeground="black", # selected date number
                 tooltipforeground = "pink",

                 selectbackground="mediumpurple2", # selected date background
                    #background colors - use background_color variable
                 background = background_color, 
                 disabledbackground=background_color,
                 bordercolor=background_color,
                 headersbackground=background_color, 
                 normalbackground=background_color,
                 weekendbackground=background_color, 
                 
                 )
calendar_window = canvas.create_window(75, 75, anchor="nw", window=myCal)

button_frame = tk.Frame(root, bg="#9e7ca8")
canvas.create_window(135,3, anchor="nw", window=button_frame, width=550)

# --- Today button ---
btn_today = ttk.Button(button_frame,text="Go to Today", command=lambda: go_to_today(myCal))
btn_today.pack(side="left", padx=20, pady=10)

# --- Screenshot button ---
btn_screenshot = ttk.Button(button_frame,text="Save Screenshot", command=lambda: save_window_screenshot(root))

btn_screenshot.pack(side="left", padx=20, pady=10)

pattern = [3, 3, 2, 2, 3, 1]
start_date = date(2025, 4, 16)  # Starting work day
days_to_show = 360  # Total days to visualize the schedule

current = start_date
pattern_index = 0
working = True

myCal.tag_config('work', background=background_color, foreground='olivedrab1') 

while current < start_date + timedelta(days=days_to_show):
    block_days = pattern[pattern_index % len(pattern)]

    if working:
        for i in range(block_days):
            if current >= start_date + timedelta(days=days_to_show):
                break
            myCal.calevent_create(current, 'Work 10a-8p', 'work')
            current += timedelta(days=1)
    else:
        current += timedelta(days=block_days)

    working = not working
    pattern_index += 1


root.mainloop()
