#!/usr/bin/env python3
"""
Dynamic task generates choice tasks where is python3 code with generator
function in the question and possible outputs of this code in answers. Student
must select correct program output.
"""

class GeneratorTask(datamodel.ChoiceOutputDynamicTask):
    def __init__(self):
        super().__init__()
        self.params_range = [3, 3, 4, 2, 4, 3, 2, 4, 2, 3, 2, 4]
        self.answers_num = 6
        self.question = "Co vypíše následující program v Pythonu 3 na " + \
                        "standardní výstup (neuvažujte chybový výstup)?"

    def get_code_and_output(self, params):
        import subprocess
        # first generate code according params
        code = "def f(n):\n"
        if params[0] != 0:
            code += "\tn = " + str(params[0]+1) + "\n"
        code += "\tprint('fraz:', n, end=', ')\n"
        if params[1] != 0:
            code += "\tn += " + str(params[1]) + "\n"
        code += "\twhile n < " + str(params[2] + 5) + ":\n"
        code += "\t\tyield n\n"
        code += "\t\tn += " + str(params[3] + 1) + "\n"
        code += "\t\tprint('fdva:', n, end=', ')\n"
        code += "\tprint('ftri:', n, end=', ')\n"
        code += "n = " + str(params[4]) + "\n"
        code += "x = f(n)\n"
        if params[5] != 0:
            code += "n += " + str(params[5]) + "\n"
        if params[6] != 0:
            code += "x = f(n)\n"
        if params[7] == 0:
            code += "print('mraz:', n, end=', ')\n"
        else:
            code += "print('mraz:', next(x), end=', ')\n"
        if params[8] != 0:
            code += "next(x)\n"
        if params[9] == 0:
            code += "print('mdva:', n, end=', ')\n"
        else:
            code += "print('mdva:', next(x), end=', ')\n"
        if params[10] != 0:
            code += "next(x)\n"
        if params[11] == 0:
            code += "print('mtri:', n, end=', ')"
        else:
            code += "print('mtri:', next(x), end=', ')"
        # now get stdout from this program
        python3_comm = common.get_config().get_intern_python3path()
        p = subprocess.Popen([python3_comm], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate(code.encode("u8"))
        return (code, stdoutdata.decode("u8"))
        
        
task = GeneratorTask()

