import sys
import os
import time
import serial.serialutil
import serial.tools.list_ports


def receiveCOMData(receiveDataFile):
    '''
    Receive raw data through COM-USB, just for TOPCON GTS-102N (GTS format)
    '''
    ports = list(serial.tools.list_ports.comports())
    portsLength = len(ports)
    if 0 >= portsLength:
        print("No Available COM!")
        sys.exit(-1)
    elif 1 == portsLength:
        print("COM found!")
        port = list(ports[0])
        port_serial = port[0]
    else:
        print("Please Enter Your COM Name:", end='')
        port_serial = input()

    serialFd = serial.Serial(port=port_serial,
                            baudrate=9600,
                            bytesize=serial.serialutil.EIGHTBITS,
                            stopbits=serial.serialutil.STOPBITS_ONE,
                            timeout=2,
                            inter_byte_timeout=1)
    if serialFd.isOpen():
        print("Open COM Success!")
        print(serialFd.name + " Connected!")
    else:
        print("Open failed!")
        sys.exit(-1)

    print("Waiting for data...")
    line = ''
    receiveFile = open(receiveDataFile, "w+", encoding='utf-8')

    while True:
        if serialFd.in_waiting:
            line = serialFd.read(1).decode('utf-8')
            print("***Start Receive...***")
            print(line, end='')
            receiveFile.write(line)
            break

    while True:
        line = serialFd.read(1).decode('utf-8')
        if '\x04' == line:
            break # stop flag
        print(line, end='')
        receiveFile.write(line)

    print("***Receive Success!***")
    receiveFile.close()
    serialFd.close()


if __name__ == "__main__":

    rawdataPath = ".\\raw\\" # set default dir

    if not os.path.exists(rawdataPath):
        os.mkdir(rawdataPath)
    receiveCOMData(time.strftime(rawdataPath + "%Y%m%d%H%M%S.gt6", time.localtime()))