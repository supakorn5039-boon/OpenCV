import cv2
import time

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

        print("Photo captured successfully.")

        # Wait for 10 seconds
        time.sleep(20)

except KeyboardInterrupt:
    # Release the camera when the user interrupts the script (e.g., presses Ctrl+C)
    print("Interrupted by user.")
finally:
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
