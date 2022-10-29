#!/usr/bin/env python3
import time
import sys
import subprocess

import cv2
import numpy as np

import src.hand_tracking as ht
from src.logger import *

LOGGER = Logger()

def main():
    global LOGGER
    ##########################
    w_cam, h_cam = 640, 480
    frameR = 60 # Frame Reduction
    smoothening = 4
    #########################
    
    p_time = 0
    ploc_x, ploc_y = 0, 0
    cloc_x, cloc_y = 0, 0
    
    cap = cv2.VideoCapture(0)
    cap.set(3, w_cam)
    cap.set(4, h_cam)
    detector = ht.handDetector(max_hands=1)

    dims = subprocess.check_output("xdotool getwindowfocus getwindowgeometry".split(" "))
    dims = str(dims).split("Geometry:")[-1]
    dims = str(dims).strip()[:-3]
    w_scr, h_scr = float(dims.split("x")[0]), float(dims.split("x")[1])
    LOGGER.log(f"Sreensize: {w_scr}x{h_scr}\n")

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            LOGGER.log(f"IndexFinger:MiddleFinger: {x1},{y1}:{x2}:{y2}\n")
            
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            LOGGER.log(f"Fingers: {fingers}\n")
            #cv2.rectangle(img, (frameR, frameR), (w_cam - frameR, h_cam - frameR),
            #    (255, 0, 255), 2)
            
            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, w_cam - frameR), (0, w_scr))
                y3 = np.interp(y1, (frameR, h_cam - frameR), (0, h_scr))
                
                # 6. Smoothen Values
                cloc_x = ploc_x + (x3 - ploc_x) / smoothening
                cloc_y = ploc_y + (y3 - ploc_y) / smoothening
            
                # 7. Move Mouse
                w_scr = int(w_scr)
                cloc_x = int(cloc_x)
                cloc_y = int(cloc_y)
                mouse_x = w_scr - cloc_x
                mouse_y = cloc_y
                LOGGER.log(f"Mouse Coords: {mouse_x},{mouse_y}\n")
                subprocess.check_output(f"xdotool mousemove {mouse_x} {mouse_y}".split(" "))
                #cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                ploc_x, ploc_y = cloc_x, cloc_y

                # 8. Both Index and middle fingers are up : Clicking Mode Left Click
            if fingers[1] == 1 and fingers[2] == 1:

                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img, draw=False) # False for CLI mode
                LOGGER.log(f"FingerDistance: {length}\n")

                # 10. Click mouse if distance short
                if length < 50:
                    #cv2.circle(img, (lineInfo[4], lineInfo[5]),
                    #    15, (0, 255, 0), cv2.FILLED)
                    subprocess.check_output("xdotool click --delay 0.1 1".split(" "))
                    fingers[1] = 0
                    fingers[2] = 0  
            
            # 8. Right Click 
            if fingers[2] == 1 and fingers[3] == 1:

                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(12,16,img,draw=False)
                LOGGER.log(f"FingerDistance: {length}\n")

                # 10. Click mouse if distance short
                if length < 50:
                    #cv2.circle(img, (lineInfo[4], lineInfo[5]),
                    #    15, (0, 255, 0), cv2.FILLED)
                    subprocess.check_output("xdotool click --delay 0.1 3".split(" "))
                    fingers[2] = 0
                    fingers[3] = 0 

 
            
            # 11. Frame Rate
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            #cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
            #    (255, 0, 0), 3)
            
            # 12. Display
            #cv2.imshow("Image", img)
            #cv2.waitKey(1)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
