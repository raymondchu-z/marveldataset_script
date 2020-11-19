"""
dataset_divide.py
根据  ClassName_file.txt 里面记录的类别名：IMO号来将整个数据集划分成trainval和test。
这是基于同一类船的外观相似的先验知识。
具体在操作时，trainval取上整数，避免某个只有一艘船的类分入了test。
"""
import os
import re #用正则表达来分离括号
import math

class_file = open("ClassName_file.txt","r")
trainval_file = open("trainval.txt","w")
test_file = open("test.txt","w")
class_lines = class_file.readlines()

trainval_count = 0
test_count = 0
for eachLine in class_lines:
    clas_line_list = re.split(r",(?![^[\]]*\])", eachLine)
    class_name = clas_line_list[0]
    IMOs = clas_line_list[1]
    IMOs = IMOs.rstrip().replace('[','').replace(']','').replace('\'','').replace(' ','')
    IMO_list = IMOs.split(',')
    trainval_num = math.ceil( len(IMO_list)/2 )#3/2的上整数是2，则代表拿2个进train
    test_num =len(IMO_list) - trainval_num

    #前闭后开，【0:2】正好拿两个
    if trainval_num:
        trainval_file.write(class_name + "," + str(IMO_list[:trainval_num]).replace("'",'').replace(" ",'')+"\n")
    if test_num:
        test_file.write(class_name + "," + str(IMO_list[trainval_num:]).replace("'",'').replace(" ",'')+"\n")
    trainval_count += trainval_num
    test_count += test_num
print(trainval_count,test_count)

    

class_file.close()
trainval_file.close()
test_file.close()