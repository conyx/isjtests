#!/usr/bin/env python3
"""
Utilities used by multiple modules for ISJ tests.

Author:
Tomas Bambas  xbamba01@stud.fit.vutbr.cz
"""


def latex_format(text):
    REPLACE_LIST = [
        ("\\", r"\textbackslash{}"),
        ("#BACKSLASH#", "\\"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("#LEFT_BRACE#", "{"),
        ("#RIGHT_BRACE#", "}"),
        ("\n", "\\\\\n"),
        ("\r\n", "\\\\\n"),
        ("_", r"\_{}"),
        ("|", r"\textbar{}"),
        ("<", r"\textless{}"),
        (">", r"\textgreater{}"),
        ("\t", r"\hspace*{0.6cm}"),
        ("/", r"\slash{}"),
        ("§", r"\S{}"),
        ("#", r"\#{}"),
        ("$", r"\${}"),
        ("%", r"\%{}"),
        ("&", r"\&{}"),
        ("~", r"\~{}"),
        ("^", r"\^{}"),
    ]
    for old, new in REPLACE_LIST:
        text = text.replace(old, new)
    return text
               
               