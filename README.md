The program Sangbog.py generates a tex file containing a songbook which is then compilated into a pdf file.

To use it first install the required packages: rstr and reportlab. Do this using pip. Example: python -m pip install rstr. Next the songs package need to be installed, it can be downloaded at http://songs.sourceforge.net/downloads.html.

It has 7 options

-c, --camp                                        To tell the program that it is used for a camp, also sets unf to true

-u, --unf                                         If the songbook is UNF related

-e, --empty                                       If one wants an empty first page

-l, --logo "file"                                 Used to specify logo to be used on the first page (cannot be used with -e)

-n, --name "name"                                 The name/title for the songbook

-s, --style "style"                               Specifies the pagenumber style to be used

-p, --new_style "name regular expression"         Specifies a new style to be added.

-S, --sort                                        Specifies the songs to be sorted in alphabetic order

-f, --fixed                                       This makes it order them by a specified number set in the song files. Read more below.


Usage example: python Sangbog.py -n Mat -c -s hex -l pic.svg
This gives a songbook where the title is Mat, and it is a camo, it uses hexadecimal as pagenumbers, and the logo is pic.svg.


For the new_style option one has to enter the new style of form: "name [regular expression", for example python Sangbog.py -p "example ([a-z]|[A-Z])\d"

Logos have to be either svg, png or jpg.

If the style specified in the option --style does not exist then arabic style will be used.

The sorting by fixed numbers works by putting a comment followed by a number in the songs file, so the first line of any song will look like:

line1: \beginsong{song title}[options]%5
line2-x: song

The declaration of the song can be split up over several lines so it becomes

line1-x: \beginsong{song title}[options%5
line x: ]
line x+1-y: song

This means the song will be number 5. For the songs that have no number specified they will get sorted by title.
