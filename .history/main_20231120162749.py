import cv2
import pickle
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

width, height = 70, 27
YOUR_THRESHOLD_VALUE = 3  # Adjust this threshold value based on your requirements

# Initialize Firebase
cred = credentials.Certificate("smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json")
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
        if count < YOUR_THRESHOLD_VALUE:
            color = (0, 255, 0)  # Green
            thickness = 5
            emptyCount += 1
            textColor = (255, 255, 255)  # White text color
        else:
            # Use shades of red based on the count value
            red_shade = int(count / 10)  # Adjust the division factor as needed
            color = (0, 0, 255 - red_shade)  # Darker shades of red for higher occupancy
            thickness = 1
            fullCount += 1
            textColor = (0, 0, 0)  # Black text color
        cv2.rectangle(imgOriginal, pos, (x + width, y + height), color, thickness) 

    # Calculate the total count of parking spaces
    totalCount = emptyCount + fullCount

    # Display the counts of empty, full, and total parking spaces on the original image
    cv2.putText(imgOriginal, f"Free: {emptyCount}/{totalCount}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    
    
    try:
        
        # Example: Add a document to a 'users' collection
        doc_ref = db.collection('available-lot')
        doc_ref.add({
            'available': emptyCount,
            'timestamp': datetime.now()
        })

        print("Document added successfully.")
        time.sleep(5)
    except Exception as e:
     print("Error:", str(e))


# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()





