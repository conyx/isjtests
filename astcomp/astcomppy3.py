#!/usr/bin/env python3
"""
------------------------- AST Comparator for Python3 --------------------------
USAGE:
./astcomppy3.py folder_with_program_input_files

DESCRIPTION:
This script serves as abstract syntax trees comparator of Python 3 programs.
First argument must be folder with program files generated by evaluator.
(id_login.python3, id_login.python2, id_login.ruby, id_login.unknown)
Program creates text files in this folder (id_ast_python3.txt) with groups of
students logins, which have the same syntax.

AUTHOR:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""

import ast
import sys
import re
import os.path

SEPARATOR = """
===============================================================================
""".strip()
SEPARATOR2 = """
###############################################################################
""".strip()


class CustomNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self._str_repr = ""
        
    def visit(self, node):
        self._str_repr += str(type(node)) + " children: " + \
                          str(len(node._fields)) + "\n"
        self.generic_visit(node)
        
    def __str__(self):
        return self._str_repr.strip()


if __name__ == "__main__":
    dir_path = sys.argv[1]
    pattern = re.compile(r"^(\w+)_(x\w{5}\d{2})\.(python3|unknown)$")
    files = os.listdir(dir_path)
    results = {}
    # load programs and compare AST
    print("loading programs for comparison...")
    for f_name in files:
        m = re.match(pattern, f_name)
        if (m != None):
            prog_id = m.group(1)
            login = m.group(2)
            print("id: " + prog_id + " login: " + login)
            # create key in results if not exist
            if prog_id not in results:
                results.update({prog_id: [["SYNTAX ERROR", []]]})
            # read program
            with open(os.path.join(dir_path, f_name), mode="rb") as f:
                source = f.read()
            # try to parse to AST
            try:
                tree = ast.parse(source)
                visitor = CustomNodeVisitor()
                visitor.visit(tree)
                match = False
                for ast_, logins in results[prog_id]:
                    if ast_ == str(visitor):
                        logins.append(login)
                        match = True
                        break
                if not match:
                    results[prog_id].append([str(visitor), [login]])
            # syntax error
            except SyntaxError:
                results[prog_id][0][1].append(login)
    # write comparison results
    print("writing results...")
    for prog_id in results:
        filename = prog_id + "_ast_python3.txt"
        print(filename)
        with open(os.path.join(sys.argv[1], filename), "w") as f:
            i = 1
            for ast_, logins in results[prog_id]:
                print(SEPARATOR2, file=f)
                print("GROUP " + str(i), file=f)
                print(SEPARATOR, file=f)
                print(ast_, file=f)
                print(SEPARATOR, file=f)
                print(logins, file=f)
                i += 1
                
