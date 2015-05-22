#!/usr/bin/python3

import Network
import Guess

class FakeQtWindow:
    def __init__(self):
        None
    
    def updateInterface(self):
        None

def SetInitPara():
    filePath = {}
    filePath['FirstNetFile'] = "network/friend_undirected.csv"
    filePath['SecondNetFile'] = "network/twitter_undirected.csv"
    filePath['TrueMapFile'] = "network/usermapping.csv"

    delimiter = "\t"

    return filePath, delimiter

def InitDataSet():
    filePath, delimiter = SetInitPara()

    networkDataSet = {}
    networkDataSet["firstNetEdgeList"] = ReadEdgeListCSV(
            filePath['FirstNetFile'], delimiter)
    networkDataSet["secondNetEdgeList"] = ReadEdgeListCSV(
            filePath['SecondNetFile'], delimiter)
    networkDataSet["trueNodeMapping"], networkDataSet["trueReverseMapping"] = ReadMappingCSV(filePath["TrueMapFile"], delimiter)
