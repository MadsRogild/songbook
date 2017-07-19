# -*- coding: utf-8 -*-
import sys, os, getopt, re
import preamble, style_tex, auxiliary
from subprocess import call
from random import shuffle, seed, randint
current_version = sys.version_info


"""This function is used to create the tex file that is the songbook"""
def create_songbook(author, name, style, logo, empty, twosided, sort, fixed, random):
    index = 1
    songs = []
    filer = auxiliary.recursive_walk("Sange/")        #list of files in Sange/, this is where all the songs we want in the songbook is.

    path = sys.path[0]          #set the path t  our current folder
    fil = None
    style = auxiliary.search_styles(style)      #check if the specified style exist
    if style == "hex":
        style = "hexX"
    elif style == "binary":
        style = "binaryX"
    elif style == "oct":
        style = "octX"

    preamble.create_preamble(author, name, style, logo, empty, twosided)       #create the preamble of the tex file
    for fil in filer:
        if fil.endswith(".txt"):
            sang = open(fil, 'r')
            line0 = sang.readline()         #read the first line of the song, which contain the title
            title = re.search('(?<=song{)(.*?)}',line0)     #get the title
            title = title.group(0).split('}')[0]        #get the part before }, which is the title
            if "%" in line0 and fixed:
                try:
                    order = int(float(line0[line0.index("%")+1:]))
                except ValueError:
                    order = sys.maxint
                    print("Misplaced % in file: " + fil)
                    import time
                    time.sleep(3)
            elif "Fulbert og Beatrice" in title:
                order = 12
            elif "I Morgen er Verden Vor" in title:
                order = 42
            elif "DAT62(1/2)80 Slagsang" in title:
                order = 43
            else:
                order = sys.maxint
            songs.append((title, fil, order))          #put the title in a list along with its respective filename
            sang.close()      
    if sort:
        songs = sorted(songs, key=lambda songs: songs[0].replace('\\','').replace('$','').lower())       #sort the songs according to name
    if random:
        shuffle(songs)
    if fixed:
        songs = sorted(songs, key=lambda songs: songs[2])
        order = []
        index = []
        for i in range(0,len(songs)):
            (_,_,o) = songs[i]
            if o < sys.maxint:
                order.append(songs[i])
                index.append(i)

        for i in range(len(index)-1,-1,-1):
            del songs[i]
        if not(random):
            songs = sorted(songs, key=lambda songs: songs[0].replace('\\','').replace('$','').lower())       #sort the songs according to name
        for i in range(0,len(order)):
            (_,_,o) = order[i]
            songs.insert(o, order[i])
       
    next_page = 0
    next_song = 0
    text = ""
    counter = 0
    f = open("Sanghaefte.tex",'a')      #open the tex file for the songbook
    for tup in songs:                   #go through the list of songtitles and files
        (title, fil,order) = tup              #get the title and filename for each song
        if fil.endswith(".txt"):        #only use txt files
            sang = open(fil, 'r')
            text = sang.read()         #get the entire song and append it to the text
            j = text.find("]")          #find the end of the song declaration
            if title == "Fulbert og Beatrice":      #if the song is Fulbert og Beatrice
                start = ""
                end = ""
                if songs.index(tup) != 12:          #and if it is not number 13 in the list
                    start += """\\setcounter{temp}{\\thesongnum}
\\setcounter{songnum}{12}"""        #set a counter to the current song number, and force the song number to be 12, all done in latex
                    end += """
\\setcounter{songnum}{\\thetemp}"""         #change the song number back to the original
                start += """\\renewcommand{\\thepage}{10}
\\addtocounter{pageoffset}{-1}"""           #Set page number to 10 and shift remaining page numbers by 1
                text = start + text[:j+1] + "\\hypertarget{" + title + "}{}\n\\label{song""" + str(counter) + """}\n""" + text[j+1:] + """
\\newpage
""" + end           #put all the pieces together and make a hypertarget for use in pagereferences ind indexing
                next_page = 1
            elif title == "I Morgen er Verden Vor" and (songs.index(tup) != 42):
                text = """\\setcounter{temp}{\\thesongnum}
\\setcounter{songnum}{42}""" + text[:j+1] + "\\hypertarget{" + title + "}{}\n\\label{song" + str(counter) + "}\n" + text[j+1:] + """
\\setcounter{songnum}{\\thetemp}
"""         #set a counter to the current song number, force the song number to be 42, and make a hypertarget for use in pagereferences in the index
            elif title == "DAT62(1/2)80 Slagsang" and (songs.index(tup) != 43):
                text = """\\setcounter{temp}{\\thesongnum}
\\setcounter{songnum}{43}""" + text[:j+1] + "\\hypertarget{" + title + "}{}\n\\label{song" + str(counter) + "}\n" + text[j+1:] + """
\\setcounter{songnum}{\\thetemp}
"""         #set a counter to the current song number, force the song number to be 42, and make a hypertarget for use in pagereferences in the index
            else:
                text = text[:j+1] + """\\hypertarget{""" + title.replace('\\','') + """}{}\n\\label{song""" + str(counter) + """}\n""" + text[j+1:] + """\n"""     #make a hypertarget for use in pagereferences in the index 
                next_page = next_page - 1
                if next_page == 0:
                    if """renew""" in style:
                        text += """""" + style + """\n"""
                    else:
                        text += """\\setcounter{temppage}{\\value{page}}\n\\pagenumbering{shiftedpage}\n\\setcounter{page}{\\value{temppage}}"""          #change the style back to the set style, using temppage to avoid the fact that pagenumbering resets page.
                    text += """\n"""       #and change the pagenumber back to what it was
            f.write("""\n""" + text + """\n""")
            counter += 1


    f.write("""\n\\end{songs}""")
    if twosided:
        f.write("""\\makeatletter
\\newcount\\divFour
\\divFour \\c@page
\\divide\\divFour by 4
\\multiply\\divFour by 4
\\advance\\divFour by-\\c@page
\\edef\\remainFour{\\the\\divFour}
\\ifnum\\remainFour = 0
  \\clearpage\\null\\clearpage\\null\\clearpage\\null
\\else\\ifnum\\remainFour = -1
  \\clearpage\\null\\clearpage\\null
\\else\\ifnum\\remainFour = -2
  \\clearpage\\null
\\fi\\fi\\fi""")
    f.write("""
\\newgeometry{margin=2cm,top=2cm,bottom=2cm}
\\setlength{\\headwidth}{\\textwidth}
\\showindex[2]{Sange}{titleidx}
\\end{document}""")                 #add the index
    index_file = open("titlefile.sbx",'w+')             #start writing to the index file
#    index_file.write("""\\begin{idxblock}\n\n""")       #start writing the index
    index_file.write("""\\setlength{\parindent}{-4em}\\addtolength{\\leftskip}{4em}\n""")       #start writing the index


    songs_index = sorted(songs, key=lambda songs: songs[0].replace('\\','').replace('$','').lower())
    for i in range(0, len(songs_index)):
        (title,_,_) = songs_index[i]            #get the title of the songs
        index = songs.index([item for item in songs if item[0] == title][0])
#        index_file.write("\\idxentry{" + title.replace('\\','') + "}{Sang nummer: \\hyperlink{" + title.replace('\\','') + "}{" + str(index) + "} På side: \pageref{song" + str(index) + "}}\n")        #create the hyperlink to the hypertarget, and get the song number and pagenumber
        index_file.write("\makebox[2em][r]{\\hyperlink{" + title.replace('\\','') + "}{" + str(index) + "}} {\idxtitlefont " + title + "}\ \dotfill\ side~\pageref{song" + str(index) + "}\n\n")        #create the hyperlink to the hypertarget, and get the song number and pagenumber


#    index_file.write("""\\end{idxblock}""")     #end index
    f.close()
    index_file.close()
    call(["pdflatex", "Sanghaefte.tex"])
    call(["pdflatex", "Sanghaefte.tex"])
#    os.remove("Sanghaefte.tex")


def usage():
    print("Usage: "+sys.argv[0]+" -a <used to set the name of the author of the songbook> -p <used to define new pagenumbering style> -s <choose pagenumbering style> -n <name of songbook> -l <file for logo, svg or png>")
    print("Options: -e (if you do no want a front page) -S (if you want the songs to be sorted by title) -f (if you want the songs to be sorted by a fixed number) -r (if you want the songs shuffled. Combines with -f to shuffle only the non-fixed songs) -t (twosided print intended for booklets) --seed (specify seed for -r)")

def main(argv):
    author = ""
    name = ""           #name of the songbook
    style = ""          #the chosen style
    new_style = ""      #the new style to be defined
    empty = False       #if you want a front page or not
    twosided = False       #if you want twosided for book print or not
    logo = ""           #the file containing the logo for the front page
    sort = False
    fixed = False
    random = False
    
    strSeed = str(randint(0, sys.maxint))+str(randint(0,sys.maxint))+str(randint(0,sys.maxint))
    seed(strSeed)
    try:
        opts, args = getopt.getopt(argv,"heatp:s:n:l:Sfr",["help","empty","author=","twosided","new_style=","style=","name=", "logo=", "sort", "fixed","random","seed="])     
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):          #option used to print usage
            usage()
            sys.exit()
        elif opt in ("-p", "--style"):          #option used for making a new pagenumber style
            new_style = arg
        elif opt in ("-s", "--number_style"):       #option used to set the pagenumber style in the tex file
            style = arg
        elif opt in ("-n", "--name"):           #option used to set the name
            name = arg
        elif opt in ("-a", "--author"):         #option used to set both unf to true
            author = arg
        elif opt in ("-l", "--logo"):           #option used to get a logo on the front page
            logo = arg
        elif opt in ("-e","--empty"):           #option used to not have a front page
            if logo != "" or author != "":          #cant be used together with the logo option
                usage()
                sys.exit()
            else:
                empty = True
        elif opt in ("-t","--twosided"):
            twosided = True
        elif opt in ("-S","--sort"):
            sort = True
        elif opt in ("-f","--fixed"):
            fixed = True
        elif opt in ("-r","--random"):
            random = True
        elif opt in ("--seed"):
            if random:
                strSeed = arg
                seed(strSeed)
            else:
                usage()
                sys.exit()
        else:
            usage()
            sys.exit()
    if new_style != "":         #check if the new_style is empty, that is if the new_style option was used or not
        n = new_style.split()[0]        #split the argument into two parts, a name
        s = new_style.split()[1]        #and the style, that will be a regular expression
        if auxiliary.search_styles(n) != n:         #check if the name is already in use, cannot have two styles by the same name
            style_tex.new_page_style(n,s)
        else:
            print("There is already a style with that name.")
    create_songbook(author, name, style, logo, empty, twosided, sort, fixed, random)         #call to create sangbog
    if random:
        print("Seed used for shuffling: " + strSeed)

if __name__=='__main__':
    (main(sys.argv[1:]))
