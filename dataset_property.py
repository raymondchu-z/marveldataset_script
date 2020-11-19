import os

IMO_file = open("imgs_each_IMO.txt","w")
all_IMO_path = '/home/zlm/dataset/vessel_reid/ALL-IMG'
dirs = os.listdir( all_IMO_path )#IMO文件夹
imgs_count = {}
for dir in dirs:
    files = os.listdir( os.path.join(all_IMO_path,dir ))#每张图片
    # IMO_file.write(dir +","+str(len(files)) +"\n")
    imgs_count[dir] = len(files)
imgs_count = sorted(imgs_count.items(), key = lambda kv:(kv[1], kv[0]))
IMO_file.write(str(imgs_count))  



