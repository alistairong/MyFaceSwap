# Standard imports
import cv2
import numpy as np 
 
# Read images
src = cv2.imread("harambe.jpg")
dst = cv2.imread("white.jpg")
 
 
# Create a rough mask around the face.
src_mask = np.zeros(src.shape, src.dtype)
poly = np.array([ [1,1], [1,700], [700,700], [700,1] ], np.int32)
cv2.fillPoly(src_mask, [poly], (255, 255, 255))
 
# This is where the CENTER of the airplane will be placed
width, height, channels = src.shape
center = ((int(height / 2)), (int(width / 2)))
 
# Clone seamlessly.
output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
 
# Save result
cv2.imwrite("test.jpg", output);

# import cv2
# import numpy as np
 
# # Read images : src image will be cloned into dst
# im = cv2.imread("harambe.jpg")
# obj= cv2.imread("white.jpg")
 
# # Create an all white mask
# mask = 255 * np.ones(obj.shape, obj.dtype)
 
# # The location of the center of the src in the dst
# width, height, channels = im.shape
# center = ((int(height / 2)), (int(width / 2)))
# print (center)
 
# # Seamlessly clone src into dst and put the results in output
# #normal_clone = cv2.seamlessClone(obj, im, mask, center, cv2.NORMAL_CLONE)
# mixed_clone = cv2.seamlessClone(obj, im, mask, center, cv2.MIXED_CLONE)
 
# # Write results
# #cv2.imwrite("test.jpg", normal_clone)
# cv2.imwrite("test2.jpg", mixed_clone)