import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../resource/3Di/002.jpg', 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
edges = cv2.Canny(img,60,90)
dilation = cv2.dilate(edges, None, 1)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dilation,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
