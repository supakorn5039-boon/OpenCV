import cv2

img = cv2.imread('carParkImg.png')

# Define the coordinates for the three vertices of the triangle
vertices = [(100, 100), (200, 100), (150, 50)]

# Create an array of points in the format required by fillPoly
pts = [vertices]

# Draw a filled triangle on the image
cv2.fillPoly(img, pts, (0, 255, 0))

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
