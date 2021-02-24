import re

file = open("testingswap.s", "r")
lines = file.readlines()
file.close()

# Global Storages
RAM = []
ram_iter = 0
ram_label = {}
instr_label = {}
PC = 0

r = [0]
at = 0
v = [0] * 2
a = [0] * 4
t = [0] * 10
s = [0] * 9
k = [0] * 2
p = 0x10008000
sp = 0x7ffff8bc
ra = 0

is_program_done = False
i = 0

# Removing all comments and unnecessary white spaces
while i < len(lines):
    lines[i] = lines[i].strip().lower()
    # print(i, line)

    if re.findall(r"# *", lines[i]) or (re.findall(r"^\n", lines[i]) and len(lines[i] == '\n'.length())):
        # print("it is a comment")  # comment can be added in middle also
        lines.remove(lines[i])
        i -= 1
    if len(lines[i]) == 0:
        lines.remove(lines[i])
        i -= 1

    i += 1

i = 0
while i < len(lines):

    # .data
    if re.search(r"^\.data", lines[i]):
        print("data", lines[i])

        while True:
            lines[i] = lines[i].strip().lower()
            i += 1
            print(lines[i])

            if re.findall(r"^\.text", lines[i]):
                i -= 1;
                break

            if lines[i][0] != '.':
                s = lines[i].split(sep=':', maxsplit=1)         # new line after label for .word
                lines[i] = s[1][1:]
                s = s[0]
                ram_label[s] = ram_iter
                print(s)

            if re.findall(r"^\.word", lines[i]):
                line = lines[i][6:]
                line = re.sub(r',', '', line)
                line = line.split(sep=' ')
                RAM.append(list(map(int, line)))
                print(RAM)
                ram_iter += 1

            elif re.findall(r"^\.asciiz", lines[i]):
                line = lines[i][9:len(lines[i]) - 1]
                RAM.append(line)
                print(RAM)
                ram_iter += 1
    if re.findall(r"^\.globl", lines[i]):
        i -= 1;
        break
    i += 1

def instr_type (line):
    s = line.split(sep=" ", maxsplit=1)[0]
    add = 0
    sub = 1
    bne = 2
    beq = 3
    jump = 4
    lw = 5
    sw = 6
    lui = 7
    sll = 8
    if (s == 'add'):
        return add
    elif (s == 'sub'):
        return sub
    elif (s == 'bne'):
        return bne
    elif (s == 'beq'):
        return beq
    elif (s == 'jump'):
        return jump
    elif (s == 'lw'):
        return lw
    elif (s == 'sw'):
        return sw
    elif (s == 'lui'):
        return lui
    elif (s == 'sll'):
        return sll

while i < len(lines):
    if re.findall(r"^\.main", lines[i]):
        n = instr_type(lines[i])
        print(n)
    i +=1

