#!/usr/bin/env python3
r"""
Task generates various of choice task with regexp in question and strings in
answers. Tests {x}, (xxx), (?:xxx), \x knowledge.
"""

class RegexpTask(datamodel.DynamicTask):
    def __init__(self):
        super().__init__()
        self.fixed_params_range = [9, 9, 9, 9, 9, 9]
        self.params_range = [3, 3, 3, 3, 3, 2, 2, 2, 2, 3]
        self.answers_num = 6
        
    def generate_re_string(self, params, fixed_params):
        # generate RexExp according params
        regexp = "^"
        regexp += "("
        if params[5] != 0:
            regexp += "?:"
        regexp += "("
        if params[6] != 0:
            regexp += "?:"
        regexp += str(fixed_params[0]+1)
        regexp += str(fixed_params[1]+1)
        regexp += "){"
        regexp += str(params[0]+1)
        regexp += "}("
        if params[7] != 0:
            regexp += "?:"
        regexp += "("
        if params[8] != 0:
            regexp += "?:"
        regexp += str(fixed_params[2]+1)
        regexp += str(fixed_params[3]+1)
        regexp += "){"
        regexp += str(params[1]+1)
        regexp += "}("
        regexp += str(fixed_params[4]+1)
        regexp += str(fixed_params[5]+1)
        regexp += "){"
        regexp += str(params[2]+1)
        regexp += "}){"
        regexp += str(params[3]+1)
        regexp += "}){"
        regexp += str(params[4]+1)
        regexp += "}\\"
        regexp += str(params[9])
        regexp += "$"
        # generate string
        groups = [None]*5
        groups[1] = str(fixed_params[0]+1) + str(fixed_params[1]+1)
        groups[3] = str(fixed_params[2]+1) + str(fixed_params[3]+1)
        groups[4] = str(fixed_params[4]+1) + str(fixed_params[5]+1)
        groups[2] = groups[3] * (params[1] + 1) + groups[4] * (params[2] + 1)
        groups[0] = groups[1] * (params[0] + 1) + groups[2] * (params[3] + 1)
        string = groups[0] * (params[4] + 1)
        groups_remember = []
        for i in range(4):
            if params[i+5] == 0:
                groups_remember.append(groups[i])
        groups_remember.append(groups[4])
        string += groups_remember[params[9]-1]
        return (regexp, string)
        
    def generate(self):
        from random import randrange
        # init params by random numbers
        params = []
        fixed_params = []
        for r in self.params_range:
            params += [randrange(r)]
        params[9] += 3
        params[9] = min(params[9], 5-sum(params[5:9]))
        for r in self.fixed_params_range:
            fixed_params += [randrange(r)]
        # create task
        task = datamodel.ChoiceTask()
        # get regexp and correct string
        (regexp, string) = self.generate_re_string(params, fixed_params)
        # set question
        task.set_question("Regulárnímu výyrazu: " + regexp + " odpovídá " + \
                          "řetězec:")
        # set correct answer
        answers = [(string, True)]
        # fill answers with similar strings
        while len(answers) < self.answers_num:
            answer_generated = False
            while not answer_generated:
                # try change one param... we need different, but similar string
                iparam = randrange(len(self.params_range))
                params[iparam] = randrange(self.params_range[iparam])
                if iparam == 9:
                    params[9] += 3
                params[9] = min(params[9], 5-sum(params[5:9]))
                (regexp, string) = self.generate_re_string(params,
                                                           fixed_params)
                # check if output differs from standing answers
                answer_generated = True
                for (answer, rest) in answers:
                    if answer == string:
                        answer_generated = False
                        break
                if answer_generated:
                    answers += [(string, False)]
        task.set_answers(answers)
        return task
        
task = RegexpTask()

