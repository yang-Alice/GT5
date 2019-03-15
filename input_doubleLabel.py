#-*-coding:UTF-8-*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import os
import random
import sys
import threading

import numpy as np
import tensorflow as tf
from PIL import Image
import PIL

train_directory='/home/yangshuhui/code/GT5data/label'
output_directory='/home/yangshuhui/code/GT5data/TFRecordfiles'
test='/home/yangshuhui/code/GT5data/test'

def _bytes_feature(value):
	return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _numpy_feature(value):
	value=value.tostring()
	return _bytes_feature(value)

def find_image_files(onechasspath):
	allfilename=os.listdir(onechasspath)
	allfilename.sort()
	filenames={}

	for i in range(int(len(allfilename)/2)):
		first=allfilename[2*i]
		second=allfilename[2*i+1]
		if first[0:5]==second[0:5]:
			filenames[i]=[]
			first=onechasspath+'/'+first
			second=onechasspath+'/'+second
			filenames[i].append(first)
			filenames[i].append(second)
			
		else:
			print('double data name is wrong')
			print(onechasspath)
			print(first[0:5]+second)
	return filenames
'''
{0: ['/home/yangshuhui/code/GT5data/test/1/00117bicycle.PNG', '/home/yangshuhui/code/GT5data/test/1/00117bridge.PNG'], 
1: ['/home/yangshuhui/code/GT5data/test/1/00118bicycle.PNG', '/home/yangshuhui/code/GT5data/test/1/00118bridge.PNG'], 
2: ['/home/yangshuhui/code/GT5data/test/1/00120bicycle.PNG', '/home/yangshuhui/code/GT5data/test/1/00120bridge.PNG']}

'''

def add_two_image(imageone,imagetwo):
	oneimage=np.asarray(PIL.Image.open(imageone))
	twoimage=np.asarray(PIL.Image.open(imagetwo))
	doubleimage=np.stack((oneimage,twoimage),axis=0) 
	doubleimage=doubleimage.reshape((2,1052,1914,1))
	return doubleimage
			

def _convert_to_example(filename, label,image):
	example=tf.train.Example(features=tf.train.Features(feature={
			'filename':_bytes_feature(filename),
			'label':_bytes_feature(label),
			'image':_numpy_feature(image)}))
	return example

def find_road(filenames):
	str1=filenames[0][0]
	str2=filenames[0][1]
	tag=False
	if str1.find('road')>-1 or str2.find('road')>-1:
		tag=True
	return tag 
	

def create_record(rootpath):
	labels=os.listdir(rootpath)
	labels.sort()

	for label in labels:
		output_filename=("Train_TFRecords_%.5d" %int(label))
		output_file = os.path.join(output_directory, output_filename)		
		onechasspath=rootpath+'/'+label
		filenames=find_image_files(onechasspath)

		if find_road(filenames):
			writer=tf.python_io.TFRecordWriter(path=output_file)
			print(label)
			for doubleimagepath in filenames.values():
				oneimage=doubleimagepath[0]
				twoimage=doubleimagepath[1]
				doubleimage=add_two_image(oneimage,twoimage)
				Fname=oneimage.split('/')[-1][:-4]+twoimage.split('/')[-1][:-4]
				example=_convert_to_example(Fname,label,doubleimage)
				writer.write(record=example.SerializeToString())
			writer.close()
'''
filenames=find_image_files('/home/yangshuhui/code/GT5data/test/1')
print(filenames)

imageone='/home/yangshuhui/code/GT5data/test/2/00458bicycle.PNG'
imagetwo='/home/yangshuhui/code/GT5data/test/2/04101bus.PNG'
oneimage=np.asarray(PIL.Image.open(imageone))
twoimage=np.asarray(PIL.Image.open(imagetwo))
doubleimage=np.dstack((oneimage,twoimage))
Fname=imageone.split('/')[-1][:-4]+imagetwo.split('/')[-1][:-4]
print(doubleimage.shape)

doubleimage2=np.hstack((oneimage,twoimage))
print('hstack')
print(doubleimage2.shape)

doubleimage3=np.vstack((oneimage,twoimage))
print('vstack')
print(doubleimage3.shape)
doubleimage4=np.stack((oneimage,twoimage),axis=0)
print(doubleimage4.shape)
doubleimage4=np.stack((oneimage,twoimage),axis=2)
print(doubleimage4.shape)  结果：(2,1052, 1914)

create_record(train_directory)

imageone='/home/yangshuhui/code/GT5data/test/2/00458bicycle.PNG'
imagetwo='/home/yangshuhui/code/GT5data/test/2/04101bus.PNG'
oneimage=np.asarray(PIL.Image.open(imageone))
twoimage=np.asarray(PIL.Image.open(imagetwo))
doubleimage=np.stack((oneimage,twoimage),axis=0)
doubleimage=doubleimage.reshape((2,1052,1914,1))
print(doubleimage.shape)
sum=0
for i in range(1052):
	for j in range(1914):
		sum=sum+twoimage[i,j]-doubleimage[1,i,j,0]
print(sum)
'''
