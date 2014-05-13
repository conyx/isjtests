#!/usr/bin/env python3
"""
Data model for ISJ tests.
Student data representation.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""


class Student:
    
    def __init__(self):
        self.set_login(None)
        self.set_name(None)
    
    def set_login(self, login):
        self._login = login
        
    def get_login(self):
        return self._login
        
    def set_name(self, name):
        self._name = name
    
    def get_name(self):
        return self._name