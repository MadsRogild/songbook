import re
import os

standard = ["arabic", "roman", "Roman", "alph", "Alph", "hex", "binary", "oct"]         #the standard defined pagenumber styles in latex


"""This function is used to search for a specific pagenumber style,
in the file page_numbering.tex, if the style does not exist,
it returns arabic"""
def search_styles(style):
    if style == "":         #if not style is defined just return arabic
            style = "arabic"
    else:
        f_style = open("""page_numbering.tex""", 'r')           #open the tex file for reading only
        text = f_style.read()
        list_styles = re.findall('\@\w*}',text)     #use a regular expressions to get the strings where a specific combination of chars occur
        for i in range(len(list_styles)):           #go through the list of strings found
            list_styles[i] = list_styles[i][1:len(list_styles[i])-1]        #remove the first char from all entries in the list
        list_styles = list_styles+standard          #concat the list with the standard pagenumber style
        if style not in list_styles:        #check if the style is in the list
            style = "arabic"        #if not return arabic
    return style        #otherwise return the style

def recursive_walk(start):
    files = []
    i = 0
    for root, subdirs, f in os.walk(start):
        for j in range(0,len(f)):
            f[j] = root + "/" + f[j]
        files += f
    return files
