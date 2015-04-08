#!/usr/bin/python3

import csv
import sys

def CommandParse():
    files = {}

    if not len(sys.argv) == 6:
        print('Usage: flatnet.py splitter firstnet.csv secnet.csv node mapping.csv outfile.csv')
        exit()

    delimiter = sys.argv[1]

    files['FirstNetFile'] = sys.argv[2]
    files['SecondNetFile'] = sys.argv[3]
    files['NodeMappingFile'] = sys.argv[4]
    files['OutputFile'] = sys.argv[5]

    return files, delimiter

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
        print('Warn: No "Source" node found')

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

filePath, delimiter = CommandParse()

print('Reading first network...') 
firstNetEdgeList = ReadEdgeListCSV(filePath['FirstNetFile'], delimiter)

print('Reading second network...')
secondNetEdgeList = ReadEdgeListCSV(filePath['SecondNetFile'], delimiter)

print('Reading node mapping...')
nodeMapping, reverseMapping = ReadMappingCSV(filePath['NodeMappingFile'], delimiter)

print('Generating flat net...')
flatNet = FlatNetwork(firstNetEdgeList, secondNetEdgeList, nodeMapping, reverseMapping)

with open(filePath['OutputFile'], mode = 'w') as outCsv:
    for user in flatNet:
        for friend in flatNet[user]:
            print('{0},{1}'.format(user, friend), file = outCsv)
