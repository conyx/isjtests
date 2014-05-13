#!/usr/bin/env python3
"""
Dynamic task generates choice tasks where is ruby code in the question and
possible outputs of this code in answers. Student must select correct program
output.
"""

class RubyTask(datamodel.DynamicTask):
    def __init__(self):
        super().__init__()
        self.params_range = [3, 3, 3, 4, 4, 4, 4, 2, 3, 2, 2, 2, 3, 2, 2, 2]
        self.answers_num = 6
        self.question = "Co vypíše následující program v Ruby na " + \
                        "standardní výstup?"
        
    def get_code_and_output(self, params):
        import subprocess
        # first generate code according params
        code = ""
        code += "x = " + str(params[0]) + "\n"
        code += "z = " + str(params[1]) + "\n"
        code += "n = " + str(params[2]) + "\n"
        code += "a = [" + str(params[3]+1) + "," + str(params[4]+1) + "," + \
                str(params[5]+1) + "," + str(params[6]+1) + "]\n"
        if params[7] == 0:
            code += "(n.." + str(params[8] + 5) + ").each{|y| z += x += y}\n"
        else:
            code += "(n..." + str(params[8] + 5) + ").each{|y| z += x += y}\n"
        if params[9] != 0:
            code += "x, z = z, x\n"
        if params[10] == 0:
            code += "x.times {|i| x -= " + str(params[11] + 1) + "}\n"
        else:
            code += "x.times {|i| z -= " + str(params[11] + 1) + "}\n"
        a_str = ["last", "first", "length"]
        b_str = ["x", "z"]
        code += "n.upto(a." + a_str[params[12]] + ") {|y| " + \
                b_str[params[13]] + " -= y}\n"
        code += "n.upto(a." + a_str[params[14]] + "+a.first) {|y| " + \
                b_str[params[15]] + " -= y}\n"
        code += "print x.abs - z.abs"
        # now get stdout from this program
        ruby_comm = common.get_config().get_intern_ruby_path()
        p = subprocess.Popen([ruby_comm], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate(code.encode("u8"))
        return (code, stdoutdata.decode("u8"))
    
    def generate(self):
        import random
        params = []
        # init params by random numbers
        for r in self.params_range:
            params += [random.randrange(r)]
        # generate python code and correct output
        (code, output) = self.get_code_and_output(params)
        task = datamodel.ChoiceTask()
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
        answers = [(output, True)]
        alt_params = params[:]
        # change ".." for "..." or vice versa
        alt_params[7] = 0 if alt_params[7] == 1 else 1
        # generate output
        (code, output) = self.get_code_and_output(alt_params)
        if output != answers[0][0]:
            answers += [(output, False)]
        # generate other similar outputs
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
                    if answer == output:
                        answer_generated = False
                        break
                if answer_generated:
                    answers += [(output, False)]
        task.set_answers(answers)
        return task


task = RubyTask()

