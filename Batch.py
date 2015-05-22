#!/usr/bin/python3

import Network
import Guess
import MessageSystem
import gettext

def ReadConfigure():
    global gConfigure
    with open('conf.json') as configureFile:
        try:
            gConfigure = json.load(configureFile)
        except:
            gConfigure = {}
    if 'lang' in gConfigure:
        userLang = [gConfigure['lang']]
        langtext = gettext.translation('flatnet',
                localedir = 'locale', languages = userLang)
        langtext.install()
    else:
        gettext.install('flatnet')

class FakeQtWindow:
    def __init__(self):
        None
    
    def updateInterface(self):
        None
    
    def insertLog(self, msg):
        None
    
    def getIsInfoLog(self):
        return False
    
    def getIsWarnLog(self):
        return False
        
    def getIsFatalLog(self):
        return False
        
    def getIsImportantLog(self):
        return False
    
    def getIsVerboseLog(self):
        return False

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
    networkDataSet["firstNetEdgeList"] = Network.ReadEdgeListCSV(filePath['FirstNetFile'], delimiter)
    networkDataSet["secondNetEdgeList"] = Network.ReadEdgeListCSV(filePath['SecondNetFile'], delimiter)
    networkDataSet["trueNodeMapping"], networkDataSet["trueReverseMapping"] = Network.ReadMappingCSV(filePath["TrueMapFile"], delimiter)
    
    return networkDataSet
    
def Batching():
    networkDataSet = InitDataSet()
    
    startNumSample = input("Start from number of sample: ")
    
    startNumSample = int(startNumSample)
    memberIndexList = [1, 3, 4]
    sampleIndexRange = range(1,6)
    
    for numSample in range(startNumSample, 11000, 1000):
        for memberIndex in memberIndexList:
            print("Current working set: samples/{}/member_{}/".format(numSample, memberIndex))
            input("Enter to continue...\n")
            
            for sampleIndex in sampleIndexRange:
                samplePath = "network\\samples\\{}\\member_{}\\sample_{}\\".format(numSample, memberIndex, sampleIndex)
                nodeMapPath = samplePath + "reduced_map.csv"
                friendListPath = samplePath + "friend_sample.csv"
                twitterListPath = samplePath + "twitter_sample.csv"
                sampleListPath = {}
                sampleListPath["first"] = friendListPath
                sampleListPath["second"] = twitterListPath
                delimiter = "\t"
                nodeMap, reverseMap = Network.ReadMappingCSV(nodeMapPath, delimiter)
                sampleUserTable = Guess.LoadSampleList(sampleListPath)
                
                
                result = Guess.UserLink(
                    networkDataSet["firstNetEdgeList"],
                    networkDataSet["secondNetEdgeList"],
                    nodeMap,
                    sampleUserTable["first"],
                    sampleUserTable["second"]
                )
                
                matchResult = Guess.CheckMatchRate(result, networkDataSet["trueNodeMapping"])
                
                print("Result of {}: {}".format(samplePath, matchResult))

if __name__ == '__main__':
    ReadConfigure()
    fakeQt = FakeQtWindow()
    Network.Init(fakeQt)
    Guess.Init(fakeQt)
    MessageSystem.Init(fakeQt)
    Batching()