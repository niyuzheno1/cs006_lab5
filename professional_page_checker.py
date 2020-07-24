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
import copy 
import mismatchdetection

class Findallh1h2tags(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

    def read(self, data):
        self.pm = {}
        self.pm['h1'] = {}
        self.pm['h2'] = {}
        self.pm['footer'] = {}
        self.pm['dt'] = {}
        self.name = ""
        self.data = []
        self.hgroup = False
        self.lasttagx = ""
        self.howmanyh1 = 0
        self.feed(data)
        
        return (self.pm,self.howmanyh1)
    def handle_starttag(self, tag, attrs):
        if tag in ['hgroup']:
            self.hgroup = True
        if tag in ["h1", "h2", 'footer']:
            self.lasttagx  = tag
        if tag == "h1":
            self.howmanyh1 = self.howmanyh1 + 1
        if tag in ['dt']:
            self.pm[self.lasttagx][self.name] = self.data
            self.data = []
            self.name = ""
            self.lasttagx = ""
            self.lasttagx = tag

        
    def handle_endtag(self, tag):
        if self.hgroup == True:
            if tag in ['h1', 'h2']:
                self.pm[self.lasttagx][self.name] = self.data
                self.data = []
                self.name = ""
                self.lasttagx = ""
        else:
            if tag in ['ul',  'footer', 'dl']:
                if self.lasttagx != "":
                    self.pm[self.lasttagx][self.name] = self.data
                self.data = []
                self.name = ""
                self.lasttagx = ""
        if tag in ['hgroup']:
            self.hgroup = False
        pass
    def handle_data(self, data):
        if len(self.lasttagx) != 0 and self.name == "":
            self.name = data
            if self.lasttagx == 'footer':
                self.name = 'waterprint'
        elif len(self.lasttagx) != 0 and self.name != "":
            self.data.append(data)
def fdtext(html):
    s = Findallh1h2tags()
    return s.read(html)

def conglomorate(xx):
    ans = {}
    for x in xx:
        tmp = {}
        for y in xx[x]:
            resultstr = ' '.join(xx[x][y])
            tmp[y] = re.sub(r"[\n\t\s]*", "", resultstr)
        ans[x] = tmp
    return ans 

def ppagecheckerbegin(html,html2):
   

    res, howmanyh1forone = fdtext(html)
    c1 = conglomorate(res)
    
    res2, howmanyh1fortwo = fdtext(html2)
    c2 = conglomorate(res2)
    outputlog = ""

    totalpts = 0

    extrasymbol = 0
    for x in c1:
        if x == 'h1':
            continue
        for y in c1[x]:
            if y == "Honors" or y == "Mobile:" or y == "Experience":
                continue
            if not(x in c2):
                outputlog += ("The html element {} with content {} is extra (?) \n".format(x,y))
                extrasymbol = extrasymbol + 1
            elif not (y in c2[x]):
                outputlog += ("The html element {} with content {} is extra (?) \n".format(x,y))
                extrasymbol = extrasymbol + 1
            elif (c1[x][y] == c2[x][y] and len(c1[x][y]) > 0):
                outputlog += ("The html element {} with content {} is unmodified (-1) \n".format(x,y))
                totalpts = totalpts + 1

    for x in c2:
        if x == 'h1':
            continue
        for y in c2[x]:
            if not(x in c1):
                outputlog += ("The html element {} with content {} is missing (-1) \n".format(x,y))
                totalpts = totalpts + 1
            elif not (y in c1[x]) and not (mismatchdetection.finds(c1[x],y)):
                outputlog += ("The html element {} with content {} is missing (-1) \n".format(x,y))
                totalpts = totalpts + 1

    if howmanyh1forone < 2:
        outputlog += ("There are less than 2 h1 present {} \n".format(2 - howmanyh1forone))
        totalpts = totalpts + 2 - howmanyh1forone
    ptoff = 0
    for x in c1['h1'].keys():
        if x in c2['h1']:
            if x == "CS006 Winter 2020":
                continue
            outputlog += ("One of the h1 elements is not properly formatted. (-1) \n")
            ptoff += 1
    # if ptoff == 0 and "CS006 Winter 2020" not in c1['h1']:
    #     outputlog += ("Missing header element with content CS006 Winter 2020 (-1) \n")
    #     ptoff = 1
    totalpts = totalpts + ptoff
    
    totalpts = 10 - totalpts
    if totalpts < 0:
        totalpts = 0
    return (totalpts, outputlog)
