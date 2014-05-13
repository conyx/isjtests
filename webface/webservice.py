#!/usr/bin/env python3
"""
Main module for web service interface.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import http.server
import re
import socket
import urllib.parse
import hashlib
import os.path
import random
import sys

import datamodel
import logger
import util
import common
from .evaluator import evaluate

# global list with tuples (tasks, number)
# tasks is list with datamodel.Task objects
# number is number of tasks per student from this list
_tasks = []
# global list with tuple (student, tasks, status, sid)
# student is datamodel.Student object
# tasks is list with datamodel.Task objects
# status: 0 means student has not got his tasks
#         1 means student got his tasks
#         2 means student sent answers
# sid is session id for this student
_students = []
# XHTML templates
_templates = ()
# global error status
_status = 0


def load_templates():
    """
    Load XHTML templates for http responses.
    """
    module_path = os.path.dirname(__file__)
    template_index_path = os.path.join(module_path,
                                      "templates",
                                      "index.xhtml")
    template_test_path = os.path.join(module_path,
                                      "templates",
                                      "test.xhtml")
    template_test_results_path = os.path.join(module_path,
                                              "templates",
                                              "test_results.xhtml")
    template_403_path = os.path.join(module_path,
                                     "templates",
                                     "403.xhtml")
    template_404_path = os.path.join(module_path,
                                     "templates",
                                     "404.xhtml")
    with open(template_index_path, encoding="u8") as f:
        template_index = f.read()
    with open(template_test_path, encoding="u8") as f:
        template_test = f.read()
    with open(template_test_results_path, encoding="u8") as f:
        template_test_results = f.read()
    with open(template_403_path, encoding="u8") as f:
        template_403 = f.read()
    with open(template_404_path, encoding="u8") as f:
        template_404 = f.read()
    return(template_index, template_test, template_test_results, template_403,
           template_404)
    

def serve(students, tasks):
    """
    Assign tasks to students (if anonymous mode is off) and start web server.
    """
    # init global variables
    global _tasks
    global _students
    global _templates
    global _status
    _tasks = tasks
    _templates = load_templates()
    # assign tasks to students
    if not common.get_config().is_anonymous():
        for student in students:
            logger.print_msg("assigning tasks for student: " + \
                             student.get_login())
            tasks_for_student = util.random_assign(tasks)
            # generate random session id
            m = hashlib.md5()
            m.update((student.get_name() + \
                      student.get_login() + \
                      str(random.randrange(0xFFFFFFFFFFFFFFFF))).encode("u8"))
            sid = m.hexdigest()
            _students += [(student, tasks_for_student, 0, sid)]
    # start web service
    try:
        serve_forever()
    except KeyboardInterrupt:
        _status = 0
    return _status
    
    
def serve_forever():
    """
    Start web server on user specified port
    """
    server_address = ('', common.get_config().get_webserver_port())
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
    logger.print_msg("starting web service on port " + str(server_address[1]))
    print_students_info()
    httpd.serve_forever()
    
    
def print_students_info():
    statuses = [0, 0, 0]
    for (*rest, status, sid) in _students:
        statuses[status] += 1
    logger.print_msg(str(statuses[2]) + " students answered, " + \
                     str(statuses[1]) + " students answering, " + \
                     str(statuses[0]) + " students not logged in")
    
    
class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def handle(self):
        try:
            super(HTTPRequestHandler, self).handle()
        except socket.error as e:
            logger.print_warning("socket error while comunicating with " +
                                 self.client_address[0] + " " + str(e))
        
    def do_GET(self):
        # somebody is trying to get index page, send him login form
        if self.path == "/":
            response = self.prepare_index_response()
            self.send_200(response)
        # unknown request
        else:
            self.send_404()
        
    def do_POST(self):
        # somebody is trying to get test, check password and send him test
        if self.path == "/test":
            cl_header = self.headers.get("Content-Length")
            if cl_header != None:
                try:
                    data = self.rfile.read(int(cl_header)).decode("ascii")
                    data = urllib.parse.parse_qs(data)
                    # check login and password
                    if self.check_login(data) and self.check_password(data):
                        # prepare and send test form
                        response = self.prepare_test_response(data)
                        self.send_200(response)
                        print_students_info()
                    else:
                        self.send_403()
                # incorrect form data
                except UnicodeDecodeError:
                    self.send_403()
            else:
                self.send_403()
        # somebody is trying to send test answers and get results
        elif self.path == "/testresults":
            cl_header = self.headers.get("Content-Length")
            if cl_header != None:
                try:
                    data = self.rfile.read(int(cl_header)).decode("ascii")
                    data = urllib.parse.parse_qs(data)
                    points_list = self.evaluate_answers(data)
                    if points_list != None:
                        response = self.prepare_results_response(data,
                                                                 points_list)
                        self.send_200(response)
                        print_students_info()
                    else:
                        self.send_403()
                # incorrect form data
                except UnicodeDecodeError:
                    self.send_403()
            else:
                self.send_403()
        # unknown request
        else:
            self.send_404()
        
    def send_200(self, data):
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(data)
        
    def send_403(self):
        response = self.prepare_403_response()
        self.send_response(403)
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(response)        
        
    def send_404(self):
        response = self.prepare_404_response()
        self.send_response(404)
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(response)
        
    def log_message(self, format_, *msg):
        logger.print_msg("request " +
                         str(self.client_address[0]) +
                         " " +
                         str(msg[0]))
                         
    def prepare_index_response(self):
        resp = re.sub(r"#replacepass#([^#]+)#replacepass#",
                      r'\1<input type="password" name="password" />',
                      _templates[0])
        if common.get_config().is_anonymous():
            resp = re.sub("#replacelogin#([^#]+)#replacelogin#",
                          '',
                          resp)
        else:
           resp = re.sub(r"#replacelogin#([^#]+)#replacelogin#",
                         r'\1<input type="text" name="login" />',
                         resp)
        return resp.encode("u8")
        
    def prepare_test_response(self, formdata):
        global _students
        # get tasks and student's session id
        if common.get_config().is_anonymous():
            # create new anonymous student
            student = datamodel.Student()
            login = "anonymous_" + '{:0>4}'.format(str(len(_students)))
            student.set_login(login)
            logger.print_msg("assigning tasks for student: " + login)
            tasks = util.random_assign(_tasks)
            # generate random session id
            m = hashlib.md5()
            m.update((login + \
                      str(random.randrange(0xFFFFFFFFFFFFFFFF))).encode("u8"))
            sid = m.hexdigest()
            _students += [(student, tasks, 1, sid)]
        else:
            login = formdata["login"][0]
            i = 0
            for (student_, tasks_, status, sid_) in _students:
                if student_.get_login() == login:
                    student = student_
                    tasks = tasks_
                    sid = sid_
                    break
                i += 1
            # set correct status (1 = test already requested)
            _students[i] = (student, tasks, 1, sid)
        # create xhtml form
        inputsdata = ""
        if not common.get_config().is_anonymous():
            inputsdata += "<i>" + student.get_login() + ", " + \
                          student.get_name() + "</i><br/><br/>"
        i = 0
        for task in tasks:
            inputsdata += self.create_inputs(task, i)
            i += 1
        inputsdata += '<input type="hidden" value="' + sid + '" name="' + \
                      'sid"/>'
        # return created form
        resp = _templates[1].replace(r"#replaceinputs#", inputsdata)
        return resp.encode("u8")
        
    def create_inputs(self, task, num):
        """
        Create from task HTML form inputs.
        """
        inputsdata = ""
        # question
        question = task.get_question().replace("\n", "<br/>")
        question = question.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        inputsdata += '<span style="font-size: larger">' + question + "<br/>" \
                      "[" + str(task.get_max_points()) + " points]" + \
                      "</span><br/>"
        # radio buttons
        if task.get_type() == "choice":
            i = 0
            for (answer, iscorrect) in task.get_answers():
                inputsdata += "<input type=\"radio\" name=\"" + "a_" + \
                              str(num) + '"' + " value=\"" + str(i) + \
                              '" /> ' + answer + "<br/>"
                i += 1
        # checkboxes
        elif task.get_type() == "multichoice":
            i = 0
            for (answer, iscorrect) in task.get_answers():
                inputsdata += "<input type=\"checkbox\" name=\"" + "a_" + \
                              str(num) + '"' + " value=\"" + str(i) + \
                              '" /> ' + answer + "<br/>"
                i += 1
        # text areas
        else:
            if task.get_prefill() != None:
                prefill = task.get_prefill()
            else:
                prefill = ""
            inputsdata += "<textarea name=\"" + "a_" + str(num) + \
                          "\" cols=80 rows=15 wrap=physical>" + prefill + \
                          "</textarea><br/>" 
        inputsdata += "<br/><hr/><br/>"
        return inputsdata
        
    def prepare_results_response(self, data, points_list):
        # select correct student
        sid = data["sid"][0]
        for (student_, tasks_, status_, sid_) in _students:
            if sid == sid_:
                student = student_
                tasks = tasks_
                break
        resultsdata = "#sumpoints#&nbsp;&nbsp;&nbsp;<i>"
        if not common.get_config().is_anonymous():
            resultsdata += student.get_login() + ", " + student.get_name()
        else:
            resultsdata += "anonym"
        resultsdata += "</i><br/><br/>"
        # insert questions and points
        i = 0
        sumpoints = sum(points_list)
        summaxpoints = 0
        for task in tasks:
            question = task.get_question().replace("\n", "<br/>")
            resultsdata += '<span style="font-size: larger">' + question + \
                           "</span><br/>"
            maxpoints = task.get_max_points()
            points = points_list[i]
            summaxpoints += maxpoints
            if points <= 0:
                color = "red"
            elif points == maxpoints:
                color = "green"
            else:
                color = "orange"
            resultsdata += '<span style="color: ' + color + '">' + "[" + \
                           str(round(points, 2)) + "/" + str(maxpoints) + \
                           "]" + "</span>"
            # add self learning helps
            if common.get_config().is_self_learning():
                # add help string
                if ((task.get_type() == "program" or
                     task.get_type() == "fulltext") and
                     task.get_help() != None and
                     points < maxpoints):
                    resultsdata += "<div><i>"
                    resultsdata += task.get_help()
                    resultsdata += "</i></div>"
                # add correct and bad answers
                elif (task.get_type() == "choice" or
                      task.get_type() == "multichoice"):
                    resultsdata += "<br/>"
                    resultsdata += self.create_colored_answers(task)
            resultsdata += "<br/><hr/><br/>"
            i += 1
        # insert total number of points
        if sumpoints == 0:
            color = "red"
        elif sumpoints == summaxpoints:
            color = "green"
        else:
            color = "orange"
        totalpoints = '<span style="color: ' + color + '">' + "[" + \
                      str(round(sumpoints, 2)) + "/" + str(summaxpoints) + \
                      "]" + "</span>"
        resultsdata = resultsdata.replace("#sumpoints#", totalpoints)
        # return created form
        resp = _templates[2].replace(r"#replaceresults#", resultsdata)
        return resp.encode("u8")
        
    def create_colored_answers(self, task):
        answers = ""
        i = 0
        for answer, is_true in task.get_answers():
            if is_true:
                color = "green"
            else:
                color = "red"
            answers += '<span style="color: ' + color + '">' + answer + \
                       "</span>"
            if i in task.get_student_answers():
                answers += "&nbsp;&lt;&lt;&lt;"
            answers += "<br/>"
            i += 1
        return answers
        
    def prepare_403_response(self):
        return _templates[3].encode("u8")
        
    def prepare_404_response(self):
        return _templates[4].encode("u8")
        
    def check_password(self, formdata):
        """Return True is there is a correct password in form data"""
        config = common.get_config()
        try:
            if formdata["password"][0] == config.get_webserver_pass():
                return True
            else:
                return False
        except (KeyError, IndexError):
            return False

    def check_login(self, formdata):
        """
        Return True is there is a student with given login and status 0 or 1
        In anonymous mode this is always true.
        """
        if common.get_config().is_anonymous():
            return True
        try:
            login = formdata["login"][0]
            for (student, tasks, status, sid) in _students:
                if student.get_login() == login:
                    if status < 2:
                        return True
                    else:
                        return False
            return False
        except (KeyError, IndexError):
            return False

    def evaluate_answers(self, formdata):
        """
        Evaluate student's answers and return list with points. Also set a new
        stusent's status (2).
        If something get wrong, return None.
        """
        # find a student by session id
        try:
            req_sid = formdata["sid"][0]
        except KeyError:
            return None
        i = 0
        student = None
        for (student_, tasks_, status_, sid_) in _students:
            if sid_ == req_sid and status_ == 1:
                student = student_
                tasks = tasks_
                break
            i += 1
        # student not found
        if student == None:
            return None
        # set a new user's status (student answered)
        _students[i] = (student, tasks, 2, req_sid)
        # evaluate points
        return evaluate(student, tasks, formdata)
        
    def all_students_answered(self):
        """
        Return True if all students answered.
        """
        for (*rest, status, sid) in _students:
            if status == 0 or status == 1:
                return False
        return True
        

