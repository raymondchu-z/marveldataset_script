"""
把marvel数据集的.dat文件中的路径转到一个txt中，供yolov3的source调用。
"""

import os
import codecs
import shutil 
filename = "FINAL"
FINAL = codecs.open(filename+".dat","r","utf-8")
finalContent = FINAL.readlines()
print("dat文件行数：",len(finalContent))
FINAL.close()
txt_count = 0
file_not_exist_count = 0
file_broken_count = 0
with open(filename+".txt", 'w') as f:
    for eachLine in finalContent:
        strlist = eachLine.split(',')
        image_path = eachLine.split(",")[5].rstrip()
        if (len(image_path)<=1 ):
            file_not_exist_count += 1
            continue
        fsize = os.path.getsize(image_path)
        if (fsize==0):
            file_broken_count += 1
            continue
        f.writelines(image_path)
        f.write('\n')
        txt_count += 1
print("txt文件行数：",str(txt_count))
print("不存在图片数：",str(file_not_exist_count))
print("损坏图片数：",str(file_broken_count))
