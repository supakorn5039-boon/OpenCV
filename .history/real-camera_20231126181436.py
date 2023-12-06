import cv2
import firebase_admin
from firebase_admin import credentials, storage
import time
import os

# Initialize Firebase Admin SDK with the correct path to your JSON credentials file
cred = credentials.Certificate(
    "smart-parking-e0f33-firebase-adminsdk-g8j23-ba95d55480.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': "smart-parking-e0f33.appspot.com"})

# Function to delete an image


def delete_image(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted image: {file_path}")
    except Exception as e:
        print(f"Error deleting image: {e}")


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

        # Convert color format from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Save the captured frame as an image
        image_path = "captured_photo.jpg"
        cv2.imwrite(image_path, rgb_frame)

        # Upload the captured photo to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f"images/{int(time.time())}.jpg")

        try:
            blob.upload_from_filename(image_path)
            print("Photo captured and uploaded to Firebase successfully.")
        except Exception as e:
            print(f"Error uploading to Firebase Storage: {e}")

        # Delete the temporary image file
        delete_image(image_path)

        # Wait for 20 seconds
        time.sleep(10)

except KeyboardInterrupt:
    # Release the camera when the user interrupts the script (e.g., presses Ctrl+C)
    print("Interrupted by user.")

finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
