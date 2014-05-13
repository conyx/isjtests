#!/usr/bin/env python3
"""
Common variables and constants

Author:
Tomas Bambas xbamba01@stud.fit.vutbr.cz
"""

# constants
EXIT_OK = 0
EXIT_ERROR_OPTIONS = 1
EXIT_ERROR_LOGGER = 2
EXIT_ERROR_STUDENTS = 3
EXIT_ERROR_TASKS = 4
EXIT_ERROR_INTERFACE = 5
# variables
_config = None

def set_config(configuration):
    global _config
    _config = configuration

def get_config():
    return _config