import cv2 as cv
import tkinter,tkinter.filedialog,tkinter.messagebox,os
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
import numpy as np
import random

root = tkinter.Tk()
root.withdraw()
fType = [("",".*")]
iDir = os.path.abspath(os.path.dirname(__file__))
filepath = tkinter.filedialog.askopenfilename(filetypes = fType,initialdir = iDir)

file = open(filepath, 'rb')

rawdata = file.read()
#img = Image.open(BytesIO(rawdata))
#print(type(rawdata))

width = 1024
height = 895
widthstep = 2048
buff = [0] * (width * height)

#16→8bitに変換
for i in range(height):
    for j in range (width):
        offset = widthstep * i + j * 2
        lower = rawdata[offset]
        upper = rawdata[offset + 1]
        val = bin(int((upper << 8)) | lower)
        fval = int(val, 0) * 0.05 - 1000

        offset2 = i * width + j
        buff[offset2] = min(255, max(0, fval))

sBuff = buff[:]
sBuff.sort()
cval = 0
size = len(sBuff)
#
#print((size / 2) - 1)
if size % 2 == 1:
    cval = sBuff[(size - 1) / 2]
else:
    cval = (sBuff[int((size / 2) - 1)] + sBuff[int(size / 2)]) / 2

#f = np.frombuffer(buff, dtype = np.uint8, count = height * width)

print(cval)
# 16bit→8bitに変換したbuffをnparrayに変換
data = np.array(buff, np.uint8)
data = data.reshape((height, width))
#ret, th = cv.threshold(im, 0, cval, cv.THRESH_BINARY)

#nparrayをpilイメージに変換
pilImg = Image.fromarray(data)
#pilイメージをcvイメージに変換
cvImg = np.asarray(pilImg)

#blur = cv.GaussianBlur(cvImg, (3, 3), 2)
#blur = cv.GaussianBlur(blur, (3, 3), 2)

#cv.imshow('blur', blur)
#cv.waitKey(0)
#cv.destroyAllWindows()

#binalize = cv.threshold(blur, 0, cval, cv.THRESH_BINARY)[1]
binalize = cv.adaptiveThreshold(cvImg, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 651, 3)

cv.imshow('threshold', binalize)
cv.waitKey(0)
cv.destroyAllWindows()

ret, mark = cv.connectedComponents(binalize)

# ラベリング結果書き出し準備
color_src = cv.cvtColor(binalize, cv.COLOR_GRAY2BGR)
height, width = binalize.shape[:2]
colors = []

for i in range(1, ret + 1):
    colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))

# ラベリング結果を画面に表示
# 各オブジェクトをランダム色でペイント
for y in range(0, height):

    for x in range(0, width):
        if mark[y, x] > 0:
            color_src[y, x] = colors[mark[y, x]]
        else:
            color_src[y, x] = [0, 0, 0]

cv.imshow('threshold', color_src)
cv.waitKey(0)
cv.destroyAllWindows()

#img = Image.frombytes('F', (1024, 895), rawdata,"raw", 'F16B')
#npimg = np.array(buff)
#plt.hist(npimg.ravel(),256,[0,256]);plt.show()
