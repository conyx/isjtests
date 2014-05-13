#!/usr/bin/env python3
"""
Dynamic task generates choice tasks where is python2 code with iterator
class in the question and possible outputs of this code in answers. Student
must select correct program output.
"""

class IteratorTask(datamodel.ChoiceOutputDynamicTask):
    def __init__(self):
        super().__init__()
        self.params_range = [3, 3, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 3]
        self.answers_num = 6
        self.question = "Co vypíše následující program v Pythonu 2 na " + \
                        "standardní výstup?"
        
    def get_code_and_output(self, params):
        import subprocess
        # first generate code according params
        code = "class Houbogen:\n"
        code += "\tdef __init__(self, n):\n"
        code += "\t\tself.i = n + " + str(-(params[0]+3)) + "\n"
        code += "\t\tself.j = " + str(params[1]+3) + " - n\n"
        code += "\tdef __iter__(self):\n"
        code += "\t\treturn self\n"
        code += "\tdef next(self):\n"
        if params[2] != 0:
            code += "\t\tself.i += 1\n"
        if params[3] != 0 or params[2] == 0:
            code += "\t\tself.j -= 1\n"
        if params[4] == 0:
            code += "\t\tif self.i > self.j:\n"
        else:
            code += "\t\tif self.i >= self.j:\n"
        code += "\t\t\traise StopIteration()\n"
        if params[5] == 0:
            code += "\t\telif sum((self.i, self.j)) % 2 == 0:\n"
        elif params[5] == 1:
            code += "\t\telif sum((self.i, self.j)) % 2 == 1:\n"
        elif params[5] == 2:
            code += "\t\telif sum((self.i, self.j)) % 3 == 0:\n"
        elif params[5] == 3:
            code += "\t\telif sum((self.i, self.j)) % 3 == 1:\n"
        elif params[5] == 4:
            code += "\t\telif sum((self.i, self.j)) % 3 == 2:\n"
        if params[6] != 0:
            code += "\t\t\tself.i += 1\n"
        if params[7] != 0:
            code += "\t\t\tself.j -= 1\n"
        if params[8] == 0:
            code += "\t\t\treturn self.j - self.i\n"
        else:
            code += "\t\t\treturn self.i - self.j\n"
        code += "\t\telse:\n"
        if params[9] != 0:
            code += "\t\t\tself.i += 1\n"
        if params[10] != 0:
            code += "\t\t\tself.j -= 1\n"
        if params[11] == 0:
            code += "\t\t\treturn self.j - self.i\n"
        else:
            code += "\t\t\treturn self.i - self.j\n"
        if params[12] != 0:
            code += "n = 0\n"
        else:
            code += "n = 1\n"
        if params[13] == 0:
            code += "print sum(Houbogen(n))"
        elif params[13] == 1:
            code += "print max(Houbogen(n))"
        elif params[13] == 2:
            code += "print min(Houbogen(n)),"
        # now get stdout from this program
        python2_comm = common.get_config().get_intern_python2path()
        p = subprocess.Popen([python2_comm], stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate(code.encode("u8"))
        return (code, stdoutdata.decode("u8"))
        
        
task = IteratorTask()

