import cv2 as cv
import numpy as np

img = cv.imread('../resorce/rotate_chip_2.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edge = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 71, 7)
#median = np.median(gray)
#edge = cv.Canny(gray, median * 0.6, median * 1.23)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (7,7))
edge = cv.morphologyEx(edge, cv.MORPH_OPEN, kernel)

cv.imshow('', edge)
cv.waitKey(0)
cv.destroyAllWindows()

lines = cv.HoughLinesP(edge, 1, np.pi/180, 150, 10, 50)

print(lines)

if lines is not None:
    for x1,y1,x2,y2 in lines[0]:
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    cv.imshow('', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print('lines is null')

