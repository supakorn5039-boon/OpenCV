import pickle
import cv2

img = cv2.imread('carParkImg.png')

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.rectangle(img,(100,100),(200,150),(255,0,255),2)

