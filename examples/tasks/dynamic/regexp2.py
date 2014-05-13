#!/usr/bin/env python3
r"""
Task generates various of choice task with regexp in question and strings in
answers. Tests \S|\s, \D|\d, \W|\w, [^xxx], (xxx|yyy) and [x-y] knowledge.
"""

class RegexpTask(datamodel.DynamicTask):
    def __init__(self):
        super().__init__()
        self.params_range = [2, 9, 2, 2, 2, 2, 9, 9, 2, 9, 4, 5]
        self.parts = 7
        self.answers_num = 8
        
    def generate_re_string(self, params, positions):
        from random import randrange
        import string
        # generate RexExp according params
        regexp_list = []
        if params[0] == 0:
            regexp_list.append(r"[^" + str(params[1] + 1) + "]")
        else:
            regexp_list.append(r"[.^" + str(params[1] + 1) + "]")
        if params[2] == 0:
            regexp_list.append(r"\s")
        else:
            regexp_list.append(r"\S")
        if params[3] == 0:
            regexp_list.append(r"\d")
        else:
            regexp_list.append(r"\D")
        if params[4] == 0:
            regexp_list.append(r"\w")
        else:
            regexp_list.append(r"\W")
        if params[5] == 0:
            regexp_list.append(r"[^" + str(params[6] + 1) + "]")
        else:
            regexp_list.append(r"[$^" + str(params[6] + 1) + "]")
        if params[8] == 0:
            regexp_list.append(r"(" + str(params[7]+1) + str(params[9]+1) + \
                               ")")
        else:
            regexp_list.append(r"(" + str(params[7]+1) + "|" + \
                               str(params[9]+1) + ")")
        regexp_list.append("[" + str(params[10]+1) + "-" + str(params[11]+5) + "]")
        regexp = "^"
        for p in positions:
            regexp += regexp_list[p]
        regexp += "$"
        # generate string
        string_list = []
        if params[0] == 0:
            chars = [str(num+1) for num in range(9) if num != params[1]]
            string_list.append(chars[randrange(len(chars))])
        else:
            string_list.append((".^" + str(params[1]+1))[randrange(3)])
        if params[2] == 0:
            string_list.append(" ")
        else:
            string_list.append(string.hexdigits[
                                    randrange(len(string.hexdigits))])
        if params[3] == 0:
            string_list.append(string.digits[randrange(len(string.digits))])
        else:
            string_list.append(string.ascii_letters[
                                    randrange(len(string.ascii_letters))])
        if params[4] == 0:
            string_list.append(string.digits[randrange(len(string.digits))])
        else:
            string_list.append("$")
        if params[5] == 0:
            chars = [str(num+1) for num in range(9) if num != params[1]]
            string_list.append(chars[randrange(len(chars))])
        else:
            string_list.append(("$^" + str(params[6]+1))[randrange(3)])
        if params[8] == 0:
            string_list.append(str(params[7]+1) + str(params[9]+1))
        else:
            string_list.append((str(params[7]+1),
                                str(params[9]+1))[randrange(2)])
        string_list.append(str(randrange(params[10] + 1, params[11] + 6)))
        string_ = ""
        for p in positions:
            string_ += string_list[p]
        return (regexp, string_)
        
        
    def generate(self):
        import random
        import re
        # init params by random numbers
        params = []
        for r in self.params_range:
            params += [random.randrange(r)]
        positions = [i for i in range(self.parts)]
        random.shuffle(positions)
        # whitespace couldnt be at first place (part 1 is whitespace \s)
        while positions[0] == 1:
            random.shuffle(positions)
        # create task
        task = datamodel.ChoiceTask()
        # get regexp and correct string
        (regexp, string) = self.generate_re_string(params, positions)
        # set question
        task.set_question("Regulárnímu výyrazu: " + regexp + " odpovídá " + \
                          "řetězec:")
        # set correct answer
        answers = [(string, True)]
        # fill answers with similar strings
        regexp = re.compile(regexp)
        while len(answers) < self.answers_num:
            answer_generated = False
            while not answer_generated:
                # try change one param... we need different, but similar string
                iparam = random.randrange(len(self.params_range))
                params[iparam] = random.randrange(self.params_range[iparam])
                (rest, string) = self.generate_re_string(params, positions)
                # check if output differs from standing answers
                answer_generated = True
                for (answer, rest) in answers:
                    if answer == string or re.match(regexp, string) != None:
                        answer_generated = False
                        break
                if answer_generated:
                    answers += [(string, False)]
        task.set_answers(answers)
        return task
        
        
task = RegexpTask()

