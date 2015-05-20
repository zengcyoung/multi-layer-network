#!/usr/bin/python3

import json
import gettext
import MessageSystem
import Network
import Guess

gConfigure = {}

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

def SaveConfigure():
    global gConfigure
    with open('conf.json', mode = 'w') as configureFile:
        try:
            json.dump(gConfigure, configureFile)
        except:
            None

if __name__ == '__main__':

    import sys

    ReadConfigure()
