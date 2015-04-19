#!/usr/bin/python3

def Init(qtMainWindow):
    global gQtMainWindow
    gQtMainWindow = qtMainWindow

def Info(msg):
    msg = _('INFO: ') + msg
    gQtMainWindow.insertLog(msg)

def Warn(msg):
    msg = _('WARN: ') + msg
    gQtMainWindow.insertLog(msg)

def Fatal(msg):
    msg = _('FATAL: ') + msg
    gQtMainWindow.insertLog(msg)

def Important(msg):
    msg = _('IMPORTANT: ') + msg
    gQtMainWindow.insertLog(msg)
