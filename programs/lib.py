# coding: utf-8
import numpy as np
import cv2
import hashlib
from operator import xor

def cal_sigma(round_pix):
    sigma=0
    for i in range(7):
        diff=int(round_pix[i])-int(round_pix[i+1])
        diff_squar=diff**2
        sigma+=diff_squar

    diff=int(round_pix[7])-int(round_pix[0])
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
    # print('$$$$')
    # print('folded_feature:',folded_feature)
    # print('$$$$')
    middle_pix_val+=int(folded_feature,2)
    return middle_pix_val


def folder_feature(hashed_feature,num_LSB):
    hashed_feature_bin=bin(int(hashed_feature,16))
    hashed_feature_bin=hashed_feature_bin[2:]
    hashed_feature_bin=hashed_feature_bin.rjust(128,'0')
    hashed_feature_bin+="0000"
    bit_list=[]
  
    for i in range(0,len(hashed_feature_bin),num_LSB):
        bit_list.append(hashed_feature_bin[i:i+num_LSB])
   
    for j in range(len(bit_list)-1):
        this_bit=int(bit_list[j],2)
        next_bit=int(bit_list[j+1],2)
        exclusive_or=this_bit^next_bit
        exclusive_or_bin=bin(exclusive_or)
        exclusive_or_bin=exclusive_or_bin[2:]
        exclusive_or_bin=exclusive_or_bin.rjust(num_LSB,'0')
        bit_list[j+1]=exclusive_or_bin
    
    return bit_list[len(bit_list)-1]

    


"""
目前只有實作灰階  
out_path 

"""
def add_waterMarking(img_gray):
    
    img_shape=img_gray.shape
    # img_shape=(512,512)
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

            middle_pix_val=img_gray[h+1,w+1]
            folded_feature=folder_feature(hashed_feature,num_LSB)
            img_gray[h+1,w+1]=cal_hidden_val(middle_pix_val,folded_feature,num_LSB)

            block_index+=1
    return img_gray


##目前只有實作灰階
def validate_waterMarking(img_gray):
    
    modified_box_index=[]
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
                hidden_LSB_feature=middle_pix_val & 3
            elif(num_LSB==3):
                hidden_LSB_feature=middle_pix_val & 7
            else:
                hidden_LSB_feature=middle_pix_val & 15
        
            hidden_LSB_feature=bin(hidden_LSB_feature)
            hidden_LSB_feature=hidden_LSB_feature[2:]
            hidden_LSB_feature=hidden_LSB_feature.rjust(num_LSB,'0')
            
            hashed_feature=cal_hidden_hash(round_pix,block_index,ID_image,SK)
            # print('hashed_feature:',hashed_feature)
            cal_folded_feature=folder_feature(hashed_feature,num_LSB)
            # print('hidden_LSB_feature',hidden_LSB_feature)
            # print('cal_folded_feature',cal_folded_feature)
            # print('-------------------')
            if(hidden_LSB_feature!=cal_folded_feature):
                flag=False
                modified_box_index.append(block_index)
            block_index+=1
    return flag,modified_box_index

def get_modified_block(modified_box_index,img_shape):

    height=img_shape[0]
    width=img_shape[1]
    row_block_volumns=(width-1)//2
    modified_box_index+=1
    
    x=(modified_box_index%row_block_volumns)*2
    y=(modified_box_index//row_block_volumns)*2

    return (y,x)



