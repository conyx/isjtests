#!/usr/bin/env python3
"""
------------------------- WIS Importer for ISJ Tests --------------------------
Usage: ./wisimporter.py folder_with_input_files output_CSV_file

Description:
This script exports students points to CSV file in format:
xlogin00;POINTS
e.g.:
xbamba01;23,5
xjanda17;16,8
[The file in this format can be imported to WIS.]

First param must be path to folder with files named:
xlogin00_points.txt
Content of these files must be number of points in float literal format.

Second param must be name of the output CSV file.

Author:
Tomas Bambas xbamba01@stud.fit.vutbr.cz
"""

import os
import os.path
import re
import sys

if __name__ == "__main__":
    dir_path = sys.argv[1]
    pattern = re.compile(r"^(x\w{5}\d{2})_points\.txt$")
    files = os.listdir(dir_path)
    points_list = []
    # load logins and points
    for f_name in files:
        m = re.match(pattern, f_name)
        if (m != None):
            login = m.group(1)
            print("login: " + login)
            with open(os.path.join(dir_path, f_name), encoding="ascii") as f:
                points = float(f.read())
                print("points: " + str(points))
                points_list.append((login, points))
    # write CSV file
    with open(sys.argv[2], "w") as f:
        for login, points in points_list:
            print(login + ";" + str(points).replace(".", ","), file=f)
