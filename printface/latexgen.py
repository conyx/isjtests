#!/usr/bin/env python3
"""
Module for generating printable tasks in LaTeX

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import os.path

import util
import logger
import common
import string

TASK_NUM = \
"""
===============================================================================
TASK NUM
===============================================================================
""".strip()
QUESTION = \
"""
===============================================================================
QUESTION
===============================================================================
""".strip()
CORRECT_ANSWER = \
"""
===============================================================================
CORRECT ANSWER
===============================================================================
""".strip()

_header = ""
_footer = ""

def serve(students, tasks):
    """
    Assignes tasks to students and creates LaTeX file for each student.
    """
    prepare_templates()
    students_tasks = []
    for student in students:
        logger.print_msg("assigning tasks for student: " + \
                         student.get_login())
        tasks_for_student = util.random_assign(tasks)
        students_tasks += [(student, tasks_for_student)]
    generate_latex_files(students_tasks)
    return 0


def prepare_templates():
    """
    Prepares LaTeX header and footer templates.
    """
    global _header
    global _footer
    module_folder = os.path.dirname(__file__)
    with open(os.path.join(module_folder, "templates", "header.tex"),
              encoding="u8") as f:
        _header = f.read()
    with open(os.path.join(module_folder, "templates", "footer.tex"),
              encoding="u8") as f:
        _footer = f.read()
    
    
def create_choice_latex(task):
    """
    Return latex string with choice or multichoice task.
    """
    latex_part = r"\question[" + str(task.get_max_points()) + "]\n"
    latex_part += util.latex_format(task.get_question()) + "\n"
    latex_part += r"\nopagebreak" + "\n"
    latex_part += r"\begin{choices}" + "\n"
    for answer, rest in task.get_answers():
        latex_part += r"\choice" + "\n"
        latex_part += util.latex_format(answer) + "\n"
    latex_part += r"\end{choices}" + "\n"
    return latex_part
    
    
def create_fulltext_latex(task):
    """
    Return latex string with fulltext or program task.
    """
    latex_part = r"\question[" + str(task.get_max_points()) + "]\n"
    latex_part += util.latex_format(task.get_question()) + "\n"
    latex_part += r"\nopagebreak" + "\n"
    latex_part += r"\makeemptybox{10cm}" + "\n"
    return latex_part
    
    
def save_latex_file(latex_str, id_):
    """
    Save latex file to the output folder.
    """
    path = os.path.join(common.get_config().get_output_path(),
                        '{:0>4}'.format(str(id_)) + ".tex")
    try:
        with open(path, "w", encoding="u8") as f:
            print(latex_str, file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    
    
def save_correct_answers_file(answers_str, id_):
    """
    Save file with correct answers to the output folder.
    """
    path = os.path.join(common.get_config().get_output_path(),
                        '{:0>4}'.format(str(id_)) + ".txt")
    try:
        with open(path, "w", encoding="u8") as f:
            print(answers_str, file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    
    
def generate_latex_files(students_tasks):
    """
    Prepares LaTeX string for each tasks set and save it to the file.
    """
    i = 1
    for student, tasks in students_tasks:
        logger.print_msg("generating latex file for student: " + \
                         student.get_login())
        latex_str = _header
        latex_str = latex_str.replace("#ID#", '{:0>4}'.format(str(i)))
        answers_str = ""
        j = 1
        for task in tasks:
            answers_str += TASK_NUM + "\n"
            answers_str += str(j) + "\n"
            answers_str += QUESTION + "\n"
            answers_str += task.get_question() + "\n"
            answers_str += CORRECT_ANSWER + "\n"
            if (task.get_type() == "choice" or \
                task.get_type() == "multichoice"):
                latex_str += create_choice_latex(task)
                k = 0
                for answer, is_true in task.get_answers():
                    if is_true and k < len(string.ascii_uppercase):
                        answers_str += string.ascii_uppercase[k]
                    k += 1
            else:
                latex_str += create_fulltext_latex(task)
            answers_str += "\n"
            j += 1
        latex_str += _footer
        save_latex_file(latex_str, i)
        save_correct_answers_file(answers_str, i)
        i += 1
        
        