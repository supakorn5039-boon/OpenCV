import cv2

img = cv2.imread('carParkImg.png')

width, height = 107,48
posList = []

def mouseClick(events,x,y,flags,params)
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
        


while True:
                    # Draw a rectangle on the image
#cv2.rectangle(img, (1000, 2200), (50, 50), (255, 0, 255), 2)

# Display the image with the rectangle
cv2.imshow("Image", img)
cv2.setMouseCallback("Image" , mouseClick)
cv2.waitKey(0)
cv2.destroyAllWindows()
