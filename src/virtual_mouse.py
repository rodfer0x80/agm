import hand_tracking as ht

import cv2
import numpy as np

import autopy

import time
import sys

DEBUG = False

def main():
    ##########################
    w_cam, h_cam = 640, 480
    frameR = 100 # Frame Reduction
    smoothening = 7
    #########################
    
    p_time = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    
    cap = cv2.VideoCapture(0)
    cap.set(3, w_cam)
    cap.set(4, h_cam)
    detector = ht.handDetector(max_hands=1)
    wScr, hScr = autopy.screen.size()
    if DEBUG:
        print(wScr, hScr)
    try:
        while True:
            # 1. Find hand Landmarks
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            # 2. Get the tip of the index and middle fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                if DEBUG:
                    print(x1, y1, x2, y2)
            
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            if DEBUG:
                print(fingers)
                cv2.rectangle(img, (frameR, frameR), (w_cam - frameR, h_cam - frameR),
                    (255, 0, 255), 2)
            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, w_cam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, h_cam - frameR), (0, hScr))
                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
            
                # 7. Move Mouse
                autopy.mouse.move(wScr - clocX, clocY)
                if DEBUG:
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
                
            # 8. Both Index and middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if DEBUG:
                    print(length)
                # 10. Click mouse if distance short
                if length < 40:
                    if DEBUG:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]),
                            15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
            
            # 11. Frame Rate
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            if DEBUG:
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
            # 12. Display
            if DEBUG:
                cv2.imshow("Image", img)
                cv2.waitKey(1)
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
