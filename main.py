#!/usr/bin/python3

import sys
import Network
import MessageType
import gettext

zh = gettext.translation('flatnet', localedir = 'locale',
        languages = ['zh'])
zh.install()

def CommandParse():
    files = {}

    if not len(sys.argv) == 6:
        print(_('Usage: main.py splitter'),
                _('firstnet.csv secnet.csv nodemapping.csv outfile.csv'))
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

    Network.GenerateSubNetwork(filePath, delimiter, bfsLevel)
