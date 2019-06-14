import cv2 as cv
import numpy as np

def main():
    img = cv.imread("denoise.png")
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    gamma = 2.0

    imax = gray.max()

    gray = imax * (gray / imax)**(1/gamma)

    cv.imshow('aa', gray)
    cv.waitKey(0)

if __name__ == "__main__":
    main()

