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
        self.lasttigers = []
        self.lastnames = []
        self.feed(data)
        
        return self.pm
    def handle_starttag(self, tag, attrs):
        if tag in ['hgroup']:
            self.hgroup = True
        if tag in ["h1", "h2", 'footer']:
            self.lasttagx  = tag
            self.lasttigers.append(tag)
        if tag in ['dt']:
            self.pm[self.lasttagx][self.name] = self.data
            self.data = []
            self.name = ""
            self.lasttagx = ""
            self.lasttagx = tag
            self.lasttigers.append(tag)

        
    def handle_endtag(self, tag):
        if self.hgroup == True:
            if tag in ['h1', 'h2']:
                self.pm[self.lasttagx][self.name] = self.data
                self.data = []
                self.name = ""
                self.lasttagx = ""
        else:
            if tag in ['ul',  'p', 'ol', 'footer']:
                if not(len(self.lasttagx) == 0 and tag == 'footer'):
                    if self.lasttagx == "":
                        self.lasttagx = self.lasttigers[-1]
                        self.name = self.lastnames[-1]
                        self.pm[self.lasttagx][self.name] = self.pm[self.lasttagx][self.name] + self.data
                    else:
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
            self.lastnames.append(self.name)
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

def checkpersonal(html, html2):
    
    
    res = fdtext(html)
    c1 = conglomorate(res)
    outputlog = ""
    
    res2 = fdtext(html2)
    c2 = conglomorate(res2)

    totalpts = 0

    extrasymbol = 0
    for x in c1:
        for y in c1[x]:
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
        if x in ['h1']:
            continue
        for y in c2[x]:
            if not(x in c1):
                outputlog += ("The html element {} with content {} is missing (-1) \n".format(x,y))
                totalpts = totalpts + 1
            elif not (y in c1[x]):
                outputlog += ("The html element {} with content {} is missing (-1) \n".format(x,y))
                totalpts = totalpts + 1

    if list(c1['h1'].keys())[0] != list(c2['h1'].keys())[0]:
        extrasymbol = extrasymbol - 1
        outputlog += ("one of the extra symbols is the author's name \n")
    else:
        totalpts = totalpts + 1
        outputlog += ("The name is not changed (-1) \n")
    totalpts = 5-totalpts
    if totalpts < 0:
        totalpts = 0
    return (totalpts, outputlog)

