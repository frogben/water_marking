import numpy as np
import cv2
import hashlib

def cal_sigma(round_pix):
    sigma=0
    for i,v in enumerate(round_pix):
        if(i!=7):
            diff=round_pix[i]-round_pix[i+1]
            diff_squar=diff**2
            sigma+=diff_squar
        else:
            diff=round_pix[7]-round_pix[0]
            diff_squar=diff**2
            sigma+=diff_squar
    if(sigma<8):
        return 2
    elif( (8<=sigma) and (sigma<16) ):
        return 3
    else:
        return 4
def cal_hidden_hash(round_pix,block_index,ID_image,SK):
    all_str=""
    for i,v in enumerate(round_pix):
        binary_str=bin(v)
        binary_str=binary_str[2:]
        all_str+=binary_str
    binary_str=bin(block_index)
    binary_str=binary_str[2:]
    all_str+=binary_str
    binary_str=bin(ID_image)
    binary_str=binary_str[2:]
    all_str+=binary_str
    binary_str=bin(SK)
    binary_str=binary_str[2:]
    all_str+=binary_str

    #hash
    m = hashlib.md5()
    m.update(all_str.encode("utf-8"))
    h = m.hexdigest()
    return h


def cal_hidden_val(middle_pix_val,folded_feature,num_LSB):
    if(num_LSB==2):
        middle_pix_val=middle_pix_val & 252
    elif(num_LSB==3):
        middle_pix_val=middle_pix_val & 248
    else:
        middle_pix_val=middle_pix_val & 240
    middle_pix_val+=folded_feature
    return middle_pix_val


def folder_feature(hashed_feature,num_LSB):
    hashed_feature+="0000"
    bit_list=[]
    for i in range(0,len(hashed_feature),num_LSB):
	    bit_list.append(hashed_feature[i:i+num_LSB])
    for i in range(len(bit_list)-1):
        exclusive_or=int(bit_list[i],2)!=int(bit_list[i+1],2)
        binary_exclusive_or=bin(exclusive_or)
        binary_exclusive_or=binary_exclusive_or[2:]
        bit_list[i+1]=binary_exclusive_or
    return bit_list[len(bit_list)]
    

##目前只有實作灰階
def add_waterMarking(img_gray,out_path):
    
    img_shape=img_gray.shape
    #參數設定#

    #index of block
    block_index=0
    #Identification
    ID_image=20 
    #User's secrest key
    SK=16

    for h in range(0,img_shape[0]-2,2):
        for w in range(0,img_shape[1]-2,2):
            round_pix=[]
            round_pix.append(img_gray[h,w])
            round_pix.append(img_gray[h,w+1])
            round_pix.append(img_gray[h,w+2])
            round_pix.append(img_gray[h+1,w])
            round_pix.append(img_gray[h+1,w+2])
            round_pix.append(img_gray[h+2,w])
            round_pix.append(img_gray[h+2,w+1])
            round_pix.append(img_gray[h+2,w+2])
            
            num_LSB=cal_sigma(round_pix)
            hashed_feature=cal_hidden_hash(round_pix,block_index,ID_image,SK)
            block_index+=1
            middle_pix_val=img_gray[h+1,w+1]
            folded_feature=folder_feature(hashed_feature,num_LSB)
            img_gray[h+1,w+1]=cal_hidden_val(middle_pix_val,folded_feature,num_LSB)
    
    cv2.imwrite(out_path, img_gray,[cv2.IMWRITE_JPEG_QUALITY, 100])

##目前只有實作灰階
def validate_waterMarking(img_gray):
    
    img_shape=img_gray.shape
    #參數設定#

    #index of block
    block_index=0
    #Identification
    ID_image=20 
    #User's secrest key
    SK=16
    
    flag=True

    for h in range(0,img_shape[0]-2,2):
        for w in range(0,img_shape[1]-2,2):
            round_pix=[]
            round_pix.append(img_gray[h,w])
            round_pix.append(img_gray[h,w+1])
            round_pix.append(img_gray[h,w+2])
            round_pix.append(img_gray[h+1,w])
            round_pix.append(img_gray[h+1,w+2])
            round_pix.append(img_gray[h+2,w])
            round_pix.append(img_gray[h+2,w+1])
            round_pix.append(img_gray[h+2,w+2])
            
            num_LSB=cal_sigma(round_pix)

            middle_pix_val=img_gray[h+1,w+1]

            if(num_LSB==2):
                LSB_feature=middle_pix_val & 3
            elif(num_LSB==3):
                LSB_feature=middle_pix_val & 7
            else:
                LSB_feature=middle_pix_val & 15
            
            
            hashed_feature=cal_hidden_hash(round_pix,block_index,ID_image,SK)

            LSB_feature
                    

            
            block_index+=1
            
            img_gray[h+1,w+1]=cal_hidden_val(middle_pix_val,hashed_feature,num_LSB)
    
    return flag

img_path='../data/lena.jpg'
img_gray = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
add_waterMarking(img_gray,'../data/output2.jpg')