# -*- encoding:UTF-8 -*-
from TimeFormat import TimeFormat
from traceback import format_exc

from os.path import join

msg_output = None
__log_path = join('console.log')


def __print(msg):
    if msg_output is None:
        print msg
    else:
        msg_output(msg + '\r\n')


def info(msg):
    msg = TimeFormat.timestamp() + '  INFO: ' + str(msg)
    __print(msg)
    __write(msg)


def warm(msg):
    msg = TimeFormat.timestamp() + '  WARM: ' + str(msg)
    __print(msg)
    __write(msg)


def error(msg):
    msg = TimeFormat.timestamp() + ' ERROR: ' + str(msg)
    __print(msg)
    __write(msg)


def debug(msg):
    msg = TimeFormat.timestamp() + ' DEBUG: ' + str(msg)
    #__print(msg)
    __write(msg)


def result(msg):
    msg = TimeFormat.timestamp() + '  RSLT: ' + str(msg)
    __print(msg)
    __write(msg)


def __write(msg):
    if msg_output is None:
        return
    with open(__log_path, 'a', 1) as log:
        msg = msg.strip('\r\n') + '\n'
        log.write(msg)


def traceback():
    tmp = format_exc()
    if tmp != 'None\n':
        error(tmp.strip('\n'))
