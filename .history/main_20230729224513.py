import cv2
import pickle
import cvzone
import numpy as np

#video feed
cap = cv2.VideoCapture('carPark.mp4')

while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES)
    
    success,img = cap.read()
    cv2.imshow("Image",img)
    cv2.waitKey(30)

