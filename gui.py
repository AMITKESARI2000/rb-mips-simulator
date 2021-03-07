from tkinter import *

REGISTERS = {'r': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
             's0': 0, 's1': 1, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'k0': 0, 'k1': 0, 'zero': 0}

root = Tk()


simu = Label(root, text="SIMU").grid(row = 0, column = 2)
reg = Label(root, text="Registers").grid(row = 1, column = 1)
memory = Label(root, text="Memory").grid(row = 1, column = 5)
line = Label(root, text="  |  ").grid(row = 1, column = 3)

pc = Label(root, text="PC").grid(row = 2, column = 0)
equal = Label(root, text="=").grid(row = 2, column = 1)
line = Label(root, text="  |  ").grid(row = 2, column = 3)

k=3
for i in REGISTERS:
    j = Label(root, text=str(i)).grid(row = k, column = 0)
    e = Label(root, text="=").grid(row = k, column = 1)
    v = Label(root, text=REGISTERS[i]).grid(row = k, column = 2)
    l = Label(root, text="  |  ").grid(row = k, column = 3)
    k+=1
root.mainloop()