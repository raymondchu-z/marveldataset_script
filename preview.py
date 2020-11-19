import os

dataset_path = "/home/zlm/dataset/vessel_reid/pytorch/query"
txt_path = "/home/zlm/dataset/vessel_reid/query_preview.txt"
f=open(txt_path,"w")
for root,dirs,files in os.walk(dataset_path):
    for file in files:
        f.writelines(os.path.join(root,file)+"\n") 
f.close()



