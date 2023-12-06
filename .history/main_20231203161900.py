import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

width, height = 70, 27
threshold = 3  # Adjust this threshold value based on your requirements
firebase_update_interval = 10  # Update interval in seconds

# Initialize Firebase
cred = credentials.Certificate(
    "smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def checkParkingSpace(imgPro, imgOriginal):
    emptyCount = 0  # Initialize the count of empty (green) rectangles
    fullCount = 0  # Initialize the count of full (red) rectangles

    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        # Adjust the threshold value here based on your requirements
        if count < threshold:
            color = (0, 255, 0)  # Green
            thickness = 1
            emptyCount += 1
        else:
            # Use shades of red based on the count value
            red_shade = int(count / 10)  # Adjust the division factor as needed
            # Darker shades of red for higher occupancy
            color = (0, 0, 255 - red_shade)
            thickness = 1
            fullCount += 1
        cv2.rectangle(imgOriginal, pos, (x + width,
                      y + height), color, thickness)

    # Calculate the total count of parking spaces
    totalCount = emptyCount + fullCount

    # Display the counts of empty, full, and total parking spaces on the original image
    cv2.putText(imgOriginal, f"Free: {emptyCount}/{totalCount}",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return emptyCount  # Return the count of empty spaces


# video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

# Timestamp for the last Firebase update
last_firebase_update_time = time.time()

# Detect the Object
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

    # Pass imgThreshold and img_copy as arguments
    empty_count = checkParkingSpace(imgThreshold, img_copy)

    # Check if 10 seconds have passed since the last Firebase update
    current_time = time.time()
    if current_time - last_firebase_update_time >= firebase_update_interval:
        try:
            doc_ref = db.collection('available-lot')
            doc_ref.add({
                'available': empty_count,
                'timestamp': firestore.SERVER_TIMESTAMP
        })
    print("Document added successfully.")
    last_firebase_update_time = current_time  # Update the last update time
except Exception as e:
    print("Error:", str(e))


    cv2.imshow("Image", img_copy)

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
