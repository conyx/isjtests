#!/usr/bin/env python3
"""
Logging module for ISJ tests.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import sys
import datetime

import common

PROGNAME = "isjtests"

_log_file = None


def init():
    """Init module"""
    global _log_file
    if common.get_config().is_logging():
        try:
            _log_file = open(common.get_config().get_logfile(),
                             "w", encoding="u8")
        except IOError:
            print(PROGNAME + ": error: cannot open log file", file=sys.stderr)
            return 1
    # init ok
    return 0


def print_msg(msg):
    """
    If verbose mode is on, print msg to the stdout.
    If logging is on, print msg to the log file.
    """
    if common.get_config().is_verbose():
        print(PROGNAME + ": " + msg)
    if common.get_config().is_logging():
        print(get_date() + msg, file=_log_file)
        _log_file.flush()
    
def print_warning(warning):
    """
    If verbose mode is on, print warning to the stderr.
    If logging is on, print warning to the log file.
    """
    if common.get_config().is_verbose():
        print(PROGNAME + ": warning: " + warning, file=sys.stderr)
    if common.get_config().is_logging():
        print(get_date() + "warning: " + warning, file=_log_file)
        _log_file.flush()
    
def print_error(error):
    """
    Print error to the stderr.
    If logging is on, print error to the log file.
    """
    print(PROGNAME + ": error: " + error, file=sys.stderr)
    if common.get_config().is_logging():
        print(get_date() + "error: " + error, file=_log_file)
        _log_file.flush()
    
def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
    
    
    
    