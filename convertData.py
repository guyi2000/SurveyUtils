import re
import os


def convertData(rawDataFile, convertDataFile):
    '''
    convert raw data (GTS format) to SSS format txt
    '''
    tempFolder = ".\\temp\\"
    if not os.path.exists(tempFolder):
        os.mkdir(tempFolder)
    print("***Start Converting Data...***")
    with open(rawDataFile, "r", encoding='utf-8') as r, open(tempFolder + "temp1", "w", encoding='utf-8') as w:
        for line in r.readlines():
            line = re.sub(r"\n","",line)
            if line:
                line = line[1:-5]
                w.write(line)

    with open(tempFolder + "temp1", "r", encoding='utf-8') as r, open(tempFolder + 'temp2', "w", encoding='utf-8') as w:
        for line in r.readlines():
            line = re.sub(r"_\+","_\n",line)
            line = re.sub(r"'","\n'",line)
            w.write(line)

    with open(tempFolder + "temp2", "r", encoding='utf-8') as r, open(convertDataFile, "w", encoding="utf-8") as w:
        w.write("GTS-700 v3.0\n")
        for line in r.readlines():
            if "_\n" == line:
                pass
            elif "'" in line:
                converts = re.findall(r"'(.*)_\((.*)_\)(.*)_", line)
                for convert in converts:
                    w.write("STN     " + convert[0] + "," 
                            + convert[2] + "," 
                            + convert[1] + "\n")
            elif "<" in line:
                converts = re.findall(r"(.*)_ <(\d*)\+(\d*)[\-\+](\d*)d(\d*)_\*(.*)_,(.*)_", line)
                for convert in converts:
                    w.write("BS      " + convert[0] + "," 
                            + convert[6] + "," 
                            + convert[5] + "\n")
                    w.write("HV      " 
                            + str(int(convert[2][:-4])) + "." + convert[2][-4:] + "0," 
                            + str(int(convert[1][:-4])) + "." + convert[1][-4:] + "0\n")
            else:
                converts = re.findall(r"(.*)_ [LR]\+(\d*)m(\d*)\+(\d*)d([\+\-]\d*)t(.*)_\*(.*)_,(.*)_", line)
                for convert in converts:
                    w.write("FS      " + convert[0] + ","
                            + convert[7] + "," + 
                            convert[6] + "\n")
                    w.write("HD      " 
                            + str(int(convert[3][:-4])) + "." + convert[3][-4:] + "0," 
                            + str(int(convert[1][:-3])) + "." + convert[1][-3:] + "0," 
                            + ("" if convert[4][0] == "+" else "-")
                            + str(int(convert[4][:-3])) + "." + convert[4][-3:] + "0\n")
    os.remove(tempFolder + "temp1")
    os.remove(tempFolder + "temp2")
    os.removedirs(tempFolder)
    print("***Convert Data Success***")


if __name__ == "__main__":
    converts = os.listdir(".\\raw\\")
    for convert in converts:
        convertData(".\\raw\\" + convert, ".\\convert\\" + convert[:-3] + "txt")