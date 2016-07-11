# -*- coding: utf-8 -*-
import sys, os, getopt, re
from PIL import Image
from reportlab import pdfbase
#    from svglib.svglib import svg2rlg
#else:
from svglibbuild3 import svg2rlg
from reportlab.graphics import renderPDF

standard = ["arabic", "roman", "Roman", "alph", "Alph"]




def create_preamble(unf, camp, name, style, logo, empty):
    if """.svg""" in logo:          #check if the logo is in svg format
        tempf = open(logo,'r')      #open the file for reading
        s = tempf.read()
        height_k = re.search('height=\"(\d*).(\d*)',s)          #get the height of the picture, using regular expressions
        height_l = float(re.search('\"(\d*).(\d*)',height_k.group(0)).group(0)[1:])         #get only the height

        width_k = re.search('width=\"(\d*).(\d*)',s)            #get the width of the picture, using regular expressions
        width_l = float(re.search('\"(\d*).(\d*)',width_k.group(0)).group(0)[1:])           #get only the width

        drawing = svg2rlg(logo)         #draw the picture
        file_name = str.split(logo, """.svg""")[0] + """.pdf"""         #replace the .svg part with .pdf
        renderPDF.drawToFile(drawing, file_name)            #draw the picture to the file and render it
    if not empty:           #if it is anything but empty and a svg file
        tempf = open(name+"Camp_tekst.tex",'w+')            #we make a new tex file to be used for front page
        tempf.write("""\\documentclass[pdftex]{article}""")         #now we start to declare the preamble for that tex file
        if camp:
            tempf.write("""\\title{Sangbog for """ + name + """ Camp \\theyear}
\\author{Ungdommens Naturvidenskabelige Forening}""")           #we write the title for the songbook to the tex file
        elif unf:
            tempf.write("""\\title{Sangbog for """ + name + """}
\\author{Ungdommens Naturvidenskabelige Forening}""")           #we write the title for the songbook to the tex file
        else:
            tempf.write("""\\title{Sangbog for """ + name + """ \\theyear}""")          #we write the title for the songbook to the tex file
        tempf.write("""\\date{\\today}
\\begin{document}
\\pagestyle{empty}
\\begin{center}""")     #start the document
        if camp:
            tempf.write("""\\fontfamily{phv}\\selectfont\\Huge """+name+""" Camp \\the\\year\n""")        #if it is a camp write the name plus camp
        else:
            tempf.write("""\\fontfamily{phv}\\selectfont\\Huge """+name+""" \\the\\year\n""")         #otherwise just write name
        tempf.write("""\\end{center}

\\end{document}""")         #end the document

        from subprocess import call
        tempf.close()
        call(["pdflatex", name+"Camp_tekst.tex"])       #use pdflatex on the tex file


    f = open("Sanghaefte.tex", 'w+')        #now create the tex file for the songbook itself

    f.write("""\\documentclass[pdftex]{article}
\\usepackage{latexsym,fancyhdr}
\\usepackage[a4paper,includeheadfoot,margin=2.5cm]{geometry}
\\usepackage[lyric]{songs}
\\usepackage[utf8]{inputenc}
\\usepackage[danish, english]{babel}
\\usepackage{amssymb}
\\usepackage{stmaryrd}
\\usepackage{amsmath}
\\usepackage{amsthm}
\\usepackage[final]{pdfpages}
\\usepackage{tabularx}
\\usepackage[none]{hyphenat}
\\usepackage{hyperref}
\\usepackage{multicol}
\\input binhex
\\setlength{\columnsep}{2cm}
\\newindex{titleidx}{titlefile}
\\sepindexesfalse
\\title{Sangbog """ + name + """ \\the\\year}\n""")           #create preamble
    if camp or unf:
        f.write("""\\author{Ungdommens Naturvidenskabelige Forening}\n""")        #and UNF as author if its a camp or UNF songbook
    f.write("""\\date{\\today}
\\addtolength{\\headwidth}{\\marginparsep}
\\addtolength{\\headwidth}{\\marginparwidth}
\\renewcommand{\\headrulewidth}{0.4pt}
\\renewcommand{\\footrulewidth}{0.4pt}
\\fancyhead[LE,RO]{\\LHeadFont Sangbog}
\\fancyhead[CE,CO]{\\CHeadFont\\thepage}
\\fancyhead[RE,LO]{\\RHeadFont\\RelDate}\n""")
    if """renew""" in style:
        f.write("""""" + style + """\n""")
    else:
        f.write("""\\input{page_numbering}
\\pagenumbering{""" + style + """}\n""")
    f.write("""\\begin{document}
\\newcounter{temp}
\\newcounter{temppage}\n""")          #continue preamble
    if not empty:       #if empty is not specified start writing a front page
        f.write("""\\thispagestyle{empty}
\\centering
\\phantom{test}
\\vspace{1cm}\n""")          
        if """.svg""" in logo:
            scale_height = 736.75 / height_l
            scale_width = 460.625 / width_l
            scale = (min(scale_height, scale_width)) - 0.15         #calculate how much the logo can be scaled
            f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+file_name+"""}}\n""")       #include the logo in the tex file and scale it
        elif """.jpg""" in logo or """.png""" in logo:      #if its not a vector graphic image
            img = Image.open(logo)
            width, height = img.size            #get the height and width of the image
            scale_height = 736.75 / height
            scale_width = 520.625 / width
            scale = min(scale_width, scale_height)      #get the smallest of the two 
            if scale < 1:       #if the lowest is less than 1 we need to scale down so it can fit in the page, otherwise we do no scale up
                f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+logo+"""}}\n""")
            else:
                f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+logo+"""}}\n""")
        else:
            f.write("""\\mbox{\\includegraphics[]{"""+logo+"""}}\n""")
        f.write("""\\vspace{1cm}
\\begin{center}\n""")
        if camp:
            f.write("""\\fontfamily{phv}\\selectfont\\Huge """+name+""" Camp \\the\\year\n""")        #put the title for the songbook below the logo
        else:
            f.write("""\\fontfamily{phv}\\selectfont\\Huge """+name+""" \\the\\year\n""")         #put the title for the songbook below the logo
        f.write("""\\end{center}\n""")
    f.write("""\\vspace{2.5cm}
\\newpage
\\setcounter{page}{0}
\\raggedright
\\songpos{0}
\\spenalty=-10
\\vvpenalty=100
\\begin{songs}{}
\\setcounter{songnum}{0}
""")        #end the preamble
    f.close()       #and close the file
