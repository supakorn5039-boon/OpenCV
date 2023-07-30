import cv2
import pickle
import cvzone
import numpy as np

width, height = 95, 45


#video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)

while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        
    for pos in posList:
        cv2.rectangle(img_copy, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)    
    
    success,img = cap.read()
    cv2.imshow("Image",img)
    cv2.waitKey(30)

