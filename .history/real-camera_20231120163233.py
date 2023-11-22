import cv2

# Open the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Continuously capture frames from the camera
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the frame in a window
    cv2.imshow('Camera Feed', frame)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
