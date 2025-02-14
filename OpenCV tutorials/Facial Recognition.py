import cv2 as cv

face_classifier = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def detect_bounding_box(vid):
    gray_image = cv.cvtColor(vid, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # Operations on frame here
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frame = cv.flip(frame, 0)s
    
    faces = detect_bounding_box(frame)

    # Display the resulting frame
    cv.imshow('Face Detection Window', frame)
    
    if cv.waitKey(1) == ord("q"):
        break
    
# Release capture (RECORD: and out) when done
cap.release()
# out.release()
cv.destroyAllWindows()
