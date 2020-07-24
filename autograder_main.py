# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import css_checker
import professional_page_checker
import indexpage_checker
import personalpage_checker
import academicpage_checker
import glob, os
absolutepathtosolution = "C:\\Users\\zachn\\OneDrive\\Documents\\GitHub\\document2\\notebook\\cs006_lab5\\solution\\"

def autograderm(fd,htmlpo, csspo):
    grades = 0
    outputdetails = ""
    outputdetails += "grading lab5(6)_style.css:\n"
    f = open(absolutepathtosolution+"lab5_style.css", "r")
    html = f.read()
    try:
        f = open(fd["lab5_style.css"], "r")
        try:
            html2 = f.read()
        except UnicodeDecodeError as e:
            f = open(fd["lab5_style.css"], "r", encoding="utf8")
            html2 = f.read()
    except OSError as e:
        html2 = ""
    ret = css_checker.csscheckerbegin(html,html2)
    outputdetails += "grades for lab5(6)_style.css:{}/64.5, notice that we times the final grades with 1.5\n".format(ret[0]*1.5)
    grades += ret[0]*1.5
    outputdetails += "details for this file's grading is below:\n"
    outputdetails += ret[1] + "\n"

    outputdetails += "grading professional.html:\n"
    try:
        f = open(fd["professional.html"], "r")
        html = f.read()
    except OSError as e:
        html = ""
    f = open(absolutepathtosolution + "professional.html", "r")
    html2 = f.read()
    ret = professional_page_checker.ppagecheckerbegin(html,html2)
    outputdetails += "details for this file's grading is below:\n"
    outputdetails += "grades for professional.html:{}/20, notice that we times the final grades with 2\n".format(ret[0]*2)
    grades += ret[0]*2
    outputdetails += ret[1] + "\n"

    outputdetails += "grading index.html:\n"
    try:
        f = open(fd["index.html"], "r")
        html = f.read()
    except OSError as e:
        html = ""
    f = open(absolutepathtosolution+"index.html", "r")
    html2 = f.read()
    ret = indexpage_checker.checkindex(html,html2)
    outputdetails += "details for this file's grading is below:\n"
    outputdetails += "grades for index.html:{}/5\n".format(ret[0])
    grades += ret[0]
    outputdetails += ret[1] + "\n"

    
    outputdetails += "grading academics.html:\n"
    try:
        f = open(fd["academics.html"], "r")
        try:
            html = f.read()
        except UnicodeDecodeError as e:
            f = open(fd["academics.html"], "r", encoding="utf8")
            html2 = f.read()
    except OSError as e:
        html = ""
    f = open(absolutepathtosolution + "academics.html", "r")
    html2 = f.read()
    ret = academicpage_checker.checkacademicpage(html,html2)
    outputdetails += "details for this file's grading is below:\n"
    outputdetails += "grades for academics.html:{}/3\n".format(ret[0])
    grades += ret[0]
    outputdetails += ret[1] + "\n"

    outputdetails += "grading personal.html:\n"
    try:
        f = open(fd["personal.html"], "r")
        try:
            html = f.read()
        except UnicodeDecodeError as e:
            f = open(fd["personal.html"], "r", encoding="utf8")
            html2 = f.read()
    except OSError as e:
        html = ""
    f = open(absolutepathtosolution + "personal.html", "r")
    html2 = f.read()
    ret = personalpage_checker.checkpersonal(html,html2)
    outputdetails += "details for this file's grading is below: \n"
    outputdetails += "grades for personal.html:{}/5\n".format(ret[0])
    grades += ret[0]
    outputdetails += ret[1] + "\n"

    outputtmp = 0
    outputdetails += "All HTML files exist and named correctly:\n"
    if htmlpo == False:
        outputtmp = 1.5
    outputdetails += "grades for this section: {}/1.5\n".format(outputtmp)
    grades += outputtmp

    outputtmp = 0
    outputdetails += "The CSS exist and named correctly (either lab5_style.css or lab6_style.css):\n"
    if csspo == False:
        outputtmp = 1
    outputdetails += "grades for this section: {}/1\n".format(outputtmp)
    grades += outputtmp
    outputdetails += "overallscores: {}/100\n".format(grades)
    return outputdetails

def findallfiles():
    allhtmlfile = { }
    allhtmlfile['academics.html'] = ""
    allhtmlfile['index.html'] = ""
    allhtmlfile['personal.html'] = ""
    allhtmlfile['professional.html'] = ""
    allcssfile = {}
    allcssfile["lab5_style.css"] = ""
    allfile = {}

    htmlpointsoff = False

    for file in glob.glob("*.html*"):
        for x in allhtmlfile:
            fn, ex = os.path.splitext(x)
            if fn in file.lower():
                allhtmlfile[x] = file
    for x in allhtmlfile:
        y = allhtmlfile[x]
        if x != y:
            htmlpointsoff = True

    for file in glob.glob("*.css"):
        for x in ["lab5_style","lab6_style"]:
            if x in file.lower():
                allcssfile["lab5_style.css"] = file 
    csspointsoff = False
    if allcssfile["lab5_style.css"] == "":
        csspointsoff = True
    for file in glob.glob("*.css"):
        allcssfile["lab5_style.css"] = file
    for i in allhtmlfile:
        allfile[i] = allhtmlfile[i]
    for i in allcssfile:
        allfile[i] = allcssfile[i]
    ou = autograderm(allfile,htmlpointsoff,csspointsoff)

    return ou

findallfiles()