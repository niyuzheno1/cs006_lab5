# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import glob, os, re
import autograder_main
directory = "C:\\Users\\zachn\\OneDrive\\Documents\\labs\\lab5"

os.chdir(directory)

text_file = open(directory + "\\result.txt", "w")

def strcmp(x,y):
    u = re.sub(r"[\n\t\s]*", "",x)
    u = u.lower()
    if (u == y):
        return True
    return False

def directory_find(root='.'):
    for path, dirs, files in os.walk(root):
        if ".c9" in path:
            continue
        for x in dirs:
            if strcmp(x,"lab5"):
                return os.path.join(path, x)
    return None

def findallfiles(x):
    for u in x:
        if re.search('.html', u).group(0) != "":
            return True
    return False

def directory_find2(root='.'):
    for path, dirs, files in os.walk(root):
        if findallfiles(files):
            return  os.path.join(path)
    return None           

currentlevel = next(os.walk('.'))[1] 
for x in currentlevel:
    try:
        df = directory_find(directory+ "\\{0}\\environment\\".format(x))
        bfl = False 
        if df is None:
            text_file.write(x)
            text_file.write("\n")
        else:
            os.chdir(df)
            df2 = directory_find2(df)
            if df2 is None:
                text_file.write(x)
                text_file.write("\n")
                continue
            os.chdir(df2)
            result = autograder_main.findallfiles()
            f = open("grades.txt", "w")
            f.write(result)
            f.close()
            bfl = True  
    except OSError as e:
        text_file.write(x)
        text_file.write("\n")
text_file.close()