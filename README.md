To get a songbook generated run the program Sangbog.py.

To use it first install the required packages: rstr and reportlab. Do this using pip. Example: python -m pip install rstr.

It has x options

-c, --camp              To tell the program that it is used for a camp, also sets unf to true

-u, --unf               If the songbook is UNF related

-e, --empty             If one wants an empty first page

-l, --logo <file>       Used to specify logo to be used on the first page (cannot be used with -e)

-n, --name              The name/title for the songbook

-s, --style             Specifies the pagenumber style to be used

-p, --new_style         Specifies a new style to be added.

Usage example: python Sangbog.py -n Mat -c -s hex -l pic.svg
This gives a songbook where the title is Mat, and it is a camo, it uses hexadecimal as pagenumbers, and the logo is pic.svg.


For the new_style option one has to enter the new style of form: "name [regular expression", for example python Sangbog.py -p "example ([a-z]-[A-Z])\d"

