#!/usr/bin/python

import Tkinter
import subprocess



# context menu
def make_menu(w):
    global the_menu
    the_menu = Tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

# quit GUI
def quit():
    main.destroy()

# generate polymorphed shell
def run():
    # execute the shellscript
    p = subprocess.check_output(["./polymorphThatShell.sh", inputField.get("1.0", "end")])

    # Output result to user
    outputField.delete("1.0", "end")
    outputField.insert("1.0", p)
    
    
main = Tkinter.Tk()
make_menu(main)
main.title("PolymorphThatShell")

# scrollbar
scb = Tkinter.Scrollbar(main, orient="vertical")

# Input field and label
labelInputShellcode = Tkinter.Label(main, text = "Insert your shellcode (without quotes):")
labelInputShellcode["height"]  = 2
labelInputShellcode["width"] = 50
labelInputShellcode.pack()
inputField = Tkinter.Text(main, width=65, height=10)
inputField.pack(side="top")
inputField.bind_class("Text", "<Button-3><ButtonRelease-3>", show_menu)

# execute button
bRun = Tkinter.Button(main, text = "RUN", command = run)
bRun.pack()

# output field and label
labelOutputShellcode = Tkinter.Label(main, text = "Polymorphed shellcode:")
labelOutputShellcode["height"]  = 2
labelOutputShellcode["width"] = 20
labelOutputShellcode.pack()
outputField = Tkinter.Text(main, width=65, height=15, yscrollcommand=scb.set)
outputField["width"] = 80
scb["command"] = outputField.yview
outputField.pack(side="left")
outputField.bind_class("Text", "<Button-3><ButtonRelease-3>", show_menu)
scb.pack(side="left", fill="y")

main.mainloop()
