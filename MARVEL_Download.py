from bs4 import BeautifulSoup
# from urllib2 import urlopen
from urllib.request import urlopen
from PIL import Image
import traceback
import threading
import datetime
import time
import logging
import codecs
import math
import sys
import os
from func_timeout import func_set_timeout
import func_timeout
import heartrate
heartrate.trace(browser=True)

##Uncomment the related dat file ('VesselClassification.dat' for Vessel Classification, 'IMOTrainAndTest.dat' for Vessel Verification/Retrieval/Recognition tasks.)
##FILE_TO_DOWNLOAD_FROM = "VesselClassification.dat"
FILE_TO_DOWNLOAD_FROM = "IMOTrainAndTest.dat" 

NUMBER_OF_WORKERS = 32
MAX_NUM_OF_FILES_IN_FOLDER = 5000
IMAGE_HEIGHT = 512
IMAGE_WIDTH = 512
ORIGINAL_SIZE = 1 # 1 for yes, 0 for no
JUST_IMAGE = 1 # 1 for yes, 0 for no


photoDetails = ["Photographer:","Title:","Captured:","IMO:","Photo Category:","Description:"]
vesselIdentification = ["Name:","IMO:","Flag:","MMSI:","Callsign:"]
technicalData = ["Vessel type:","Gross tonnage:","Summer DWT:","Length:","Beam:","Draught:"]
additionalInformation = ["Home port:","Class society:","Build year:","Builder (*):","Owner:","Manager:"]
aisInformation = ["Last known position:","Status:","Speed, course (heading):","Destination:","Last update:","Source:"]
impText = photoDetails + vesselIdentification + technicalData + additionalInformation  
impText2 = ["Former name(s):"]

sourceLink = "http://www.shipspotting.com/gallery/photo.php?lid="

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
# logging.debug("Process started at " + str(datetime.datetime.now()))
# =============================================================================
# 下面是自己加的日志记录
# =============================================================================
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

log_path = os.getcwd() + '\\Logs\\'
log_name = log_path + rq + '.log'

logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.WARNING)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
# logger.debug('this is a logger debug message')


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch_format=logging.Formatter('(%(threadName)-10s) %(message)s')
ch.setFormatter(ch_format)
logger.addHandler(ch)



logging.warning("Process started at " + str(datetime.datetime.now()))

#@func_set_timeout(120)
def save_image(ID,justImage,outFolder):
    url = sourceLink + ID
    try: # 加了一个try        
#        html = urlopen(url,timeout = 300).read()
        h = urlopen(url,timeout = 300)
        html=h.read()
    except:
        print("timeout")
        return 0
    
    soup = BeautifulSoup(html,"lxml")

    images = [img for img in soup.findAll('img')]
    image_links = [each.get('src') for each in images]
    if not justImage:
        tags = [tr for tr in soup.findAll('td')]
        tr_text = [each.getText() for each in tags]
        
    filename = " "
    for each in image_links:
        if "http" in each and "jpg" in each and "photos/middle" in each:
            filename=each.split('/')[-1]
            f = urlopen(each)
            with open(os.path.join(outFolder,filename), "wb") as local_file:
                try:
                    local_file.write(f.read())
                except:
                    print("incompleted read")
                    return 0
            if ORIGINAL_SIZE == 0:
                img = Image.open(os.path.join(outFolder,filename)).resize((IMAGE_HEIGHT,IMAGE_WIDTH), Image.ANTIALIAS)
                os.remove(os.path.join(outFolder,filename))
                # out = file(os.path.join(outFolder,filename),"wb")
                out = os.path.join(outFolder,filename)
                img.save(out,"JPEG")
            break
        
    if filename != " " and not justImage:
        textFile = filename.split('.')[0]
        tFile = codecs.open(os.path.join(outFolder,filename)+'.dat','w','utf-8')    
        for index,each in enumerate(tr_text):
            for impT in impText:
                if impT == each:
                    tFile.write(each + ' ' + tr_text[index+1] + '\n')
                    break
        for index,each in enumerate(tr_text):
            for impT in impText2:
                if impT == each:
                    for ind in range(1,20):
                        if tr_text[index+ind] != "":
                            tFile.write(each + ' ' + tr_text[index+ind] + '\n')
                        else:
                            break
                    break
        tFile.close()
    if filename == " ":
        return 0
    else:
        return 1

#@func_set_timeout(20)
def worker(content,workerNo):
    workerIndex = 0
    folderIndex = 0
    folderNo = 1
    currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
    if not os.path.exists(currFolder):
        os.mkdir(currFolder)
    for ID in content:
        if folderIndex == MAX_NUM_OF_FILES_IN_FOLDER:
            folderIndex = 0
            folderNo = folderNo + 1
            currFolder = os.path.join(os.getcwd(),'W'+str(workerNo)+'_'+str(folderNo))
            if not os.path.exists(currFolder):
                os.mkdir(currFolder)
        try:
            status = save_image(ID,JUST_IMAGE,currFolder)
            workerIndex = workerIndex + 1
            if status == 1:
                folderIndex = folderIndex + 1
                logging.debug(str(ID) + "\t - Downloaded... - " + str(workerIndex) + "\t/" + str(len(content)))
#                print(str(ID) + "\t - Downloaded... - " + str(workerIndex) + "\t/" + str(len(content)))
            else:
                logging.warning(str(ID) + "\t - NO SUCH FILE  - " + str(workerIndex) + "\t/" + str(len(content)))
                
        except func_timeout.exceptions.FunctionTimedOut:
            print('task func_timeout  at worker'+ str(workerNo) + ' wiht ID ' + str(ID))
            continue
        except :
            traceback.print_exc()
            print("dead thread is worker"+str(workerNo))
    logging.warning(str(datetime.datetime.now()) + "-------------- DONE ")
    return



# =============================================================================
# #每180s获取当前线程名，并跟初始线程组比较，某一线程停止后自动运行
#def checkThread(sleeptimes=180,initThreadsName=[]):
#     for i in range(0,10080):#循环运行
#         nowThreadsName=[]#用来保存当前线程名称
#         now=threading.enumerate()#获取当前线程名
#         for i in now:
#             nowThreadsName.append(i.getName())#保存当前线程名称
# 
#         for name in initThreadsName:
#             if  name in nowThreadsName:
#                 pass #当前某线程名包含在初始化线程组中，可以认为线程仍在运行
#             else:
#                 print ('===' + name,'stopped，now restart')
#                 workerNo = int(name[5:])
#                 start_index = 0
#                 for ele in range(0,workerNo):                     
#                     start_index = start_index + numOfFilesPerEachWorker[ele]                 
#                 content_index = finalContent[start_index:start_index + numOfFilesPerEachWorker[workerNo]]
#                 t=threading.Thread(target=worker,args=(content_index,workerNo,))#重启线程
#                 t.setName(name='Worker'+str(workerNo))#重设name
#                 t.start()
#         time.sleep(sleeptimes)#隔一段时间重新运行，检测有没有线程down
# =============================================================================






priorFiles = []
dirs = os.listdir(os.getcwd())
for eachDir in dirs:
    if 'W' in eachDir:
        oldFiles = os.listdir(os.path.join(os.getcwd(),eachDir))
        for eachFile in oldFiles:
            if ".jpg" in eachFile:
                oldID = eachFile.split(".")[0]
                priorFiles.append(oldID)

downloadFile = codecs.open(FILE_TO_DOWNLOAD_FROM,"r","utf-8")
downloadContent = downloadFile.readlines()
downloadFile.close()
finalContent = []
for index,eachLine in enumerate(downloadContent):
    temp = eachLine.split(',')[0]
    if temp not in priorFiles:
        finalContent.append(temp)

numOfFiles = len(finalContent)

numOfFilesPerEachWorker = [int(math.floor(float(numOfFiles)/NUMBER_OF_WORKERS)) for x in range(0,NUMBER_OF_WORKERS-1)]
numOfFilesPerEachWorker.append(numOfFiles - (NUMBER_OF_WORKERS-1)*int(round(numOfFiles/NUMBER_OF_WORKERS,0)))

logging.warning("There will be %s workers in this download process" % NUMBER_OF_WORKERS)
logging.warning("%s files will be downloaded" % numOfFiles)

threads = []
#content_index = []
imageCount = 0
for i in range(0,NUMBER_OF_WORKERS):
    t = threading.Thread(name='Worker'+str(i), target=worker, args=(finalContent[imageCount:imageCount + numOfFilesPerEachWorker[i]],i,)) #args应该是worker函数的参数。
#    content_index[i] = finalContent[imageCount:imageCount + numOfFilesPerEachWorker[i]]
    imageCount = imageCount + numOfFilesPerEachWorker[i]#这部分没有把分配的文件序号记录起来，要重启就要再分配序号。
    threads.append(t)
    t.start()
# =============================================================================
# 添加线程检测   
# =============================================================================
# =============================================================================
#initThreadsName=[]#保存初始化线程组名字
#init=threading.enumerate()#获取初始化的线程对象
#for i in init:
#    initThreadsName.append(i.getName())#保存初始化线程组名字
#check=threading.Thread(target=checkThread,args=(180,initThreadsName))#用来检测是否有线程down并重启down线程
#check.setName('Thread:check')
#check.start()
  
# =============================================================================
 
#####################
#判断是否结束
    
flag = True
while flag:
    counter = 0
    for eachT in threads:
        if eachT.isAlive() == False: #判断线程是否活动，不活动就计数+1.达到线程总数就退出了。但是怎么让线程退出呢
            counter = counter + 1
            # print("counter=" + str(counter))
    if counter == NUMBER_OF_WORKERS:
        flag = False

logging.warning(str(datetime.datetime.now()) + " - list all files startes ")
allPaths = []
allIDs = []
dirs = os.listdir(os.getcwd())
for eachDir in dirs:
    if 'W' in eachDir:
        FinalList = os.listdir(os.path.join(os.getcwd(),eachDir))
        for eachFile in FinalList:
            if ".jpg" in eachFile:
                fPath = os.path.join(os.getcwd(),eachDir,eachFile)
                fID = eachFile.split(".")[0]
                allPaths.append(fPath)
                allIDs.append(fID)
logging.warning(str(datetime.datetime.now()) + " - write to disc ")

FINAL = codecs.open("FINAL.dat","w","utf-8")
for eachLine in downloadContent:
    tempID = eachLine.split(",")[0]
    try:
        tempIndex = allIDs.index(tempID)
        FINAL.write(eachLine[:-1]+","+str(allPaths[tempIndex])+"\n")#s[:-1]等价于 s[0:len(s)]，除了最后一个元素的切片.eachLine里面是\r\n 回车换行。
    except:
        FINAL.write(eachLine[:-1]+","+"-\n")
FINAL.close()















                                                                  





