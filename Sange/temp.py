# -*- coding: utf-8 -*-

import os
filer = os.listdir(".")
for f in filer:
    if ".txt" in f:
        tempf = open(f,"r+")
        lines = tempf.readlines()
        s = ""
        for line in lines:
            if "scene{" not in line:
                s = s + line
        tempf.close()
        tempf = open(f,"w+")
        tempf.write(s)
        tempf.close()

