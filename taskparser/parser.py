#!/usr/bin/env python3
"""
Module for parsing XML defined tasks for ISJ tests.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import os
import xml.etree.ElementTree as etree
import hashlib

import logger
import datamodel
import util
import common

def parse_task(xml_file_path):
    """
    Return datamodel.Task object parsed from given file path or return None if
    something got wrong.
    """
    logger.print_msg("parsing XML task " + xml_file_path)
    try:
        rootelem = etree.parse(xml_file_path)
        if rootelem == None or rootelem.getroot() == None:
            return None
        rootelem = rootelem.getroot()
        # choice type of task
        if rootelem.get("type") == "choice":
            task = datamodel.ChoiceTask()
            if (rootelem.find("question") != None and
                rootelem.find("question").text != None):
                task.set_question(rootelem.find("question").text.strip())
            answers = []
            for answer in rootelem.findall("answer"):
                if answer.text:
                    if answer.get("type") == "true":
                        answers += [(answer.text.strip(), True)]
                    elif answer.get("type") == "false":
                        answers += [(answer.text.strip(), False)]
                    else:
                        return None
                else:
                    return None
            task.set_answers(answers)
        # multichoice type of task
        elif rootelem.get("type") == "multichoice":
            task = datamodel.MultiChoiceTask()
            if (rootelem.find("question") != None and
                rootelem.find("question").text != None):
                task.set_question(rootelem.find("question").text.strip())
            answers = []
            for answer in rootelem.findall("answer"):
                if answer.text:
                    if answer.get("type") == "true":
                        answers += [(answer.text.strip(), True)]
                    elif answer.get("type") == "false":
                        answers += [(answer.text.strip(), False)]
                    else:
                        return None
                else:
                    return None
            task.set_answers(answers)
        # program type of task
        elif rootelem.get("type") == "program":
            task = datamodel.ProgramTask()
            if (rootelem.find("question") != None and
                rootelem.find("question").text != None):
                task.set_question(rootelem.find("question").text.strip())
            if (rootelem.find("language") != None and
                rootelem.find("language").text != None):
                task.set_language(rootelem.find("language").text.strip())
            program_parts = []
            for ppart in rootelem.findall("program"):
                if ppart.get("type") == "edit":
                    if ppart.get("indent") != None:
                        if ppart.get("indent").isdecimal():
                            program_parts += [(None, int(ppart.get("indent")))]
                        else:
                            return None
                    else:
                        program_parts += [(None, 0)]
                elif ppart.text != None:
                    program_parts += [(ppart.text, 0)]
                else:
                    return None
            task.set_program_parts(program_parts)
            if (rootelem.find("output") != None and
                rootelem.find("output").text != None):
                task.set_correct_output(rootelem.find("output").text)
            if (rootelem.find("input") != None and
                rootelem.find("input").text != None):
                task.set_input(rootelem.find("input").text)
            if (rootelem.find("prefill") != None and
                rootelem.find("prefill").text != None):
                task.set_prefill(rootelem.find("prefill").text.strip())
            if (rootelem.find("help") != None and
                rootelem.find("help").text != None):
                task.set_help(rootelem.find("help").text.strip())
        # fulltext type of task
        elif rootelem.get("type") == "fulltext":
            task = datamodel.FulltextTask()
            if (rootelem.find("question") != None and
                rootelem.find("question").text != None):
                task.set_question(rootelem.find("question").text.strip())
            answers = []
            for answer in rootelem.findall("answer"):
                if (answer.get("percent") != None and
                    answer.get("percent").isdecimal() and
                    answer.text != None):
                    answers += [(answer.text, float(answer.get("percent"))/100)]
                else:
                    return None
            task.set_answers(answers)
            if (rootelem.find("prefill") != None and
                rootelem.find("prefill").text != None):
                task.set_prefill(rootelem.find("prefill").text.strip())
            if (rootelem.find("help") != None and
                rootelem.find("help").text != None):
                task.set_help(rootelem.find("help").text.strip())
        else:
            return None
        m = hashlib.md5()
        m.update(xml_file_path.encode("u8"))
        task.set_id(m.hexdigest())
        return task
    except (IOError, etree.ParseError) as err:
       return None

def parse_dynamic_task(file_path):
    """
    Return datamodel.DynamicTask object parsed from given file path or return
    None if something got wrong.
    """
    logger.print_msg("parsing DYNAMIC task " + file_path)
    try:
        task = None
        with open(file_path, encoding="u8") as f:
            task_code = f.read()
            custom_locals = {}
            exec(task_code, globals(), custom_locals)
            task = custom_locals["task"]
        if isinstance(task, datamodel.DynamicTask):
            m = hashlib.md5()
            m.update(file_path.encode("u8"))
            task.set_id(m.hexdigest())
            return task
        else:
            return None
    except (KeyError, IOError) as err:
       return None


def parse_tasks(folder_path):
    """
    Parse all XML tasks from folder folder_path.
    Return list with datamodel.Task objects or None if something got wrong.
    """
    tasks = []
    try:
        for xmlfile in os.listdir(folder_path):
            file_path = os.path.join(folder_path, xmlfile)
            if file_path.endswith(".py"):
                task = parse_dynamic_task(file_path)
            elif file_path.endswith(".xml"):
                task = parse_task(file_path)
            else:
                continue
            if task == None or not task.check():
                logger.print_warning("skipped incorrect task " + file_path)
            else:
                task.set_filepath(file_path)
                tasks += [task]
    except OSError:
        return None
    return tasks


def parse_all_tasks():
    """
    Parse all tasks from user specified folders.
    Return list with tuples (tasks, number) where tasks is list of
    datamodel.Task objects and number is number of tasks per student from
    this list.
    """
    tasks = []
    tasks_paths = common.get_config().get_tasks_paths()
    for (task_path, points, number) in tasks_paths:
        tasks_from_folder = parse_tasks(task_path)
        # something got wrong
        if tasks_from_folder == None:
            logger.print_error("there is something wrong with folder " +
                               task_path)
            return None
        # too little tasks in folder
        if len(tasks_from_folder) < number:
            logger.print_error("too little tasks in folder " +
                               task_path + ", need " + str(number))
            return None
        # set max points for every task in folder
        for task in tasks_from_folder:
            task.set_max_points(points)
        # add tuple (tasks_from_folder, number) to the end list
        tasks += [(tasks_from_folder, number)]
    return tasks
    
    
    
    
    