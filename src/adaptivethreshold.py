import cv2

def main():
    org = cv2.imread('../resource/unevenness.tiff', 0)
    blocksize = 9
    c = 1
    mean = cv2.adaptiveThreshold(org, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize, c)
    gaus = cv2.adaptiveThreshold(org, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, c)

    cv2.imshow('mean', mean)
    cv2.imshow('gauss', gaus)
    cv2.waitKey(0)



if __name__ == '__main__':
    main()
