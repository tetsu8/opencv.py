import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import copy
import wavelet
import time

def main():
    print('step1:call main()')
    start = time.time()
    try:
        img1 = cv.imread('../resource/3Di/001.jpg',1)
        img2 = cv.imread('../resource/3Di/002.jpg',1)
        gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        grayImgs = [gray1, gray2]
        #showImg(gray)
        #cv.imwrite('gray.png', gray)
        res = EdfComplexWavelet(grayImgs)

        showImg(res)
    except BaseException as err:
        print('catch Exception: {}'.format(err))
        print('process time: {}s'.format(int(time.time() - start + 0.5)))

def showImg(img: np.ndarray):
    cv.namedWindow('show image', cv.WINDOW_NORMAL)
    cv.imshow('show image', img)
    cv.waitKey(0)

def EdfComplexWavelet(images: np.ndarray) -> np.ndarray:
    print('step2:Call EdfComplexWavelet()')
    nx,ny = images[0].shape
    nz = len(images)
    text = 'read image size height={}, width={}, z={}'
    print(text.format(nx,ny,nz))

    sbConsistencyCheck = True
    majConsistencyCheck = True

    scale = 1
    length = 14

    tmp = np.zeros((2, nx * ny))
    resRe = np.zeros((2, nx * ny))
    resIm = np.zeros((2, nx * ny))


    #if sbConsistencyCheck or majConsistencyCheck :



    for z in range(nz):
        img = images[z]

        buf = copy.copy(img)
        print('step3-{}: start analysis'.format(z))
        coefftemp = wavelet.ComplexWavelet.analysis(buf, scale, length)
        tmpRe = coefftmp[0]
        tmpIm = coefftmp[1]

        for i in range(nx):
            for j in range(ny):
                valRe = tmpRe[i,j]
                tmpim = tmpIm[i,j]
                newval = valRe * valRe + valIm * valIm
                oldval = tmp[i,j]

                if oldval <= newval:
                    tmp[i,j] = newval
                    resRe[i,j] = newval
                    resIm[i,j] = newval

        iabufRe = copy.copy(resRe)
        iabufIm = copy.copy(recIm)

        print('step4-{}: start synthesis'.format(z))
        coefftmp = wavelet.ComplexWavelet.synthesis(iabufRm, iabufIm, scale, length)
        tmpRe = coefftmp[0]
        tmpIm = coefftmp[1]

        return tmpRe


if __name__ == "__main__":
    main()
