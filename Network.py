#!/usr/bin/python3

import csv
import queue
import MessageSystem

def Init(qtMainWindow):
    global gQtMainWindow
    gQtMainWindow = qtMainWindow

def ReadEdgeListCSV(fileName, delimiter = ','):
    """
    Read edge list csv to a hash table.
    """
    edgeList = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = delimiter)

        for row in csvTable:
            gQtMainWindow.updateInterface()
            if row[0] not in edgeList:
                edgeList[row[0]] = set()
            edgeList[row[0]].add(row[1])
            if row[1] not in edgeList:
                edgeList[row[1]] = set()
            edgeList[row[1]].add(row[0])

    try:
        del(edgeList['Source'])
    except:
        MessageSystem.Send(100)

    return edgeList

def ReadMappingCSV(fileName, delimiter = ','):
    """
    Read user mapping file from csv.
    """
    mapping = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = delimiter)

        for row in csvTable:
            gQtMainWindow.updateInterface()
            mapping[row[0]] = row[1]

    reverseMapping = {v : k for k, v in mapping.items()}

    return mapping, reverseMapping

def CheckReversed(networkDataSet):
    # Test whether is mapping is reversed

    reverseLimit = 100

    failCount = 0
    # Check if the mapping needs to be reversed
    for testUser in networkDataSet["nodeMapping"]:
        gQtMainWindow.updateInterface()
        if not testUser in networkDataSet["firstNetEdgeList"]:
            failCount = failCount + 1
        # There are more than reverseLimit users who doesn't exist in
        # the fristNetwork
        if failCount > reverseLimit:
            MessageSystem.Send(101, reverseLimit)
            
            (networkDataSet["nodeMapping"],
            networkDataSet["reverseMapping"]) =\
                (networkDataSet["reverseMapping"],
                networkDataSet["nodeMapping"])

            refailCount = 0

            for retestUser in networkDataSet["nodeMapping"]:
                if not retestUser in networkDataSet["firstNetEdgeList"]:
                    refailCount = refailCount + 1
                if refailCount > reverseLimit:
                    MessageSystem.Send(200)
                    exit()

            MessageSystem.Send(300)
            break

def FlatV2(networkDataSet):

    flatNet = {}

    baseNet = _('1st')
    refNet = _('2nd')

    CheckReversed(networkDataSet)

    # First time iterate
    for user in networkDataSet["nodeMapping"]:
        gQtMainWindow.updateInterface()
        MessageSystem.Send(400, user)

        if user in networkDataSet["firstNetEdgeList"]:
            if not user in flatNet:
                flatNet[user] = []

            MessageSystem.Send(401, networkDataSet["firstNetEdgeList"][user])
            flatNet[user].extend(networkDataSet["firstNetEdgeList"][user])
        else:
            MessageSystem.Send(102, user, baseNet)

        userAlterName = networkDataSet["nodeMapping"][user]
        MessageSystem.Send(402, userAlterName)

        if userAlterName in networkDataSet["secondNetEdgeList"]:
            for friend in networkDataSet["secondNetEdgeList"][userAlterName]:
                if friend in networkDataSet["reverseMapping"]:
                    if not user in flatNet:
                        flatNet[user] = []
                    if user in networkDataSet["firstNetEdgeList"]:
                        if not networkDataSet["reverseMapping"][friend] in networkDataSet["firstNetEdgeList"][user]:
                            MessageSystem.Send(403, friend)
                            flatNet[user].append(networkDataSet["reverseMapping"][friend])
                    else:
                        flatNet[user].append(networkDataSet["reverseMapping"][friend])
                        MessageSystem.Send(404, friend)
        else:
            MessageSystem.Send(103, user, refNet)

    return flatNet

def BFS(edgeList, src, level = 1):
    visited = set()
    distHash = {}
    q = queue.Queue()
    q.put((src, 0))
    visited.add(src)
    dist = 0
    while not q.empty():
        gQtMainWindow.updateInterface()
        (v, dist) = q.get()
        if dist == level:
            break
        distHash[v] = dist
        nextDist = dist + 1
        if v in edgeList:
            for nextV in edgeList[v]:
                if not nextV in visited:
                    q.put((nextV, nextDist))
                    visited.add(nextV)

    return distHash

def LoadNetworkData(filePath, delimiter = ','):
    networkDataSet = {}

    MessageSystem.Info(_('Reading first network...'))
    networkDataSet["firstNetEdgeList"] = ReadEdgeListCSV(
            filePath['FirstNetFile'], delimiter)

    MessageSystem.Info(_('Reading second network...'))
    networkDataSet["secondNetEdgeList"] = ReadEdgeListCSV(
            filePath['SecondNetFile'], delimiter)

    MessageSystem.Info(_('Reading node mapping...'))
    networkDataSet["nodeMapping"], networkDataSet["reverseMapping"] = ReadMappingCSV(filePath['NodeMappingFile'], delimiter)
    
    if filePath["TrueMapFile"] != "":
        networkDataSet["trueNodeMapping"], networkDataSet["trueReverseMapping"] = ReadMappingCSV(filePath["TrueMapFile"], delimiter)


    return networkDataSet
    
def SaveFlatNetFile(filePath, flatNet):
    with open(filePath['OutputFile'], mode = 'w') as outCsv:
        for user in flatNet:
            gQtMainWindow.updateInterface()
            for friend in flatNet[user]:
                print('{0},{1}'.format(user, friend), file = outCsv)
                
def GenerateBFS(networkDataSet, bfsDataSet):
    firstNetBFS = {}
    MessageSystem.Info(_('Generating BFS node for the first network...'))
    for user in networkDataSet["firstNetEdgeList"]:
        firstNetBFS[user] = BFS(
                networkDataSet["firstNetEdgeList"], user, level = bfsLevel)

    secondNetBFSRaw = {}

    MessageSystem.Info(_('Generating BFS node for the second network...'))
    for user in networkDataSet["secondNetEdgeList"]:
        secondNetBFSRaw[user] = BFS(
                networkDataSet["secondNetEdgeList"], user, level = bfsLevel)

    # Mapping for the secondNetBFS

    secondNetBFS = {}

    for alterName in secondNetBFSRaw:
        gQtMainWindow.updateInterface()
        if alterName in networkDataSet["reverseMapping"]:
            user = networkDataSet["reverseMapping"][alterName]
            secondNetBFS[user] = []
            for alterFriendName in secondNetBFSRaw[alterName]:
                if alterFriendName in networkDataSet["reverseMapping"]:
                    friendName = networkDataSet["reverseMapping"][alterFriendName]
                    secondNetBFS[user].append(friendName)

    flatNetBFS = {}

    MessageSystem.Info(_('Generating BFS node for the flat network...'))
    for user in flatNet:
        flatNetBFS[user] = BFS(flatNet, user, level = bfsLevel)
        
    bfsDataSet["first"] = firstNetBFS.copy()
    bfsDataSet["second"] = secondNetBFS.copy()
    bfsDataSet["flat"] = flatNetBFS.copy()

def UserStatistics(bfsDataSet):
    statistics = {}
    statistics['Total'] = {}
    statistics['Avg'] = {}
    statistics['Total']['User'] = 0
    statistics['Total']['NewFriendForNet1'] = 0
    statistics['Total']['NewFriendForNet2'] = 0
    
    for user in bfsDataSet["flat"] :
        gQtMainWindow.updateInterface()
        firstNetFriendSet = set()
        secondNetFriendSet = set()
        flatNetFriendSet = set()

        if user in bfsDataSet["first"]:
            firstNetFriendSet = set(bfsDataSet["first"][user].keys())
            firstNetFriendSet.remove(user)

        if user in bfsDataSet["second"]:
            secondNetFriendSet = set(bfsDataSet["second"][user])
            secondNetFriendSet.remove(user)

        flatNetFriendSet = set(bfsDataSet["flat"] [user].keys())
        flatNetFriendSet.remove(user)

        subFirst = flatNetFriendSet - firstNetFriendSet
        subSecond = flatNetFriendSet - secondNetFriendSet
        
        statistics['Total']['User'] = statistics['Total']['User'] + 1
        statistics['Total']['NewFriendForNet1'] =\
                statistics['Total']['NewFriendForNet1'] + len(subFirst)
        statistics['Total']['NewFriendForNet2'] =\
                statistics['Total']['NewFriendForNet2'] + len(subSecond)

        MessageSystem.Verbose(_('New friend for {0}').format(user))

        if len(subFirst) > 0:
            MessageSystem.Verbose(_('    For first net'))
            for newFriend in subFirst:
                MessageSystem.Verbose(_('        {0}').format(newFriend))
        if len(subSecond) > 0:
            MessageSystem.Verbose(_('    For second net'))
            for newFriend in subSecond:
                MessageSystem.Verbose(_('        {0}').format(newFriend))

    statistics['Avg']['NewFriendForNet1'] =\
            (statistics['Total']['NewFriendForNet1'] /
                    statistics['Total']['User'])
    statistics['Avg']['NewFriendForNet2'] =\
            (statistics['Total']['NewFriendForNet2'] /
                    statistics['Total']['User'])
    
    MessageSystem.Info(_('Average number of new friends for network 1: {0}').\
            format(statistics['Avg']['NewFriendForNet1']))
    MessageSystem.Info(_('Average number of new friends for network 2: {0}').\
            format(statistics['Avg']['NewFriendForNet2']))

def GenerateSubNetwork(filePath, delimiter = ',', bfsLevel = 2):
    networkDataSet = LoadNetworkData(filePath, delimiter)

    MessageSystem.Info(_('Generating flat net...'))

    flatNet = FlatV2(networkDataSet)

    SaveFlatNetFile(filePath, flatNet)

    bfsDataSet = {}
    
    GenerateBFS(networkDataSet, bfsDataSet)
    
    UserStatistics(bfsDataSet)

