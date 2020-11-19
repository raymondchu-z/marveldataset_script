import os
import codecs
import cv2
import shutil 



# FILE_TO_DOWNLOAD_FROM = "IMO_7304314_to_download.dat" 
# downloadFile = codecs.open(FILE_TO_DOWNLOAD_FROM,"r","utf-8")
# downloadContent = downloadFile.readlines()
# downloadFile.close()


FINAL = codecs.open("FINAL-image-index-test-608.txt","r","utf-8")
finalContent = FINAL.readlines()
FINAL.close()
for eachLine in finalContent:
    strlist = eachLine.split(',')
    image_path = eachLine.split(",")[5].rstrip()
    try:
        shutil.copy(image_path,'./9070905' )
    except:
        print("Error: 没有找到文件或读取文件失败")


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


