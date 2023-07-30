import cv2
import numpy as np

img = cv2.imread('carParkImg.png')

# Define the coordinates for the three vertices of the triangle
vertices = np.array([(100, 100), (200, 100), (150, 50)], np.int32)

# Reshape the vertices to the required format
vertices = vertices.reshape((-1, 1, 2))

# Draw a filled triangle on the image
cv2.fillPoly(img, [vertices], (0, 255, 0))

cv2.imshow("image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
