import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*"XVID")
out = cv.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

while cap.isOpened():
    # Capture fram-eby-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break
    
    frame = cv.flip(frame, 0) # flip around the x-axis

    # Turns video feed gray
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # write the modified frame
    out.write(gray)

    cv.imshow("frame", gray)
    
    if cv.waitKey(1) == ord("q"):
        break

# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()