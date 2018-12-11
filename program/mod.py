import numpy as np
import cv2
import hashlib
from operator import xor


# 認證的灰階圖片
encode_path='../data/lena_encode.bmp'
# 被修改過的已認證的灰階圖片
mod_encode_path='../data/lena_encode_modified.bmp'


# 讀取未認證的灰階圖片
img_gray = cv2.imread(encode_path,cv2.IMREAD_GRAYSCALE)
img_gray[100,30]=10
cv2.imwrite(mod_encode_path,img_gray)

