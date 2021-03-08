from tkinter import *

REGISTERS = {'r': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
             's0': 0, 's1': 1, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'k0': 0, 'k1': 0, 'zero': 0}

MEMORY = [600, 'IIT TIRUPATI', 200, 12, 0, 122]

root = Tk()

# Panel
simu = PanedWindow(orient=VERTICAL, bg="black")
simu.pack(fill=BOTH, expand = 1)

# Head Panel
head_panel = PanedWindow(simu,bd=1, relief="raised", bg="black")
simu.add(head_panel)

head = Label(head_panel, text="SIMULATOR")
head_panel.add(head)

# Body Panel
body_panel = PanedWindow(simu, orient=HORIZONTAL, relief="raised", bg="black")
simu.add(body_panel)

# Register Panel
reg_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(reg_panel)

# Memory Panel
mem_panel = PanedWindow(body_panel, orient=VERTICAL,  bd=1, relief="raised", bg="black")
body_panel.add(mem_panel)

# Head Panel of Register and Memory
reg_head = PanedWindow(reg_panel, bd=1, relief="raised")
mem_head = PanedWindow(mem_panel, bd=1, relief="raised")
reg_panel.add(reg_head)
mem_panel.add(mem_head)

regHead = Label(reg_head, text="REGISTERS").grid(row = 0, column = 0)
memHead = Label(mem_head, text="MEMORY").grid(row = 0, column = 0)

# Body Panel of Register and Memory
reg_body = PanedWindow(reg_panel)
mem_body = PanedWindow(mem_panel)
reg_panel.add(reg_body)
mem_panel.add(mem_body)

# Data in Register Panel
pc = Label(reg_body, text="PC").grid(row = 3, column = 0)
equal = Label(reg_body, text="=").grid(row = 3, column = 1)
zero = Label(reg_body, text="0").grid(row = 3, column = 2)

k=4
for i in REGISTERS:
    Label(reg_body, text=str(i)).grid(row = k, column = 0)
    Label(reg_body, text="=").grid(row = k, column = 1)
    Label(reg_body, text=REGISTERS[i]).grid(row = k, column = 2)
    k+=1

# Data in Memory Panel
k=4
for i in MEMORY:
    Label(mem_body, text=str(k-4)+" : ").grid(row=k, column=0)
    Label(mem_body, text=str(i), justify=LEFT, anchor="w").grid(row=k, column=1, sticky=W)
    k+=1

root.mainloop()