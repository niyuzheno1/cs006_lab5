# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.


import tinycss
from html.parser import HTMLParser
from html.entities import name2codepoint
import re
from PIL import Image
import mismatchdetection

def addtowait(wt, z):
    for x in z:
        tmp = {}
        for y in z[x]:
            tmp[y] = ""
        wt[x] = tmp
    return wt



def process(x):
    ret = {}
    for x in x.rules:
        fulstr  = ""
        tmp = {}
        for sl in x.selector:
            fulstr = fulstr + str(sl.value)
        for decl in x.declarations:
            tmp[decl.name] = []
            
            for y in decl.value:
                if isinstance(y,tinycss.token_data.FunctionToken):
                    for z in y.content:
                        if isinstance(z,tinycss.token_data.FunctionToken):
                            for z1 in z.content:
                                tmp[decl.name].append(str(z1.value))
                        else:
                            tmp[decl.name].append(str(z.value))
                else:
                    tmp[decl.name].append(y.value)
            
            
        ret[fulstr] = tmp
    return ret

def csscheckerbegin(cssstyle,cssstyle1):
    

    outputlog = ""


    cssparser = tinycss.make_parser()


    st1 = cssparser.parse_stylesheet(cssstyle1)
    studentanswer = process(st1)

    st = cssparser.parse_stylesheet(cssstyle)


    pointsoff = {}
    musthave = {}

    exempt = {}

    def computescores(attr1, attr2):
        tot = 0
        exempt['.topfooter']['color'] = attr1 
        exempt['.topfooter']['background-color'] = attr2 
        for x in exempt:
            for y in exempt[x]:
                if mismatchdetection.existence(x,y,studentanswer):
                    tot = tot + 1
                else:
                    miss = mismatchdetection.mismatches(x,y,studentanswer, exempt)
                    if miss:
                        tot = tot + 1
                    
        return tot

    solution = process(st)
    for xname in ["body", ".header"]:
        pointsoff[xname] = {}
        pointsoff[xname]["background-color"] = solution[xname]["background-color"]

    for xname in [".column"]:
        musthave[xname] = {}
        musthave[xname]["padding-left"] = solution[xname]["padding-left"]
        musthave[xname]["padding-right"] = solution[xname]["padding-right"]
        
    for xname in ["main"]:
        musthave[xname] = {}
        musthave[xname]["background-color"] = solution[xname]["background-color"]
        

    for xname in [".topfooter"]:
        exempt[xname] = {}
        exempt[xname]["background-color"] = exempt[xname]["color"] = 1

    for xname in ["body"]:
        pointsoff[xname]["background-image"] = solution[xname]["background-image"]

    waitingroom = {}


    waitingroom = addtowait(waitingroom, pointsoff)
    waitingroom = addtowait(waitingroom, musthave)
    waitingroom = addtowait(waitingroom, exempt)



    totalpts = 0
    extrasymbol = 0
    for x in studentanswer:
        for y in studentanswer[x]:
            if x in waitingroom and y in waitingroom[x]:
                continue
            if not(x in solution):
                outputlog += ("The selector {} declaration {} is extra (?) \n".format(x,y))
                extrasymbol = extrasymbol + 1
            elif not (y in solution[x]):
                outputlog += ("The selector {} declaration {} is extra (?) \n".format(x,y))
                extrasymbol = extrasymbol + 1
            else:
                res = mismatchdetection.mismatches(x,y,studentanswer,solution)
                if res == True:
                    outputlog += ("There is a mismatch for selector {} declaration {} as what is given in the Doc File (-1) \n".format(x,y))
                    totalpts = totalpts + 1

                    
    for x in solution:
        for y in solution[x]:
            if x in waitingroom and y in waitingroom[x]:
                continue
            if not(x in studentanswer):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
            elif not (y in studentanswer[x]):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
            

    for x in pointsoff:
        for y in pointsoff[x]:
            if not(x in studentanswer):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
            elif not (y in studentanswer[x]):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
            else:
                if len(studentanswer[x][y]) != len(solution[x][y]):
                    continue
                else:
                    bad = True
                    for i in range(0,len(studentanswer[x][y])):
                        if studentanswer[x][y][i] != solution[x][y][i]:
                            bad = False
                            break
                    if bad:
                        outputlog += ("The selector {} declaration {} in your css file matchs exactly to what is given in the Doc File. However, we are required to modify it (-1) \n".format(x,y))
                        totalpts = totalpts + 1

    for x in musthave:
        for y in musthave[x]:
            if not(x in studentanswer):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
            elif not (y in studentanswer[x]):
                outputlog += ("Missing css field for selector {} declaration {} (-1) \n".format(x,y))
                totalpts = totalpts + 1
    
    
    for x in musthave:
        for y in musthave[x]:
            if (x in studentanswer) and (y in studentanswer[x]):
                if y[0] == 'p':
                    if ( not isinstance(studentanswer[x][y][0], int) )or mismatchdetection.delen(studentanswer[x][y]) != 1:
                        outputlog += ("either the attribute of {} in {} is not well-formed. It should be *px. (-1) \n".format(y,x))
                        totalpts = totalpts + 1
                else:
                        if (mismatchdetection.delen(studentanswer[x][y]) != mismatchdetection.delen(solution[x][y]) or  studentanswer[x][y][-1] == '0.75') :
                            outputlog += ("either the attribute of background-color in main is not in rgba format or the last component of rgba value is 0.75 (-1)\n")
                            totalpts = totalpts + 1

    ptsoffA = 0
    ptsoffB = 0





    if '.header' in studentanswer:
        ptsoffA = computescores(studentanswer['.header']['color'], studentanswer['.header']['background-color'])
    else:
        ptsoffA = 2
    ptsoffB = computescores( solution['.topnav a']['color'], solution['.topnav']['background-color'])

    if min(ptsoffA,ptsoffB) > 0:
        outputlog += ("the style is matching neither the nav bar nor the header ({})\n".format(-min(ptsoffA,ptsoffB)))
    totalpts = totalpts + min(ptsoffA,ptsoffB)

    if 'body' in studentanswer and 'background-image' in studentanswer['body']:
        url = studentanswer['body']['background-image'][-1]
        try:
                img = Image.open(url)
        except:
                outputlog += ("image is not well formed (-1)\n")
                totalpts = totalpts + 1

    totalpts = 43 - totalpts
    if totalpts < 0:
        totalpts = 0

    
    if extrasymbol > 1:
        outputlog += ("discounting the number of extra symbols\n")
        if  extrasymbol < 3:
            outputlog += ("total scores in css_checker has been slashed 3 percent because the number of extra symbols is greater than 1 and less than 3\n")
            totalpts = totalpts * 0.97
        elif extrasymbol < 7:
            outputlog += ("total scores in css_checker has been slashed 5 percent because the number of extra symbols is greater than 4 and less than 7\n")
            totalpts = totalpts * 0.95
        else:
            outputlog += ("total scores in css_checker has been slashed 10 percent the number of extra symbols is greater than 6\n")
            totalpts = totalpts * 0.90
    return (totalpts,outputlog)

