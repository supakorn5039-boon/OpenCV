import cv2
import pickle

width, height = 70, 27

def checkParkingSpace(imgPro):
    for pos in posList:
        x, y = pos
        cv2.rectangle(imgPro, pos, (x + width, y + height), (255, 0, 255), 2)
        
        imgCrop = imgPro[y:y + height, x:x + width]
        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            count = cv2.countNonZero(imgCrop)

            # Draw purple background for the count number
            cv2.rectangle(img_copy, (x, y + height - 20), (x + 50, y + height), (255, 0, 255), cv2.FILLED)

            # Overlay the white count number on the purple background
            cv2.putText(img_copy, str(count), (x + 5, y + height - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


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

    checkParkingSpace(imgThreshold)  # Pass imgThreshold as an argument

    cv2.imshow("Image", img_copy)
    cv2.imshow("Threshold", imgThreshold)
    

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
