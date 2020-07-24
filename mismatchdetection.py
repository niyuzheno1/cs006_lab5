# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import re

def delen(li):
    tmp = []
    for x in li:
        if isinstance(x,str):
            if re.sub(r"[\n\t\s]*", "", x) != "":
                tmp.append(x)
        else:
            tmp.append(x)
    return len(tmp)

#studentanswer : st1
#solution : st2
def mismatches(x,y,st1, st2): 
    if delen(st1[x][y]) != delen(st2[x][y]):
        return True
    else:
        for i in range(0,delen(st1[x][y])):
            if isinstance(st1[x][y][i],str):
                if st1[x][y][i].lower() != st2[x][y][i].lower() and  (re.sub(r"[\n\t\s]*", "", st1[x][y][i]) != "" or re.sub(r"[\n\t\s]*", "", st2[x][y][i]) != ""):
                    return True
            elif st1[x][y][i] != st2[x][y][i]:
                return True
    return False

def existence(x,y,z):
    if not(x in z):
        return True
    elif not (y in z[x]):
        return True
    return False

def finds(x,y):
    for u in x:
        if y in u: 
            return True
    return False