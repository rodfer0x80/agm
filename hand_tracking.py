import cv2
import numpy as np
import mediapipe as mp

import time
import math
import sys

 
class handDetector():
    def __init__(self, mode=False, max_hands=2, model_c = 1, detection_con=0.5, track_con=0.5):
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
 
    def findHands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms,
                                               self.mp_hands.HAND_CONNECTIONS)
        return img
 
    def findPosition(self, img, handNo=0, draw=True):
        xs = []
        ys = []
        b_box = []
        self.lms = []
        if self.results.multi_hand_landmarks:
            own_hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(own_hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xs.append(cx)
                ys.append(cy)
                # print(id, cx, cy)
                self.lms.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            b_box = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)
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
 
    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lms[p1][1:]
        x2, y2 = self.lms[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]
 
 
def main():
    p_time = 0
    c_time = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lms, b_box = detector.findPosition(img)
        # if len(lms) != 0:
        #     print(lms[4])
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    return 0
 
if __name__ == "__main__":
    sys.exit(main())
