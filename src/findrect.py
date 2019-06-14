import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from PIL import Image
import sys
import os

def draw_contours(ax, img, contours):
    ax.imshow(img)
    ax.axis('off')
    for i, cnt in enumerate(contours):
        cnt = np.squeeze(cnt,axis=1)
        x, y ,w, h = cv2.boundingRect(cnt)
        #ax.add_patch(Polygon(cnt, color='b', fill=None, lw=2))
        #ax.plot(cnt[:, 0], cnt[:, 1], 'ro', mew=0, ms=4)
        #ax.text(cnt[0][1], cnt[0][1], i, color='orange', size='20')
        ax.add_patch(Rectangle(xy=(x, y), width=w, height=h, color='g', fill=None, lw=2))

def getRotateRect(ax, img, contours):
    ax.imshow(img)
    ax.axis('off')
    for i, cnt in enumerate(contours):
        rect = cv2.minAreaRect(cnt)
        (cx, cy), (width, height), angle = rect
        rect_points = cv2.boxPoints(rect)
        ax.add_patch(Polygon(rect_points, color='g', fill=None, lw=2))
        ax.text(cx, cy, angle+90, color='orange', size='20')

def getExtList(path, uExt):
    extlist = []
    for dfile in os.listdir(path):
        base, ext= os.path.splitext(dfile)
        if ext == uExt:
            extlist.append(dfile)

    return extlist

def getRect(path):
    img = cv2.imread(path)
    if img is None:
        print('failed load image')
        sys.exit(1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binImg = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    #cv2.imshow('bin', binImg)
    #cv2.waitKey(0)

    kernel = np.ones((10,10), np.uint8)
    closeImg = cv2.morphologyEx(binImg, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closing', closImg)
    #cv2.waitKey(0)
    openImg = cv2.morphologyEx(closeImg, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening', openImg)
    #cv2.waitKey(0)
    #dst = cv2.GaussianBlur(dst, (5,5), 0)
    revImg = cv2.bitwise_not(openImg)
    #cv2.imshow('reverse', revImg)
    #cv2.waitKey(0)

    _, contours, hierarchy = cv2.findContours(revImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    approx_contours = []
    for i, cnt in enumerate(contours):
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        approx_contours.append(approx)

    fig, ax = plt.subplots(figsize=(6,6))
    #draw_contours(ax, img, contours)
    #draw_contours(ax, img, approx_contours)
    getRotateRect(ax, img, approx_contours)
    plt.show()

def main():
    filelist = getExtList('../resource/rectImg/', '.tiff')
    for img in filelist:
        getRect('../resource/rectImg/' + img)

# Entry point
if __name__ == "__main__":
    main()
