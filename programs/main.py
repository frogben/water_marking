import lib
import numpy as np
import cv2

"""
第一部分 

lena_gray.bmp使用add_waterMarking()認證後

存檔成 lena_encode.bmp

"""

# 未認證的灰階圖片
gray_path='../data/lena_gray.bmp'
# 認證的灰階圖片
encode_path='../data/lena_encode.bmp'
# 被修改過的已認證的灰階圖片
modified_path="../data/lena_encode_modified.bmp"

# 讀取未認證的灰階圖片
img_gray = cv2.imread(gray_path,cv2.IMREAD_GRAYSCALE)

# 認證
img_encode=lib.add_waterMarking(img_gray)

# 存檔認證過的灰階圖片
cv2.imwrite(encode_path,img_encode)


"""
第二部分 

取認證後過後的lena_encode.bmp

修改部分pixel 模擬竄改

存檔成 lena_encode_modified.bmp

"""

讀取未認證的灰階圖片
img_gray = cv2.imread(encode_path,cv2.IMREAD_GRAYSCALE)
img_gray[50,30]=10
cv2.imwrite(modified_path,img_gray)


"""
第三部分 

取被竄改過後的lena_encode_modified.bmp

利用validate_waterMarking()檢測

1)是否有被修改過
2)被修改過的大概位置

為了有對照組，使用lena_encode.bmp做比對


"""

# 測試lena_encode_modified.bmp有沒有被修改過
img_test = cv2.imread(modified_path,cv2.IMREAD_GRAYSCALE)
flag,modified_box_index=lib.validate_waterMarking(img_test)

if(flag==False):
    print(modified_path,'已被修改')
    print('被修改的位置大略為:')
    print('(   H ,   W )')
    for i in modified_box_index:
        coor=lib.get_modified_block(i,img_test.shape)
        print("(",str(coor[0]).rjust(4,' '),",",str(coor[1]).rjust(4,' '),")")
else:
    print(modified_path,'保持原樣')

# 測試lena_encode.bmp有沒有被修改過
img_test = cv2.imread(encode_path,cv2.IMREAD_GRAYSCALE)
flag,modified_box_index=lib.validate_waterMarking(img_test)
if(flag==False):
    print(modified_path,'已被修改')
    print('被修改的位置大略為:')
    print('(   H ,   W )')
    for i in modified_box_index:
        coor=lib.get_modified_block(i,img_test.shape)
        print("(",str(coor[0]).rjust(4,' '),",",str(coor[1]).rjust(4,' '),")")
else:
    print(modified_path,'保持原樣')


