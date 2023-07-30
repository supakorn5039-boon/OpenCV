import cv2
import pickle

width, height = 70, 27
YOUR_THRESHOLD_VALUE = 3  # Adjust this threshold value based on your requirements

def drawCount(imgPro, count, x, y, textColor, bgColor):
    # Create a background rectangle with the specified green or red color
    cv2.rectangle(imgPro, (x, y), (x + 50, y + 20), bgColor, -1)

    # Draw the count number as white text
    cv2.putText(imgPro, str(count), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, textColor, 1, cv2.LINE_AA)

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
            textColor = (255, 255, 255)  # White text color
            bgColor = (0, 255, 0)  # Green background color
        else:
            color = (0, 0, 255, 100)  # Red with a slight transparency (alpha = 100)
            thickness = 1
            fullCount += 1
            textColor = (0, 0, 0)  # Black text color
            bgColor = (255, 255, 255)  # White background color

        # Draw the count number with the specified text and background colors
        drawCount(imgOriginal, count, x, y + height - 20, textColor, bgColor)
        cv2.rectangle(imgOriginal, pos, (x + width, y + height), color, thickness, cv2.LINE_AA) 

    # Calculate the total count of parking spaces
    totalCount = emptyCount + fullCount

    # Display the counts of empty, full, and total parking spaces on the original image
    cv2.putText(imgOriginal, f"Free: {emptyCount}/{totalCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

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
