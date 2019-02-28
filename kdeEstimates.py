# -*- coding:utf8 -*-
import os
import cv2
from PIL import Image
import numpy as np
import re


## 统计每张图片上的每一类的像素 
def split_img_center(img_addr):
    RGBgroundtruth = {'dynamic':[111,74,0],'ground':[81,0,81],'road':[128,64,128],'sidewalk':[244,35,232],'parking':[250,170,160],'rail track':[230,150,140],\
                      'building':[70,70,70],'wall':[102,102,156],'fence':[190,153,153],'guard rail':[180,165,180],'bridge':[150,100,100],'tunnel':[150,120,90],\
                      'pole':[153,153,153],'polegroup':[153,153,153],'traffic light':[250,170,30],'traffic sign':[220,220,0],'vegetation':[107,142,35],'terrain':[152,251,152],\
                      'sky':[70,130,180],'person':[220,20,60],'rider':[255,0,0],'car':[0,0,142],'truck':[0,0,70],'bus':[0,60,100],\
                      'caravan':[0,0,90],'trailer':[0,0,110],'train':[0,80,100],'motorcycle':[0,0,230],'bicycle':[119,11,32],'license plate':[0,0,142]}
    #读取图片
    img = Image.open(img_addr)
    img = img.convert("RGB")
    #img_name=re.split('[/.]',img_addr)[-2]
    # path='/home/yangshuhui/code/data/labelsplit/'+img_name #显示创建一个子文件夹
    # os.makedirs(path)
    # print(img_name)

    class_pixel = {}    #类像素点
    class_center = {}   #类中心点
    class_road_pos = {} #每类对地位置

    for cls, rgb in RGBgroundtruth.items():
        class_pixel[cls] = []
        class_center[cls] = []

    width = img.size[0]  
    height = img.size[1] 

    ##存每类像素点坐标，列表存储
    for i in range(0, width):
        for j in range(0, height):
            r, g, b = img.getpixel((i, j))
	    for cls, rgb in RGBgroundtruth.items():
	        if (rgb[0]==r and rgb[1]==g and rgb[2]==b):
                    class_pixel[cls].append(i)
	            class_pixel[cls].append(j)

    ##计算每一类的中心点
    for cls, coor in class_pixel.items():
        if class_pixel[cls]:  #如果这张图片上有该类别
            class_center[cls].append(sum(coor[::2])/len(coor)*2)
	    class_center[cls].append(sum(coor[1::2])/len(coor)*2)
        else:
	    del class_center[cls]
        
    ##计算每类对地位置
    for cls, center in class_center.items():
        class_road_pos[cls] = []
        class_road_pos[cls].append(center[0] - class_center['road'][0])
        class_road_pos[cls].append(center[1] - class_center['road'][1])

#    class_road_pos['road'] = class_center['road']
#    del class_road_pos['imagename']

    return class_road_pos 
