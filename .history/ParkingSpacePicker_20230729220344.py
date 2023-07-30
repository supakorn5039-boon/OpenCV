import cv2

width, height = 920, 1300
posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
                

cv2.imshow("Image", img)
cv2.setMouseCallback("Image", mouseClick)

while True:
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == 27:  # Press 'Esc' to exit the loop
        break

cv2.destroyAllWindows()
