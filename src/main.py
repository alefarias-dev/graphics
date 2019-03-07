import cv2
from image_processing.filters import clarear, escurecer
from image_processing.data import histogram
import matplotlib.pyplot as plt

img = cv2.imread('../.temp/pardal.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

k = 120

f1 = clarear(img, k)
f2 = escurecer(img, k)

plt.imshow(img)
plt.show()

plt.imshow(f1)
plt.show()

plt.imshow(f2)
plt.show()

histogram(img, '../.temp/hist_original.png')