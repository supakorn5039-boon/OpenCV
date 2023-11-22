import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase
cred = credentials.Certificate("/smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

width, height = 70, 27
YOUR_THRESHOLD_VALUE = 3

def checkParkingSpace(imgPro, imgOriginal):
    # ... (the rest of your existing code)

    for i, pos in enumerate(posList):
        # ... (the rest of your existing code)

        # Update the parking space status in Firestore
        doc_ref = db.collection('parking_spaces').document(f'space_{i + 1}')
        doc_ref.set({
            'status': 'empty' if count < YOUR_THRESHOLD_VALUE else 'occupied'
        })

    totalCount = emptyCount + fullCount
    cv2.putText(imgOriginal, f"Free: {emptyCount}/{totalCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Rest of your script remains unchanged

# video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('carParkPos', 'rb') as f:
    posList = pickle.load(f)

while True:
    # ... (the rest of your existing code)

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
