import cv2
import pickle
import cvzone
import numpy as np

#Video feed

cap = cv2.VideoCapture('stock-footage-car-parking-near-the-shopping-center-aerial-shooting')

while True:
    success, img = cap.read()
    cv2.imshow("Image",img)
    cv2.waitKey(0)