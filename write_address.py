import os
dir = "/home/yangshuhui/code/data/GT5label/label1"
filelist=[]
filenames = os.listdir(dir)
for fn in filenames:     
	fullfilename = os.path.join(dir,fn)     
	filelist.append(fullfilename)
fo=open("/home/yangshuhui/code/data/labels_list.txt","a")
for j in filelist:     
	fo.write(str(j)+"\n")



