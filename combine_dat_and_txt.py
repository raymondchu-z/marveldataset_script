"""
把marvel数据集的xxx.dat文件和经过检测目标数量的xxx-object.txt结合到一个文件
FINAL里包含了没有文件的条目，所以FINAL的顺序要慢于object的顺序。
根据FINAL.dat里的每一行的vessel_ID在obj里面找。
只添加了船舶数量，没有添加BBOX信息
"""

import os
import codecs
import shutil 
from collections import Counter #用来列表元素计数
import re #用正则表达来分离括号
filename = "FINAL"
FINAL = codecs.open(filename+".dat","r","utf-8")
finalContent = FINAL.readlines()
FINAL.close()
object_file = open(filename+"-objects.txt","r")
object_line = object_file.readline()

object_nums = []

IMO_VESSEL_OBJ = open(filename+"-image-index.txt","w")
Unmatch_count = 0
FileNotFound_count = 0
for eachLine in finalContent: #以dat文件为循环
    # strlist = re.split(r",(?![^(]*\))", eachLine)
    strlist = eachLine.split(',')
    image_path = strlist[5].rstrip()
    if(image_path != "-"): #排除没下载的
        vessel_ID = strlist[0]
        # file_path = object_line.split(',')[0] #比对xxx-object.txt的一行
        object_line_list = re.split(r",(?![^[\]]*\])", object_line)
        file_path = object_line_list[0]
        (filepath, tempfilename) = os.path.split(file_path)
        (filename, extension) = os.path.splitext(tempfilename)
        if(vessel_ID == filename):#判断当前vessel_ID和当前filename是否相同
            # object_num = object_line.split(',')[1].rstrip() # 船只数量
            object_num = object_line_list[1]
            del object_line_list[0]
            object_line_str = ",".join(object_line_list)
            # print(eachLine.rstrip()+","+ object_line_str.rstrip())
            IMO_VESSEL_OBJ.write(eachLine.rstrip()+","+ object_line_str.rstrip()+"\n")
            object_nums.append(int(object_num))
            try:
                object_line = next(object_file) #读取txt有可能为最后一行
            except StopIteration:
                pass 
            continue
        else:
            # print("vessel_ID!=filename")
            Unmatch_count += 1
    else:
        # print("image_path为空")
        FileNotFound_count += 1
print("vessel_ID!=filename:"+str(Unmatch_count))
print("image_path为空:"+str(FileNotFound_count))
result = Counter(object_nums)
print(result)
IMO_VESSEL_OBJ.close()
    
        



            
        




    
