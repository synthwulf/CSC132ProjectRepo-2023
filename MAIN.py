import cv2
import imutils
import threading
import time

cap = cv2.VideoCapture(1)

Text = False
Text_mode = False
Text_counter = 0

# Initialize start_frame
ret, start_frame = cap.read()
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

def Texter():
    global Text
    for i in range(5):
        if not Text_mode:
            break
        print("ALARM")
        time.sleep(1)
    Text = False

while True:
    ret, frame = cap.read()  # Check if the frame capture was successful
    if not ret:
        print("Error capturing frame. Exiting.")
        break

    frame = imutils.resize(frame, width=650)

    if Text_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        # Ensure start_frame and frame_bw have the same dimensions
        start_frame = cv2.resize(start_frame, (frame_bw.shape[1], frame_bw.shape[0]))

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300:
            Text_counter += 1
        else:
            if Text_counter > 0:
                Text_counter -= 1
        cv2.imshow("cam", threshold)
    else:
        cv2.imshow("cam", frame)

    if Text_counter > 20:
        if not Text:
            Text = True
            threading.Thread(target=Texter).start()
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('t'):
        Text_mode = not Text_mode
        Text_counter = 0
    if key_pressed == ord('q'):
        Text_mode = False
        break

cap.release()
cv2.destroyAllWindows()

