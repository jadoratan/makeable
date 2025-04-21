# Importing the required dependencies 
import time
import cv2
import dlib # for face and landmark detection 
import imutils 
from scipy.spatial import distance as dist # for calculating dist b/w the eye landmarks  
from imutils import face_utils # to get the landmark ids of the left and right eyes; you can do this manually too
import pyautogui # mouse control
import numpy as np # for sorting array of faces

start_time = time.time()
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use appropriate backend

if not cam.isOpened():
	print("Error: Couldn't open camera")
else:
	print(f"Camera initialized in {time.time() - start_time:.2f} seconds")

# Eye landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye'] 

# Initializing the Models for Landmark and 
# face Detection 
detector = dlib.get_frontal_face_detector() 
landmark_predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 
print("Initialized models for landmark and face detection")

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
		print(f"Face {i} area: {my_area}")
		if my_area > max_area:
			max_area = my_area
			max_index = i
	
	return max_index

user = -1

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

	if (user>=0):
		face = faces[user]
		# print(type(face))
		# face_rect = dlib.rectangle(face.left(), face.top(), face.right(), face.bottom())

		# landmark detection 
		shape = landmark_predict(img_gray, face) 
		# print("Landmarks predicted")

		# converting the shape class directly 
		# to a list of (x,y) coordinates 
		shape = face_utils.shape_to_np(shape) 
		# print("Face utils to shape")

		# Drawing facial landmarks
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
			
	cv2.imshow("Video", frame) 
	if cv2.waitKey(5) & 0xFF == ord('q'): 
		break

cam.release() 
cv2.destroyAllWindows() 
