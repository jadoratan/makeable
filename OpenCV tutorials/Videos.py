import numpy as np
import cv2 as cv

# https://docs.opencv.org/4.x/dc/d4d/tutorial_py_table_of_contents_gui.html

######### Live Capture ###########
cap = cv.VideoCapture(0)

# RECORD: define the codec and create the VideoWriter object
# fourcc = cv.VideoWriter_fourcc(*"XVID")
# out = cv.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # Operations on frame here
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frame = cv.flip(frame, 0)
    
    # Display the resulting frame
    cv.imshow('Image Window', frame)
    
    if cv.waitKey(1) == ord("q"):
        break
    
# Release capture (RECORD: and out) when done
cap.release()
# out.release()
cv.destroyAllWindows()

# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# # print(cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE))
# im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(im2, contours, -1, (0,255,0), 3)`