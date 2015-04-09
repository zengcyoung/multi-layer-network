#!/usr/bin/python3

import sys
import Network
import MessageType

def CommandParse():
    files = {}

    if not len(sys.argv) == 6:
        print('Usage: flatnet.py splitter firstnet.csv secnet.csv nodemapping.csv outfile.csv')
        exit()

    delimiter = sys.argv[1]
    if len(delimiter) > 1:
        if delimiter[1] == 't':
            delimiter = '\t'

    files['FirstNetFile'] = sys.argv[2]
    files['SecondNetFile'] = sys.argv[3]
    files['NodeMappingFile'] = sys.argv[4]
    files['OutputFile'] = sys.argv[5]

    return files, delimiter

if __name__ == "__main__":
    bfsLevel = 2
    filePath, delimiter = CommandParse()

    MessageType.info('Reading first network...') 
    firstNetEdgeList = Network.ReadEdgeListCSV(filePath['FirstNetFile'], delimiter)

    MessageType.info('Reading second network...')
    secondNetEdgeList = Network.ReadEdgeListCSV(filePath['SecondNetFile'], delimiter)

    MessageType.info('Reading node mapping...')
    nodeMapping, reverseMapping = Network.ReadMappingCSV(filePath['NodeMappingFile'], delimiter)

    MessageType.info('Generating flat net...')
    flatNet = Network.FlatV2(firstNetEdgeList, secondNetEdgeList, nodeMapping, reverseMapping)

    with open(filePath['OutputFile'], mode = 'w') as outCsv:
        for user in flatNet:
            for friend in flatNet[user]:
                print('{0},{1}'.format(user, friend), file = outCsv)

    firstNetBFS = {}

    MessageType.info('Generating BFS node for the first network...')
    for user in firstNetEdgeList:
        firstNetBFS[user] = Network.BFS(firstNetEdgeList, user, level = bfsLevel)

    secondNetBFSRaw = {}

    MessageType.info('Generating BFS node for the second network...')
    for user in secondNetEdgeList:
        secondNetBFSRaw[user] = Network.BFS(secondNetEdgeList, user, level = bfsLevel)

    # Mapping for the secondNetBFS

    secondNetBFS = {}

    for alterName in secondNetBFSRaw:
        if alterName in reverseMapping:
            user = reverseMapping[alterName]
            secondNetBFS[user] = []
            for alterFriendName in secondNetBFSRaw[alterName]:
                if alterFriendName in reverseMapping:
                    friendName = reverseMapping[alterFriendName]
                    secondNetBFS[user].append(friendName)

    flatNetBFS = {}

    MessageType.info('Generating BFS node for the flat network...')
    for user in flatNet:
        flatNetBFS[user] = Network.BFS(flatNet, user, level = bfsLevel)

    for user in flatNetBFS:
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

        MessageType.info('New friend for {0}'.format(user))
        if len(subFirst) > 0:
            MessageType.info('    For first net')
            for newFriend in subFirst:
                MessageType.info('        {0}'.format(newFriend))
        if len(subSecond) > 0:
            MessageType.info('    For second net')
            for newFriend in subSecond:
                MessageType.info('        {0}'.format(newFriend))

