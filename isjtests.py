#!/usr/bin/env python3
"""
---------------------------------- ISJ Tests ----------------------------------
Usage: ./isjtests.py [-h] -c file

Options:
-h, --help                  prints this help and exit
-c, --config-file           path to XML configuration file

Description:
ISJ Tests is configurable tool for generating and evaluating individual tests
for Scripting Languages course (ISJ) on Faculty of Information Technology,
Brno University of Technology.

Author:
Tomas Bambas xbamba01@stud.fit.vutbr.cz
"""

import sys
import xml.etree.ElementTree as etree
import csv

import datamodel
import logger
import taskparser
import webface
import printface
import common

def parse_options():
    """
    Parse program options, parse XML configuration file and return tuple
    (state, configuration) where...
            state is 0 if everything ok
                     1 print help and exit
                     2 if something failed
            configuration is datamodel.Configuration object
    """
    # define constants
    PROG_NAME_ERROR = "isjtests: error"
    INCORRECT_CONFIG =  PROG_NAME_ERROR + ": incorrect config file: "
    # check program options
    if len(sys.argv) < 2:
        print(PROG_NAME_ERROR + ": bad input params, try --help",
              file=sys.stderr)
        return (2, None)
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        return (1, None)
    elif (sys.argv[1] != "-c" and sys.argv[1] != "--config-file" or
          len(sys.argv) != 3):
        print(PROG_NAME_ERROR + ": bad input params, try --help",
              file=sys.stderr)
        return (2, None)
    # parse xml configuration file
    config_file = sys.argv[2]
    try:
        rootelem = etree.parse(config_file)
    except (IOError, etree.ParseError) as err:
        print(PROG_NAME_ERROR + ": incorrect config file", file=sys.stderr)
        return (2, None)
    # get config options
    configuration = datamodel.Configuration()
    # get mode
    elem = rootelem.find("mode")
    if elem != None:
        if elem.text.strip() == "web" or elem.text.strip() == "print":
            configuration.set_mode(elem.text.strip())
        else:
            print(INCORRECT_CONFIG + "incorrect mode option",
                  file=sys.stderr)
            return (2, None)
    # get verbose
    elem = rootelem.find("verbose")
    if elem != None:
        if elem.text.strip() == "on":
            configuration.set_verbose(True)
        elif elem.text.strip() == "off":
            configuration.set_verbose(False)
        else:
            print(INCORRECT_CONFIG + "incorrect verbose option",
                  file=sys.stderr)
            return (2, None)
    # get logging
    elem = rootelem.find("logging")
    if elem != None:
        if elem.text.strip() == "on":
            configuration.set_logging(True)
        elif elem.text.strip() == "off":
            configuration.set_logging(False)
        else:
            print(INCORRECT_CONFIG + "incorrect logging option",
                  file=sys.stderr)
            return (2, None)
    # get logfile path
    elem = rootelem.find("logfile")
    if elem != None:
        if elem.text != None:
            configuration.set_logfile(elem.text.strip())
        else:
            print(INCORRECT_CONFIG + "incorrect logfile path option",
                  file=sys.stderr)
            return (2, None)
    # get interpreter commands paths for evaluator usage
    epathselem = rootelem.find("evaluator_paths")
    if epathselem != None:
        # get python 2 path
        elem = epathselem.find("python2path")
        if elem != None:
            if elem.text != None:
                configuration.set_python2path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect python 2 path option",
                      file=sys.stderr)
                return (2, None)
        # get python 3 path
        elem = epathselem.find("python3path")
        if elem != None:
            if elem.text != None:
                configuration.set_python3path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect python 3 path option",
                      file=sys.stderr)
                return (2, None)
        # get ruby path
        elem = epathselem.find("rubypath")
        if elem != None:
            if elem.text != None:
                configuration.set_ruby_path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect ruby path option",
                      file=sys.stderr)
                return (2, None)
    # get interpreter commands paths for internal usage
    ipathselem = rootelem.find("internal_paths")
    if ipathselem != None:
        # get python 2 path
        elem = ipathselem.find("python2path")
        if elem != None:
            if elem.text != None:
                configuration.set_intern_python2path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect python 2 path option",
                      file=sys.stderr)
                return (2, None)
        # get python 3 path
        elem = ipathselem.find("python3path")
        if elem != None:
            if elem.text != None:
                configuration.set_intern_python3path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect python 3 path option",
                      file=sys.stderr)
                return (2, None)
        # get ruby path
        elem = ipathselem.find("rubypath")
        if elem != None:
            if elem.text != None:
                configuration.set_intern_ruby_path(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect ruby path option",
                      file=sys.stderr)
                return (2, None)
    # get path for output files
    elem = rootelem.find("outputpath")
    if elem != None:
        if elem.text != None:
            configuration.set_output_path(elem.text.strip())
        else:
            print(INCORRECT_CONFIG + "incorrect output path option",
                  file=sys.stderr)
            return (2, None)
    # get path of CSV file with students
    elem = rootelem.find("students")
    if elem != None:
        if elem.text != None:
            configuration.set_students_csv_file_path(elem.text.strip())
        else:
            print(INCORRECT_CONFIG + "incorrect students CSV path option",
                  file=sys.stderr)
            return (2, None)
    # get tasks folder paths
    taskselem = rootelem.find("tasks")
    if taskselem != None:
        tasks = []
        for elem in taskselem.findall("taskspath"):
            if (elem.text != None and
                elem.get("points") != None and
                elem.get("number") != None and
                elem.get("points").isdecimal() and
                elem.get("number").isdecimal() and
                int(elem.get("points")) > 0 and
                int(elem.get("number")) > 0):
                tasks += [(elem.text.strip(),
                           int(elem.get("points")),
                           int(elem.get("number")))]
            else:
                print(INCORRECT_CONFIG + "incorrect tasks paths option",
                      file=sys.stderr)
                return (2, None)
        if len(tasks) == 0:
            print(INCORRECT_CONFIG + "please specify some tasks",
                  file=sys.stderr)
            return (2, None)
        configuration.set_tasks_paths(tasks)
    # get options for web interface
    webelem = rootelem.find("webface")
    if webelem != None:
        # get port
        elem = webelem.find("port")
        if elem != None:
            if elem.text != None and elem.text.strip().isdecimal():
                configuration.set_webserver_port(int(elem.text.strip()))
            else:
                print(INCORRECT_CONFIG + "incorrect web server port option",
                      file=sys.stderr)
                return (2, None)
        # get common password
        elem = webelem.find("commonpassword")
        if elem != None:
            if elem.text != None:
                configuration.set_webserver_pass(elem.text.strip())
            else:
                print(INCORRECT_CONFIG + "incorrect web server passw option",
                      file=sys.stderr)
                return (2, None)
        # get evaluator strictness option
        elem = webelem.find("eval_strict")
        if elem != None:
            if (elem.text != None and elem.text.strip().isdecimal() and
                int(elem.text.strip()) >= 0 and int(elem.text.strip()) <= 1):
                configuration.set_evaluator_strictness(int(elem.text.strip()))
            else:
                print(INCORRECT_CONFIG + \
                      "incorrect evaluator strictness option",
                      file=sys.stderr)
                return (2, None)
        # get evaluator timeout option
        elem = webelem.find("eval_timeout")
        if elem != None:
            if (elem.text != None and elem.text.strip().isdecimal() and
                int(elem.text.strip()) > 0):
                configuration.set_evaluator_timeout(int(elem.text.strip()))
            else:
                print(INCORRECT_CONFIG + \
                      "incorrect evaluator timeout option",
                      file=sys.stderr)
                return (2, None)
        # get anonymous option
        elem = webelem.find("anonymous")
        if elem != None:
            if elem.text.strip() == "on":
                configuration.set_anonymous(True)
            elif elem.text.strip() == "off":
                configuration.set_anonymous(False)
            else:
                print(INCORRECT_CONFIG + "incorrect anonymous option",
                      file=sys.stderr)
                return (2, None)
        # get self learning option
        elem = webelem.find("self_learning")
        if elem != None:
            if elem.text.strip() == "on":
                configuration.set_self_learning(True)
            elif elem.text.strip() == "off":
                configuration.set_self_learning(False)
            else:
                print(INCORRECT_CONFIG + "incorrect self learning option",
                      file=sys.stderr)
                return (2, None)
    return (0, configuration)


def read_students_list():
    """
    Read students list from CSV file and return list with datamodel.Student
    objects.
    """
    students = []
    csv.register_dialect('students', quoting=csv.QUOTE_NONE)
    try:
        with open(common.get_config().get_students_csv_file_path(),
                  encoding="u8",
                  newline='') as f:
            reader = csv.reader(f, 'students')
            for row in reader:
                if len(row) != 2:
                    logger.print_error("incorrect students list CSV file")
                    return None
                else:
                    student = datamodel.Student()
                    student.set_login(row[0])
                    student.set_name(row[1])
                    students += [student]
    except IOError:
        logger.print_error("cannot open students list " + 
                           common.get_config().get_students_csv_file_path())
        return None
    if len(students) < 1:
        logger.print_error("none students has been found")
    else:
        logger.print_msg("students list successfully loaded")
    return students


def print_help():
    """Print program usage help."""
    print(__doc__)


def main():
    """
    Main function
    
    1) parse program options
    2) init logger module
    3) parse students list
    4) parse tasks
    5) send data to print or web interface module
    """
    # parse program params and XML configuration file
    (state, configuration) = parse_options()
    # print help
    if state == 1:
        print_help()
        return common.EXIT_OK
    # something got wrong
    elif state != 0 or configuration == None:
        return common.EXIT_ERROR_OPTIONS
    # config ok
    else:
        common.set_config(configuration)
    # init logger module
    state = logger.init()
    # something got wrong
    if state != 0:
        return common.EXIT_ERROR_LOGGER
    logger.print_msg("isjtests started")
    # parse students list
    students = read_students_list()
    # something got wrong
    if students == None or len(students) == 0:
        return common.EXIT_ERROR_STUDENTS
    # parse tasks
    tasks = taskparser.parse_all_tasks()
    # something got wrong
    if tasks == None or len(tasks) == 0:
        return common.EXIT_ERROR_TASKS
    # send data to interface module, wait for finish
    if configuration.get_mode() == "print":
        status = printface.serve(students, tasks)
    elif configuration.get_mode() == "web":
        status = webface.serve(students, tasks)
    # something got wrong
    if status != 0:
        return common.EXIT_ERROR_INTERFACE
    # everything ok
    return 0


if __name__ == "__main__":
    sys.exit(main())
    
    
    