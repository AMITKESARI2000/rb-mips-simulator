from tkinter import *
import re

# Data just for checking
file = open("testingbubblesort.asm", "r")
lines = file.readlines()
file.close()

i=0
while i < len(lines):
    lines[i] = lines[i].strip().lower()

    if re.findall(r"^# *", lines[i]) or (re.findall(r"^\n", lines[i]) and len(lines[i] == '\n'.length())):
        lines.remove(lines[i])
        i -= 1
    if len(lines[i]) == 0:
        lines.remove(lines[i])
        i -= 1
    i += 1

REGISTERS = {'r': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
             's0': 0, 's1': 1, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'k0': 0, 'k1': 0, 'zero': 0}

MEMORY = [600, 'IIT TIRUPATI', 200, 12, 0, 122]

root = Tk()

root.resizable(width=False, height=False) #Restricting Resizable

# Panel
simulator_body = PanedWindow(orient=VERTICAL, bg="black")
simulator_body.pack(fill=BOTH, expand = 1)

# Head Panel
head_panel = PanedWindow(simulator_body,bd=1, relief="raised", bg="black")
simulator_body.add(head_panel)

head = Label(head_panel, text="SIMULATOR")
head_panel.add(head)

# Body Panel
body_panel = PanedWindow(simulator_body, orient=HORIZONTAL, relief="raised", bg="black")
simulator_body.add(body_panel)

# Register Panel
reg_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(reg_panel)

# Memory Panel
mem_panel = PanedWindow(body_panel, orient=VERTICAL,  bd=1, relief="raised", bg="black")
body_panel.add(mem_panel)

# User Text Panel
user_panel = PanedWindow(body_panel, orient=VERTICAL,  bd=1, relief="raised", bg="black")
body_panel.add(user_panel)

# Head Panel of Register and Memory and User
reg_head = PanedWindow(reg_panel, bd=1, relief="raised")
mem_head = PanedWindow(mem_panel, bd=1, relief="raised")
user_head = PanedWindow(user_panel, bd=1, relief="raised")
reg_panel.add(reg_head)
mem_panel.add(mem_head)
user_panel.add(user_head)

regHead = Label(reg_head, text="REGISTERS").grid(row = 0, column = 0)
memHead = Label(mem_head, text="MEMORY").grid(row = 0, column = 0)
userHead = Label(user_head, text="USER TEXT").grid(row = 0, column = 0)

# Body Panel of Register and Memory and User
reg_body = PanedWindow(reg_panel, bg = "white")
mem_body = PanedWindow(mem_panel, bg = "white")
user_body = PanedWindow(user_panel, bg = "white")

reg_panel.add(reg_body)
mem_panel.add(mem_body)
user_panel.add(user_body)

scroll_reg = Scrollbar(reg_body ,orient="vertical")
scroll_mem = Scrollbar(mem_body ,orient="vertical")
scroll_user = Scrollbar(user_body ,orient="vertical")
scroll_reg.pack(side=RIGHT, fill=Y)
scroll_mem.pack(side=RIGHT, fill=Y)
scroll_user.pack(side=RIGHT, fill=Y)

t_reg = Text(reg_body, width = 10, wrap = NONE, yscrollcommand = scroll_reg.set)
t_mem = Text(mem_body, width = 30, wrap = NONE, yscrollcommand = scroll_mem.set)
t_user = Text(user_body, width = 70, wrap = NONE, yscrollcommand = scroll_user.set)

# Data in Register Panel
t_reg.insert(END, "PC = 0\n")
k=4
for i in REGISTERS:
    t_reg.insert(END, str(i) + " = " + str(REGISTERS[i])+"\n")
    k+=1
t_reg.pack(side=TOP, fill=X)
scroll_reg.config(command=t_reg.yview)

# Data in Memory Panel
k=4
for i in MEMORY:
    t_mem.insert(END, str(k-4) + " : " + str(i) + "\n")
    k+=1
t_mem.pack(side=TOP, fill=X)
scroll_mem.config(command=t_mem.yview)

# Data in User Text Panel
k=4
for i in lines:
    t_user.insert(END, str(k-3)+" : " + str(i) + "\n")
    k+=1
t_user.pack(side=TOP, fill=X)
scroll_user.config(command=t_user.yview)
root.mainloop()