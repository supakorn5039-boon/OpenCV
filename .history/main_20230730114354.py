import cv2
import pickle

width, height = 70, 27

def checkParkingSpace():
    for pos in posList:
        cv2.rectangle(img_copy, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

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

    img_copy = img.copy()  # Create a copy of the frame to draw rectangles on the copy.
    checkParkingSpace()    # Draw rectangles on the copy of the frame

    # Draw the triangle here if it's part of the original frame
    # For example, to draw a triangle at points (x1, y1), (x2, y2), and (x3, y3) with color (0, 255, 0) and thickness 1:
    # cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 1)
    # cv2.line(img_copy, (x2, y2), (x3, y3), (0, 255, 0), 1)
    # cv2.line(img_copy, (x3, y3), (x1, y1), (0, 255, 0), 1)

    cv2.imshow("Image", img_copy)

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
