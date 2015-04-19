#!/usr/bin/python3

import csv
import queue
import MessageType

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
            if not row[0] in edgeList:
                edgeList[row[0]] = []
            edgeList[row[0]].append(row[1])

    try:
        del(edgeList['Source'])
    except:
        MessageType.Warn(_('No "Source" node found'))

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

def Flat(firstNet, secondNet, mapping, reverseMapping):
    """
    Create a flat network using node mapping.
    The user name is based on the firstNet.
    """
    flatNet = {}

    for user in firstNet:
        gQtMainWindow.updateInterface()
        flatNet[user] = []
        if not user in mapping:
            MessageType.Warn(_('Mapping reversing for {0}. ').format(user) +
                    _('Please check the order of the networks.'))
            if not user in reverseMapping:
                MessageType.Fatal(_('Reversing failed, exiting...'))
                exit()
            else:
                secondName = reverseMapping[user]
        else:
            secondName = mapping[user]
        # Can't use code below
        # flatNet[user] = firstNet[user].copy()
        # In case the friend doesn't exist in the other network

        for friend in firstNet[user]:
            if friend in mapping:
                flatNet[user].append(friend)

        if not secondName in secondNet:
            MessageType.Warn(_("{} doesn't exist in the 2nd network!").format(
                secondName))
        else:
            for secondNetFriend in secondNet[secondName]:
                if not secondNetFriend in reverseMapping:
                    continue # The friend doesn't belong to both network
                friendNameInFirstNet = reverseMapping[secondNetFriend]
                if not friendNameInFirstNet in firstNet[user]:
                    flatNet[user].append(friendNameInFirstNet)

    return flatNet

def FlatV2(firstNet, secondNet, mapping, reverseMapping):
    # Test whether is mapping is reversed

    reverseLimit = 100

    failCount = 0
    baseNet = _('1st')
    refNet = _('2nd')
    for testUser in mapping:
        gQtMainWindow.updateInterface()
        if not testUser in firstNet:
            failCount = failCount + 1
        if failCount > reverseLimit:
            MessageType.Warn(_('Over {0} users were not ').format(reverseLimit) +
                    _('found in the first network, ') +
                    _('trying to reverse the mapping now...'))
            mapping, reverseMapping = reverseMapping, mapping
            baseNet, refNet = refNet, baseNet

            refailCount = 0

            for retestUser in mapping:
                if not retestUser in mapping:
                    refailCount = refailCount + 1
                if refailCount > reverseLimit:
                    MessageType.Fatal(_('Reverse failed. ') +
                            _('Please check whether the node mapping is correct'))
                    exit()

            MessageType.Important(_('Reverse successfully.'))
            break

    flatNet = {}

    # First time iterate
    for user in mapping:
        gQtMainWindow.updateInterface()
        MessageType.Info(_('Current user: {0}').format(user))

        if user in firstNet:
            if not user in flatNet:
                flatNet[user] = []

            MessageType.Info(_('    Friends: {0}').format(firstNet[user]))
            flatNet[user].extend(firstNet[user])
        else:
            MessageType.Warn(_("{0} doesn't exist in the {1} network").format(
                user, baseNet))

        userAlterName = mapping[user]
        MessageType.Info(_('    Alternative name got: {0}').format(
            userAlterName))

        if userAlterName in secondNet:
            for friend in secondNet[userAlterName]:
                if friend in reverseMapping:
                    if not user in flatNet:
                        flatNet[user] = []
                    if user in firstNet:
                        if not reverseMapping[friend] in firstNet[user]:
                            MessageType.Info(
                                    _('    New friend from another network: ') +
                                    _('{0}').format(friend))
                            flatNet[user].append(reverseMapping[friend])
                    else:
                        flatNet[user].append(reverseMapping[friend])
                        MessageType.Info(
                                _('    New friend from another network: ') +
                                _('{0}').format(friend))
        else:
            MessageType.Warn(_("{0} doesn't exist in ").format(user) +
                    _('the {0} network as out node').format(refNet))

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

def GenerateSubNetwork(filePath, delimiter = ',', bfsLevel = 2):
    MessageType.Info(_('Reading first network...'))
    firstNetEdgeList = ReadEdgeListCSV(
            filePath['FirstNetFile'], delimiter)

    MessageType.Info(_('Reading second network...'))
    secondNetEdgeList = ReadEdgeListCSV(
            filePath['SecondNetFile'], delimiter)

    MessageType.Info(_('Reading node mapping...'))
    nodeMapping, reverseMapping = ReadMappingCSV(
            filePath['NodeMappingFile'], delimiter)

    MessageType.Info(_('Generating flat net...'))
    flatNet = FlatV2(
            firstNetEdgeList, secondNetEdgeList, nodeMapping, reverseMapping)

    with open(filePath['OutputFile'], mode = 'w') as outCsv:
        for user in flatNet:
            for friend in flatNet[user]:
                print('{0},{1}'.format(user, friend), file = outCsv)

    firstNetBFS = {}

    MessageType.Info(_('Generating BFS node for the first network...'))
    for user in firstNetEdgeList:
        firstNetBFS[user] = BFS(
                firstNetEdgeList, user, level = bfsLevel)

    secondNetBFSRaw = {}

    MessageType.Info(_('Generating BFS node for the second network...'))
    for user in secondNetEdgeList:
        secondNetBFSRaw[user] = BFS(
                secondNetEdgeList, user, level = bfsLevel)

    # Mapping for the secondNetBFS

    secondNetBFS = {}

    for alterName in secondNetBFSRaw:
        gQtMainWindow.updateInterface()
        if alterName in reverseMapping:
            user = reverseMapping[alterName]
            secondNetBFS[user] = []
            for alterFriendName in secondNetBFSRaw[alterName]:
                if alterFriendName in reverseMapping:
                    friendName = reverseMapping[alterFriendName]
                    secondNetBFS[user].append(friendName)

    flatNetBFS = {}

    MessageType.Info(_('Generating BFS node for the flat network...'))
    for user in flatNet:
        flatNetBFS[user] = BFS(flatNet, user, level = bfsLevel)

    for user in flatNetBFS:
        gQtMainWindow.updateInterface()
        firstNetFriendSet = set()
        secondNetFriendSet = set()
        flatNetFriendSet = set()

        if user in firstNetBFS:
            firstNetFriendSet = set(firstNetBFS[user].keys())
            firstNetFriendSet.remove(user)

        if user in secondNetBFS:
            secondNetFriendSet = set(secondNetBFS[user])
            secondNetFriendSet.remove(user)

        flatNetFriendSet = set(flatNetBFS[user].keys())
        flatNetFriendSet.remove(user)

        subFirst = flatNetFriendSet - firstNetFriendSet
        subSecond = flatNetFriendSet - secondNetFriendSet

        MessageType.Info(_('New friend for {0}').format(user))
        if len(subFirst) > 0:
            MessageType.Info(_('    For first net'))
            for newFriend in subFirst:
                MessageType.Info(_('        {0}').format(newFriend))
        if len(subSecond) > 0:
            MessageType.Info(_('    For second net'))
            for newFriend in subSecond:
                MessageType.Info(_('        {0}').format(newFriend))

