#!/usr/bin/python

import os
import re

name = raw_input('Search for: ')
data = re.compile(name)
newname = raw_input('New name: ')

count = 0
for file in os.listdir(os.getcwd()):
    allowed_name = re.compile(file).match
    if allowed_name(file):
        count = count + 1
        ext = os.path.splitext(file)
        num = str(count)
        new = (newname + '_' + num.zfill(3) + ext[1])
        os.rename(file, new)
