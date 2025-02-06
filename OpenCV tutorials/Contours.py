import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Contour hierarchy docs
# https://docs.opencv.org/4.x/d9/d8b/tutorial_py_contours_hierarchy.html

im = cv.imread("shapes.png")
assert im is not None, "file could not be read, check with os.path.exists()"
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)

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