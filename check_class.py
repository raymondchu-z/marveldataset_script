import os
import codecs
import json

FINAL = codecs.open("FINAL.dat","r","utf-8")
finalContent = FINAL.readlines()
FINAL.close()
ClassName = {}
IMO = {}
for eachLine in finalContent:
    strlist = eachLine.split(',')
    vessel_ID = strlist[0]
    # set_index = strlist[1]
    # class_label = strlist[2]
    class_label_name = strlist[3]
    IMO_number = strlist[4]
    image_path = strlist[5]
    if (image_path.rstrip() == '-'):
        continue
    ClassName.setdefault(class_label_name,[])
    if IMO_number not in ClassName[class_label_name]:
        ClassName[class_label_name].append(IMO_number)
    IMO.setdefault(IMO_number,[]).append(vessel_ID)

    # dict[strlist[3]] = {} #key是class_label_name，value是一个嵌套字典
    # dict[strlist[3]].setdefault(strlist[4],[]).append(strlist[0]) #嵌套字典中的值为列表，初始化 键为IMO_number，值为vessel_ID
print("len(ClassName)",len(ClassName))
print("len(IMO)",len(IMO))
for key in ClassName:
    print(key ,len(key))
# for key in IMO:
#     print(print(key ,len(key)))

with open('./ClassName_file.json','w') as ClassName_file:
    json.dump(ClassName,ClassName_file)
with open('./IMO_file.json','w') as IMO_file:
    json.dump(IMO,IMO_file)




    # vessel_ID = eachLine.split(",")[0]
    # set_index = eachLine.split(",")[1]
    # class_label = eachLine.split(",")[2]
    # class_label_name = eachLine.split(",")[3]
    # IMO_number = eachLine.split(",")[4]
    # image_path = eachLine.split(",")[5]