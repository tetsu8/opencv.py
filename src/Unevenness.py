import cv2 as cv
import sys
import numpy as np

def main():
    orgImg = cv.imread('../resource/unevenness.tiff', 0)
    if orgImg is None:
        print('fialed load image')
        sys.exit(1)

    #kernel = np.ones((15,15), np.uint8)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (100,100))
    openImg = cv.morphologyEx(orgImg, cv.MORPH_OPEN, kernel)
    closeImg = cv.morphologyEx(orgImg, cv.MORPH_CLOSE, kernel)
    cv.imshow('org', orgImg)
    cv.imshow('opening', openImg)
    cv.imshow('closeImg', closeImg)

    cv.waitKey(0)

    mask = cv.absdiff(orgImg, closeImg)

    cv.imshow('mask', mask)
    cv.waitKey(0)

    cv.imwrite('./foreground.tiff', mask)

if __name__ == "__main__":
    main()
