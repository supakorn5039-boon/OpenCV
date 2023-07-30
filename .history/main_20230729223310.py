import cv2

# Video feed
cap = cv2.VideoCapture('stock-footage-car-parking-near-the-shopping-center-aerial-shooting')  # Replace 'path/to/your/video/file.mp4' with the actual file path.

while True:
    success, img = cap.read()
    if not success:
        # End of video or video cannot be read.
        break

    cv2.imshow("Image", img)

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
