import re
from tkinter import *
from tkinter.messagebox import showinfo, askyesno
import simu_1

simu_1.rm_comments()

root = Tk()

# root.resizable(width=False, height=False) #Restricting Resizable
root.title("RB Mips simu_1lator 😎")
# Panel
simu_1lator_body = PanedWindow(orient=VERTICAL, width=1300, height=600, bg="black")
simu_1lator_body.pack(fill=BOTH, expand=1)

# Head Panel
head_panel = PanedWindow(simu_1lator_body, bd=1, relief="raised", bg="black")
simu_1lator_body.add(head_panel)

head = Label(head_panel, text="simu_1LATOR", font=("Arial", 14))
head_panel.add(head)

# Execution Panel
step_exe = Button(text="Step By Step Execution", bg="#f94b5d", fg="#efefef",
                  command=lambda: modify_gui_data_once())
step_exe.pack(side=LEFT)
# command=lambda: showinfo("Message", "STILL IN PROGRESS!!!")).pack(side=LEFT)
space1 = Button(text="      ", bg="white", state=DISABLED).pack(side=LEFT)
once_exe = Button(text="At Once Execution", bg="#2f6fca", fg="#efefef", command=lambda: modify_gui_data()).pack(
    side=LEFT)
space2 = Button(text="      ", bg="white", state=DISABLED).pack(side=LEFT)
console_button = Button(text="Upload a file", bg="#f79400", fg="#efefef",
                        command=lambda: showinfo("Message", "STILL IN PROGRESS!!!")).pack(side=LEFT)

# Body Panel
body_panel = PanedWindow(simu_1lator_body, orient=HORIZONTAL, relief="raised", bg="black")
simu_1lator_body.add(body_panel)

# Register Panel
reg_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(reg_panel)

# Memory Panel
mem_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(mem_panel)

# User Text Panel
user_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black")
body_panel.add(user_panel)

# Head Panel of Register and Memory and User
reg_head = PanedWindow(reg_panel, bd=1, relief="raised")
mem_head = PanedWindow(mem_panel, bd=1, relief="raised")
user_head = PanedWindow(user_panel, bd=1, relief="raised")
reg_panel.add(reg_head)
mem_panel.add(mem_head)
user_panel.add(user_head)

regHead = Label(reg_head, text="REGISTERS", height=1, font=("Arial", 10)).grid(row=0, column=0)
memHead = Label(mem_head, text="MEMORY", height=1, font=("Arial", 10)).grid(row=0, column=0)
userHead = Label(user_head, text="USER TEXT", height=1, font=("Arial", 10)).grid(row=0, column=0)

# Body Panel of Register and Memory and User
reg_body = PanedWindow(reg_panel, bg="white")
mem_body = PanedWindow(mem_panel, bg="white")
user_body = PanedWindow(user_panel, bg="white")

reg_panel.add(reg_body)
mem_panel.add(mem_body)
user_panel.add(user_body)

scroll_reg = Scrollbar(reg_body, orient="vertical")
scroll_mem = Scrollbar(mem_body, orient="vertical")
scroll_user = Scrollbar(user_body, orient="vertical")
scroll_reg.pack(side=RIGHT, fill=Y)
scroll_mem.pack(side=RIGHT, fill=Y)
scroll_user.pack(side=RIGHT, fill=Y)

t_reg = Text(reg_body, height=50, width=15, wrap=NONE, yscrollcommand=scroll_reg.set, font=("Roboto", 9))
t_mem = Text(mem_body, height=50, width=35, wrap=NONE, yscrollcommand=scroll_mem.set, font=("Roboto", 9))
t_user = Text(user_body, height=15, width=50, wrap=NONE, yscrollcommand=scroll_user.set, font=("Roboto", 9))

# Console Panel
console_panel = PanedWindow(user_panel, orient="vertical", relief="raised", bg="white")
user_panel.add(console_panel)

console_head = Label(console_panel, text="CONSOLE", relief="raised", height=1, font=("Arial", 10))
console_panel.add(console_head)

console = Label(console_panel, bg="black", font=("Arial", 13), fg="yellow")
console_panel.add(console)

t_console = Text(console, height=50, width=70, bg="#0e141e", wrap=NONE, font=("Roboto", 9), fg="#00ea64")

# Current Execution line
current_instr_label = Text(root, height=1, width=10, font=("Roboto", 12), fg="#484767")
current_instr_label.insert(END, "On Line: " + str(simu_1.PC + 1))
current_instr_label.pack()


def run_gui_data():
    t_reg.configure(state='normal')
    t_mem.configure(state='normal')
    t_user.configure(state='normal')
    t_console.configure(state='normal')

    t_reg.delete("1.0", "end")
    t_mem.delete("1.0", "end")
    t_user.delete("1.0", "end")

    # Data in Register Panel
    t_reg.insert(END, "PC = 0\n")
    k = 4
    for i in simu_1.REGISTERS:
        t_reg.insert(END, str(i) + " = " + str(simu_1.REGISTERS[i]) + "\n")
        k += 1
    t_reg.pack(side=TOP, fill=X)
    scroll_reg.config(command=t_reg.yview)

    # Data in Memory Panel
    k = 4
    for i in simu_1.RAM:
        i = re.sub(r"\n", " ", str(i))
        t_mem.insert(END, str(k - 4) + " : " + str(i) + "\n")
        k += 1
    t_mem.pack(side=TOP, fill=X)
    scroll_mem.config(command=t_mem.yview)

    # Data in User Text Panel
    k = 4
    for i in simu_1.lines:
        t_user.insert(END, str(k - 3) + " : " + str(i) + "\n")
        k += 1
    t_user.pack(side=TOP, fill=X)
    scroll_user.config(command=t_user.yview)

    # Data in console
    for i in simu_1.cnsl:
        t_console.insert(END, str(i) + " ")
    t_console.pack(side=TOP, fill=X)
    simu_1.cnsl = []

    t_reg.configure(state='disabled')
    t_mem.configure(state='disabled')
    t_user.configure(state='disabled')
    t_console.configure(state='disabled')


def modify_gui_data():
    simu_1.main()
    if simu_1.Throw_error_instr.is_error_there:
        response = 0

        def popclick():
            response = askyesno("Execution Stopped!", "Error found in your assembly code on line " +
                                str(simu_1.Throw_error_instr.line_fault + 1) + ".\n\n" + str(
                simu_1.lines[simu_1.Throw_error_instr.line_fault]) +
                                "\n\nExit?")
            if response == 1:
                root.destroy()

        if response == 1:
            root.quit()
        popclick()

    else:
        run_gui_data()
        current_instr_label.configure(state='normal')
        current_instr_label.delete("1.0", END)
        current_instr_label.insert(END, "On Line: " + str(simu_1.PC))
        current_instr_label.configure(state='disabled')
        step_exe.configure(state=DISABLED)


simu_1.pre_data_process()


def modify_gui_data_once():
    simu_1.main_once()
    # current_instr_label.grid_forget()
    current_instr_label.configure(state='normal')
    current_instr_label.delete("1.0", END)
    current_instr_label.insert(END, "On Line: " + str(simu_1.PC))
    current_instr_label.configure(state='disabled')
    if simu_1.PC >= simu_1.REGISTERS["ra"]:
        step_exe.configure(state=DISABLED)
    if simu_1.Throw_error_instr.is_error_there:
        response = 0

        def popclick():
            response = askyesno("Execution Stopped!", "Error found in your assembly code on line " +
                                str(simu_1.Throw_error_instr.line_fault + 1) + ".\n\n" + str(
                simu_1.lines[simu_1.Throw_error_instr.line_fault]) +
                                "\n\nExit?")
            if response == 1:
                root.destroy()

        if response == 1:
            root.quit()
        popclick()

    else:
        run_gui_data()


run_gui_data()
root.mainloop()
