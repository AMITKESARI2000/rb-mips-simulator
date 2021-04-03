import re

file = open("bubblesort.asm", "r")
lines = file.readlines()
file.close()

# Global Storages
global RAM, ram_iter, ram_label, instr_label, PC, i, cnsl
RAM = []
ram_iter = 0
ram_label = {}
instr_label = {}
PC = 0
cnsl = []


class InstrSyntaxError:
    def __init__(self, is_error_there, line_fault):
        self.is_error_there = is_error_there
        self.line_fault = line_fault

    def error_occurred(self, index):
        print("Syntax Error occurred on line '", lines[index], "'. Please fix it.")
        self.is_error_there = True
        self.line_fault = index
        global PC
        PC = REGISTERS["ra"]


Throw_error_instr = InstrSyntaxError(is_error_there=False, line_fault=0)

REGISTERS = {'zero': 0, 'ra': 0, 'at': 0, 'v0': 0, 'v1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0,
             's0': 0, 's1': 1, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'r': 0, 'k0': 0, 'k1': 0, 'sp': '0x20000'}  # 32

BaseAdr = "0x1000"

is_program_done = False


# Removing all comments and unnecessary white spaces
def rm_comments():
    i = 0
    while i < len(lines):
        lines[i] = lines[i].strip()

        if re.findall(r"^# *", lines[i]) or (re.findall(r"^\n", lines[i]) and len(lines[i] == '\n'.length())):
            lines.remove(lines[i])
            i -= 1
        if len(lines[i]) == 0:
            lines.remove(lines[i])
            i -= 1

        i += 1


def pre_data_process():
    # Processing all input data
    RAM.clear()
    i = 0
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
                    lines[i] = s[1].strip()
                    s = s[0].strip()
                    global ram_iter
                    ram_label[s] = ram_iter

                # Process int values
                if re.findall(r"^\.word", lines[i]):
                    line = lines[i][6:]
                    # line = re.sub(r',', '', line)
                    line = line.split(sep=',')  # rm spaces for array
                    for l in line:
                        l = l.strip()
                        RAM.append(int(l))
                        ram_iter += 1

                # Process strings
                elif re.findall(r"^\.asciiz", lines[i]):
                    line = lines[i][9:len(lines[i]) - 1]
                    line = re.sub(r"\\n", "\n", line)
                    line = re.sub(r"\\t", "\t", line)
                    RAM.append(line)
                    ram_iter += 1

                else:
                    Throw_error_instr.error_occurred(i)
                    return
        if re.findall(r"^\.globl", lines[i]):
            i += 1
            break

        i += 1

    print("Initial Memory:\n", RAM)
    print("=" * 100)
    global PC
    PC = i
    REGISTERS["ra"] = len(lines)

    # Removing all comments from instruction lines
    while i < len(lines):
        pos = lines[i].find('#')
        if pos >= 0:
            j = pos
            while lines[i][j - 1] == ' ':
                j -= 1
            lines[i] = lines[i][:j]

        i += 1

    # Preprocess all labels
    i = PC
    while i < len(lines):
        if re.findall(r"^\w*:", lines[i]):
            label_name = lines[i].split(sep=":", maxsplit=1)[0].strip()
            instr_label[label_name] = i

        i += 1


def main():
    pre_data_process()

    while PC < len(lines):
        main_once()

    print("Final Memory state: \n", RAM)
    print("=" * 100)
    print("Register values: \n", REGISTERS)


def main_once():
    # Process instructions line by line
    global PC

    PC = find_instr_type(lines[PC])


# Define the functions for simulating
def add_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])

    # If address is stored add subtract only val/4 because of indexing
    # add $t2, $zero, $s0
    if isinstance(REGISTERS[instr_line[1]], str) and isinstance(REGISTERS[instr_line[2]], int):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]][2:]) + int(REGISTERS[instr_line[2]]) // 4
        REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], str):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) // 4 + int(REGISTERS[instr_line[2]][2:])
        REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])

    # Normal add instruction of register having two ints
    # add $t2, $t1, $t0
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], int):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) + int(REGISTERS[instr_line[2]])

    else:
        print("Invalid instruction format.")
    return PC + 1


def sub_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])
    if isinstance(REGISTERS[instr_line[1]], str) and isinstance(REGISTERS[instr_line[2]], int):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]][2:]) - int(REGISTERS[instr_line[2]]) // 4
        REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], str):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) // 4 - int(REGISTERS[instr_line[2]][2:])
        REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])

    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], int):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) - int(REGISTERS[instr_line[2]])

    else:
        print("Invalid instruction format.")
    return PC + 1


def lw_instr(instr_line):
    # lw $s3, 0($t3)
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])

    instr_line[1] = instr_line[1].strip()
    adv = int(instr_line[1].split(sep="(", maxsplit=1)[0]) // 4

    instr_line[1] = instr_line[1].split(sep="$", maxsplit=1)[1][:-1]

    # To load register from memory
    REGISTERS[instr_line[0]] = RAM[int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv]

    return PC + 1


def sw_instr(instr_line):
    # sw $s3, 0($t3)
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])

    instr_line[1] = instr_line[1].strip()
    adv = int(instr_line[1].split(sep="(", maxsplit=1)[0]) // 4

    instr_line[1] = instr_line[1].split(sep="$", maxsplit=1)[1][:-1]

    # To store register into memory
    RAM[int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv] = int(REGISTERS[instr_line[0]])
    return PC + 1


def bne_instr(instr_line):
    #  bne $t1, $s2, loop
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()
    if REGISTERS[instr_line[0]] == REGISTERS[instr_line[1]]:
        return PC + 1

    return int(instr_label[instr_line[2]])


def beq_instr(instr_line):
    #  beq $t1, $s2, loop
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()
    if REGISTERS[instr_line[0]] != REGISTERS[instr_line[1]]:
        return PC + 1

    return int(instr_label[instr_line[2]])


def j_instr(instr_line):
    return instr_label[instr_line]


def lui_instr(instr_line):
    # lui $s0, 0x1001
    instr_line = instr_line.split(",")
    instr_line[0] = instr_line[0].strip()[1:]
    instr_line[1] = instr_line[1].strip()
    REGISTERS[instr_line[0]] = instr_line[1]
    global BaseAdr
    BaseAdr = str(instr_line[1])
    return PC + 1


def addi_instr(instr_line):
    # addi $s2, $s2, -1
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()

    if isinstance(REGISTERS[instr_line[1]], str):
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]][2:]) + int(instr_line[2]) // 4
        REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])
    else:
        REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) + int(instr_line[2])

    return PC + 1


def li_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[1] = instr_line[1].strip()
    REGISTERS[instr_line[0]] = int(instr_line[1])

    return PC + 1


def sll_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])

    REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) * pow(2, int(instr_line[2]))

    return PC + 1


def srl_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])

    REGISTERS[instr_line[0]] = int(REGISTERS[instr_line[1]]) // pow(2, int(instr_line[2]))

    return PC + 1


def la_instr(instr_line):
    # la $a0, space
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])
    instr_line[1] = str(instr_line[1].strip())

    # Getting adr of label
    REGISTERS[instr_line[0]] = int(BaseAdr[2:]) + ram_label[instr_line[1]]
    REGISTERS[instr_line[0]] = "0x" + str(REGISTERS[instr_line[0]])

    return PC + 1


def slt_instr(instr_line):
    # slt $t4, $s3, $s4               #set $t4 = 1 if $s3 < $s4
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])
    REGISTERS[instr_line[0]] = int(int(REGISTERS[instr_line[1]]) < int(REGISTERS[instr_line[2]]))

    return PC + 1


def syscall_instr():
    l_type = lines[PC - 1]
    l_type = l_type.split(sep=" ")
    l_type[0] = l_type[0].strip()
    l_type[1] = l_type[1].strip()[1:-1]
    l_type[2] = l_type[2].strip()
    if l_type[0] == "li" and l_type[1][0] == 'v':
        # For exit
        #   li $v0, 10
        #   syscall

        if int(l_type[2]) == 10:
            return REGISTERS["ra"]

    else:
        # Others
        # li $v0, 4
        # la $a0, space
        # syscall

        l_print = l_type
        l_type = lines[PC - 2]

        l_type = l_type.split(sep=" ")
        l_type[0] = l_type[0].strip()
        l_type[1] = l_type[1].strip()[1:-1]
        l_type[2] = l_type[2].strip()

        if int(l_type[2]) == 1:
            # Print register value
            cnsl.append(REGISTERS[l_print[1]])
            print(REGISTERS[l_print[1]])

        elif int(l_type[2]) == 4:
            # Print asciiz text
            cnsl.append(RAM[ram_label[l_print[2]]])
            print(RAM[ram_label[l_print[2]]])

    return PC + 1


# Finding the type of current instruction to be parsed
def find_instr_type(line):
    # Checking for labels beforehand
    if re.findall(r"^\w*\s*:", line):
        label = line.split(sep=":", maxsplit=1)
        line = label[1].strip()
        label = label[0].strip()
        instr_label[label] = PC
        if line == '':
            return PC + 1

    instr_word = line.split(sep=" ", maxsplit=1)
    try:
        instr_line = instr_word[1]
    except:
        pass
    instr_word = instr_word[0]

    # Switching:
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
    elif instr_word == 'addi':
        return addi_instr(instr_line)
    elif instr_word == 'sll':
        return sll_instr(instr_line)
    elif instr_word == 'srl':
        return srl_instr(instr_line)
    elif instr_word == 'jr':
        return REGISTERS["ra"]
    elif instr_word == 'li':
        return li_instr(instr_line)
    elif instr_word == 'la':
        return la_instr(instr_line)
    elif instr_word == 'slt':
        return slt_instr(instr_line)

    elif instr_word == 'syscall':
        return syscall_instr()
    else:
        print("Invalid Instruction Set ", instr_word, " !!! Aborting...")
        Throw_error_instr.error_occurred(PC)

        return len(lines)

