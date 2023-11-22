import cv2
import firebase_admin
from firebase_admin import credentials, storage
import time

# Initialize Firebase Admin SDK (replace 'path/to/your/credentials.json' with your Firebase Admin SDK JSON file)
cred = credentials.Certificate('/smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'smart-parking-e0f33'})

# Open the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    while True:
        # Capture a single frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Save the captured frame as an image
        cv2.imwrite("captured_photo.jpg", frame)

        # Upload the captured photo to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f"images/{int(time.time())}.jpg")
        blob.upload_from_filename("captured_photo.jpg")

        print("Photo captured and uploaded to Firebase successfully.")

        # Wait for 20 seconds
        time.sleep(20)

except KeyboardInterrupt:
    # Release the camera when the user interrupts the script (e.g., presses Ctrl+C)
    print("Interrupted by user.")
finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
