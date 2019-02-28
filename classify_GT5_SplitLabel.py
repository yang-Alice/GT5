#-*-coding:UTF-8-*-
import io
import os
import shutil

import tensorflow as tf
singleLabel=['dynamic','ground','road','sidewalk','parking','rail track',\
	'building','wall','fence','guard rail','bridge','tunnel',\
	'pole','polegroup','traffic light','traffic sign','vegetation','terrain',\
	'sky','person','rider','car','truck','bus',\
	'caravan','trailer','train','motorcycle','bicycle','license plate']

# double label 一共有406类：29个元素中的组合
def double_label(list):
	list.sort()
	double_label_dic={}
	t=0
	for i in range(0,len(list)):
		for j in range(i+1,len(list)):
			double_label_dic[t]=[list[i],list[j]]
			t=t+1
	return double_label_dic

def findKey(lists,dic):
	for key,value in dic.items():
		if lists[0]==value[0] and lists[1]==value[1]:
			return key
#判断文件夹是否存在，不存在就建立一个
def mkdir(path):
    # 判断路径是否存在. 存在:True
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
 # 得到图片的名字列表
def getname(fullnamelist):
	namelist=[]
	for fullname in fullnamelist:
		namelist.append(fullname.split('.')[0])
	return namelist

# 得到所有类别的组合字典
double_label_dic=double_label(singleLabel)

root='/home/yangshuhui/code/GT5data/label'
labelsplit_path='/home/yangshuhui/code/GT5data/labelsplit'
picturefiles = os.listdir(labelsplit_path)  #picturefiles=['00001',....]

for splitfiles in picturefiles:
	singlelabel=labelsplit_path+'/'+splitfiles
	labelsplit_namelist = os.listdir(singlelabel) 
	labelsplit_namelist=getname(labelsplit_namelist)
	# 得到单个文件夹下类别的组合字典onepathdouble_label
	onepathdouble_label=double_label(labelsplit_namelist)
	for value in onepathdouble_label.values():
		labelnum=findKey(value,double_label_dic)
		labelpath=root+'/'+str(labelnum)+'/'
		mkdir(labelpath)
		for i in range(0,2):
			splitimagedir=singlelabel+'/'+value[i]+'.PNG'
			topath=labelpath+splitfiles+value[i]+'.PNG'
			shutil.copy(splitimagedir,topath)
	print(splitfiles)



