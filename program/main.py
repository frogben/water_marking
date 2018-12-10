import numpy as np
import cv2


img_path='../data/lena.jpg'
img = cv2.imread(img_path)

img_gray = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)



cv2.imshow('My Image', img_gray)

# 按下任意鍵則關閉所有視窗
cv2.waitKey(0)
cv2.destroyAllWindows()