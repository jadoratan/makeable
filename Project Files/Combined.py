# DOCS:
# https://forum.arduino.cc/t/arduino-accelerometer-to-python-output/638283

import serial # USB communication
import pyautogui # mouse control
import threading
import time

# Imports for blink_click
import cv2 # for video rendering 
import dlib # for face and landmark detection 
import imutils # for calculating dist b/w the eye landmarks 
from imutils import face_utils 
from scipy.spatial import distance as dist # to get the landmark ids of the left and right eyes 


# Initialize Serial Connection (Adjust COM port as needed)
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct port (e.g., '/dev/ttyUSB0' on Linux)

# Get screen dimensions
screen_width, screen_height = pyautogui.size()
cursor_x, cursor_y = screen_width // 2, screen_height // 2  # Start in center

# Cursor Movement (Arduino/Accelerometer) Function
def move_cursor():
    global cursor_x, cursor_y
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            try:
                xValue, yValue = map(int, data.split(","))
                
                # Convert accelerometer values to cursor movement
                cursor_x += (xValue - 512) // 50  # Adjust sensitivity
                cursor_y += (yValue - 512) // 50

                # Boundaries to keep cursor within screen
                cursor_x = max(0, min(screen_width, cursor_x))
                cursor_y = max(0, min(screen_height, cursor_y))

                # Move cursor
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.05)
            except ValueError:
                pass  # Ignore errors from corrupted serial data

# EAR Calculation Function
def calculate_EAR(eye): 

    # calculate the vertical distances 
    y1 = dist.euclidean(eye[1], eye[5]) 
    y2 = dist.euclidean(eye[2], eye[4]) 

    # calculate the horizontal distance 
    x1 = dist.euclidean(eye[0], eye[3]) 

    # calculate the EAR 
    EAR = (y1+y2) / x1 
    return EAR 

# Blink Detection (Webcam) Function
def blink_click():
    cam = cv2.VideoCapture(0) 

    if not cam.isOpened():
        print("Error: Could not open camera.")
        exit()
    else:
        print("Camera opened! :D")

    # Variables 
    BLINK_THRESH = 0.35 # EAR must fall below this value to count as a blink
    SUCC_FRAME = 3 # for preventing false detections from slight eye movement or noise
    BLINK_DISPLAY_FRAMES = 10 # Number of frames to display message

    both_count_frame = 0 # number of blink frames in this set (EAR < BLINK_THRESH)
    display_counter = 0 # Counter for displaying blink message
    long_blink_counter = 0 # for counting consecutive long blinks

    TIMEOUT = 30 # how many frames can pass without blinking to be considered 2 long blinks
    consecutive_blink_timeout = 0 # how many frames left in timeout

    # Eye landmarks
    (L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
    (R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye'] 

    # Initializing the Models for Landmark and 
    # face Detection 
    detector = dlib.get_frontal_face_detector() 
    landmark_predict = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') 
    print("Initialized models for landmark and face detection")

    while True:
        _, frame = cam.read() 
        frame = imutils.resize(frame, width=640) 
        # frame = cv2.flip(frame, 1)

        # converting frame to gray scale to 
        # pass to detector 
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        # detecting the faces 
        faces = detector(img_gray) 
        for face in faces: 

            # landmark detection 
            shape = landmark_predict(img_gray, face) 

            # converting the shape class directly 
            # to a list of (x,y) coordinates 
            shape = face_utils.shape_to_np(shape) 

            # parsing the landmarks list to extract 
            # lefteye and righteye landmarks--# 
            # they're switched because the mirroring messes it up #
            righteye = shape[L_start: L_end]
            lefteye = shape[R_start:R_end] 

            # Calculate the EAR (Eye Aspect Ratio)
            left_EAR = calculate_EAR(lefteye) 
            right_EAR = calculate_EAR(righteye) 

            # Avg of left and right eye EAR 
            avg = (left_EAR+right_EAR)/2
            if (avg < BLINK_THRESH): # if blinking
                both_count_frame += 1 # incrementing the frame count for right eye 
                # print("Long eye blink detected")
                # print(f"Avg EAR: {avg}")
            else: 
                # Testing for a single long blink
                if both_count_frame >= SUCC_FRAME: 
                    print(f"both_count_frame (before): {both_count_frame}")
                    both_count_frame = 0
                    print(f"both_count_frame (after): {both_count_frame}")
                    
                    display_counter = BLINK_DISPLAY_FRAMES # num of frames blink message will be displayed

                    # Reset consecutive_blink_timeout when a long blink is detected
                    consecutive_blink_timeout = TIMEOUT # num of frames that can pass by without blinking to still be consecutive

                    long_blink_counter += 1 # num of long blinks
                    print(f"long_blink_counter: {long_blink_counter}")

            # Only decrement the timeout after first long blink
            if consecutive_blink_timeout > 0:
                consecutive_blink_timeout -= 1
                print(f"consecutive_blink_timeout: {consecutive_blink_timeout}")
            elif display_counter > 0: # timeout finishes
                if (long_blink_counter == 1): # 1 long blink for left click 
                    cv2.putText(frame, 'Left Click', (30, 130), 
                                cv2.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1) 
                elif (long_blink_counter >= 2): # 2 long blinks for right click
                        cv2.putText(frame, 'Right Click', (30, 130), 
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 200), 1) 
                display_counter -= 1
            else: # actually click once display finishes
                if (long_blink_counter == 1): # 1 long blink for left click 
                    pyautogui.click(button="left")
                    print("Left Click")
                elif (long_blink_counter >= 2): # 2 long blinks for right click
                    pyautogui.click(button="right")
                    print("Right Click")
                
                long_blink_counter = 0 # Reset if timeout occurs or once display has finished
                            
            
                
        cv2.imshow("Video", frame) 
        if cv2.waitKey(5) & 0xFF == ord('q'): 
            break

    cam.release() 
    cv2.destroyAllWindows() 

# Start Threads
t1 = threading.Thread(target=move_cursor)
t2 = threading.Thread(target=blink_click)

t1.start()
t2.start()

t1.join()
t2.join()
