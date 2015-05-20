#!/usr/bin/python3

def GetMessage(msgArgs):
    global gQtMainWindow

    msgList = [x for x in range(500)]

    # Message starts from 0 means info

    # starts from 100 means warn
    msgList[100] = _("No \"Source\" node found")
    msgList[101] = _('Over {0} users were not found in the first network, trying to reverse the mapping now...')
    msgList[102] = _("{0} doesn't exist in the {1} network")
    msgList[103] = _("{0} doesn't exist in the {1} network as out node")

    # starts from 200 means fatal
    msgList[200] = _('Reverse failed. Please check whether the node mapping is correct')

    # starts from 300 means important
    msgList[300] = _('Reverse successfully.')

    # starts from 400 means verbose
    msgList[400] = _('Current user: {0}')
    msgList[401] = _('    Friends: {0}')
    msgList[402] = _('    Alternative name got: {0}')
    msgList[403] = _('    New friend from another network: {0}')
    msgList[404] = _('    New friend from another network: {0}')

    if len(msgArgs) == 1:
        finalMsg = msgList[msgArgs[0]]
    elif len(msgArgs) == 2:
        finalMsg = msgList[msgArgs[0]].format(msgArgs[1])
    elif len(msgArgs) == 3:
        finalMsg = msgList[msgArgs[0]].format(msgArgs[1],
                msgArgs[2])
    elif len(msgArgs) == 4:
        finalMsg = msgList[msgArgs[0]].format(msgArgs[1],
                msgArgs[2], msgArgs[3])
    else:
        finalMsg = "TOO MANY ARGUMENTS!"

    if msgArgs[0] < 100 and gQtMainWindow.getIsInfoLog():
        finalMsg = _("INFO: ") + finalMsg
    elif msgArgs[0] < 200 and gQtMainWindow.getIsWarnLog():
        finalMsg = _("WARN: ") + finalMsg
    elif msgArgs[0] < 300 and gQtMainWindow.getIsFatalLog():
        finalMsg = _("FATAL: ") + finalMsg
    elif msgArgs[0] < 400 and gQtMainWindow.getIsImportantLog():
        finalMsg = _("IMPORTANT: ") + finalMsg
    elif msgArgs[0] < 500 and gQtMainWindow.getIsVerboseLog():
        finalMsg = _("VERBOSE: ") + finalMsg
    else:
        finalMsg = ""

    return finalMsg

def Send(*msgArgs):
    msg = GetMessage(msgArgs)

    if not msg == "":
        gQtMainWindow.insertLog(msg)

def Init(qtMainWindow):
    global gQtMainWindow
    gQtMainWindow = qtMainWindow

def Info(msg):
    msg = _('INFO: ') + msg
    if gQtMainWindow.getIsInfoLog():
        gQtMainWindow.insertLog(msg)

def Warn(msg):
    msg = _('WARN: ') + msg
    if gQtMainWindow.getIsWarnLog():
        gQtMainWindow.insertLog(msg)

def Fatal(msg):
    msg = _('FATAL: ') + msg
    if gQtMainWindow.getIsFatalLog():
        gQtMainWindow.insertLog(msg)

def Important(msg):
    msg = _('IMPORTANT: ') + msg
    if gQtMainWindow.getIsImportantLog():
        gQtMainWindow.insertLog(msg)

def Verbose(msg):
    msg = _('VERBOSE: ') + msg
    if gQtMainWindow.getIsVerboseLog():
        gQtMainWindow.insertLog(msg)
