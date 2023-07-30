import cv2

img = cv2.imread('carParkImg.png')

width, height = 1000, 1500
posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

cv2.imshow("Image", img)
cv2.setMouseCallback("Image", mouseClick)

while True:
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == 27:  # Press 'Esc' to exit the loop
        break

cv2.destroyAllWindows()
