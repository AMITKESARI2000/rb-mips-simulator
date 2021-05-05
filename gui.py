from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno

import cache
import simu
import pipeline

root = Tk()
# root.resizable(width=False, height=False) #Restricting Resizable
root.title("RB Mips simulator 😎")

notebook = ttk.Notebook(root)
notebook.pack(expand=True)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)

notebook.add(frame1, text='General Info')
notebook.add(frame2, text='Pipeline Details')

# =====================================FRAME 1==================================================
# Panel
simulator_body = PanedWindow(frame1, orient=VERTICAL, width=1024, height=640, bg="black")
simulator_body.pack(fill=BOTH, expand=1)

# Head Panel
head_panel = PanedWindow(simulator_body, bd=1, relief="raised", bg="black")
simulator_body.add(head_panel)

head = Label(head_panel, text="SIMULATOR", font=("Arial", 14))
head_panel.add(head)

# Menu Panel
menu_panel = PanedWindow(simulator_body, orient=HORIZONTAL, bd=1, relief="raised", bg="white")
simulator_body.add(menu_panel)

step_exe = Button(menu_panel, text="Step By Step Execution", bg="#f94b5d", fg="#efefef",
                  command=lambda: modify_gui_data_once()).pack(side=LEFT)
space1 = Button(menu_panel, text="   ", bg="white", state=DISABLED).pack(side=LEFT)
once_exe = Button(menu_panel, text="At Once Execution", bg="#f94b5d", fg="#efefef",
                  command=lambda: modify_gui_data()).pack(side=LEFT)
space2 = Button(menu_panel, text="   ", bg="white", state=DISABLED).pack(side=LEFT)
upload_file = Button(menu_panel, text="Upload a File", bg="#2f6fca", fg="#efefef",
                     command=lambda: UploadAction()).pack(side=LEFT)
space3 = Button(menu_panel, text="   ", bg="white", state=DISABLED).pack(side=LEFT)
settings = Button(menu_panel, text="Cache Settings", bg="#2f6fca", fg="#efefef",
                  command=lambda: change_settings()).pack(side=LEFT)
space4 = Button(menu_panel, text="   ", bg="white", state=DISABLED).pack(side=LEFT)
forwarding = Checkbutton(menu_panel, text="Forwarding", variable=pipeline.forward_enable, onvalue=True, offvalue=False,
                         command=lambda: forWarding(), bg='#2f6fca', fg='#e5e5e5', selectcolor="black", relief="raised")
forwarding.pack(side=LEFT)

# Body Panel
body_panel = PanedWindow(simulator_body, orient=HORIZONTAL, bd=1, relief="raised", bg="black", height=400)
simulator_body.add(body_panel)

# Register Panel
reg_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black", width=200, height=400)
body_panel.add(reg_panel)

# Memory Panel
mem_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black", width=200, height=400)
body_panel.add(mem_panel)

# User Text Panel
user_panel = PanedWindow(body_panel, orient=VERTICAL, bd=1, relief="raised", bg="black", width=900, height=400)
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
user_body = PanedWindow(user_panel, bg="white", height=50)

reg_panel.add(reg_body)
mem_panel.add(mem_body)
user_panel.add(user_body)

scroll_reg = Scrollbar(reg_body, orient="vertical")
scroll_mem = Scrollbar(mem_body, orient="vertical")
scroll_user = Scrollbar(user_body, orient="vertical")
scroll_reg.pack(side=RIGHT, fill=Y)
scroll_mem.pack(side=RIGHT, fill=Y)
scroll_user.pack(side=RIGHT, fill=Y)

t_reg = Text(reg_body, height=300, width=150, wrap=NONE, yscrollcommand=scroll_reg.set, font=("Roboto", 9))
t_mem = Text(mem_body, height=300, width=150, wrap=NONE, yscrollcommand=scroll_mem.set, font=("Roboto", 9))
t_user = Text(user_body, height=12, width=500, wrap=NONE, yscrollcommand=scroll_user.set, font=("Roboto", 9))

# Console Panel
console_panel = PanedWindow(user_panel, orient="vertical", relief="raised", bg="white", height=50)
user_panel.add(console_panel)

console_head = Label(console_panel, text="CONSOLE", relief="raised", height=1, font=("Arial", 10))
console_panel.add(console_head)

console = Label(console_panel, bg="black", font=("Arial", 13), fg="yellow")
console_panel.add(console)

t_console = Text(console, height=20, width=70, bg="#0e141e", wrap=NONE, font=("Roboto", 9), fg="#00ea64")

# Extra info panel
info_panel = PanedWindow(simulator_body, relief="raised", bd=1, bg="black", width=1300, orient=VERTICAL)
simulator_body.add(info_panel)

# info_head = Label(info_panel, text="INFO", relief="raised", height=1, font=("Arial", 10), width=1300)
# info_panel.add(info_head)

info = Label(info_panel, bg="white", font=("Arial", 13), fg="black")
info_panel.add(info)

t_info = Text(info, height=7, width=70, bg="#0e141e", wrap=NONE, font=("Roboto", 9), fg="#00ea64")

# Default Cache Information
cache_panel = PanedWindow(info_panel, relief="raised", bd=1, bg="white", width=1300, height=10)
info_panel.add(cache_panel)

cache_info = Label(cache_panel, bg="white", fg="black")
cache_panel.add(cache_info)

t_cache = Text(cache_info, wrap=NONE, font=("Roboto", 9), fg="black")
t_cache.insert(END, "Size of Cache 1 (in B): " + str(cache.cache1_size) + " || ")
t_cache.insert(END, "Size of Cache 2 (in B): " + str(cache.cache2_size) + " || ")
t_cache.insert(END, "Size of Block 1 (in B): " + str(cache.block1_size) + " || ")
t_cache.insert(END, "Size of Block 2 (in B): " + str(cache.block2_size) + " || ")
t_cache.insert(END, "Associativity of Cache 1: " + str(cache.assoc1) + " || ")
t_cache.insert(END, "Associativity of Cache 2: " + str(cache.assoc2) + "\n\n")
t_cache.insert(END, "Stalls of Cache 1: " + str(cache.stalls1) + " || ")
t_cache.insert(END, "Stalls of Cache 2: " + str(cache.stalls2) + " || ")
t_cache.insert(END, "Stalls of Memory: " + str(cache.stalls3))
t_cache.pack(side=TOP, fill=X)

current_instr_label = Text(menu_panel, height=1, width=10, font=("Roboto", 12), fg="#484767")

# =====================================FRAME 2==================================================
# Panel
simulator2_body = PanedWindow(frame2, orient=VERTICAL, width=1024, height=640, bg="black")
simulator2_body.pack(fill=BOTH, expand=1)

# Head Panel
head2_panel = PanedWindow(simulator2_body, bd=1, relief="raised", bg="black")
simulator2_body.add(head2_panel)

head2 = Label(head2_panel, text="SIMULATOR", font=("Arial", 14))
head2_panel.add(head2)

# Body Panel
body2_panel = PanedWindow(simulator2_body, bd=1, relief="raised", bg="black", orient=VERTICAL)
simulator2_body.add(body2_panel)

# Body head
body2_head = Label(body2_panel, text="Visualisation of Pipelining", font=("Arial", 14))
body2_panel.add(body2_head)

# Body body
body2_body = PanedWindow(body2_panel, bd=1, relief="raised", bg="black")
body2_panel.add(body2_body)

# Pipeline Details
pipe_detail = Label(body2_body, bg="white", fg="black", height=600)
body2_body.add(pipe_detail)

scroll_pipe = Scrollbar(pipe_detail, orient="vertical")
scroll_pipe.pack(side=RIGHT, fill=Y)

t_pipe = Text(pipe_detail, wrap=NONE, font=("Roboto", 9), fg="black", height=600, yscrollcommand=scroll_pipe.set)


def run_gui_data():
    t_reg.configure(state='normal')
    t_mem.configure(state='normal')
    t_user.configure(state='normal')
    t_console.configure(state='normal')
    t_info.configure(state='normal')
    current_instr_label.configure(state='normal')
    t_pipe.configure(state='normal')

    t_reg.delete("1.0", "end")
    t_mem.delete("1.0", "end")
    t_user.delete("1.0", "end")
    t_info.delete("1.0", "end")
    current_instr_label.delete("1.0", "end")
    t_pipe.delete("1.0", "end")

    # Data in Register Panel
    t_reg.insert(END, "PC = 0\n")
    k = 4
    for i in simu.REGISTERS:
        t_reg.insert(END, str(i) + " = " + str(simu.REGISTERS[i]) + "\n")
        k += 1
    t_reg.pack(side=TOP, fill=X)
    scroll_reg.config(command=t_reg.yview)

    # Data in Memory Panel
    k = 4
    for i in simu.RAM:
        i = re.sub(r"\n", " ", str(i))
        t_mem.insert(END, str(k - 4) + " : " + str(i) + "\n")
        k += 1
    t_mem.pack(side=TOP, fill=X)
    scroll_mem.config(command=t_mem.yview)

    # Data in User Text Panel
    k = 4
    for i in simu.lines:
        t_user.insert(END, str(k - 3) + " : " + str(i) + "\n")
        k += 1
    t_user.pack(side=TOP, fill=X)
    scroll_user.config(command=t_user.yview)

    # Data in console
    for i in simu.cnsl:
        t_console.insert(END, str(i) + " ")
    t_console.pack(side=TOP, fill=X)
    simu.cnsl = []

    # Data in info
    ipc = (pipeline.CLOCK_OF_GOD / (pipeline.STALL_OF_GOD + 1))
    if ipc != 0.0:
        ipc = ipc ** -1
    t_info.insert(END, "INFO: \n\n")
    t_info.insert(END, "Total Clock Cycles: " + str(pipeline.CLOCK_OF_GOD) + "\n")
    t_info.insert(END, "Total Stalls: " + str(pipeline.STALL_OF_GOD) + "\n")
    t_info.insert(END, "Total Cache Miss: " + str(cache.CACHE_MISS) + "\n")
    t_info.insert(END, "IPC: " + str(ipc) + "\n")
    t_info.pack(side=TOP, fill=X)

    # Current Execution line
    current_instr_label.insert(END, "On Line: " + str(pipeline.Pipeline_units[0].current_instr_line + 1))
    current_instr_label.pack()

    # Pipeline Details
    for i in pipeline.PIPELINE_DETAILS:
        for j in i:
            t_pipe.insert(END, str(j) + "\n")
        t_pipe.insert(END, "." * 100 + "\n")
    t_pipe.pack(side=TOP, fill=X)
    scroll_pipe.config(command=t_pipe.yview)

    t_reg.configure(state='disabled')
    t_mem.configure(state='disabled')
    t_user.configure(state='disabled')
    t_console.configure(state='disabled')
    t_info.configure(state='disabled')
    current_instr_label.configure(state='disabled')
    t_pipe.configure(state='disabled')


def modify_gui_data():
    simu.main()
    if simu.Throw_error_instr.is_error_there:
        response = 0

        def popclick():
            response = askyesno("Execution Stopped!!!", "Error found in your assembly code on line " +
                                str(simu.Throw_error_instr.line_fault + 1) + ".\n\n" + str(
                simu.lines[simu.Throw_error_instr.line_fault]) +
                                "\n\nExit?")
            if response == 1:
                root.destroy()

        if response == 1:
            root.quit()
        popclick()

    else:
        pipeline.program_execution()
        pipeline.pipelining()
        pipeline.print_info()
        run_gui_data()
        # current_instr_label.configure(state='normal')
        # current_instr_label.delete("1.0", END)
        # current_instr_label.insert(END, "On Line: " + str(simu.PC))
        # current_instr_label.configure(state='disabled')
        # step_exe.configure(state=DISABLED)


def modify_gui_data_once():
    simu.main_once()
    # current_instr_label.grid_forget()
    # current_instr_label.configure(state='normal')
    # current_instr_label.delete("1.0", END)
    # current_instr_label.insert(END, "On Line: " + str(simu.PC))
    # current_instr_label.configure(state='disabled')
    if simu.PC >= simu.REGISTERS["ra"]:
        step_exe.configure(state=DISABLED)
    if simu.Throw_error_instr.is_error_there:
        response = 0

        def popclick():
            response = askyesno("Execution Stopped!", "Error found in your assembly code on line " +
                                str(simu.Throw_error_instr.line_fault + 1) + ".\n\n" + str(
                simu.lines[simu.Throw_error_instr.line_fault]) +
                                "\n\nExit?")
            if response == 1:
                root.destroy()

        if response == 1:
            root.quit()
        popclick()

    else:
        run_gui_data()


def change_settings():
    global settings
    settings = Tk()
    settings.title("SETTINGS")
    cache1_size = Label(settings, text="Size of Cache 1 (in B): ").grid(row=0, column=0)
    cache1Size = Entry(settings, bd=5)
    cache1Size.grid(row=0, column=1)
    cache2_size = Label(settings, text="Size of Cache 2 (in B): ").grid(row=1, column=0)
    cache2Size = Entry(settings, bd=5)
    cache2Size.grid(row=1, column=1)
    block1_size = Label(settings, text="Size of Block 1 (in B): ").grid(row=2, column=0)
    block1Size = Entry(settings, bd=5)
    block1Size.grid(row=2, column=1)
    block2_size = Label(settings, text="Size of Block 2 (in B): ").grid(row=3, column=0)
    block2Size = Entry(settings, bd=5)
    block2Size.grid(row=3, column=1)
    assco1 = Label(settings, text="Associativity of Cache 1: ").grid(row=4, column=0)
    assc1 = Entry(settings, bd=5)
    assc1.grid(row=4, column=1)
    assco2 = Label(settings, text="Associativity of Cache 2: ").grid(row=5, column=0)
    assc2 = Entry(settings, bd=5)
    assc2.grid(row=5, column=1)
    stalls1 = Label(settings, text="Stall of Cache 1: ").grid(row=6, column=0)
    stall1 = Entry(settings, bd=5)
    stall1.grid(row=6, column=1)
    stalls2 = Label(settings, text="Stall of Cache 2: ").grid(row=7, column=0)
    stall2 = Entry(settings, bd=5)
    stall2.grid(row=7, column=1)
    stalls3 = Label(settings, text="Stall of Memory: ").grid(row=8, column=0)
    stall3 = Entry(settings, bd=5)
    stall3.grid(row=8, column=1)
    update = Button(settings, text="Update", command=lambda: [cache.update_settings(
        cache1=cache1Size.get(), cache2=cache2Size.get(), block1=block1Size.get(), block2=block2Size.get(),
        assco1=assc1.get(), assco2=assc2.get(), stall1=stall1.get(), stall2=stall2.get(), stall3=stall3.get()
    ), cancel_settings()]).grid(row=9, column=0)
    cancel = Button(settings, text="Cancel", command=lambda: cancel_settings()).grid(row=9, column=1)

    settings.mainloop()


def cancel_settings():
    # Data in Cache Info
    t_cache.configure(state='normal')
    t_cache.delete("1.0", "end")
    t_cache.insert(END, "Size of Cache 1: " + str(cache.cache1_size) + " || ")
    t_cache.insert(END, "Size of Cache 2: " + str(cache.cache2_size) + " || ")
    t_cache.insert(END, "Size of Block 1: " + str(cache.block1_size) + " || ")
    t_cache.insert(END, "Size of Block 2: " + str(cache.block2_size) + " || ")
    t_cache.insert(END, "Associativity of Cache 1: " + str(cache.assoc1) + " || ")
    t_cache.insert(END, "Associativity of Cache 2: " + str(cache.assoc2) + "\n\n")
    t_cache.insert(END, "Stalls of Cache1: " + str(cache.stalls1) + " || ")
    t_cache.insert(END, "Stalls of Cache2: " + str(cache.stalls2) + " || ")
    t_cache.insert(END, "Stalls of Memory: " + str(cache.stalls3) + " || ")
    t_cache.pack(side=TOP, fill=X)
    t_cache.configure(state='disabled')
    global settings
    settings.destroy()
    pass


def forWarding():
    if not pipeline.forward_enable:
        pipeline.forward_enable = True
        print("Data Forwarding Enabled")
    else:
        pipeline.forward_enable = False
        print("Data Forwarding Disabled")


def UploadAction():
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    # msg = Tk()
    # msgs = Message(msg, text="Selected File: " + filename)
    # msgs.pack()

    tmp = StringVar()
    tmp.set(filename.split("/")[-1])
    file_label = Label(user_head, textvariable=tmp, height=1, font=("Arial", 10), fg="#f5468c").grid(row=0, column=1)

    simu.file_add(filename)
    root.title(filename)
    run_gui_data()
    # msg.mainloop()


run_gui_data()
root.mainloop()
