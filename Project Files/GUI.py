# DOCS:
# https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/tutorial/

# Imports
# import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *

# Functions
def on_toggle():
	on = start_toggle_bool.get()
	tracking_message = ""

	if (on):
		tracking_message = "Tracking has been turned ON."
		next_state = "Stop tracking"
		print("Tracking ON")


	else:
		tracking_message = "Tracking has been turned OFF."
		next_state = "Start tracking"
		print("Tracking OFF")
	
	start_string.set(next_state)
	toast = ToastNotification(
		title="Tracking Mouse",
		message=tracking_message,
		duration=3000,
		bootstyle="info"
	)
	toast.show_toast()
    

# Window
window = ttk.Window(themename="yeti", iconphoto="lab_rats_logo.png")
window.title("Tracking Mouse")
window.geometry("1000x800")
colors = window.style.colors

# Title + Intro Frame
intro_frame = ttk.Frame(master=window)
title_label = ttk.Label(master=intro_frame, text="Tracking Mouse", font="Calibri 24 bold")
intro_label = ttk.Label(master=intro_frame, text="Welcome to Tracking Mouse, a hands-free computer mouse built for your convenience!")
title_label.pack()
intro_label.pack()
intro_frame.pack()


# Key - table of cursor action and user input
key_frame = ttk.Frame(master=window)

coldata = [
    {"text": "Cursor Action", "stretch": False},
    {"text": "User Input", "stretch": False},
]

rowdata = [
    ("Move cursor in any direction", "Wear headband and move head in desired direction"),
	("Left click", "1 long blink"),
	("Right click", "2 long blinks")
]

key_dt = Tableview(
    master=key_frame,
    coldata=coldata,
    rowdata=rowdata,
	autofit=True,
	height=3,
    searchable=False, # search entries
	paginated=False, # next page
    bootstyle=PRIMARY,
    stripecolor=(colors.light, None),
)

key_dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)
key_frame.pack()


# Program status
status_frame = ttk.Frame(master=window)
status_title_label = ttk.Label(master=status_frame, text="App Status:", font="Calibri 24 bold")

start_toggle_bool = ttk.BooleanVar()
start_toggle_button = ttk.Checkbutton(
							master=status_frame, 
							bootstyle="success-round-toggle", 
							command=on_toggle, 
							variable=start_toggle_bool
							)
start_string = ttk.StringVar()
start_label = ttk.Label(master=status_frame, textvariable=start_string)
start_string.set("Start tracking")

headband_toggle_bool = ttk.BooleanVar()
headband_checkbox = ttk.Checkbutton(
							master=status_frame, 
							bootstyle="success", 
							variable=headband_toggle_bool,
							#state="disabled"
							)
headband_string = ttk.StringVar()
headband_label = ttk.Label(master=status_frame, textvariable=headband_string)
headband_string.set("Headband not connected")

camera_toggle_bool = ttk.BooleanVar()
camera_checkbox = ttk.Checkbutton(
							master=status_frame, 
							bootstyle="success",
							variable=camera_toggle_bool,
							#state="disabled"
							)
camera_string = ttk.StringVar()
camera_label = ttk.Label(master=status_frame, textvariable=camera_string)
camera_string.set("Camera not connected")

# Pack everything lol
status_title_label.pack()

start_toggle_button.pack()
start_label.pack()

headband_checkbox.pack()
headband_label.pack()

camera_checkbox.pack()
camera_label.pack()

status_frame.pack()

# Run
window.mainloop()