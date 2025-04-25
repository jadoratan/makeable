# DOCS:
# https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/tutorial/
# https://www.geeksforgeeks.org/eye-blink-detection-with-opencv-python-and-dlib/
# https://stackoverflow.com/questions/56294517/select-one-face-detector-from-multiple-faces-in-image
# https://stackoverflow.com/questions/51131812/wrap-text-inside-row-in-tkinter-treeview

# Media credits:
# [1] ChatRat Image (window icon) - https://logopond.com/SKitanovic/showcase/detail/276227
# [2] Mouse Click Sound - https://pixabay.com/sound-effects/mouse-click-290204/
# [3] Camera With Slash Image - https://www.svgrepo.com/svg/357442/camera-slash


################################# Imports #################################
# GUI Imports
# import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import textwrap

# Backend Imports
import cv2 # for video rendering 
# import numpy as np
import dlib # for face and landmark detection 
import imutils 
from scipy.spatial import distance as dist # for calculating dist b/w the eye landmarks  
from imutils import face_utils # to get the landmark ids of the left and right eyes; you can do this manually too
import pyautogui # mouse control
import numpy as np # for sorting array of faces
import pygame # sound effects


################################# Global Constants & Variables #################################
global BLINK_THRESH # EAR must fall below this value to count as a blink
global SUCC_FRAME # for preventing false detections from slight eye movement or noise
global BLINK_DISPLAY_FRAMES # Number of frames to display message
global TIMEOUT # how many frames can pass without blinking to be considered 2 long blinks

BLINK_THRESH = 0.40
SUCC_FRAME = 7
BLINK_DISPLAY_FRAMES = 5
TIMEOUT = 40

global both_count_frame, long_blink_counter, consecutive_blink_timeout # blink tracker variables


################################# BACKEND #################################
# Initalize sound 
pygame.mixer.init()
click_sound = pygame.mixer.Sound("click_sound_20.mp3")
click_sound.set_volume(1.0)  # range is 0.0 to 1.0


# Backend Functions
# Calculates the eye aspect ratio (EAR) 
def calculate_EAR(eye): 
	# calculate the vertical distances 
	y1 = dist.euclidean(eye[1], eye[5]) 
	y2 = dist.euclidean(eye[2], eye[4]) 

	# calculate the horizontal distance 
	x1 = dist.euclidean(eye[0], eye[3]) 

	# calculate the EAR 
	EAR = (y1+y2) / x1 
	return EAR 


# Identifies the user's face (the nearest face to the camera in theory)
def nearest_face(faces):
	def area(x, y, w, h):
		return (w - x) * (h - y)

	max_area = -1
	max_index = -1

	for i, face in enumerate(faces):
		x = face.left()
		y = face.top()
		w = face.right()
		h = face.bottom()
		my_area = area(x, y, w, h)
		# print(f"Face {i} area: {my_area}")
		
		if my_area > max_area: # face with highest area is nearest face
			max_area = my_area
			max_index = i
	
	return max_index # return index of nearest face from list of faces
	
	
# the actual blink tracking program
def tracking():
	# Initialize camera and models(only once)
	global cam, detector, landmark_predict, L_start, L_end, R_start, R_end
	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	if not cam.isOpened():
		print("Error: Could not open camera.")
		return

	print("Camera opened! :D")
	camera_toggle_bool.set(True)
	camera_string.set("Camera connected")

	(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
	detector = dlib.get_frontal_face_detector()
	landmark_predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

	print("Initialized models for landmark and face detection")

	# Reset any blink tracking state vars
	reset_tracking_state()

	# Start frame loop
	# window.after(0, track_frame)
	track_frame()


def track_frame():
	global cam, detector, landmark_predict
	global both_count_frame, long_blink_counter, consecutive_blink_timeout

	if not start_toggle_bool.get(): # if toggle is not on
		cam.release()
		cv2.destroyAllWindows()
		return

	ret, frame = cam.read()
	if not ret:
		print("Failed to grab frame")
		window.after(10, track_frame)
		return

	frame = imutils.resize(frame, width=640)
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = detector(img_gray)
	user = nearest_face(faces)

	# print(f"Frame size: {img_gray.shape}")
	# return

	if user >= 0:
		face = faces[user]
		shape = landmark_predict(img_gray, face)
		shape = face_utils.shape_to_np(shape)

		righteye = shape[L_start:L_end]
		lefteye = shape[R_start:R_end]
		left_EAR = calculate_EAR(lefteye)
		right_EAR = calculate_EAR(righteye)
		avg = (left_EAR + right_EAR) / 2

		if avg < BLINK_THRESH:
			both_count_frame += 1
		else:
			if both_count_frame >= SUCC_FRAME:
				consecutive_blink_timeout = TIMEOUT
				long_blink_counter += 1
				print(f"long_blink_counter: {long_blink_counter}")
			
			both_count_frame = 0

		if consecutive_blink_timeout > 0:
			consecutive_blink_timeout -= 1
			print(f"consecutive_blink_timeout: {consecutive_blink_timeout}")
		else:
			if long_blink_counter == 1:
				pyautogui.click(button="left")
				click_sound.play()

				last_click.set("Last click: LEFT click")
				last_click_label.config(bootstyle="warning")

				print("Left Click")
			elif long_blink_counter >= 2:
				pyautogui.click(button="right")
				click_sound.play()

				last_click.set("Last click: RIGHT click")
				last_click_label.config(bootstyle="danger")

				print("Right Click")

			long_blink_counter = 0

		for (x, y) in shape:
			cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

	# Convert BGR to RGB
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	final_img = Image.fromarray(frame)
	imgtk = ImageTk.PhotoImage(image=final_img)

	# Update the image in label
	video_label.imgtk = imgtk  # Prevent garbage collection
	video_label.config(image=imgtk)

	# cv2.imshow("Video", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		on_toggle()  # Stop tracking if user hits 'q'
		return

	window.after(10, track_frame)  # Schedule next frame


def reset_tracking_state():
	global both_count_frame, long_blink_counter, consecutive_blink_timeout
	both_count_frame = 0
	long_blink_counter = 0
	consecutive_blink_timeout = 0

	
################################# GUI #################################
# GUI Functions
# Wrapping text in widgets
def wrap(string, length=30):
    return "\n".join(textwrap.wrap(string, length))

# For turning the blink tracking program on/off
def on_toggle():
	if (start_toggle_bool.get()): # if toggle is on
		start_string.set("Stop tracking")
		toast = ToastNotification(
			title="Tracking Mouse",
			message="Tracking has been turned ON.",
			duration=3000,
			bootstyle="info"
		)

		toast.show_toast()
		print("Tracking ON")

		tracking()
	else:
		start_string.set("Start tracking")
		toast = ToastNotification(
			title="Tracking Mouse",
			message="Tracking has been turned OFF.",
			duration=3000,
			bootstyle="info"
		)

		headband_toggle_bool.set(False)
		headband_string.set("Headband not connected")
		camera_toggle_bool.set(False)
		camera_string.set("Camera not connected.")

		camera_off_img = Image.open("camera-off.png").resize((640,480))
		img = ImageTk.PhotoImage(image=camera_off_img)

		# Update the image in label
		video_label.imgtk = img  # Prevent garbage collection
		video_label.config(image=img)

		toast.show_toast()
		print("Tracking OFF")


# Elements
# Window
window = ttk.Window(themename="yeti", iconphoto="lab_rats_logo.png")
window.title("Tracking Mouse")
window.geometry("1000x900")
colors = window.style.colors

# Left & Right Panels (Frames)
top_panel = ttk.Frame(master=window)
bottom_panel = ttk.Frame(master=window)

# Title + Intro Frame
intro_frame = ttk.Frame(master=top_panel, bootstyle="success")
title_label = ttk.Label(master=intro_frame, font="Calibri 25 bold", text="Tracking Mouse")
intro_label = ttk.Label(master=intro_frame, font="Calibri 15", text=wrap("Welcome to Tracking Mouse, a hands-free computer mouse built for your convenience!"))

title_label.pack(side="top", pady=10)
intro_label.pack(pady=10)

intro_frame.pack(side="left", padx=20, fill=BOTH, expand=True)


# Program status
status_frame = ttk.Frame(master=bottom_panel, bootstyle="secondary")
status_title_label = ttk.Label(master=status_frame, font="Calibri 25 bold", text="App Status:")

start_toggle_frame = ttk.Frame(master=status_frame, bootstyle="light")
start_toggle_bool = ttk.BooleanVar()
start_toggle_button = ttk.Checkbutton(
							master=start_toggle_frame, 
							bootstyle="success-round-toggle", 
							command=on_toggle, 
							variable=start_toggle_bool
							)
start_string = ttk.StringVar()
start_label = ttk.Label(master=start_toggle_frame, font="Calibri 15", textvariable=start_string)
start_string.set("Start tracking")

headband_toggle_frame = ttk.Frame(master=status_frame, bootstyle="dark")
headband_toggle_bool = ttk.BooleanVar()
headband_checkbox = ttk.Checkbutton(
							master=headband_toggle_frame, 
							bootstyle="success", 
							variable=headband_toggle_bool,
							state="disabled"
							)
headband_string = ttk.StringVar()
headband_label = ttk.Label(master=headband_toggle_frame, font="Calibri 15", textvariable=headband_string)
headband_string.set("Headband not connected")

camera_toggle_frame = ttk.Frame(master=status_frame, bootstyle="light")
camera_toggle_bool = ttk.BooleanVar()
camera_checkbox = ttk.Checkbutton(
							master=camera_toggle_frame, 
							bootstyle="success",
							variable=camera_toggle_bool,
							state="disabled"
							)
camera_string = ttk.StringVar()
camera_label = ttk.Label(master=camera_toggle_frame, font="Calibri 15", textvariable=camera_string)
camera_string.set("Camera not connected")

last_click = ttk.StringVar()
last_click.set("Last click: N/A")
last_click_label = ttk.Label(master=status_frame, font="Calibri 15 bold", textvariable=last_click)

# Pack everything lol
status_title_label.pack(side="top", pady=10)

start_toggle_button.pack(side="left", pady=10)
start_label.pack(side="right", pady=5)
start_toggle_frame.pack(pady=10)

headband_checkbox.pack(side="left", pady=10)
headband_label.pack(side="right", pady=5)
headband_toggle_frame.pack(pady=10)

camera_checkbox.pack(side="left", pady=10)
camera_label.pack(side="right", pady=5)
camera_toggle_frame.pack(pady=10)

last_click_label.pack(pady=10)

status_frame.pack(side="left", padx=20, fill=BOTH, expand=True)


# Key - table of cursor action and user input
key_frame = ttk.Frame(master=top_panel, bootstyle="info")
key_title_label =  ttk.Label(master=key_frame, text="Inputs", font="Calibri 25 bold")

# Unique style for datatables to change font size
key_dt_style = ttk.Style()
key_dt_style.theme_use("yeti")  # Re-apply theme explicitly
key_dt_style.configure("Treeview", font=("Calibri", 15), rowheight=70)  # Entries
key_dt_style.configure("Treeview.Heading", font=("Calibri", 15, "bold"))  # Header

coldata = [
	{"text": "Cursor Action", "stretch": False},
	{"text": "User Input", "stretch": False},
]

rowdata = [
	("Move cursor\n(any direction)", "Wear headband and move\nhead in desired direction"),
	("Left click", "1 long blink"),
	("Right click", "2 long blinks")
]


key_dt = ttk.Treeview(
	master=key_frame,
	columns=coldata,
	show="headings",
	height=3,
)

key_dt.heading(column=0, text="Cursor Action")
key_dt.heading(column=1, text="User Input")

key_dt.column(0, width=200, stretch=True)
key_dt.column(1, width=350, stretch=True)

for entry in rowdata:
	# height = 40 # default row height
	# if (i==1): # only for the really long first row
	# 	height=70
	key_dt.insert("", "end", values=(entry[0], entry[1]))


key_title_label.pack(pady=10)
key_dt.pack(ipadx=5, pady=10, fill=BOTH, expand=TRUE)
key_frame.pack(padx=20)


# Video Feed
video_frame = ttk.Frame(master=bottom_panel, bootstyle="warning")
video_label = ttk.Label(master=video_frame)

camera_off_img = Image.open("camera-off.png").resize((640,480))
img = ImageTk.PhotoImage(image=camera_off_img)

# Update the image in label
video_label.imgtk = img  # Prevent garbage collection
video_label.config(image=img)
# print(f"Image size: {video_label.imgtk.width()}x{video_label.imgtk.height()}")

video_label.pack(pady=10)
video_frame.pack(padx=20, fill=BOTH, expand=True)

# Run
top_panel.pack(side="top", pady=10, expand=True, fill=BOTH)
bottom_panel.pack(side="bottom", pady=10, expand=True, fill=BOTH)
window.mainloop()