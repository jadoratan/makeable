import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Contour hierarchy docs
# https://docs.opencv.org/4.x/d9/d8b/tutorial_py_contours_hierarchy.html

# im = cv.imread("shapes.png")
# assert im is not None, "file could not be read, check with os.path.exists()"

# Live Capture
cap = cv.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = cap.read()

if ret:
    # Save the frame
    cv.imwrite("test.jpg", frame)
    print("Photo captured and saved as test.jpg.")
else:
    print("Error: Could not capture frame.")

# Release the camera
cap.release()

im = cv.imread("test.jpg")
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 100, 150, cv.THRESH_BINARY)

temp = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
for i in range(len(temp)):
    print(temp[i][0])

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(im, contours, -1, (0,255,0), 3) # pass -1 for all contours
cv.drawContours(imgray, contours, -1, (0,255,0), 3) # pass -1 for all contours
cv.imshow("color with contours", im)
cv.imshow("gray with contours", imgray)
cv.waitKey(0)
cv.destroyAllWindows()