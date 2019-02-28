# -*- coding:utf8 -*-
import os
import cv2
from PIL import Image
import numpy as np
import re

def split_img_center(imgaddress):
	RGBgroundtruth={'dynamic':[111,74,0],'ground':[81,0,81],'road':[128,64,128],'sidewalk':[244,35,232],'parking':[250,170,160],'rail track':[230,150,140],\
	'building':[70,70,70],'wall':[102,102,156],'fence':[190,153,153],'guard rail':[180,165,180],'bridge':[150,100,100],'tunnel':[150,120,90],\
	'pole':[153,153,153],'polegroup':[153,153,153],'traffic light':[250,170,30],'traffic sign':[220,220,0],'vegetation':[107,142,35],'terrain':[152,251,152],\
	'sky':[70,130,180],'person':[220,20,60],'rider':[255,0,0],'car':[0,0,142],'truck':[0,0,70],'bus':[0,60,100],\
	'caravan':[0,0,90],'trailer':[0,0,110],'train':[0,80,100],'motorcycle':[0,0,230],'bicycle':[119,11,32],'license plate':[0,0,142]}
	img = Image.open(imgaddress)#读取系统的内照片
	#img1 = cv2.imread(imgaddress)
	img= img.convert("RGB")
	img_name=re.split('[/.]',imgaddress)[-2]
	path='/home/yangshuhui/code/data/labelsplit/'+img_name #显示创建一个子文件夹
	os.makedirs(path)
	print(img_name)
	pix_position={} #存放每个类别的像素点
	pix_center={} #存放每个类别的中心点
	pix_center['imagename']=img_name #记住每张图片的名字
	for keys,values in RGBgroundtruth.items():
	    pix_position[keys]=[]
	    pix_center[keys]=[]

	width = img.size[0]#长度
	height = img.size[1]#宽度
	for i in range(0,width):#遍历所有长度的点
	    for j in range(0,height):#遍历所有宽度的点
		r,g,b = img.getpixel((i,j))
		for pixclass,pixvalue in RGBgroundtruth.items():
		    if (pixvalue[0]==r and pixvalue[1]==g and pixvalue[2]==b):
		        pix_position[pixclass].append(i)
		        pix_position[pixclass].append(j)

	for pixclass,pixposition in pix_position.items():
		if pix_position[pixclass]:  #如果这张图片上有该类别
			imgsplit = np.zeros((height,width,1), dtype=np.uint8) 
			length=int(len(pixposition)/2)
			x=0
			y=0
			for i in range(0,length-1):
			    imgsplit[pixposition[2*i+1],pixposition[2*i]]=255
			    x=x+int(pixposition[2*i])
			    y=y+int(pixposition[2*i+1])
			x=int(x/length)
			y=int(y/length)
			pix_center[pixclass].append(x)
			pix_center[pixclass].append(y)
			#cv2.circle(img1, (x, y), 10, (255,255,255), 0)
			cv2.imwrite('/home/yangshuhui/code/data/labelsplit/'+img_name+'/'+pixclass+'.PNG', imgsplit) #保存分割图
		else:
			del pix_center[pixclass]
	return pix_center 
	#cv2.namedWindow("image")
	#cv2.imshow('image', img1)
	#cv2.waitKey (10000) # 显示 10000 ms 即 10s 后消失
	#cv2.destroyAllWindows()
