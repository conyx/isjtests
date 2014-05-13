#!/usr/bin/env python3
"""
This task is example of dynamic task, which generates program task about
matrix addition.
"""

class MatrixAddTask(datamodel.DynamicTask):
    def __init__(self):
        super().__init__()
        
    def generate(self):
        from random import randrange
        # generate language of the task
        language_str = ["Python 2", "Python 3", "Ruby"]
        language_id = ["python2", "python3", "ruby"]
        language = randrange(len(language_id))
        # generate M x N params (size of matrix)
        m = randrange(5, 11)
        n = randrange(5, 11)
        # generate content of the matrix A
        a_mat = []
        for i in range(m):
            row = []
            for j in range(n):
                row += [randrange(10)]
            a_mat += [row]
        # generate content of the matrix B
        b_mat = []
        for i in range(m):
            row = []
            for j in range(n):
                row += [randrange(10)]
            b_mat += [row]
        # add matrices
        c_mat = []
        for i in range(m):
            row = []
            for j in range(n):
                row += [a_mat[i][j] + b_mat[i][j]]
            c_mat += [row]
        # create task
        start = ""
        end = ""
        if common.get_config().get_mode() == "web":
            start = "<pre>"
            end = "</pre>"
        elif common.get_config().get_mode() == "print":
            start = "\n#BACKSLASH#texttt#LEFT_BRACE#"
            end = "#RIGHT_BRACE#\n"
        task = datamodel.ProgramTask()
        question = "Napište program v jazyce " + language_str[language] + \
                   " který sečte libovolně velké matice a vytiskne " + \
                   "výsledek na standardní výstup. Prvky matice jsou " + \
                   "odděleny mezerou. Matice na vstupu jsou od sebe " + \
                   "odděleny prázdným řádkem a mají stejnou velikost. " + \
                   "Příklad vstupu:" + start + "1 1\n2 2\n\n3 3\n4 4" + end + \
                   "Odpovídající výstup:" + start + "4 4\n6 6" + end
        task.set_question(question)
        task.set_language(language_id[language])
        #~ task.set_language("unknown")
        task.set_program_parts([(None, 0)])
        pinput = ""
        for row in a_mat:
            for i in range(len(row)):
                pinput += str(row[i])
                if i != len(row) - 1:
                    pinput += " "
            pinput += "\n"
        pinput += "\n"
        for row in b_mat:
            for i in range(len(row)):
                pinput += str(row[i])
                if i != len(row) - 1:
                    pinput += " "
            if row != b_mat[-1]:
                pinput += "\n"
        task.set_input(pinput)
        poutput = ""
        for row in c_mat:
            for i in range(len(row)):
                poutput += str(row[i])
                if i != len(row) - 1:
                    poutput += " "
            poutput += "\n"
        task.set_correct_output(poutput)
        # return created task
        return task
        
        
task = MatrixAddTask()

