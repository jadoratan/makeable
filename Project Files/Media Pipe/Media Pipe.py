import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv

# Docs
# https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker
# https://github.com/google-ai-edge/mediapipe-samples/blob/main/examples/face_landmarker/python/%5BMediaPipe_Python_Tasks%5D_Face_Landmarker.ipynb

# Model Setup
model_path = 'face_landmarker.task'
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a face landmarker instance with the live stream mode:
def print_result(result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('face landmarker result: {}'.format(result))

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)


# Cam Setup
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: could not open camera")
    exit()

with FaceLandmarker.create_from_options(options) as landmarker:
  # The landmarker is initialized. Use it here.
  # ...


while True:
    with FaceLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting")
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Send live image data to perform face landmarking.
        # The results are accessible via the `result_callback` provided in
        # the `FaceLandmarkerOptions` object.
        # The face landmarker must be created with the live stream mode.
        landmarker.detect_async(mp_image, timestamp)

        cv.imShow("Live Video Feed", frame)

        if cv.waitKey(1) == ord("q"):
            break

cap.release()
cap.destroyAllWindows()




################### Prepare data #######################
# Load image and turn into mediapipe.Image object


# print(type(mp_image))

    






