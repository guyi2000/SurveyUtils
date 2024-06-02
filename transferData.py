import os
import pandas as pd


def transferData(caculateDataFile, transerDataFile):
    '''
    transfer caculated data for cass
    '''
    print("***Transfer Data Start...***")
    pd.read_csv(caculateDataFile, header=None).reindex(columns=[3,5,1,0,2]).round(3).to_csv(transerDataFile,header=None,index=None)
    print("***Transfer Data Success!***")


if __name__ == "__main__":
    outputs = os.listdir(".\\output\\")
    for output in outputs:
        transferData(".\\output\\" + output, ".\\cass\\" + output[:-3] + "dat")