#!/usr/bin/python3

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
    msg = _('Verbose: ') + msg
    if gQtMainWindow.getIsVerboseLog():
        gQtMainWindow.insertLog(msg)