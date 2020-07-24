# autograder --- Student Version to grade all the files
#
# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import os
import autograder_main
print("What's the directory where the files (index.html, academics.html, etc.) reside? ")
directory = input()



try:
    os.chdir(directory)
    result = autograder_main.findallfiles()
    print(result)
except OSError as e:
    print("File or directory does not exist!")