import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("bv02.png", 0)
#hist = cv.calcHist([img], [0], None[256], [0, 256])
plt.hist(img.ravel(),256,[0,256]);plt.show()
