import os
import time
from receiveData import receiveCOMData
from convertData import convertData
from caculateData import caculateData
from transferData import transferData


rawdataPath = ".\\raw\\"
convertdataPath = ".\\convert\\"
caculatedataPath = ".\\output\\"
cassPath = ".\\cass\\"
KZDPath = ".\\KZD.dat"
if not os.path.exists(rawdataPath):
    os.mkdir(rawdataPath)
if not os.path.exists(convertdataPath):
    os.mkdir(convertdataPath)
if not os.path.exists(caculatedataPath):
    os.mkdir(caculatedataPath)
if not os.path.exists(cassPath):
    os.mkdir(cassPath)

rawFileName = time.strftime("%Y%m%d%H%M%S.gt6", time.localtime())
receiveCOMData(rawdataPath + rawFileName)
convertFileName = rawFileName[:-3] + "txt"
convertData(rawdataPath + rawFileName, convertdataPath + convertFileName)
caculateFileName = convertFileName
caculateData(convertdataPath + convertFileName, caculatedataPath + caculateFileName, KZDPath)
cassFileName = caculateFileName[:-3] + "dat"
transferData(caculatedataPath + convertFileName, cassPath + cassFileName)
os.system("pause")