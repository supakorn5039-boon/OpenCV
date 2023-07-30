import cv2
import pickle

width, height = 70, 27
YOUR_THRESHOLD_VALUE = 5  # Adjust this threshold value based on your requirements

def checkParkingSpace(imgPro, imgOriginal):
    emptyCount = 0  # Initialize the count of empty (green) rectangles
    fullCount = 0  # Initialize the count of full (red) rectangles

    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
        
        # Adjust the threshold value here based on your requirements
        if count < YOUR_THRESHOLD_VALUE:
            color = (0, 255, 0)  # Green
            thickness = 5
            emptyCount += 1
        else:
            color = (0, 0, 255)  # Red
            thickness = 1
            fullCount += 1
        cv2.rectangle(imgOriginal, pos, (x + width, y + height), color, thickness) 

    # Display the counts of empty and full rectangles on the original image
    cv2.putText(imgOriginal, f"Empty Count: {emptyCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
    cv2.putText(imgOriginal, f"Full Count: {fullCount}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

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

    img_copy = img.copy()  # Create a copy of the frame to draw rectangles on
    
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
