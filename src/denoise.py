import cv2
from matplotlib import pyplot as plt

img = cv2.imread('sample_3.png', 1)

dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.imwrite("denoise.png", dst)
