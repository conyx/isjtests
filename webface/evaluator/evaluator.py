#!/usr/bin/env python3
"""
Module for evaluating students' tasks answers.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import os
import os.path
import re
import subprocess
import datetime
import copy
from threading import Thread
from time import sleep

import logger
import common


QUESTION = \
"""
===============================================================================
QUESTION
===============================================================================
""".strip()
CHOICES = \
"""
===============================================================================
CHOICES
===============================================================================
""".strip()
ANSWER = \
"""
===============================================================================
ANSWER
===============================================================================
""".strip()
CORRECT_ANSWER = \
"""
===============================================================================
CORRECT ANSWER
===============================================================================
""".strip()
PROGRAM = \
"""
===============================================================================
PROGRAM
===============================================================================
""".strip()
INPUT = \
"""
===============================================================================
INPUT
===============================================================================
""".strip()
OUTPUT = \
"""
===============================================================================
OUTPUT
===============================================================================
""".strip()
CORRECT_OUTPUT = \
"""
===============================================================================
CORRECT OUTPUT
===============================================================================
""".strip()
ERROR_OUTPUT = \
"""
===============================================================================
ERROR OUTPUT
===============================================================================
""".strip()
POINTS = \
"""
===============================================================================
POINTS
===============================================================================
""".strip()


def evaluate(student, tasks, formdata):
    """
    Evaluate student's answers (formdata) on tasks. Also write student's
    answers (file login_task_xx.txt) and points (file login_points.txt) to
    the output folder given by the configuration file.
    
    Return list with hit points.
    """
    # init
    logger.print_msg("evaluating of " + student.get_login() + "'s answers " + \
                     "started")
    points = [None] * len(tasks)
    i = 0
    max_points = 0
    # create thread for every task and start it
    for task in tasks:
        task_type = task.get_type()
        max_points += task.get_max_points()
        # choice task
        if task_type == "choice":
            eval_fnc = eval_choice
        # multichoice task
        elif task_type == "multichoice":
            eval_fnc = eval_multichoice
        # fulltext task
        elif task_type == "fulltext":
            eval_fnc = eval_fulltext
        # program task
        elif task_type == "program":
            eval_fnc = eval_program
        t = Thread(target=eval_fnc, \
                   args=(student, task, i, formdata, points))
        t.start()
        i += 1
    # wait until all tasks aren't evaluated
    while None in points:
        sleep(0.2)
    # write points to output folder
    write_points(student, points)
    # log results (points)
    logger.print_msg("evaluating of " + student.get_login() + "'s answers " + \
                     "ended")
    logger.print_msg("student " + student.get_login() + " hit " + \
                     str(round(sum(points), 2)) + " from " + \
                     str(max_points) + " max points")
    # return final points
    return points


def write_points(student, points):
    path = os.path.join(common.get_config().get_output_path(), \
                        student.get_login() + "_points.txt")
    try:
        with open(path, "w", encoding="u8") as f:
            print(str(round(sum(points), 2)), file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    

def eval_choice(student, task, num, formdata, points):
    """
    Evaluate student's answer on choice task.
    """
    # no answer ... 0 points
    try:
        answer_nums = formdata["a_" + str(num)]
    except KeyError:
        write_choice_task(student, task, formdata, num, 0)
        points[num] = 0
        return
    # too much answers (some little hacker) ... 0 points
    if len(answer_nums) != 1 or not answer_nums[0].isdigit():
        write_choice_task(student, task, formdata, num, 0)
        points[num] = 0
        return
    answer_num = int(answer_nums[0])
    task.set_student_answers([answer_num])
    # check correct answer
    i = 0
    for (answer, iscorrect) in task.get_answers():
        if iscorrect and i == answer_num:
            write_choice_task(student, task, formdata, num, \
                              task.get_max_points())
            points[num] = task.get_max_points()
            return
        i += 1
    # oh dear student... wrong answer
    write_choice_task(student, task, formdata, num, 0)
    points[num] = 0
    
    
def eval_multichoice(student, task, num, formdata, points_list):
    """
    Evaluate student's answer on multichoice task.
    """
    # no answer ... 0 points
    try:
        answer_nums = formdata["a_" + str(num)]
    except KeyError:
        write_choice_task(student, task, formdata, num, 0)
        points_list[num] = 0
        return
    # init temp data
    correct_answers = []
    i = 0
    for (answer, iscorrect) in task.get_answers():
        if iscorrect:
            correct_answers += [i]
        i += 1
    value_correct_answer = task.get_max_points()/len(correct_answers)
    # check correct answers
    points = 0
    student_answers = []
    for answer in answer_nums:
        # some hacker?
        if not answer.isdigit() or int(answer) >= len(task.get_answers()):
            write_choice_task(student, task, formdata, num, 0)
            points_list[num] = 0
            return
        # correct answer
        if int(answer) in correct_answers:
            points += value_correct_answer
        # wrong answer
        else:
            points -= value_correct_answer
        student_answers += [int(answer)]
    task.set_student_answers(student_answers)
    # float -> int if possible
    if points.is_integer():
        points = int(points)
    # minimum is 0 points
    write_choice_task(student, task, formdata, num, max(0, points))
    points_list[num] = max(0, points)
    
    
def write_choice_task(student, task, formdata, num, points):
    """
    Write choice or multichoice task to the output folder (with student's
    answer and hit points)
    """
    path = os.path.join(common.get_config().get_output_path(), \
                        student.get_login() + "_task_" + \
                        '{:0>2}'.format(str(num+1)) + ".txt")
    try:
        with open(path, "w", encoding="u8") as f:
            print(QUESTION, file=f)
            print(task.get_question().strip(), file=f)
            print(CHOICES, file=f)
            i = 1
            for (choice, is_correct) in task.get_answers():
                print("[" + str(i) + "] " + str(is_correct), file=f)
                print(choice, file=f)
                i += 1
            print(ANSWER, file=f)
            answer = ""
            try:
                i = 0
                for ans in formdata["a_" + str(num)]:
                    if ans.isdigit():
                        answer += str(int(ans)+1)
                    else:
                        answer += ans
                    if i < len(formdata["a_" + str(num)]) - 1:
                        answer += ","
                    i += 1
            except KeyError:
                answer = ""
            print(answer, file=f)
            print(POINTS, file=f)
            print(round(points, 2), file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    
    
def string_equals(str1, str2):
    """
    Compare two string. Use edit distance 1.
    """
    if len(str1) == len(str2):
        if str1 == str2:
            return True
        else:
            for i in range(len(str1)):
                if str1[0:i] + str2[i+1:len(str1)] == \
                   str2[0:i] + str2[i+1:len(str2)]:
                    return True
    elif len(str1)+1 == len(str2):
        for i in range(len(str2)):
            if str2[0:i] + str2[i+1:len(str2)] == str1:
                return True
    elif len(str2)+1 == len(str1):
        for i in range(len(str1)):
            if str1[0:i] + str1[i+1:len(str1)] == str2:
                return True
    return False
    
def eval_fulltext(student, task, num, formdata, points):
    """
    Evaluate student's answer on fulltext task.
    """
    # write task to the output folder
    path = os.path.join(common.get_config().get_output_path(), \
                        student.get_login() + "_task_" + \
                        '{:0>2}'.format(str(num+1)) + ".txt")
    try:
        answer = formdata["a_" + str(num)][0]
    except (KeyError, IndexError):
        answer = ""
    if common.get_config().get_evaluator_strictness() == 0:
        pattern = re.compile(r'\s+')
        cleaned_answer = re.sub(pattern, '', answer)
    else:
        cleaned_answer = answer.strip()
    final_points = 0
    for correct_answer, coef in task.get_answers():
        if common.get_config().get_evaluator_strictness() == 0:
            pattern = re.compile(r'\s+')
            correct_answer = re.sub(pattern, '', correct_answer)
        else:
            correct_answer = correct_answer.strip()
        if string_equals(cleaned_answer, correct_answer):
            p = task.get_max_points() * coef
            if p.is_integer():
                p = int(p)
        else:
            p = 0
        final_points = max(final_points, p)
    try:
        with open(path, "w", encoding="u8") as f:
            print(QUESTION, file=f)
            print(task.get_question().strip(), file=f)
            for correct_answer, coef in task.get_answers():
                print(CORRECT_ANSWER, file=f)
                print(correct_answer.strip() + " (" + str(coef) + ")", file=f)
            print(ANSWER, file=f)
            print(answer.strip(), file=f)
            print(POINTS, file=f)
            print(final_points, file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    # set points
    points[num] = final_points


def eval_program(student, task, num, formdata, points_list):
    """
    Evaluate student's answer on program task.
    """
    # first get student's input program part
    try:
        student_program_part = formdata["a_" + str(num)][0].replace("\r\n", \
                                                                    "\n")
    except (KeyError, IndexError):
        student_program_part = ""
    # create file with program
    try:
        # prepare folder for program script
        dir_path = os.path.join(common.get_config().get_output_path(),
                                "programs")
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        prog_path = os.path.join(dir_path, task.get_id() + "_" + \
                                 student.get_login() + "." + \
                                 task.get_language())
        # create program as string
        program = ""
        for (program_part, indent) in task.get_program_parts():
            if program_part != None:
                program += program_part.replace("\r\n", "\n")
            else:
                program += indent_all_rows(student_program_part, indent)
            program += "\n"
        # write program to the file
        with open(prog_path, "w", encoding="u8", newline="") as f:
            f.write(program)
    except IOError:
        logger.print_error("cannot write file to the output folder")
        points_list[num] = 0
        return
    final_points = 0
    if task.get_language() == "unknown":
        python2_task = copy.deepcopy(task)
        python2_task.set_language("python2")
        python3_task = copy.deepcopy(task)
        python3_task.set_language("python3")
        ruby_task = copy.deepcopy(task)
        ruby_task.set_language("ruby")
        tasks_for_eval = [python2_task, python3_task, ruby_task]
    else:
        tasks_for_eval = [task]
    for task_for_eval in tasks_for_eval:
        # run program and get output
        (output, error_output) = get_output(task_for_eval, prog_path)
        # compare output with the correct output
        correct_output = task_for_eval.get_correct_output()
        cleaned_output = output
        if common.get_config().get_evaluator_strictness() == 0:
            pattern = re.compile(r'\s+')
            correct_output = re.sub(pattern, '', correct_output)
            cleaned_output = re.sub(pattern, '', output)
        if cleaned_output == correct_output:
            points = task_for_eval.get_max_points()
        else:
            points = 0
        final_points = max(points, final_points)
        if final_points == task_for_eval.get_max_points():
            break
    # write task with results to the output folder
    path = os.path.join(common.get_config().get_output_path(),
                        student.get_login() + "_task_" + \
                        '{:0>2}'.format(str(num+1)) + ".txt")
    try:
        with open(path, "w", encoding="u8") as f:
            print(QUESTION, file=f)
            print(task.get_question().strip(), file=f)
            print(ANSWER, file=f)
            answer = student_program_part
            print(answer, file=f)
            print(PROGRAM, file=f)
            print(prog_path, file=f)
            print(INPUT, file=f)
            prog_input = ""
            if task.get_input() != None:
                prog_input = task.get_input().strip()
            print(prog_input, file=f)
            print(CORRECT_OUTPUT, file=f)
            print(task.get_correct_output().strip(), file=f)
            print(OUTPUT, file=f)
            print(output.strip(), file=f)
            print(ERROR_OUTPUT, file=f)
            print(error_output, file=f)
            print(POINTS, file=f)
            print(round(final_points, 2), file=f)
    except IOError:
        logger.print_error("cannot write file to the output folder")
    # write points and return
    points_list[num] = final_points
    

def indent_all_rows(text, indent):
    """
    Shift all rows from given text by specified indent. Return shifted text.
    """
    result = ""
    for line in text.splitlines(True):
        result += "\t" * indent + line
    return result
    

def get_output(task, prog_path):
    """
    Run program specified by prog_path and return tuple (output, error_output).
    """
    # check task language and set relevant interpreter
    if task.get_language() == "python2":
        interpreter = common.get_config().get_python2path()
    elif task.get_language() == "python3":
        interpreter = common.get_config().get_python3path()
    elif task.get_language() == "ruby":
        interpreter = common.get_config().get_ruby_path()
    else:
        logger.print_error("unknown task language")
        return ("", "")
    # run subprocess
    try:
        p = subprocess.Popen([interpreter, prog_path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except OSError:
        logger.print_error("cannot run interpreter for language " + \
                           task.get_language())
        return ("", "")
    # send input to subprocess in another thread
    outputs = ["", ""]
    t = Thread(target=subprocess_communicate,
               args=(p, task.get_input(), outputs))
    t.start()
    # wait until subprocess ends or time out
    timeout = common.get_config().get_evaluator_timeout()
    start = datetime.datetime.now()
    while p.poll() == None:
        sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            p.kill()
            logger.print_warning("subprocess with interpreter " + \
                                 task.get_language() + " " + \
                                 "has been killed")
            break
    # wait until communication thread ends or time out (5 sec)
    timeout = 5
    start = datetime.datetime.now()
    while t.is_alive():
        sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            logger.print_warning("subprocess communication thread is " + \
                                 "still running, interpreter: " + \
                                 task.get_language())
            break
    return (outputs[0], outputs[1])


def subprocess_communicate(process, input_str, outputs):
    """
    Send input_str to the process and wait until send it's output
    """
    if input_str != None:
        input_data = input_str.encode("u8")
    else:
        input_data = b""
    try:
        (output, error_output) = process.communicate(input_data)
        outputs[0] = output.decode("u8", errors="replace")
        outputs[1] = error_output.decode("u8", errors="replace")
    except IOError:
        logger.print_warning("IOError while comunicating with subprocess")
        outputs[0] = "IOError"
        outputs[1] = "IOError"
    

