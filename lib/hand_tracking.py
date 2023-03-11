import cv2
import numpy as np
import mediapipe as mp

import time
import math
import sys

 
class handDetector():
    def __init__(self, mode=False, max_hands=2, model_c = 1, detection_con=0.7, track_con=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.model_c = model_c
        self.detection_con = detection_con
        self.track_con = track_con
 
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_c,
                                        self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
 
    def findHands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        return img
 
    def findPosition(self, img, handNo=0):
        xs = []
        ys = []
        b_box = []
        self.lms = []
        if self.results.multi_hand_landmarks:
            own_hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(own_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xs.append(cx)
                ys.append(cy)
                self.lms.append([id, cx, cy])
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            b_box = xmin, ymin, xmax, ymax
        return self.lms, b_box
 
    def fingersUp(self):
        fingers = []
        # Thumb
        try:
            if self.lms[self.tip_ids[0]][1] > self.lms[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        except:
           fingers.append(0)
        # Fingers
        for id in range(1, 5):
            try:
                if self.lms[self.tip_ids[id]][2] < self.lms[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            except:
                fingers.append(0)
        # totalFingers = fingers.count(1)
        return fingers

    def findDistance(self, p1, p2, img, r=15, t=3):
        x1, y1 = self.lms[p1][1:]
        x2, y2 = self.lms[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]
