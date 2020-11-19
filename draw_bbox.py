""" 
draw_bbox.py
根据路径，读取图片，并画出bbox，然后保存
"""
import cv2
import os
import re #用正则表达来分离括号
import numpy as np
import torch



def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[0] = x[0] - x[2] / 2  # top left x
    y[1] = x[1] - x[3] / 2  # top left y
    y[2] = x[0] + x[2] / 2  # bottom right x
    y[3] = x[1] + x[3] / 2  # bottom right y
    return y



def plot_one_box(x, img, color=(0,255,255), label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)



finalContent = "1447014,2,38,General Cargo,7614666,/home/zlm/dataset/marveldataset2016/W30_1/1447014.jpg,2,[[0.42133620381355286, 0.4416666626930237, 0.6400862336158752, 0.8833333253860474], [0.9709051847457886, 0.6183333396911621, 0.04094827547669411, 0.01666666753590107]]"

save_path = "/home/zlm/dataset/marveldataset2016/plot_test/"
object_line_list = re.split(r",(?![^[\]]*\])", finalContent)
image_path = object_line_list[5].rstrip()
vessel_ID = object_line_list[0]
img = cv2.imread(image_path)
height = img.shape[0]
width = img.shape[1]
bbox_xywh = ','
bbox_xywh = bbox_xywh.join(object_line_list[7:]).rstrip()
bbox = []
bbox_list = re.split(r",(?![^[\]]*\])", bbox_xywh)
for one_bbox in bbox_list: 
    one_bbox = one_bbox.rstrip().replace('[','').replace(']','')
    one_bbox = one_bbox.split(',')
    one_bbox = list(map(float, one_bbox))
    bbox.append(one_bbox)

for xyxy in bbox:
    xyxy[0] = int(xyxy[0]* width)
    xyxy[1] = int(xyxy[1]* height)
    xyxy[2] = int(xyxy[2]* width)
    xyxy[3] = int(xyxy[3]* height) 
    xyxy = np.array(xyxy)
    xyxy = xywh2xyxy(xyxy)
    plot_one_box(xyxy, img)
    print(xyxy)
cv2.imwrite(save_path + vessel_ID + ".jpg", img)
