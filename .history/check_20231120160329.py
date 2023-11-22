import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json")
firebase_admin.initialize_app(cred)

print(cred)
db = firestore.client()

width, height = 70, 27
YOUR_THRESHOLD_VALUE = 3

def checkParkingSpace(imgPro, imgOriginal):
    emptyCount = 0
    fullCount = 0

    for i, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < YOUR_THRESHOLD_VALUE:
            color = (0, 255, 0)
            thickness = 5
            emptyCount += 1
            textColor = (255, 255, 255)
        else:
            red_shade = int(count / 10)
            color = (0, 0, 255 - red_shade)
            thickness = 1
            fullCount += 1
            textColor = (0, 0, 0)

        cv2.rectangle(imgOriginal, pos, (x + width, y + height), color, thickness)

        # Update the parking space status in Firestore
        doc_ref = db.collection('parking_spaces').document(f'space_{i + 1}')
        doc_ref.set({
            'status': 'empty' if count < YOUR_THRESHOLD_VALUE else 'occupied'
        })

    totalCount = emptyCount + fullCount
    cv2.putText(imgOriginal, f"Free: {emptyCount}/{totalCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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

    img_copy = img.copy()
    img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    saturation = img_hsv[:, :, 1]
    _, imgThreshold = cv2.threshold(saturation, 100, 255, cv2.THRESH_BINARY)

    checkParkingSpace(imgThreshold, img_copy)

    cv2.imshow("Image", img_copy)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
