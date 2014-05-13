#!/usr/bin/env python3
"""
Module defines functions for tasks assignment to students.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import random
import copy
import datamodel
import logger


def random_assign(tasks):
    """
    Get list with tuples (tasks, number) tasks is list with datamodel.Task
    objects and number is number of tasks per student
    
    Return list with randomly selected tasks.
    """
    final_tasks = []
    for (tasks_list, number) in tasks:
        indexes = [i for i in range(len(tasks_list))]
        random.shuffle(indexes)
        i = 0
        while i < number:
            # get random task from given list
            origtask = tasks_list[indexes[i]]
            # if task is dynamic type, generate task
            if origtask.get_type() == "dynamic":
                task = origtask.generate()
                if (not isinstance(task, datamodel.ChoiceTask) and
                    not isinstance(task, datamodel.MultiChoiceTask) and
                    not isinstance(task, datamodel.ProgramTask) and
                    not isinstance(task, datamodel.FulltextTask)):
                    logger.print_error("incorrect generated task by dynamic " +
                                       "task (incorrect type " + \
                                       str(type(task)) + ") " + \
                                       origtask.get_filepath())
                    raise ValueError("error in task " + \
                                     origtask.get_filepath())
                if task.get_id() == None:
                    task.set_id(origtask.get_id())
                task.set_filepath(origtask.get_filepath())
                task.set_max_points(origtask.get_max_points())
                if not task.check():
                    logger.print_error("incorrect generated task by dynamic " +
                                       "task " + origtask.get_filepath())
                    raise ValueError("error in task " + \
                                     origtask.get_filepath())
            else:
                task = origtask
            # make a deep copy of the task
            task = copy.deepcopy(task)
            if task.get_type() == "choice" or task.get_type() == "multichoice":
                task.shuffle_answers()
            # add task to the final list
            final_tasks += [task]
            i += 1
    return final_tasks
    