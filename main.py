import cv2
import mediapipe
import numpy
import autopy
import pyautogui

cap = cv2.VideoCapture(0)
ih = mediapipe.solutions.hands
m_H = ih.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils
wScr, hScr = autopy.screen.size()
pX, pY = 0, 0
cX, cY = 0, 0


def HL(colorImg):
    point_list = []

    l_position = m_H.process(colorImg)

    check = l_position.multi_hand_landmarks
    if check:
        for hand in check:
            for index, landmark in enumerate(
                    hand.landmark):
                draw.draw_landmarks(img, hand,
                                    ih.HAND_CONNECTIONS)
                h, w, c = img.shape
                centerX, centerY = int(landmark.x * w), int(
                    landmark.y * h)
                point_list.append([index, centerX, centerY])

    return point_list


def f(landmarks):
    ft = []
    t_id = [4, 8, 12, 16, 20]
    if landmarks[t_id[0]][1] > lmList[t_id[0] - 1][1]:
        ft.append(1)
    else:
        ft.append(0)


    for id in range(1, 5):
        if landmarks[t_id[id]][2] < landmarks[t_id[id] - 3][2]:
            ft.append(1)
        else:
            ft.append(0)

    return ft


while True:
    check, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = HL(imgRGB)


    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        finger = f(lmList)
        #To find the screen aspect ratio
        cv2.rectangle(img,(75,75),(640-75,480-75),(255,0,255),2)
        if finger[1] == 1 and finger[2] == 0:
            #for i in range(5):
             #   print(finger[i],end=" ")
            #print()
            x3 = numpy.interp(x1, (75, 640 - 75),
                              (0, wScr))
            y3 = numpy.interp(y1, (75, 480 - 75),
                              (0, hScr))

            cX = pX + (x3 - pX) / 7
            cY = pY + (y3 - pY) / 7

            autopy.mouse.move(wScr - cX,
                              cY)
            pX, pY = cX, cY

        if finger[1] == 0 and finger[0] == 1:
            autopy.mouse.click()
        if finger[0] == 0 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4]== 1:
            pyautogui.click(button='right')

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break