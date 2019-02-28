# -*- coding:utf8 -*-
import kdeEstimates
import os 
import numpy as np
from sklearn.neighbors import KernelDensity
import seaborn as sns
import csv

# 分割图路径 
label_list = '/home/yangshuhui/code/data/label_list.txt'

pos_list = {'dynamic':[],'ground':[],'road':[],'sidewalk':[],'parking':[],'rail track':[],\
	'building':[],'wall':[],'fence':[],'guard rail':[],'bridge':[],'tunnel':[],\
	'pole':[],'polegroup':[],'traffic light':[],'traffic sign':[],'vegetation':[],'terrain':[],\
	'sky':[],'person':[],'rider':[],'car':[],'truck':[],'bus':[],\
	'caravan':[],'trailer':[],'train':[],'motorcycle':[],'bicycle':[],'license plate':[]}

#class_road_pos = {}


# 功能：将一个二重列表写入到csv文件中
# 输入：文件名称，数据列表
def createListCSV(fileName = "", dataList = []):
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        for data in dataList:
            csvWriter.writerow(data)
        csvFile.close

# 读取groundtruth图片，计算每一类的中心点
with open(label_list) as file_object:
    lines = file_object.readlines()
    # line example: /home/yangshuhui/code/data/GT5label/label3/06753.png
    for line in lines:
	class_road_pos = kdeEstimates.split_img_center(line.rstrip())
	for cls, pos in class_road_pos.items():
            pos_list[cls].append(pos)

# kde函数生成
for cls, pos in pos_list.items():
    #createListCSV(cls, pos)
    if pos:
        X = np.array(pos)
        print(X)
        kde = KernelDensity(kernel = 'gaussian', bandwidth = 0.2).fit(X) 
