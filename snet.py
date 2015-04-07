#!/usr/bin/python3

import csv

def ReadEdgeListCSV(fileName):
    """
    Read edge list csv to a hash table.
    The CSV file's splitter should be tab.
    """
    edgeList = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = ',')

        for row in csvTable:
            if not row[0] in edgeList:
                edgeList[row[0]] = []
            edgeList[row[0]].append(row[1])


    return edgeList

def ReadMappingCSV(fileName):
    """
    Read user mapping file from csv.
    """
    mapping = {}

    with open(fileName, newline = '') as csvFile:
        csvTable = csv.reader(csvFile, delimiter = ',')

        for row in csvTable:
            mapping[row[0]] = row[1]

    reverseMapping = {v : k for k, v in mapping.items()}

    return mapping, reverseMapping

def FlatNetwork(firstNet, secondNet, mapping, reverseMapping):
    """
    Create a flat network using node mapping.
    The user name is based on the firstNet.
    """
    flatNet = {}

    for user in firstNet:
        flatNet[user] = []
        if not user in mapping:
            print('Mapping reversing for {0}'.format(user))
            if not user in reverseMapping:
                print('Reversing failed, exiting...')
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
            print("{} doesn't exist in the 2nd network!".format(secondName))
        else:
            for secondNetFriend in secondNet[secondName]:
                if not secondNetFriend in reverseMapping:
                    continue # The friend doesn't belong to both network
                friendNameInFirstNet = reverseMapping[secondNetFriend]
                if not friendNameInFirstNet in firstNet[user]:
                    flatNet[user].append(friendNameInFirstNet)

    return flatNet

print('Reading friendfeed network...') 
friendfeed = ReadEdgeListCSV(r'F:\Programming\Graduation Project\simple ml\anet.csv')

print('Reading twitter network...')
twitter = ReadEdgeListCSV(r'F:\Programming\Graduation Project\simple ml\bnet.csv')

print('Reading node mapping...')
nodeMapping, reverseMapping = ReadMappingCSV(r'F:\Programming\Graduation Project\simple ml\mapping.csv')

print(twitter)
print(friendfeed)

print('Generating flat net...')
flat = FlatNetwork(friendfeed, twitter, nodeMapping, reverseMapping)

with open(r'F:\Programming\Graduation Project\simple ml\flat.csv', mode = 'w') as outCsv:
    for user in flat:
        for friend in flat[user]:
            print('{0},{1}'.format(user, friend), file = outCsv)
