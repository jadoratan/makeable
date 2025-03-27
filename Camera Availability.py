import time
import cv2

start_time = time.time()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use appropriate backend

if not cap.isOpened():
    print("Error: Couldn't open camera")
else:
    print(f"Camera initialized in {time.time() - start_time:.2f} seconds")
