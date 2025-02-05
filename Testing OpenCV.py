import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a frame
ret, frame = cap.read()

# Check if the frame was captured successfully
if ret:
    # Save the frame
    cv.imwrite("test.jpg", frame)
    print("Photo captured and saved as test.jpg.")
else:
    print("Error: Could not capture frame.")

# Release the camera
# cap.release()

im = cv.imread('test.jpg')
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)

# Display the image in a window
cv.imshow('Image Window', imgray)

# Wait for a key press
cv.waitKey(0)

# Close the window
cv.destroyAllWindows()

# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# # print(cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE))
# im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(im2, contours, -1, (0,255,0), 3)