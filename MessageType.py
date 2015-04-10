#!/usr/bin/python3

def info(msg):
    msg = _('INFO: ') + msg
    print(msg)

def warn(msg):
    msg = _('WARN: ') + msg
    print(msg)

def fatal(msg):
    msg = _('FATAL: ') + msg
    print(msg)

def important(msg):
    msg = _('IMPORTANT: ') + msg
    print(msg)
