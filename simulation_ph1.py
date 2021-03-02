import re

file = open("testingswap.asm", "r")
lines = file.readlines()
file.close()

# Global Storages
RAM = []
ram_iter = 0
ram_label = {}
instr_label = {}
PC = 0

REGISTERS = {'r': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
             's0': 0, 's1': 1, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'k0': 0, 'k1': 0}  # 29

p = 0x10008000
sp = 0x7ffff8bc
ra = 0

is_program_done = False
i = 0

# Removing all comments and unnecessary white spaces
while i < len(lines):
    lines[i] = lines[i].strip().lower()

    if re.findall(r"^# *", lines[i]) or (re.findall(r"^\n", lines[i]) and len(lines[i] == '\n'.length())):
        # print("it is a comment")  # comment can be added in middle also
        lines.remove(lines[i])
        i -= 1
    if len(lines[i]) == 0:
        lines.remove(lines[i])
        i -= 1

    i += 1

i = 0

# Processing all input data
while i < len(lines):
    # .data
    if re.search(r"^\.data", lines[i]):

        while True:
            i += 1

            # Process data segment until .text is seen
            if re.findall(r"^\.text", lines[i]):
                i -= 1
                break

            # Process labels
            if lines[i][0] != '.':
                s = lines[i].split(sep=':', maxsplit=1)  # new line after label for .word
                lines[i] = s[1][1:]
                s = s[0]
                ram_label[s] = ram_iter

            if re.findall(r"^\.word", lines[i]):
                line = lines[i][6:]
                line = re.sub(r',', '', line)
                line = line.split(sep=' ')  # rm spaces for array
                for l in line:
                    RAM.append(int(l))
                ram_iter += 1

            elif re.findall(r"^\.asciiz", lines[i]):
                line = lines[i][9:len(lines[i]) - 1]
                RAM.append(line)
                ram_iter += 1
    if re.findall(r"^\.globl", lines[i]):
        i -= 1
        break
    i += 1

print(RAM)
PC = i

# Removing all comments from inside instruction lines
while i < len(lines):
    pos = lines[i].find('#')
    if pos >= 0:
        j = pos
        while lines[i][j - 1] == ' ':
            j -= 1;
        lines[i] = lines[i][: j]

    i += 1


def add_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])

    REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) + int(REGISTERS[instr_line[2]])

    return PC + 1


def sub_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])

    REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) - int(REGISTERS[instr_line[2]])

    return PC + 1


def lw_instr(instr_line):
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])
    adv = (int(instr_line[1].strip()[0]) // 4) + (int(instr_line[1].strip()[4:5]))
    instr_line[1] = str(instr_line[1].strip()[3:5])

    REGISTERS[instr_line[0]] = RAM[REGISTERS[instr_line[1]] + adv]  # To change register into memory

    return PC + 1


def sw_instr(instr_line):
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])
    adv = (int(instr_line[1].strip()[0]) // 4) + (int(instr_line[1].strip()[4:5]))
    instr_line[1] = str(instr_line[1].strip()[3:5])

    RAM[REGISTERS[instr_line[1]] + adv] = int(REGISTERS[instr_line[0]])  # To change register into memory
    return PC + 1


def bne_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2][1:]
    if REGISTERS[instr_line[0]] == REGISTERS[instr_line[1]]:
        return PC + 1

    return int(instr_label[instr_line[2]])


def beq_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2][1:]
    if REGISTERS[instr_line[0]] != REGISTERS[instr_line[1]]:
        return PC + 1

    return int(instr_label[instr_line[2]])


def j_instr(instr_line):
    return instr_label[instr_line]


def lui_instr(instr_line):
    REGISTERS[instr_line[0]] = 0
    return PC + 1


def sll_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])

    REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) * pow(2, int(instr_line[2]))

    return PC + 1


# Finding the type of current instruction to be parsed
def find_instr_type(line):
    if re.findall(r"\w?\w: ", line):
        label = line.split(sep=":", maxsplit=1)
        line = label[1][1:]
        label = label[0]
        instr_label[label] = PC

    instr_word = line.split(sep=" ", maxsplit=1)
    instr_line = instr_word[1]
    instr_word = instr_word[0]

    if instr_word == 'add':
        return add_instr(instr_line)
    elif instr_word == 'sub':
        return sub_instr(instr_line)
    elif instr_word == 'bne':
        return bne_instr(instr_line)
    elif instr_word == 'beq':
        return beq_instr(instr_line)
    elif instr_word == 'j':
        return j_instr(instr_line)
    elif instr_word == 'lw':
        return lw_instr(instr_line)
    elif instr_word == 'sw':
        return sw_instr(instr_line)
    elif instr_word == 'lui':
        return lui_instr(instr_line)
    elif instr_word == 'sll':
        return sll_instr(instr_line)
    elif instr_word == 'jr':
        return REGISTERS[ra]
    else:
        print("Invalid Instruction Set. Abort")
        return len(lines)


# Find main label
while PC < len(lines):
    if re.findall(r"^main:", lines[PC]):
        instr_label["main"] = PC
        PC += 1
        break
    PC += 1
REGISTERS[ra] = len(lines)

# Process instructions
while PC < len(lines):
    PC = find_instr_type(lines[PC])

print(RAM)
print("=" * 100)
print(REGISTERS)
