"""
 reid_dataset_organizer.py
 完成：根据txt信息，把同一imo号的图片的bbox写入到以imo为名的文件夹下，大小为384*256。

筛选目标bbox,包含中心点的才要,而且只要一个
读取文件路径，bbox信息
处理bbox信息，去掉中括号，wh乘0.1

写入目标文件夹
"""

import os
import codecs
import cv2
import shutil 
import re #用正则表达来分离括号
import torch
import numpy as np
import random
# import torch.nn as nn
# import torchvision

def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)

def xywh2xyxy(x, width, height):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    # y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y = [0]*4
    y[0] = int(max(x[0] - x[2] / 2 , 0))  # top left x
    y[1] = int(max(x[1] - x[3] / 2 , 0)) # top left y
    y[2] = int(min(x[0] + x[2] / 2 , width)) # bottom right x
    y[3] = int(min(x[1] + x[3] / 2 , height)) # bottom right y
    return y
def float2int(x, width, height):
    y = [0]*4
    y[0] = int(x[0]* width)
    y[1] = int(x[1]* height)#
    y[2] = int(x[2]* width)
    y[3] = int(x[3]* height)
    return y


def takeWidth(elem):
    return elem[2]
"""
如何判断值传递和引用传递
如果传入的参数对象是可变对象：列表，字典，这个时候就是引用传递，如果参数在函数体内被修改，那么源对象也会被修改。
如果传入的参数对象是不可变的对象：数字，元组，字符串，这个时候就是值传递。那么源对象是不会改变的，
"""
# def resize_by_oneside(bbox, oneside, the_otherside, width, height):
#     oneside = min(oneside+0.05*oneside, 1)# 此时还是小数
#     #转换成整数
#     bbox = float2int(bbox, width, height)
#     the_otherside = int(oneside * 2 / 3) 


def get_bbox(bbox_xywh, width, height):
        """ 
        要兼顾处理有多个bbox的，选出最大的且包含中心点的
        """
        bbox_list = []
        bbox_str_list = re.split(r",(?![^[\]]*\])", bbox_xywh)
        for one_bbox in bbox_str_list: 
            one_bbox = one_bbox.rstrip().replace('[','').replace(']','')
            one_bbox = one_bbox.split(',')
            one_bbox = list(map(float, one_bbox))
            bbox_list.append(one_bbox)
        bbox_list = sorted(bbox_list, key=takeWidth, reverse=True) #先排序再加
        # print(bbox)
        
        the_bbox = bbox_list[0] #最大的那个xywh
        bbox_width = int(the_bbox[2] * width)
        bbox_height = int(the_bbox[3] * height)
        raw_bbox = the_bbox.copy()#记录没扩大的bbox
        if bbox_height > bbox_width and int(bbox_height * 1.5) < width:#瘦高且不超出边界
            the_bbox[3] = min(the_bbox[3]+0.05 * the_bbox[3], 1)
            the_bbox = float2int(the_bbox, width, height)
            the_bbox[2] = int(the_bbox[3]* 3 / 2 )
        else:
            the_bbox[2] = min(the_bbox[2]+0.05*the_bbox[2], 1)# 此时还是小数
            #转换成整数
            the_bbox = float2int(the_bbox, width, height)
            the_bbox[3] = int(the_bbox[2] * 2 / 3)


        #将raw_bbox从归一化小数转成整数
        raw_bbox = float2int(raw_bbox, width, height)
        the_bbox_xyxy = xywh2xyxy(the_bbox, width, height)
        raw_bbox_xyxy = xywh2xyxy(raw_bbox, width, height)
        return the_bbox_xyxy, raw_bbox_xyxy


filename = "FINAL"
imgsize = "-512"
testflag = False
if testflag :
    IMO_VESSEL_OBJ = open(filename+"-image-index" + "-test" + imgsize +".txt","r")
else :
    IMO_VESSEL_OBJ = open(filename+"-image-index" + imgsize +".txt","r")
finalContent = IMO_VESSEL_OBJ.readlines()
IMO_VESSEL_OBJ.close()
dataset_path = "/home/zlm/dataset/vessel_reid/ALL-IMG"
if not testflag :
    if os.path.exists(dataset_path):
        shutil.rmtree(dataset_path)  # delete output folder
    os.makedirs(dataset_path)  # make new output folder
    center_out_of_bbox = open("/home/zlm/dataset/vessel_reid/center_out_of_bbox.txt","w")
count = 1
if testflag :
    save_path = "/home/zlm/dataset/marveldataset2016/Z_test/"
    shutil.rmtree(save_path)

for eachLine in finalContent:
    object_line_list = re.split(r",(?![^[\]]*\])", eachLine)
    object_num = int(object_line_list[6])
    vessel_ID = object_line_list[0]
    IMO_number = object_line_list[4]
    if not testflag :
        save_path = dataset_path+ "/" + IMO_number + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # make new output folder
    
    if object_num >= 1  and object_num <= 4:# 目标数量在范围内的才处理
        if (vessel_ID ):
            print(str(count)+"," + vessel_ID +",",end="")
        image_path = object_line_list[5].rstrip()
        bbox_xywh = ','
        bbox_xywh = bbox_xywh.join(object_line_list[7:]).rstrip()
        img = cv2.imread(image_path)
        height = img.shape[0]
        width = img.shape[1]
        xyxy,raw_xyxy = get_bbox(bbox_xywh, width, height)
        if(raw_xyxy[0]>width/2 or raw_xyxy[1]>height/2 or raw_xyxy[2]<width/2 or raw_xyxy[3]<height/2):#判断包含中心点
            print( "最大的边界框不包含中心点")
            if not testflag :
                center = (int(width/2), int(height/2))      
                bad_bbox = vessel_ID+","+str(xyxy)+","+str(center)+"\n"
                center_out_of_bbox.write(bad_bbox)
                # center_out_of_bbox.write(vessel_ID + ",xyxy:"+str(xyxy) + "，center:"+ str(width/2) +","+ str(height/2))
            continue
        print(xyxy)
        cropImg = img[xyxy[1]:xyxy[3],xyxy[0]:xyxy[2]]   #裁剪图像
        resizeImg = cv2.resize(cropImg, (384, 256)) #输出尺寸格式为（宽，高）
        cv2.imwrite(save_path + vessel_ID + ".jpg", resizeImg)
        count += 1
if not testflag :
    center_out_of_bbox.close()


    # try:
    #     shutil.copy(image_path,'./7304314' )
    # except:
    #     print("Error: 没有找到文件或读取文件失败")


    # img = cv2.imread(image_path)
    # cv2.namedWindow("Image")
    # cv2.imshow("Image", img)
    # cv2.waitKey (0)
    # cv2.destroyAllWindows()
    # vessel_ID = eachLine.split(",")[0]
    # set_index = eachLine.split(",")[1]
    # class_label = eachLine.split(",")[2]
    # class_label_name = eachLine.split(",")[3]
    # IMO_number = eachLine.split(",")[4]
    # image_path = eachLine.split(",")[5]
    # 用IMO_number做字典的key，value放class_label，class_label_name，vessel_ID
    # 用class_label_name做字典的key，value放class_label，IMO_number，vessel_ID


