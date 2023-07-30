import cv2
import pickle
import cvzone

width, height = 70, 27

def drawCount(imgPro, count, x, y):
    text = str(count)
    font_scale = 0.5
    thickness = 1

    # Get the size of the text to determine the size of the background rectangle
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)

    # Create a background rectangle with increased alpha to make it brighter
    overlay = imgPro.copy()
    background_height = text_height + 10
    cv2.rectangle(overlay, (x, y + height - background_height), (x + text_width + 10, y + height), (255, 255, 255), -1)
    cv2.addWeighted(overlay, 0.8, imgPro, 0.2, 0, imgPro)  # Increased alpha value (0.8) for a brighter background

    # Create a mask for the text region to overlay on the original image
    mask = overlay[:, :, 0]  # Use one of the channels as the mask
    mask_inv = cv2.bitwise_not(mask)
    img_bg = cv2.bitwise_and(imgPro, imgPro, mask=mask_inv)
    img_text = cv2.bitwise_and(overlay, overlay, mask=mask)

    # Resize the overlay arrays to match the background size
    img_text_resized = cv2.resize(img_text, (img_bg.shape[1], background_height))

    # Make sure both arrays have the same number of channels
    img_text_resized = img_text_resized[:,:,:3]

    # Overlay the text on the background image in the region of interest (ROI)
    imgPro[y + height - background_height:y + height, x:x + text_width + 10] = cv2.addWeighted(img_bg, 1, img_text_resized, 1, 0)

    # Draw the count number as black text
    cv2.putText(imgPro, text, (x + 5, y + height - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)


def checkParkingSpace(imgPro, imgOriginal):
    for pos in posList:
        x, y = pos
        cv2.rectangle(imgOriginal, pos, (x + width, y + height), (255, 0, 255), 2)
        
        imgCrop = imgPro[y:y + height, x:x + width]
        if imgCrop.shape[0] > 0 and imgCrop.shape[1] > 0:
            count = cv2.countNonZero(imgCrop)
            drawCount(imgOriginal, count, x, y)  # Draw count inside the parking space

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

    img_copy = img.copy()  # Create a copy of the frame to draw rectangles and text on the copy.
    
    # Preprocess the image - Convert to HSV and threshold on the saturation channel
    img_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    saturation = img_hsv[:, :, 1]  # Saturation channel
    _, imgThreshold = cv2.threshold(saturation, 100, 255, cv2.THRESH_BINARY)

    checkParkingSpace(imgThreshold, img_copy)  # Pass imgThreshold and img_copy as arguments

    cv2.imshow("Image", img_copy)
    cv2.imshow("Threshold", imgThreshold)
    

    # Wait for a small delay (e.g., 30 milliseconds) and check if 'q' is pressed to exit.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()
