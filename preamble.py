# -*- coding: utf-8 -*-
import sys, os, getopt, re
from PIL import Image
from reportlab import pdfbase
#    from svglib.svglib import svg2rlg
#else:
from svglibbuild3 import svg2rlg
from reportlab.graphics import renderPDF

standard = ["arabic", "roman", "Roman", "alph", "Alph","binary","hex","oct"]




def create_preamble(author, name, style, logo, empty, twosided):
    if """.svg""" in logo:          #check if the logo is in svg format
        tempf = open(logo,'r')      #open the file for reading
        s = tempf.read()
        height_k = re.search('height=\"(\d*).(\d*)',s)          #get the height of the picture, using regular expressions
        height_l = re.search('\"(\d*).(\d*)',height_k.group(0)).group(0)[1:]         #get only the height
        height_l = float(re.sub("[^0-9]", "", height_l))
        
        width_k = re.search('width=\"(\d*).(\d*)',s)            #get the width of the picture, using regular expressions
        width_l = re.search('\"(\d*).(\d*)',width_k.group(0)).group(0)[1:]           #get only the width
        width_l = float(re.sub("[^0-9]", "", width_l))

        drawing = svg2rlg(logo)         #draw the picture
        file_name = str.split(logo, """.svg""")[0] + """.pdf"""         #replace the .svg part with .pdf
        renderPDF.drawToFile(drawing, file_name)            #draw the picture to the file and render it
    if not empty:           #if it is anything but empty and a svg file
        tempf = open(name+"Camp_tekst.tex",'w+')            #we make a new tex file to be used for front page
        tempf.write("""\\documentclass[pdftex]{article}""")         #now we start to declare the preamble for that tex file
        tempf.write("""\\title{Sangbog for """ + name + """ \\theyear}""")
        if author != "":
            tempf.write("""\\author{"""+author+"""}""")           #we write the title for the songbook to the tex file
        tempf.write("""\\date{\\today}
\\begin{document}
\\pagestyle{empty}
\\begin{center}""")     #start the document
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
        f.write("""\\usepackage[a4paper,includeheadfoot,left=1.8cm,right=1.2cm,,top=2cm,bottom=2cm,twoside]{geometry}\n""")
    else:
        f.write("""\\usepackage[a4paper,includeheadfoot,margin=1.5cm,top=2cm,bottom=2cm]{geometry}\n""")
    f.write("""\\usepackage[lyric]{songs}
\\usepackage[utf8]{inputenc}
\\DeclareUnicodeCharacter{FEFF}{}
\\usepackage[english,danish]{babel}
%\\usepackage[english]{babel}
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
    if author != "":
        f.write("""\\author{"""+author+"""}\n""")        #
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
            scale_height = 1122.519685 / height_l
            scale_width = 818.110236 / width_l
            scale = (min(scale_height, scale_width))         #calculate how much the logo can be scaled
            new_height = scale*height_l
            new_width = scale*width_l
            f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+file_name+"""}}\n""")       #include the logo in the tex file and scale it
        elif """.jpg""" in logo or """.png""" in logo:      #if its not a vector graphic image
            img = Image.open(logo)
            width, height = img.size            #get the height and width of the image
            scale_height = 1122.519685 / height
            scale_width = 818.110236 / width
            scale = min(scale_width, scale_height)      #get the smallest of the two 
            if scale < 1:       #if the lowest is less than 1 we need to scale down so it can fit in the page, otherwise we do no scale up
                f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+logo+"""}}\n""")
            else:
                f.write("""\\mbox{\\includegraphics[scale="""+str(scale)+"""]{"""+logo+"""}}\n""")
        elif """.pdf""" in logo:
            f.write("""\\mbox{\\includegraphics[width=\\textwidth]{"""+logo+"""}}\n""")
        f.write("""\\vspace{.5cm}
\\begin{center}\n""")
        if name == "":
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
\\interlinepenalty=200
\\versesep=12pt plus 24pt minus 3pt
\\setlength{\parindent}{1cm}
\\begin{songs}{}
\\setcounter{songnum}{0}
""")        #end the preamble
    f.close()       #and close the file
