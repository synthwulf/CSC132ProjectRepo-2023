import cv2
import imutils
import winsound
import threading

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)


Text = False
Text_mode = False
Text_counter = 0


def Texter():
    global Text
    for i in range(5):
        if not Text_mode:
            break
        print("ALARM")
        winsound.Beep(2500,1000)
    alarm = False

while True:

    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if Text_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5),0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25,255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300:
            Text_counter += 1
        else:
            if Text_counter > 0:
                Text_counter -= 1
        cv2.imshow("cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if Text_counter >20:
        if not Text:
            Text = True
            threading.Thread(target=Texter).start()
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        Text_mode = not Text_mode
        Text_counter = 0
    if key_pressed == ord("q"):
        Text_mode = False
        break

cap.release()
cv2.destroyAllWindows()

                          
