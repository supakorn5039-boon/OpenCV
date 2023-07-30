import cv2
import pickle
import cvzone
import numpy as np

#Video feed

cap = cv2.VideoCapture('carPark.mp4')

while True:
    success, img = cap.read()
    cv2.imshow("Image",img)
    cv2.waitKey(0)