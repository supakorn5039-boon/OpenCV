import cv2
import pickle
from PIL import Image
import numpy as np

img_path = 'IMG_6310.HEIC'
img_pil = Image.open(img_path).convert('RGB')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

width, height = 55, 20

# Try to load posList from the file, or initialize it as an empty list
try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []


def mouseClick(events, x, y, flags, params):
    global posList

    if events == cv2.EVENT_LBUTTONDOWN:  # Left Click to create a Triangle
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:  # Right Click to Delete a Triangle
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    # Save the updated posList to the file after each change
    with open('carParkPos', 'wb') as f:
        pickle.dump(posList, f)


if img is None:
    print(f"Error: Image not loaded. Check the file path: {img_path}")
else:
    print("Image loaded successfully. Shape:", img.shape)

    # Display the loaded image
    cv2.imshow("Image", img)

    while True:
        img_copy = img.copy()  # Create a copy of the original image to draw on
        for pos in posList:
            cv2.rectangle(
                img_copy, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Image", img_copy)
        key = cv2.waitKey(1)

        if key == 27:  # Press 'Esc' to exit the loop
            break

    cv2.destroyAllWindows()
