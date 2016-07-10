# -*- coding: utf-8 -*-
import sys, os, getopt, re
import preamble, style_tex, auxiliary
from subprocess import call
current_version = sys.version_info


"""This function is used to create the tex file that is the songbook"""
def create_sangbog(unf, camp, name, style, logo, empty, sort, fixed):
    index = 1
    songs = []
    filer = os.listdir("Sange/")        #list of files in Sange/, this is where all the songs we want in the songbook is.

    for fil in filer:
        if fil.endswith(".txt"):        #we only use txt files
            sang = open("""Sange/"""+fil, 'r')      #we open the files
            s = sang.read().lower()                 #read the song, and make all letters lowercase
            s = s.replace(",","")                   #remove commas
            s = s.replace(" ","")                   #remove spaces
            s = s.replace(".","")                   #remove punctuations
            sang.close()                            #close the file
            if "morgenerverdenvor" in s:    #the if and elifs is used to check if the song is "I morgen er verden vor" or "DAT62(1/2)80 Slagsang"
                os.remove("""Sange/"""+fil) #remove them if they are either of those two songs
            elif "fooogbar" in s:
                os.remove("""Sange/"""+fil)
            elif "morgen" in s and "verden" in s and "vor" in s:
                os.remove("""Sange/"""+fil)
            elif "foo" in s and "bar" in s and "automaten" in s:
                os.remove("""Sange/"""+fil)
    path = sys.path[0]          #set the path to our current folder
    os.system("""./check""")    #run the file check
    fil = None
    style = auxiliary.search_styles(style)      #check if the specified style exist
    if style == "hex":
        style = "\\renewcommand*{\\thepage}{0x\\hex{\\value{page}}}"
    elif style == "binary":
        style = "\\renewcommand*{\\thepage}{\\binary{\\value{page}}}"
    elif style == "oct":
        style = "\\renewcommand*{\\thepage}{0\\oct{\\value{page}}}"

    preamble.create_preamble(unf, camp, name, style, logo, empty)       #create the preamble of the tex file
    for fil in filer:
        if fil.endswith(".txt"):
            sang = open("""Sange/"""+fil, 'r')
            line0 = sang.readline()         #read the first line of the song, which contain the title
            title = re.search('(?<=song{)(.*?)}',line0)     #get the title
            title = title.group(0).split('}')[0]        #get the part before }, which is the title
            if "%" in line0:
                try:
                    order = int(float(line0[line0.index("%")+1]))
                except ValueError:
                    order = sys.maxint
                    print("Misplaced % in file: " + fil)
                    import time
                    time.sleep(4)
            else:
                order = sys.maxint
            songs.append((title, fil, order))          #put the title in a list along with its respective filename
            sang.close()      
    temp = []
    if [item for item in songs if "Fulbert og Beatrice" in item]:       #if Fulbert and Beatrice is in the list of songs
        i = songs.index([item for item in songs if "Fulbert og Beatrice" in item][0])       #get the index of Fulbert and Beatrice
        if i != 12:
            temp.append(songs[i])       #if its not number 12, then put it in a list
            del songs[i]                #and remove it from the list of songs
    if [item for item in songs if "I Morgen er Verden Vor" in item]:        #if I Morgen er Verden Vor is in the list of songs
        i = songs.index([item for item in songs if "I Morgen er Verden Vor" in item][0])        #get the index of I Morgen er Verden Vor
        if i != 42:
            temp.append(songs[i])   #if its not number 42, then put it in a list
            del songs[i]            #and remove it from the list of songs
    if [item for item in songs if "DAT62(1/2)80 Slagsang" in item]:     #if DAT62(1/2)80 Slagsang is in the list of songs
        i = songs.index([item for item in songs if "DAT62(1/2)80 Slagsang" in item][0])         #get the index of DAT62(1/2)80 Slagsang
        if i != 43:
            temp.append(songs[i])   #if its not number 43, then put it in a list
            del songs[i]            #and remove it from the list of songs
 
    if sort:
        songs = sorted(songs, key=lambda songs: songs[0])       #sort the songs according to name
    if fixed:
        songs = sorted(songs, key=lambda songs: songs[2])
        order = []
        index = []
        for i in range(0,len(songs)):
            (_,_,o) = songs[i]
            if o < sys.maxint:
                order.append(songs[i])
                index.append(i)
        for ind in index:
            del songs[ind]
        songs = sorted(songs, key=lambda songs: songs[0])
        for i in range(0,len(order)):
            (_,_,o) = order[i]
            songs.insert(o, order[i]) 
             
       
 
    for i in range(0,len(temp)):
        if "Fulbert og Beatrice" == temp[i][0]:
            songs.insert(12, temp[i])       #insert Fulbert og Beatrice in place 12
        elif "I Morgen er Verden Vor" == temp[i][0]:
            songs.insert(42, temp[i])       #insert I Morgen er Verden Vor in place 42
        elif "DAT62(1/2)80 Slagsang" == temp[i][0]:
            songs.insert(43, temp[i])       #insert DAT62(1/2)80 Slagsang in place 43



    next_page = 0
    next_song = 0
    text = ""
    counter = 0
    f = open("Sanghaefte.tex",'a')      #open the tex file for the songbook
    for tup in songs:                   #go through the list of songtitles and files
        (title, fil,order) = tup              #get the title and filename for each song
        if fil.endswith(".txt"):        #only use txt files
            sang = open("""Sange/"""+fil, 'r')      #open the song
#            text = """\\label{song""" + str(counter) + """}\n"""        #make a label
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
                start += """\\setcounter{temppage}{\\value{page}}       
\\pagenumbering{arabic}
\\setcounter{page}{10}"""           #set counter to the current page number, change the pagenumbering to arabic and change the page number to 10
                text = start + text[:j+1] + "\\hypertarget{" + title + "}{}\n\\label{song""" + str(counter) + """}\n""" + text[j+1:] + """
\\newpage
""" + end           #put all the pieces together and make a hypertarget for use in pagereferences ind indexing
                next_page = 2
            elif title == "I Morgen er Verden Vor" and (songs.index(tup) != 42):
                text = """\\setcounter{temp}{\\thesongnum}
\\setcounter{songnum}{42}""" + text[:j+1] + "\\hypertarget{" + title + "}{}\n" + text[j+1:] + """
\\setcounter{songnum}{\\thetemp}
"""         #set a counter to the current song number, force the song number to be 42, and make a hypertarget for use in pagereferences in the index
            elif title == "DAT62(1/2)80 Slagsang" and (songs.index(tup) != 43):
                text = """\\setcounter{temp}{\\thesongnum}
\\setcounter{songnum}{43}""" + text[:j+1] + "\\hypertarget{" + title + "}{}\n" + text[j+1:] + """
\\setcounter{songnum}{\\thetemp}
"""         #set a counter to the current song number, force the song number to be 42, and make a hypertarget for use in pagereferences in the index
            else:
                text = text[:j+1] + """\\hypertarget{""" + title.replace('\\','') + """}{}\n\\label{song""" + str(counter) + """}\n""" + text[j+1:] + """\n"""     #make a hypertarget for use in pagereferences in the index 
                next_page = next_page - 1
                if next_page == 0:
                    if """renew""" in style:
                        text += """""" + style + """\n"""
                    else:
                        text += """\\pagenumbering{""" + style + """}\n"""          #change the style back to the set style
                    text += """\\setcounter{page}{\\value{temppage}}\n"""       #and change the pagenumber back to what it was
            f.write("""\n""" + text + """\n""")
            counter += 1


    f.write("""\n\\end{songs}
\\showindex[2]{Sange}{titleidx}
\\end{document}""")                 #add the index
    index_file = open("titlefile.sbx",'w+')             #start writing to the index file
    index_file.write("""\\begin{idxblock}\n\n""")       #start writing the index


    for i in range(0, len(songs)):
        (title,_,_) = songs[i]            #get the title of the songs
        index_file.write("\\idxentry{" + title.replace('\\','') + "}{Sang nummer: \\hyperlink{" + title.replace('\\','') + "}{" + str(i) + "} På side: \pageref{song" + str(i) + "}}\n")        #create the hyperlink to the hypertarget, and get the song number and pagenumber


    index_file.write("""\\end{idxblock}""")     #end index
    f.close()
    index_file.close()
    call(["pdflatex", "Sanghaefte.tex"])
    call(["pdflatex", "Sanghaefte.tex"])
#    os.remove("Sanghaefte.tex")


def usage():
    print("Usage: "+sys.argv[0]+" -p <used to define new pagenumbering style> -s <choose pagenumbering style> -n <name of sangbook> -l <file for logo, svg or png>")
    print("Options: -c (if it is a camp) -u (if it is UNF) -e (if you do no want a front page) -S (if you want the songs to be sorted by title) -f (if you want the songs to be sorted by a fixed number)")

def main(argv):
    name = ""           #name of the songbook
    camp = False        #if its a camp or not
    style = ""          #the chosen style
    new_style = ""      #the new style to be defined
    unf = False         #if its for UNF or not
    empty = False       #if you want a front page or not
    logo = ""           #the file containing the logo for the front page
    sort = False
    fixed = False
    try:
        opts, args = getopt.getopt(argv,"hucep:s:n:l:Sf",["help","unf","camp","empty","new_style=","style=","name=", "logo=", "sort", "fixed"])     
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
        elif opt in ("-c","--camp"):            #option used to set the camp and unf variable to true
            camp = True
            unf = True
        elif opt in ("-u","--unf"):             #option used to set both unf to true
            unf = True
        elif opt in ("-l", "--logo"):           #option used to get a logo on the front page
            logo = arg
        elif opt in ("-e","--empty"):           #option used to not have a front page
            if logo != "":          #cant be used together with the logo option
                usage()
                sys.exit()
            else:
                empty = True
        elif opt in ("-S","--sort"):
            sort = True
        elif opt in ("-f","--fixed"):
            fixed = True
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
    create_sangbog(unf, camp, name, style, logo, empty, sort, fixed)         #call to create sangbog


if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))
