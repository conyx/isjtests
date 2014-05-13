#!/usr/bin/env python3
"""
Data model for ISJ tests.
Init module.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

from .student import Student
from .task import ChoiceTask, MultiChoiceTask, FulltextTask, ProgramTask, \
                  DynamicTask, Task, ChoiceOutputDynamicTask
from .configuration import Configuration
