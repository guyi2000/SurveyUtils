import re
import os
import math
import pandas as pd


def convertStrAngle(angleStr):
    '''
    convert string angle to float64
    Examples
    --------
    >>> convertStrAngle("256.30000")
    256.5
    '''
    return int(angleStr[:-6]) + int(angleStr[-5:-3]) / 60 + int(angleStr[-3:-1]) / 3600

def caculateFS(radis,theta):
    '''
    convert polar to Cartesian, theta for degrees
    '''
    return radis * math.cos(math.radians(theta % 360)), radis * math.sin(math.radians(theta % 360))

def caculateData(convertDataFile, caculateDataFile, KZDDataFile):
    '''
    caculate the FS, using KZDData(csv format)

    KZDData csv format: Name, X, Y, H
    '''
    STNName = ""
    YG = 1.800
    JG = 1.800
    BSName = ""
    FXJ = ""
    BSFXJ = ""

    print("***Caculate Data Start...***")
    with open(convertDataFile, "r", encoding="utf-8") as r, open(caculateDataFile, "w", encoding="utf-8") as w:
        lines = r.readlines()
        for i in range(len(lines)):
            if "STN" in lines[i]:
                caculates = re.findall(r"STN\s*(.*),(.*),(.*)", lines[i])
                for caculate in caculates:
                    STNName = caculate[0]
                    YG = float(caculate[1])

            elif "BS" in lines[i]:
                caculates = re.findall(r"BS\s*(.*),(.*),(.*)", lines[i])
                for caculate in caculates:
                    BSName = caculate[0]
                    JG = float(caculate[1])
                i += 1
                caculates = re.findall(r"HV\s*(.*),(.*)", lines[i])
                for caculate in caculates:
                    FXJ = convertStrAngle(caculate[0])

            elif "FS" in lines[i] or "SS" in lines[i]:
                PN = ""
                caculates = re.findall(r"[FS]S\s*(.*),(.*),(.*)", lines[i])
                for caculate in caculates:
                    PN = caculate[0]
                    JG = float(caculate[1])

                if "" == STNName:
                    print("Please enter STNName: ", end='')
                    STNName = input()
                    print("Please enter YG: ", end='')
                    YG = float(input())
                if "" == BSName:
                    print("Please enter BSName: ", end='')
                    BSName = input()
                    print("Please enter BS angle: ", end='')
                    FXJ = convertStrAngle(input())
                KZDData = pd.read_csv(KZDDataFile, index_col=0, header=None)
                while True:
                    try:
                        STNInfo = KZDData.loc[STNName]
                        break
                    except KeyError:
                        print("Error Station, please enter STNName agian!\nOr check the station in KDZ.dat")
                        STNName = input()
                        print("Please enter YG: ", end='')
                        YG = float(input())
                while True:
                    try:
                        BSInfo = KZDData.loc[BSName]
                        break
                    except KeyError:
                        print("Error Station, please enter BSName agian!\nOr check the station in KDZ.dat")
                        BSName = input()
                        print("Please enter BS angle: ", end='')
                        FXJ = convertStrAngle(input())

                STNX = STNInfo[1]
                STNY = STNInfo[2]
                STNH = STNInfo[3]

                BSX = BSInfo[1]
                BSY = BSInfo[2]

                deltaBX = BSX - STNX
                deltaBY = BSY - STNY

                if deltaBX >= 0 and deltaBY >= 0:
                    BSFXJ = math.degrees(math.atan(deltaBY / deltaBX))
                elif deltaBX < 0 and deltaBY >= 0:
                    BSFXJ = math.degrees(math.atan(deltaBY / deltaBX)) + 180.0
                elif deltaBX < 0 and deltaBY < 0:
                    BSFXJ = math.degrees(math.atan(deltaBY / deltaBX)) + 180.0
                elif deltaBX >= 0 and deltaBY < 0:
                    BSFXJ = math.degrees(math.atan(deltaBY / deltaBX)) + 360.0

                i += 1
                caculates = re.findall(r"HD\s*(.*),(.*),(.*)", lines[i])        
                for caculate in caculates:
                    delta_x, delta_y = caculateFS(float(caculate[1]),convertStrAngle(caculate[0]) - FXJ + BSFXJ)
                    w.write(str(round(delta_x + STNX, 3)) + "," 
                          + str(round(delta_y + STNY, 3)) + "," 
                          + str(round(STNH + YG - JG + float(caculate[2]), 3)) + ","
                          + PN + '\n')

    print("***Caculate Data Success!***")

    
if __name__ == "__main__":
    caculates = os.listdir(".\\convert\\")
    for caculate in caculates:
        caculateData(".\\convert\\" + caculate, ".\\output\\" + caculate, "KZD.dat")