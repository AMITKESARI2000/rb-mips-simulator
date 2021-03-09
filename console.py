import tkinter as tk
import simu

console = tk.Tk()
console.title("CONSOLE")

console_body = tk.PanedWindow(orient=tk.VERTICAL, width=600, height=400, bg="grey")
console_body.pack(fill=tk.BOTH, expand = 1)

scroll_reg = tk.Scrollbar(console_body,orient="vertical")
cnsprnt = tk.Text(console_body, wrap = tk.NONE, yscrollcommand = scroll_reg.set, font=("Arial", 9))

def console_print(x):
    cnsprnt.configure(state='normal')
    cnsprnt.insert(tk.END, str(x)+'\n')



console.mainloop()