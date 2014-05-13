#!/usr/bin/env python3
"""
Data model for ISJ tests.
Task data representation.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import random

import common

class Task:
    def __init__(self):
        self.set_type(None)
        self.set_question(None)
        self.set_id(None)
        self.set_max_points(None)
        self.set_filepath(None)
    
    def set_id(self, id_):
        self._id = id_
        
    def get_id(self):
        return self._id
    
    def set_type(self, type_):
        self._type = type_
        
    def get_type(self):
        return self._type
        
    def set_question(self, question):
        self._question = question
        
    def get_question(self):
        return self._question
        
    def set_max_points(self, points):
        self._max_points = points
    
    def get_max_points(self):
        return self._max_points
        
    def set_filepath(self, path):
        self._filepath = path
        
    def get_filepath(self):
        return self._filepath
        
        
class ChoiceTask(Task):
    def __init__(self):
        super().__init__()
        self.set_type("choice")
        self.set_answers([])
        self.set_student_answers([])
        
    def set_answers(self, answers):
        self._answers = answers
        
    def get_answers(self):
        return self._answers
        
    def set_student_answers(self, answers):
        self._student_answers = answers
        
    def get_student_answers(self):
        return self._student_answers
            
    def shuffle_answers(self):
        random.shuffle(self._answers)
        
    def check(self):
        if (len(self.get_answers()) >= 2 and self.get_question() != None and
            self.get_type() != None and self.get_id() != None):
            true_answers = 0
            for (ans, ans_bool) in self.get_answers():
                if ans_bool:
                    true_answers += 1
            if true_answers == 1:
                return True
        else:
            return False
        
    
class MultiChoiceTask(Task):
    def __init__(self):
        super().__init__()
        self.set_type("multichoice")
        self.set_answers([])
        self.set_student_answers([])
        
    def set_answers(self, answers):
        self._answers = answers
        
    def get_answers(self):
        return self._answers
        
    def set_student_answers(self, answers):
        self._student_answers = answers
        
    def get_student_answers(self):
        return self._student_answers
            
    def shuffle_answers(self):
        random.shuffle(self._answers)
        
    def check(self):
        if (len(self.get_answers()) >= 2 and self.get_question() != None and
            self.get_type() != None and self.get_id() != None):
            return True
        else:
            return False
        

class FulltextTask(Task):
    def __init__(self):
        super().__init__()
        self.set_type("fulltext")
        self.set_answers([])
        self.set_prefill(None)
        self.set_help(None)
    
    def set_answers(self, answers):
        self._answers = answers
        
    def get_answers(self):
        return self._answers
    
    def set_prefill(self, prefill):
        self._prefill = prefill
        
    def get_prefill(self):
        return self._prefill
        
    def set_help(self, help_):
        self._help = help_
        
    def get_help(self):
        return self._help
    
    def check(self):
        if (self.get_question() != None and self.get_type() != None and
            self.get_id() != None and self.get_answers() != None and
            len(self.get_answers()) > 0):
            for answer, coef in self.get_answers():
                if coef > 1 or coef <= 0:
                    return False
            return True
        else:
            return False

class ProgramTask(Task):
    def __init__(self):
        super().__init__()
        self.set_type("program")
        self.set_language(None)
        self.set_program_parts([])
        self.set_correct_output(None)
        self.set_input(None)
        self.set_prefill(None)
        self.set_help(None)
        
    def set_language(self, lang):
        self._language = lang
        
    def get_language(self):
        return self._language
        
    def set_program_parts(self, parts):
        self._program_parts = parts
    
    def get_program_parts(self):
        return self._program_parts
        
    def set_correct_output(self, output):
        self._correct_output = output
        
    def get_correct_output(self):
        return self._correct_output
        
    def set_input(self, input_):
        self._input = input_
        
    def get_input(self):
        return self._input
        
    def set_prefill(self, prefill):
        self._prefill = prefill
        
    def get_prefill(self):
        return self._prefill
        
    def set_help(self, help_):
        self._help = help_
        
    def get_help(self):
        return self._help
        
    def check(self):
        if (self.get_question() != None and self.get_type() != None and
            self.get_id() != None and (self.get_language() == "python2" or
            self.get_language() == "python3" or
            self.get_language() == "ruby" or
            self.get_language() == "unknown") and
            self.get_correct_output() != None):
            num_unset_parts = 0
            for program_part in self.get_program_parts():
                if not isinstance(program_part, tuple):
                    return False
                if program_part[0] == None:
                    num_unset_parts += 1
            if num_unset_parts == 1:
                return True
        else:
            return False
        
        
class DynamicTask(Task):
    def __init__(self):
        super().__init__()
        self.set_type("dynamic")
        
    def generate(self):
        return None
    
    def check(self):
        return True


class ChoiceOutputDynamicTask(DynamicTask):
    def __init__(self):
        super().__init__()
        # init values must be redefined in child class
        self.params_range = [2, 2]
        self.answers_num = 4
        self.question = "Question?"
        
    def generate(self):
        params = []
        # init params by random numbers
        for r in self.params_range:
            params += [random.randrange(r)]
        # generate python code and correct output
        (code, output) = self.get_code_and_output(params)
        task = ChoiceTask()
        # create question
        question = code.strip()
        if common.get_config().get_mode() == "web":
            question = "<pre>" + question + "</pre>"
        elif common.get_config().get_mode() == "print":
            question = "\n#BACKSLASH#texttt#LEFT_BRACE#" + question + \
                       "#RIGHT_BRACE#"
        question = self.question + question
        task.set_question(question)
        # create answers
        answers = [(output.strip(), True)]
        while len(answers) < self.answers_num:
            answer_generated = False
            while not answer_generated:
                iparam = random.randrange(len(self.params_range))
                # try change one param... we need different, but similar output
                params[iparam] = random.randrange(self.params_range[iparam])
                (code, output) = self.get_code_and_output(params)
                # check if output differs from standing answers
                answer_generated = True
                for (answer, rest) in answers:
                    if answer == output.strip():
                        answer_generated = False
                        break
                if answer_generated:
                    answers += [(output.strip(), False)]
        task.set_answers(answers)
        return task
        
    def get_code_and_output(self, params):
        """This method must be redefined in child class"""
        return ("", "")
   
