import cv2
import pickle
import numpy as np

width, height = 70, 27

def checkParkingSpace():
    for pos in posList:
        x, y = pos
        cv2.rectangle(img_copy, pos, (x + width, y + height), (255, 0, 255), 2)
        
        imgCrop = img[y:y + height, x:x + width]
        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            cv2.imshow(f"Parking Space at ({x}, {y})", imgCrop)


# video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel)
    
    
    
    if not success:
        # End of video or video cannot be read.
        break

    img_copy = img.copy()  # Create a copy of the frame to draw rectangles on the copy.
    checkParkingSpace()    # Draw rectangles on the copy of the frame

    cv2.imshow("Image", img_copy)
    cv2.imshow("ImageBlur", imgBlur)
    cv2.imshow("ImageThreshold", imgMedian)

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
