import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv

# Docs
# https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker

model_path = '/absolute/path/to/face_landmarker.task'

################### Prepare data #######################
# Load the input image from an image file.
img = cv.imread("test.jpg")

print(type(img))

# # Load the input image from a numpy array.
# mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_image)
    

# BaseOptions = mp.tasks.BaseOptions
# FaceLandmarker = mp.tasks.vision.FaceLandmarker
# FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode

# options = FaceLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=VisionRunningMode.IMAGE)

# with FaceLandmarker.create_from_options(options) as landmarker:
#   # The landmarker is initialized. Use it here.
