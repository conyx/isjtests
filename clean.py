#!/usr/bin/env python3
"""
Removes recursivelly all __pycache__ folders and .pyc files from
working directory.
"""

import os
import os.path
import shutil

def clean_dir(path):
    dirs = os.listdir(path)
    for dir_ in dirs:
        dir_path = os.path.join(path, dir_)
        if os.path.isdir(dir_path):
            if dir_ == "__pycache__":
                shutil.rmtree(dir_path)
            else:
                clean_dir(dir_path)
        elif dir_.endswith(".pyc"):
            os.remove(dir_path)
            
    
if __name__ == "__main__":
    clean_dir(".")

