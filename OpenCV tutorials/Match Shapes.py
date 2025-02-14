import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Match Shapes docs
# https://docs.opencv.org/4.x/d5/d45/tutorial_py_contours_more_functions.html

imA = cv.imread("shapeA.jpg", cv.COLOR_BGR2GRAY)
imB = cv.imread("shapeB.jpg", cv.COLOR_BGR2GRAY)
imA = imA.astype("uint8")
imB = imB.astype("uint8")

np.info(imA)

assert imA is not None, "shapeA.jpg could not be read, check with os.path.exists()"
assert imB is not None, "shapeB.jpg could not be read, check with os.path.exists()"

ret, thresh = cv.threshold(imA, 127, 255,0)
ret, thresh2 = cv.threshold(imA, 127, 255,0)
contours,hierarchy = cv.findContours(thresh,2,1)
cnt1 = contours[0]
contours,hierarchy = cv.findContours(thresh2,2,1)
cnt2 = contours[0]

ret = cv.matchShapes(cnt1,cnt2,1,0.0)
print(ret)
