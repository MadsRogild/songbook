# -*- coding: utf-8 -*-

import os
import auxiliary

filer = auxiliary.recursive_walk("Sange/") 
for f in filer:
    print(f)
    if ".txt" in f:
        tempf = open(f,"r+")
        text = tempf.read()
        s = text.replace('"', '')
        #s = ""
        #for line in lines:
        #    if "scene{" not in line:
        #        s = s + line
        tempf.close()
        tempf = open(f,"w+")
        tempf.write(s)
        tempf.close()

