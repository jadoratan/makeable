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
BLINK_THRESH = 0.35
SUCC_FRAME = 1 # for preventing false detections from slight eye movement or noise

left_count_frame = 0 # how many consecutive frames left eye is unblinking
right_count_frame = 0 # how many consecutive frames right eye is unblinking

BLINK_DISPLAY_FRAMES = 15 # Number of frames to display message
left_blink_counter = 0 # Counter for displaying blink message

# right_blink_display_frames = 10 # Number of frames to display message
right_blink_counter = 0 # Counter for displaying blink message

# Eye landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye'] 

# Initializing the Models for Landmark and 
# face Detection 
detector = dlib.get_frontal_face_detector() 
landmark_predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 
print("Initialized models for landmark and face detection")

while 1: 
	
	# If the video is finished then reset it 
	# to the start 
	if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get( 
			cv2.CAP_PROP_FRAME_COUNT): 
		cam.set(cv2.CAP_PROP_POS_FRAMES, 0) 

	# print("hi")

	else: 
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

			# Just left eye EAR
			if (left_EAR < BLINK_THRESH): # if left eye is blinking
				left_count_frame += 1 # incrementing the frame count for left eye
			else: 
				if left_count_frame >= SUCC_FRAME: 
					left_blink_counter = BLINK_DISPLAY_FRAMES
					print("Left eye blink detected")
					left_count_frame -= 1
				else:
					print(f"Left EAR: {left_EAR}")
					
			# frame = cv2.flip(frame, 1)

			if left_blink_counter > 0:
				cv2.putText(frame, 'Left Eye Blink Detected', (30, 30), 
								cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1) 
				left_blink_counter -= 1

			# Just right eye EAR
			if (right_EAR < BLINK_THRESH): # if right eye is unblinking
				right_count_frame += 1 # incrementing the frame count for right eye 
			else: 
				if right_count_frame >= SUCC_FRAME: 
					right_blink_counter = BLINK_DISPLAY_FRAMES
					print("Right eye blink detected")
					right_count_frame -= 1
				else:
					print(f"Right EAR: {right_EAR}")
			
			if right_blink_counter > 0:
				cv2.putText(frame, 'Right Eye Blink Detected', (30, 130), 
								cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 1) 
				right_blink_counter -= 1

			# # Avg of left and right eye EAR 
			# avg = (left_EAR+right_EAR)/2
			# if avg < BLINK_THRESH: 
			# 	left_count_frame += 1 # incrementing the frame count 
			# else: 
			# 	if left_count_frame >= SUCC_FRAME: 
			# 		cv2.putText(frame, 'Blink Detected', (30, 30), 
			# 					cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 1) 
			# 	else: 
			# 		left_count_frame = 0


		cv2.imshow("Video", frame) 
		if cv2.waitKey(5) & 0xFF == ord('q'): 
			break

cam.release() 
cv2.destroyAllWindows() 
