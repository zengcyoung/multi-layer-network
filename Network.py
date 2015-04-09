#!/usr/bin/python3

import csv
import queue
import MessageType

def ReadEdgeListCSV(fileName, delimiter = ','):
    """
    Read edge list csv to a hash table.
    """
    edgeList = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = delimiter)

        for row in csvTable:
            if not row[0] in edgeList:
                edgeList[row[0]] = []
            edgeList[row[0]].append(row[1])

    try:
        del(edgeList['Source'])
    except:
        MessageType.warn('No "Source" node found')

    return edgeList

def ReadMappingCSV(fileName, delimiter = ','):
    """
    Read user mapping file from csv.
    """
    mapping = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = delimiter)

        for row in csvTable:
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
        flatNet[user] = []
        if not user in mapping:
            MessageType.warn('Mapping reversing for {0}. Please check the order of the networks.'.format(user))
            if not user in reverseMapping:
                MessageType.fatal('Reversing failed, exiting...')
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
            MessageType.warn("{} doesn't exist in the 2nd network!".format(secondName))
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
    baseNet = '1st'
    refNet = '2nd'
    for testUser in mapping:
        if not testUser in firstNet:
            failCount = failCount + 1
        if failCount > reverseLimit:
            MessageType.warn('Over {0} users were not found in the first network, trying to reverse the mapping now...'.format(reverseLimit))
            mapping, reverseMapping = reverseMapping, mapping
            baseNet, refNet = refNet, baseNet

            refailCount = 0

            for retestUser in mapping:
                if not retestUser in mapping:
                    refailCount = refailCount + 1
                if refailCount > reverseLimit:
                    MessageType.fatal('Reverse failed. Please check whether the node mapping is correct')
                    exit()

            MessageType.important('Reverse successfully.')
            break

    flatNet = {}

    # First time iterate
    for user in mapping:
        MessageType.info('Current user: {0}'.format(user))

        if user in firstNet:
            if not user in flatNet:
                flatNet[user] = []

            MessageType.info('    Friends: {0}'.format(firstNet[user]))
            flatNet[user].extend(firstNet[user])
        else:
            MessageType.warn("{0} doesn't exist in the {1} network".format(user, baseNet))

        userAlterName = mapping[user]
        MessageType.info('    Alternative name got: {0}'.format(userAlterName))

        if userAlterName in secondNet:
            for friend in secondNet[userAlterName]:
                if friend in reverseMapping:
                    if not user in flatNet:
                        flatNet[user] = []
                    if user in firstNet:
                        if not reverseMapping[friend] in firstNet[user]:
                            MessageType.info('    New friend from another network: {0}'.format(friend))
                            flatNet[user].append(reverseMapping[friend])
                    else:
                        flatNet[user].append(reverseMapping[friend])
                        MessageType.info('    New friend from another network: {0}'.format(friend))
        else:
            MessageType.warn("{0} doesn't exist in the {1} network as out node".format(user, refNet))

    return flatNet

def BFS(edgeList, src, level = 1):
    visited = set()
    distHash = {}
    q = queue.Queue()
    q.put((src, 0))
    visited.add(src)
    dist = 0
    while not q.empty():
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
