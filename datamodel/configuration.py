#!/usr/bin/env python3
"""
Data model for ISJ tests.
Configuration data representation.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

class Configuration:
    def __init__(self):
        self.set_mode("web")
        self.set_verbose(True)
        self.set_logging(False)
        self.set_logfile("isjtests.log")
        self.set_python2path("python")
        self.set_python3path("python3")
        self.set_ruby_path("ruby")
        self.set_intern_python2path("python")
        self.set_intern_python3path("python3")
        self.set_intern_ruby_path("ruby")
        self.set_output_path("output")
        self.set_students_csv_file_path("students.csv")
        self.set_tasks_paths([("tasks", 1, 10)])
        self.set_webserver_port(8866)
        self.set_webserver_pass("password")
        self.set_evaluator_strictness(0)
        self.set_evaluator_timeout(10)
        self.set_anonymous(False)
        self.set_self_learning(False)
        
        
    def set_mode(self, mode):
        self._mode = mode
        
    def get_mode(self):
        return self._mode
        
    def set_verbose(self, verbose):
        self._verbose = verbose
        
    def is_verbose(self):
        return self._verbose
        
    def set_logging(self, logging):
        self._logging = logging
        
    def is_logging(self):
        return self._logging
        
    def set_logfile(self, logfile_path):
        self._logfile = logfile_path
        
    def get_logfile(self):
        return self._logfile
        
    def set_python2path(self, path):
        self._python2path = path
        
    def get_python2path(self):
        return self._python2path
        
    def set_python3path(self, path):
        self._python3path = path
        
    def get_python3path(self):
        return self._python3path
        
    def set_ruby_path(self, path):
        self._ruby_path = path
        
    def get_ruby_path(self):
        return self._ruby_path
        
    def set_intern_python2path(self, path):
        self._intern_python2path = path
        
    def get_intern_python2path(self):
        return self._intern_python2path
        
    def set_intern_python3path(self, path):
        self._intern_python3path = path
        
    def get_intern_python3path(self):
        return self._intern_python3path
        
    def set_intern_ruby_path(self, path):
        self._intern_ruby_path = path
        
    def get_intern_ruby_path(self):
        return self._intern_ruby_path
        
    def set_output_path(self, path):
        self._output_path = path
        
    def get_output_path(self):
        return self._output_path
        
    def set_students_csv_file_path(self, path):
        self._students_csv_file_path = path
        
    def get_students_csv_file_path(self):
        return self._students_csv_file_path
        
    def set_tasks_paths(self, paths):
        self._tasks_paths = paths
        
    def get_tasks_paths(self):
        return self._tasks_paths
        
    def set_webserver_port(self, port):
        self._webserver_port = port
    
    def get_webserver_port(self):
        return self._webserver_port
        
    def set_webserver_pass(self, password):
        self._webserver_password = password
        
    def get_webserver_pass(self):
        return self._webserver_password
        
    def set_evaluator_strictness(self, strictness):
        self._strictness = strictness
        
    def get_evaluator_strictness(self):
        return self._strictness
        
    def set_evaluator_timeout(self, timeout):
        self._timeout = timeout
        
    def get_evaluator_timeout(self):
        return self._timeout
        
    def set_anonymous(self, anonymous):
        self._anonymous = anonymous
        
    def is_anonymous(self):
        return self._anonymous
        
    def set_self_learning(self, sl):
        self._self_learning = sl
        
    def is_self_learning(self):
        return self._self_learning
    
    