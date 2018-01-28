# Standard imports
import cv2
import numpy as np 
from recogniseFace import getFaceCoordinates

#def overlapImage(image):
# Read images
src = cv2.imread("barack-obama.jpg")
coord1 = getFaceCoordinates(src)
dst = cv2.imread("white.jpg")
coord2 = getFaceCoordinates(dst, returnmode = '1D')
 
# Create a rough mask around the source image face
src_mask = np.zeros(src.shape, src.dtype)
#access the array to get left, up, right, down, and make 4 coords from it in array form
for (top_left, top_right, bottom_right, bottom_left) in coord1:
	poly = np.array([ top_left, bottom_left, bottom_right, top_right ], np.int32)
	cv2.fillPoly(src_mask, [poly], (255, 255, 255))
 
# Placing cropped image to the centre of the face of destination image
for (left, top, right, bottom) in coord2:
	center = ((int((left + right) / 2)), (int((top + bottom) / 2)))
	
	# Clone the images seamlessly, stitching both together
	output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
 	
 	# Save result
	cv2.imwrite("hello.jpg", output);