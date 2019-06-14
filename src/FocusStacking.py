import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def main():
    img1 = cv.imread('../resource/3Di/001.jpg',1)
    img2 = cv.imread('../resource/3Di/002.jpg',1)
    gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    gray2 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    grayImgs = [gray1, gray2]
    #showImg(gray)
    #cv.imwrite('gray.png', gray)
    EdfComplexWavelet(grayImgs)

def showImg(img):
    cv.namedWindow('show image', cv.WINDOW_NORMAL)
    cv.imshow('show image', img)
    cv.waitKey(0)

def EdfComplexWavelet(images):
    nx,ny = images[0].shape
    nz = len(images)
    text = 'read image size height={}, width={}, z={}'
    print(text.format(nx,ny,nz))

    sbConsistencyCheck = True
    majConsistencyCheck = True

    scale = 1

    buf = [][]


if __name__ == "__main__":
    main()
