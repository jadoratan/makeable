# DOCS:
# https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/tutorial/
# https://www.geeksforgeeks.org/eye-blink-detection-with-opencv-python-and-dlib/
# https://stackoverflow.com/questions/56294517/select-one-face-detector-from-multiple-faces-in-image



# Imports
# GUI Imports
# import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

# Backend Imports
import cv2 # for video rendering 
import dlib # for face and landmark detection 
import imutils 
from scipy.spatial import distance as dist # for calculating dist b/w the eye landmarks  
from imutils import face_utils # to get the landmark ids of the left and right eyes; you can do this manually too
import pyautogui # mouse control
import numpy as np # for sorting array of faces



# Functions
# For turning the blink tracking program on/off
def on_toggle():
	on = start_toggle_bool.get()

	if (on):
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
		camera_toggle_bool.set(False)
		toast.show_toast()
		print("Tracking OFF")
	
	
# the actual blink tracking program
def tracking():
	# Variables 
	BLINK_THRESH = 0.40 # EAR must fall below this value to count as a blink
	SUCC_FRAME = 7 # for preventing false detections from slight eye movement or noise
	BLINK_DISPLAY_FRAMES = 5 # Number of frames to display message

	both_count_frame = 0 # number of blink frames in this set (EAR < BLINK_THRESH)
	display_counter = 0 # Counter for displaying blink message
	long_blink_counter = 0 # for counting consecutive long blinks

	TIMEOUT = 40 # how many frames can pass without blinking to be considered 2 long blinks
	consecutive_blink_timeout = 0 # how many frames left in timeout

	# Functions
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

	# Camera initialization
	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use appropriate backend

	if not cam.isOpened():
		print("Error: Could not open camera.")
		exit()
	else:
		print("Camera opened! :D")
		camera_toggle_bool.set(True)


	# Identifying user's face
	# if no face is detected, program continues searching for face until one is identified

	# Eye landmarks
	(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
	(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye'] 

	# Initializing the Models for Landmark and 
	# face Detection 
	detector = dlib.get_frontal_face_detector() 
	landmark_predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 
	print("Initialized models for landmark and face detection")

	while True:
		_, frame = cam.read() 
		frame = imutils.resize(frame, width=640) 
		# frame = cv2.flip(frame, 1)
		# print("Cam capturing")

		# converting frame to gray scale to 
		# pass to detector 
		img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

		# detecting the faces 
		faces = detector(img_gray) 
		user = nearest_face(faces)
		
		if (user>=0): # if a face is detected (index is not -1)
			face = faces[user] # set the nearest face as the one to track

			# landmark detection 
			shape = landmark_predict(img_gray, face) 
			# print("Landmarks predicted")

			# converting the shape class directly 
			# to a list of (x,y) coordinates 
			shape = face_utils.shape_to_np(shape) 
			# print("Face utils to shape")

			# parsing the landmarks list to extract 
			# lefteye and righteye landmarks--# 
			# they're switched because the mirroring messes it up #
			righteye = shape[L_start: L_end]
			lefteye = shape[R_start:R_end] 

			# Calculate the EAR (Eye Aspect Ratio)
			left_EAR = calculate_EAR(lefteye) 
			right_EAR = calculate_EAR(righteye) 
			# print("Calculations")

			# Avg of left and right eye EAR 
			avg = (left_EAR+right_EAR)/2
			# print(avg)
			if (avg < BLINK_THRESH): # if blinking
				both_count_frame += 1 # incrementing the frame count for right eye 
				# print("Long eye blink detected")
				# print(f"Avg EAR: {avg}")
			else: 
				# Testing for a single long blink
				if both_count_frame >= SUCC_FRAME: 
					print(f"both_count_frame (before): {both_count_frame}")
					
					# display_counter = BLINK_DISPLAY_FRAMES # num of frames blink message will be displayed

					# Reset consecutive_blink_timeout when a long blink is detected
					consecutive_blink_timeout = TIMEOUT # num of frames that can pass by without blinking to still be consecutive

					long_blink_counter += 1 # num of long blinks
					print(f"long_blink_counter: {long_blink_counter}")
				
				# Reset consecutive frames count regardless of short or long blink
				both_count_frame = 0
				# print(f"both_count_frame (after): {both_count_frame}")

			# Only decrement the timeout after first long blink
			if consecutive_blink_timeout > 0:
				consecutive_blink_timeout -= 1
				print(f"consecutive_blink_timeout: {consecutive_blink_timeout}")
			# elif display_counter > 0: # timeout finishes
			# 	if (long_blink_counter == 1): # 1 long blink for left click 
			# 		cv2.putText(frame, 'Left Click', (30, 130), 
			# 					cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1) 
			# 	elif (long_blink_counter >= 2): # 2 long blinks for right click
			# 			cv2.putText(frame, 'Right Click', (30, 130), 
			# 					cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 1) 
			# 	display_counter -= 1
			else: # actually click once display finishes
				if (long_blink_counter == 1): # 1 long blink for left click 
					pyautogui.click(button="left")
					print("Left Click")
				elif (long_blink_counter >= 2): # 2 long blinks for right click
					pyautogui.click(button="right")
					print("Right Click")
				
				long_blink_counter = 0 # Reset if timeout occurs or once display has finished
							
			# Drawing facial landmarks
			for (x, y) in shape:
				cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
				
		cv2.imshow("Video", frame) 
		if cv2.waitKey(5) & 0xFF == ord('q'): 
			break
	

# Window
window = ttk.Window(themename="yeti", iconphoto="lab_rats_logo.png")
window.title("Tracking Mouse")
window.geometry("1000x800")
colors = window.style.colors

# Left & Right Panels (Frames)
left_panel = ttk.Frame(master=window)
right_panel = ttk.Frame(master=window)

# Title + Intro Frame
intro_frame = ttk.Frame(master=left_panel)
title_label = ttk.Label(master=intro_frame, text="Tracking Mouse", font="Calibri 24 bold")
intro_label = ttk.Label(master=intro_frame, text="Welcome to Tracking Mouse, a hands-free \ncomputer mouse built for your convenience!")

title_label.pack()
intro_label.pack()

intro_frame.pack(padx=10, pady=10)


# Program status
status_frame = ttk.Frame(master=left_panel)
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
							state="disabled"
							)
headband_string = ttk.StringVar()
headband_label = ttk.Label(master=status_frame, textvariable=headband_string)
headband_string.set("Headband not connected")

camera_toggle_bool = ttk.BooleanVar()
camera_checkbox = ttk.Checkbutton(
							master=status_frame, 
							bootstyle="success",
							variable=camera_toggle_bool,
							state="disabled"
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

status_frame.pack(padx=10, pady=10)


# Key - table of cursor action and user input
key_frame = ttk.Frame(master=right_panel)
key_title_label =  ttk.Label(master=key_frame, text="Inputs", font="Calibri 24 bold")
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

key_title_label.pack()
key_dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

key_frame.pack(side="top")

# Run
left_panel.pack(side="left", expand=True, fill=BOTH)
right_panel.pack(side="right", expand=True, fill=BOTH)
window.mainloop()