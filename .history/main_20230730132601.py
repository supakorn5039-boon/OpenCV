import cv2
import pickle

width, height = 70, 27

def drawCount(imgPro, count, x, y):
    # Create a white rectangle as the background for the count number
    cv2.rectangle(imgPro, (x, y), (x + 50, y + 20), (255, 255, 255), -1)

    # Draw the count number as black text
    cv2.putText(imgPro, str(count), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

def checkParkingSpace(imgPro, imgOriginal):
    for pos in posList:
        x, y = pos
        cv2.rectangle(imgOriginal, pos, (x + width, y + height), (255, 0, 255), 2)
        
        imgCrop = imgPro[y:y + height, x:x + width]
        count = 0  # Initialize count to 0
        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            count = cv2.countNonZero(imgCrop)
            drawCount(imgOriginal, count, x, y + height - 20)  # Draw count inside the parking space
            
        if count < 40 :
            color = (0,255,0)
            thickness = 5
        else:
            color = (0,0,255)
            thickness = 1    
        cv2.rectangle(img, pos ,(pos[0] + width , pos[1] + height) , color, thickness)        
      

# video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    if not success:
        # End of video or video cannot be read.
        break

    img_copy = img.copy()  # Create a copy of the frame to draw rectangles and text on the copy.
    
    # Preprocess the image - Convert to HSV and threshold on the saturation channel
    img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    saturation = img_hsv[:, :, 1]  # Saturation channel
    _, imgThreshold = cv2.threshold(saturation, 100, 255, cv2.THRESH_BINARY)

    checkParkingSpace(imgThreshold, img_copy)  # Pass imgThreshold and img_copy as arguments

    cv2.imshow("Image", img_copy)
    

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
