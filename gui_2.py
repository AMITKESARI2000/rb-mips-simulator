from tkinter import *
from tkinter.messagebox import showinfo, askyesno

root = Tk()

# root.resizable(width=False, height=False) #Restricting Resizable
root.title("RB Mips simulator 😎")
# Panel
simulator_body = PanedWindow(orient=VERTICAL, width=1300, height=600, bg="black")
simulator_body.pack(fill=BOTH, expand=1)

# Head Panel
head_panel = PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(head_panel)

head = Label(head_panel, text="SIMULATOR", font=("Arial", 14))
head_panel.add(head)

# Body Panel
body_panel = PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(body_panel)

body = Label(body_panel, text="BODY", font=("Arial", 14))
body_panel.add(body)

v_scroll = Scrollbar(body_panel, orient="vertical")
v_scroll.pack(side=RIGHT, fill=Y)

h_scroll = Scrollbar(body_panel, orient="horizontal")
h_scroll.pack(side=BOTTOM, fill=X)

t_pipe = Text(body_panel, height=50, width=15, wrap=NONE, yscrollcommand=v_scroll.set,
              xscrollcommand=h_scroll.set, font=("Roboto", 9))


def pipelining(x):
    t_pipe.insert(END, str(x) + " | ")
    t_pipe.pack(side=TOP, fill=X)
    h_scroll.config(command=t_pipe.yview)


pipelining("PIPELINING:\n")


def end():
    root.mainloop()
