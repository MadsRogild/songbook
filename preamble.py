# -*- coding: utf-8 -*-
import sys, os, getopt, re
from PIL import Image
from reportlab import pdfbase
#    from svglib.svglib import svg2rlg
#else:
from svglibbuild3 import svg2rlg
from reportlab.graphics import renderPDF

standard = ["arabic", "roman", "Roman", "alph", "Alph","binary","hex","oct"]




def create_preamble(unf, camp, name, style, logo, empty, twosided):
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

    f.write("""\\documentclass[pdftex,12pt]{article}
\\usepackage{latexsym,fancyhdr}\n""")
    if twosided:
        f.write("""\\usepackage[a4paper,includeheadfoot,inner=1cm,outer=2cm,,top=2cm,bottom=2cm,twoside]{geometry}\n""")
    else:
        f.write("""\\usepackage[a4paper,includeheadfoot,margin=1.5cm,top=2cm,bottom=2cm]{geometry}\n""")
    f.write("""\\usepackage[lyric]{songs}
\\usepackage[utf8]{inputenc}
%\\usepackage[danish, english]{babel}
\\usepackage[english]{babel}
\\usepackage{amssymb}
\\usepackage{stmaryrd}
\\usepackage{amsmath}
\\usepackage{amsthm}
\\usepackage[final]{pdfpages}
\\usepackage[none]{hyphenat}
\\usepackage{hyperref}
\\usepackage{multicol}
\\input binhex
\\setlength{\columnsep}{1.5cm}
\\newindex{titleidx}{titlefile}
\\sepindexesfalse
\\noversenumbers
\\title{Sangbog """ + name + """ \\the\\year}\n""")           #create preamble
    if camp or unf:
        f.write("""\\author{Ungdommens Naturvidenskabelige Forening}\n""")        #and UNF as author if its a camp or UNF songbook
    f.write("""\\date{\\today}
%\\addtolength{\\headwidth}{\\marginparsep}
%\\addtolength{\\headwidth}{\\marginparwidth}
\\renewcommand{\\headrulewidth}{.4pt}
%\\renewcommand{\\footrulewidth}{0.4pt}
\\fancyhead{}
\\fancyhead[CE,CO]{}
\\fancyhead[RE,LO]{\\thepage}
\\fancyfoot{}\n""")
    if twosided:
        f.write("""\pagestyle{fancy}\n""")
    if """renew""" in style:
        f.write("""""" + style + """\n""")
    else:
        f.write("""\\newcommand{\\countstyle}{""" + style + """}
\\input{page_numbering}
\\pagenumbering{shiftedpage}\n""")
    f.write("""\\begin{document}
\\newcounter{temp}
\\newcounter{temppage}
\\newcounter{pageoffset}
\\setcounter{page}{0}\n""")          #continue preamble
    if not empty:       #if empty is not specified start writing a front page
        f.write("""\\newgeometry{margin=.5cm,top=4cm,bottom=.5cm}
\\thispagestyle{empty}
\\addtocounter{pageoffset}{-1}
\\centering
\\phantom{test}
\n""")          
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
        f.write("""\\vspace{.5cm}
\\begin{center}\n""")
        if camp:
            f.write("""\\fontfamily{phv}\\fontsize{50}{60}\\selectfont """+name+""" Camp\\\\\\the\\year\n\n\\vspace{1cm}\n\\fontsize{35}{40}\\selectfont Sangbog""")        #put the title for the songbook below the logo
        elif name == "":
            f.write("""\\fontfamily{phv}\\fontsize{50}{60}\\selectfont \\the\\year\n""")         #If name is empty, only show the year
        else:
            f.write("""\\fontfamily{phv}\\fontsize{50}{60}\\selectfont """+name+"""\\\\\\the\\year\n""")         #put the title for the songbook below the logo
        f.write("""\\end{center}\n\\restoregeometry""")
    f.write("""
\\raggedright
\\songpos{0}
\\spenalty=50
\\vvpenalty=100
\\vcpenalty=100
\\cvpenalty=100
\\ccpenalty=100
\\interlinepenalty=120
\\setlength{\parindent}{1cm}
\\begin{songs}{}
\\setcounter{songnum}{0}
""")        #end the preamble
    f.close()       #and close the file
