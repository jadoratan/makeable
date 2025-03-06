# DOCS:
# https://www.geeksforgeeks.org/eye-blink-detection-with-opencv-python-and-dlib/


# Importing the required dependencies 
import cv2 # for video rendering 
import dlib # for face and landmark detection 
import time
import imutils 
# for calculating dist b/w the eye landmarks 
from scipy.spatial import distance as dist 
# to get the landmark ids of the left and right eyes 
# you can do this manually too 
from imutils import face_utils 

# from imutils import 

cam = cv2.VideoCapture(0) 

if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()
else:
	print("Camera opened! :D")

# defining a function to calculate the EAR 
def calculate_EAR(eye): 

	# calculate the vertical distances 
	y1 = dist.euclidean(eye[1], eye[5]) 
	y2 = dist.euclidean(eye[2], eye[4]) 

	# calculate the horizontal distance 
	x1 = dist.euclidean(eye[0], eye[3]) 

	# calculate the EAR 
	EAR = (y1+y2) / x1 
	return EAR 

# Variables 
LEFT_BLINK_THRESH = 0.35 # 0.32
BLINK_THRESH = 0.35
SUCC_FRAME = 3 # for preventing false detections from slight eye movement or noise

left_count_frame = 0 # how many consecutive frames left eye is unblinking
right_count_frame = 0 # how many consecutive frames right eye is unblinking
both_count_frame = 0

BLINK_DISPLAY_FRAMES = 15 # Number of frames to display message
left_display_counter = 0 # Counter for displaying blink message
right_display_counter = 0 # Counter for displaying blink message
display_counter = 0 # Counter for displaying blink message

long_blink_counter = 0 # for counting consecutive long blinks

TIMEOUT = 30
consecutive_blink_timeout = 0 # how many frames can pass without blinking to be considered 2 long blinks

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

	# converting frame to gray scale to 
	# pass to detector 
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

	# detecting the faces 
	faces = detector(img_gray) 
	for face in faces: 

		# landmark detection 
		shape = landmark_predict(img_gray, face) 

		# converting the shape class directly 
		# to a list of (x,y) coordinates 
		shape = face_utils.shape_to_np(shape) 

		# parsing the landmarks list to extract 
		# lefteye and righteye landmarks--# 
		# they're switched because the mirroring messes it up #
		righteye = shape[L_start: L_end]
		lefteye = shape[R_start:R_end] 

		# Calculate the EAR (Eye Aspect Ratio)
		left_EAR = calculate_EAR(lefteye) 
		right_EAR = calculate_EAR(righteye) 

		# # Just left eye EAR
		# if (left_EAR < LEFT_BLINK_THRESH): # if left eye is blinking
		# 	left_count_frame += 1 # incrementing the frame count for left eye
		# 	print("Left eye blink detected")
		# 	print(f"Left EAR: {left_EAR}")
		# else: 
		# 	if left_count_frame >= SUCC_FRAME: 
		# 		left_blink_counter = BLINK_DISPLAY_FRAMES
		# 		left_count_frame -= 1
			
		# # frame = cv2.flip(frame, 1)

		# if left_blink_counter > 0:
		# 	cv2.putText(frame, 'Left Eye Blink Detected', (30, 30), 
		# 					cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1) 
		# 	left_blink_counter -= 1

		# # Just right eye EAR
		# if (right_EAR < RIGHT_BLINK_THRESH): # if right eye is unblinking
		# 	right_count_frame += 1 # incrementing the frame count for right eye 
		# 	print("Right eye blink detected")
		# 	print(f"Right EAR: {right_EAR}")
		# else: 
		# 	if right_count_frame >= SUCC_FRAME: 
		# 		right_blink_counter = BLINK_DISPLAY_FRAMES
		# 		right_count_frame -= 1
			
		
		# if right_blink_counter > 0:
		# 	cv2.putText(frame, 'Right Eye Blink Detected', (30, 130), 
		# 					cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 1) 
		# 	right_blink_counter -= 1

		# Avg of left and right eye EAR 
		avg = (left_EAR+right_EAR)/2
		if (avg < BLINK_THRESH): # if blinking
			both_count_frame += 1 # incrementing the frame count for right eye 
			# print("Long eye blink detected")
			# print(f"Avg EAR: {avg}")
		else: 
			# Testing for a single long blink
			if both_count_frame >= SUCC_FRAME: 
				print(f"both_count_frame (before): {both_count_frame}")
				both_count_frame = 0
				print(f"both_count_frame (after): {both_count_frame}")
				
				display_counter = BLINK_DISPLAY_FRAMES # num of frames blink message will be displayed

				# Reset consecutive_blink_timeout when a long blink is detected
				consecutive_blink_timeout = TIMEOUT # num of frames that can pass by without blinking to still be consecutive

				long_blink_counter += 1 # num of long blinks
				print(f"long_blink_counter: {long_blink_counter}")

		# Only decrement the timeout after first long blink
		if consecutive_blink_timeout > 0:
			consecutive_blink_timeout -= 1
			print(f"consecutive_blink_timeout: {consecutive_blink_timeout}")
		else:
			if (long_blink_counter == 1): # 1 long blink for left click 
				if display_counter > 0:
					cv2.putText(frame, 'Left Click', (30, 130), 
								cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1) 
					display_counter -= 1
			elif (long_blink_counter == 2): # 2 long blinks for right click
				if display_counter > 0:
					cv2.putText(frame, 'Right Click', (30, 130), 
							cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 1) 
					display_counter -= 1
						
				# long_blink_counter = 0
				# print("Timed out")

			long_blink_counter = 0  # Reset if timeout occurs
		
			
	cv2.imshow("Video", frame) 
	if cv2.waitKey(5) & 0xFF == ord('q'): 
		break

cam.release() 
cv2.destroyAllWindows() 
