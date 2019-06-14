import cv2 as cv
import tkinter,tkinter.filedialog,tkinter.messagebox,os
from matplotlib import pyplot as plt

img = cv.imread("image.tiff", 0)

ret, th = cv.threshold(img, 0, 255, cv.THRESH_OTSU)

cv.imwrite("th_otsu.tiff", th)
