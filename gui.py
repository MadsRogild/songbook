# -*- coding: utf-8 -*-
#!/usr/bin/python3

import os
from Tkinter import *
import Songbook
import auxiliary

checks = "Sort the songs based on number in song","No front page"
options = ["How to sort the songs"]
fields = "Name:","Author:","Style:","Logo:","New style:"

def fetch(entries, root):
    if root.grid_size()[1] > 9:
        for label in root.grid_slaves():
            if int(label.grid_info()["row"]) > 9:
                label.grid_forget()
    author = ""
    name = ""           #name of the songbook
    style = ""          #the chosen style
    new_style = ""      #the new style to be defined
    empty = False       #if you want a front page or not
    logo = ""           #the file containing the logo for the front page
    sort = "none"
    fixed = False
    random = False
    for entry in entries:
        field = entry[0]
        if field == "Logo:":
            temp = entry[1].get()
            if "/" in temp:
                list_logo = temp.split("/")
                directory = ""
                for i in range(0,len(list_logo)-1):
                    directory += list_logo[i] + "/"
                filer = os.listdir(directory)
                if list_logo[len(list_logo)-1] in filer:
                    logo = list_logo[len(list_logo)-1]
                    entry[1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
                else:
                    entry[1].configure(highlightbackground="red", highlightcolor="red")
            else:
                filer = os.listdir(".")
                if temp in filer:
                    logo = temp
                    entry[1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
                elif temp != "":
                    entry[1].configure(highlightbackground="red", highlightcolor="red")
        elif field == "Name:":
            name = entry[1].get()
        elif field == "Style:":
            style = entry[1].get()
            if auxiliary.search_styles(style) != style and style != "":
                Label(root, text="*No style exist with that name.", fg="red").grid(row=root.grid_size()[1], sticky=W, pady=5)
                entry[1].configure(highlightbackground="red", highlightcolor="red")
            else:
                entry[1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
        elif field == "New style:":
            new_style = entry[1].get()
            if new_style != "":
                n = new_style.split()[0]
                s = new_style.split()[1]
                if auxiliary.search_styles(n) != n:
                    entry[1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
                    style_tex.new_page_style(n,s)
                else:
                    lab = Label(root, text="*There is already a style with that name.", fg="red").grid(row=root.grid_size()[1], sticky=W, pady=5, columnspan=10)
                    entry[1].configure(highlightbackground="red", highlightcolor="red")
        elif field == "Author:":
            author = entry[1].get()
            if not empty and author != "":
                for e in entries:
                    if e[0] == "No front page" and not e[1][0].get():
                        e[1][1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
                        break
        elif field == "No front page":
            if entry[1][0].get():
                if name == "" and author == "" and logo == "":
                    entry[1][1].configure(highlightcolor="black", highlightbackground="#D3D3D3")
                    empty = True
                else:
                    lab = Label(root, text="*Empty is set while either logo or author is set.", fg="red").grid(row=root.grid_size()[1], sticky=W, pady=5, columnspan=10)
                    entry[1][1].configure(highlightbackground="red", highlightcolor="red")
        elif field == "Sort the songs based on number in song":
            if entry[1][0].get():
                fixed = True
        elif field == "How to sort the songs":
            sort = entry[1][0].get()
    Songbook.create_songbook(author, name, style, logo, empty, fixed, sort, True)
    done = Tk()
    done.title("Songbook created")
    lab = Label(done, width=42, text="Songbook has been created, press ok to close this box.", anchor='w')
    lab.pack(side=TOP)
    b = Button(done, text='Ok', command=done.destroy)
    b.pack(padx=5, pady=5)


def makeform(root, fields, checks, options):
    entries = []
    r = 1
    for field in fields:
        Label(root, text=field).grid(row=r, sticky=W, pady=7, columnspan=9, column=1, padx=40)
        ent = Entry(root, width=30)
        ent.grid(row=r, pady=5, sticky=W, columnspan=9, column=5)
        entries.append((field, ent))
        r += 1
    for check in checks:
        var = IntVar()
        Label(root, text=check).grid(row=r, sticky=W, pady=5, columnspan=9, column=1, padx=40)
        chk = Checkbutton(root, variable=var)
        chk.grid(row=r, pady=5, column=13, sticky=E)
        entries.append((check, (var,chk)))
        r += 1
    for option in options:
        Label(root, text=option).grid(row=r, sticky=W, pady=5, columnspan=7, column=1, padx=40)
        var = StringVar(root)
        var.set("none") # initial value
        opt = OptionMenu(root, var, "none", "alphabetically", "random")
        opt.grid(row=r, sticky=E, pady=10, column=13)
        entries.append((option, (var,opt)))
        r += 1
    return entries

if __name__ == '__main__':
    root = Tk()
    root.title("Songbook")
    root.geometry("530x350")
    root.resizable(0, 0)
    ents = makeform(root, fields, checks, options)
    root.bind('<Return>', (lambda event, e=ents: fetch(e,root)))   
    Button(root, text='Create songbook', command=(lambda e=ents: fetch(e,root))).grid(row=root.grid_size()[1], pady=5, column=1, padx=35)
    Button(root, text='Quit', command=root.quit).grid(row=root.grid_size()[1]-1, pady=5, column=2)
    root.mainloop()
