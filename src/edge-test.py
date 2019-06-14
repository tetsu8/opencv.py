import cv2 as cv

def main():
    edge = cv.imread('../resource/circle/edge.png',0)
    dst = cv.imread('../resource/circle/bin.png',1)

    print(dst)

if __name__ == "__main__":
    main()
