#!/usr/bin/env python3
import time
import sys
import subprocess

import cv2
import numpy as np

import lib.hand_tracking as ht


def main():
    w_cam, h_cam = 640, 480 # camera size
    frameR = 60 # 60 is default for human vision
    smoothening = 4 

    default_click_timout = 15 # timeout for clicks
    default_finger_distance = 30 # finger distance for click detection


    timeout = 0
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

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if timeout > 0:
            timeout = timeout - 1

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            fingers = detector.fingersUp()

            if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
                x3 = np.interp(x1, (frameR, w_cam - frameR), (0, w_scr))
                y3 = np.interp(y1, (frameR, h_cam - frameR), (0, h_scr))

                cloc_x = ploc_x + (x3 - ploc_x) / smoothening
                cloc_y = ploc_y + (y3 - ploc_y) / smoothening

                w_scr = int(w_scr)
                cloc_x = int(cloc_x)
                cloc_y = int(cloc_y)
                mouse_x = w_scr - cloc_x
                mouse_y = cloc_y

                subprocess.check_output(f"xdotool mousemove {mouse_x} {mouse_y}".split(" "))
                ploc_x, ploc_y = cloc_x, cloc_y

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and timeout == 0:
                timeout = default_click_timout
                length_a, img, lineInfo = detector.findDistance(12,16,img)
                length_b, img, lineInfo = detector.findDistance(8,12,img)
                length = (length_a + length_b) / 2 - smoothening*2

                if length < default_finger_distance:
                    subprocess.check_output("xdotool click --delay 0.1 3".split(" "))
                    fingers[1] = 0
                    fingers[2] = 0
                    fingers[3] = 0

            elif fingers[1] == 1 and fingers[2] == 1 and timeout == 0:
                timeout = default_click_timout
                length, img, lineInfo = detector.findDistance(8, 12, img)
                
                if length < default_finger_distance:
                    subprocess.check_output("xdotool click --delay 0.1 1".split(" "))
                    fingers[1] = 0
                    fingers[2] = 0  
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
