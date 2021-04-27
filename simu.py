import re
import cache

file = open("./testingswap.asm", "r")

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
syscall_array = []


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
             's0': "0x1001", 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0,
             't0': 0, 't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
             'r': 0, 'k0': 0, 'k1': 0, 'sp': '0x20000'}  # 32

BaseAdr = "0x1001"

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
            label_name_array = lines[i].split(sep=":", maxsplit=1)
            label_name = label_name_array[0].strip()
            if len(label_name_array[1]) == 0:
                lines.remove(lines[i])
            instr_label[label_name] = i

        i += 1

    # Process syscalls
    i = PC
    while i < len(lines):
        if re.findall(r"^syscall", lines[i]):
            syscall_array.append(i - 1)
            lines.remove(lines[i])

        i += 1
    REGISTERS["ra"] = len(lines)


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


def memory_op(instr_word, instr_line, adv):
    if instr_word == "lw":
        # To load register from memory
        # result_MEM = RAM[int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv]

        result_MEM, stalls_MEM = cache.CacheOP.cache_hit_1(int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv)

    elif instr_word == "sw":
        # To store register into memory
        # result_MEM = RAM[int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv] = int(REGISTERS[instr_line[0]])

        RAM[int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv] = int(REGISTERS[instr_line[0]])
        cache.CacheOP.insert_cache1(int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv)
        cache.CacheOP.insert_cache1(int(REGISTERS[instr_line[1]][2:]) - int(BaseAdr[2:]) + adv)
        result_MEM = 0
        stalls_MEM = 0

    return result_MEM, stalls_MEM


def write_back_op(instr_line, result_MEM_ALU):
    try:
        REGISTERS[instr_line[0]] = result_MEM_ALU
        return 1
    except:
        return -1


# Define the functions for simulating
def add_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])

    # If address is stored add subtract only val/4 because of indexing
    # add $t2, $zero, $s0
    if isinstance(REGISTERS[instr_line[1]], str) and isinstance(REGISTERS[instr_line[2]], int):
        result_ALU = int(REGISTERS[instr_line[1]][2:]) + int(REGISTERS[instr_line[2]]) // 4
        result_ALU = "0x" + str(result_ALU)
        return result_ALU, instr_line
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], str):
        result_ALU = int(REGISTERS[instr_line[1]]) // 4 + int(REGISTERS[instr_line[2]][2:])
        result_ALU = "0x" + str(result_ALU)
        return result_ALU, instr_line

    # Normal add instruction of register having two ints
    # add $t2, $t1, $t0
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], int):
        result_ALU = int(REGISTERS[instr_line[1]]) + int(REGISTERS[instr_line[2]])
        return result_ALU, instr_line

    else:
        print("Invalid instruction format for add.")
    return -1, instr_line


def sub_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])
    if isinstance(REGISTERS[instr_line[1]], str) and isinstance(REGISTERS[instr_line[2]], int):
        result_ALU = int(REGISTERS[instr_line[1]][2:]) - int(REGISTERS[instr_line[2]]) // 4
        result_ALU = "0x" + str(result_ALU)
        return result_ALU, instr_line
    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], str):
        result_ALU = int(REGISTERS[instr_line[1]]) // 4 - int(REGISTERS[instr_line[2]][2:])
        result_ALU = "0x" + str(result_ALU)
        return result_ALU, instr_line

    elif isinstance(REGISTERS[instr_line[1]], int) and isinstance(REGISTERS[instr_line[2]], int):
        result_ALU = int(REGISTERS[instr_line[1]]) - int(REGISTERS[instr_line[2]])
        return result_ALU, instr_line

    else:
        print("Invalid instruction format for sub.")
    return -1, instr_line


def lw_instr(instr_line):
    # lw $s3, 0($t3)
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])

    instr_line[1] = instr_line[1].strip()
    adv = int(instr_line[1].split(sep="(", maxsplit=1)[0]) // 4

    instr_line[1] = instr_line[1].split(sep="$", maxsplit=1)[1][:-1]

    result_ALU = adv
    return result_ALU, instr_line


def sw_instr(instr_line):
    # sw $s3, 0($t3)
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])

    instr_line[1] = instr_line[1].strip()
    adv = int(instr_line[1].split(sep="(", maxsplit=1)[0]) // 4

    instr_line[1] = instr_line[1].split(sep="$", maxsplit=1)[1][:-1]

    result_ALU = adv
    return result_ALU, instr_line


def bne_instr(instr_line, index_pc):
    #  bne $t1, $s2, loop
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()
    if REGISTERS[instr_line[0]] == REGISTERS[instr_line[1]]:
        return index_pc + 1

    return int(instr_label[instr_line[2]])


def beq_instr(instr_line, index_pc):
    #  beq $t1, $s2, loop
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()
    if REGISTERS[instr_line[0]] != REGISTERS[instr_line[1]]:
        return index_pc + 1

    return int(instr_label[instr_line[2]])


def j_instr(instr_line):
    return instr_label[instr_line]


def lui_instr(instr_line):
    # lui $s0, 0x1001
    instr_line = instr_line.split(",")
    instr_line[0] = instr_line[0].strip()[1:]
    instr_line[1] = instr_line[1].strip()
    result_ALU = instr_line[1]
    global BaseAdr
    BaseAdr = str(instr_line[1])
    return result_ALU, instr_line


def addi_instr(instr_line):
    # addi $s2, $s2, -1
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[2] = instr_line[2].strip()

    if isinstance(REGISTERS[instr_line[1]], str):
        result_ALU = int(REGISTERS[instr_line[1]][2:]) + int(instr_line[2]) // 4
        result_ALU = "0x" + str(result_ALU)
        return result_ALU, instr_line
    else:
        result_ALU = int(REGISTERS[instr_line[1]]) + int(instr_line[2])
        return result_ALU, instr_line


def li_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])
    instr_line[1] = instr_line[1].strip()
    result_ALU = int(instr_line[1])

    return result_ALU, instr_line


def sll_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])

    result_ALU = int(REGISTERS[instr_line[1]]) * pow(2, int(instr_line[2]))

    return result_ALU, instr_line


def srl_instr(instr_line):
    instr_line = instr_line.split(",")
    for l in range(len(instr_line) - 1):
        instr_line[l] = str(instr_line[l].strip()[1:])

    result_ALU = int(REGISTERS[instr_line[1]]) // pow(2, int(instr_line[2]))

    return result_ALU, instr_line


def la_instr(instr_line):
    # la $a0, space
    instr_line = instr_line.split(",")
    instr_line[0] = str(instr_line[0].strip()[1:])
    instr_line[1] = str(instr_line[1].strip())

    # Getting adr of label

    result_ALU = int(BaseAdr[2:]) + ram_label[instr_line[1]]
    result_ALU = "0x" + str(result_ALU)

    return result_ALU, instr_line


def slt_instr(instr_line):
    # slt $t4, $s3, $s4               #set $t4 = 1 if $s3 < $s4
    instr_line = instr_line.split(",")

    for l in range(len(instr_line)):
        instr_line[l] = str(instr_line[l].strip()[1:])
    # print("sltsltsltsltsltsltsltslt=> ", instr_line[1], instr_line[2], REGISTERS[instr_line[1]], REGISTERS[instr_line[2]])
    result_ALU = int(int(REGISTERS[instr_line[1]]) < int(REGISTERS[instr_line[2]]))

    return result_ALU, instr_line


def syscall_instr(index_pc):
    l_type = lines[index_pc]
    l_type = l_type.split(sep=" ")
    l_type[0] = l_type[0].strip()
    l_type[1] = l_type[1].strip()[1:-1]
    l_type[2] = l_type[2].strip()
    if l_type[0] == "li" and l_type[1][0] == 'v':
        # For exit
        #   li $v0, 10
        #   syscall

        if int(l_type[2]) == 10:
            print("Exit syscall!")
            return REGISTERS["ra"]

    else:
        # Others
        # li $v0, 4
        # la $a0, space
        # syscall

        l_print = l_type
        l_type = lines[index_pc - 1]

        l_type = l_type.split(sep=" ")
        l_type[0] = l_type[0].strip()
        l_type[1] = l_type[1].strip()[1:-1]
        l_type[2] = l_type[2].strip()

        if int(l_type[2]) == 1:
            # Print register value
            cnsl.append(REGISTERS[l_print[1]])
            print("From syscall console: ", REGISTERS[l_print[1]])

        elif int(l_type[2]) == 4:
            # Print asciiz text
            cnsl.append(RAM[ram_label[l_print[2]]])
            print(RAM[ram_label[l_print[2]]])

    # return PC + 1


# Finding the type of current instruction to be parsed
def find_instr_type(line):
    # Checking for labels beforehand
    """Since labels have been removed, check is not req
    if re.findall(r"^\w*\s*:", line):
        label = line.split(sep=":", maxsplit=1)
        line = label[1].strip()
        label = label[0].strip()
        instr_label[label] = PC
        if line == '':
            return PC + 1
    """
    instr_line = ""
    instr_word = line.split(sep=" ", maxsplit=1)
    try:
        instr_line = instr_word[1]
    except:
        pass
    instr_word = instr_word[0]

    return instr_word, instr_line


def execute_ALU(instr_word, instr_line):
    # Switching:
    if instr_word == 'add':
        return add_instr(instr_line)
    elif instr_word == 'sub':
        return sub_instr(instr_line)
    # elif instr_word == 'bne':
    #     return bne_instr(instr_line)
    # elif instr_word == 'beq':
    #     return beq_instr(instr_line)
    # elif instr_word == 'j':
    #     return j_instr(instr_line)
    elif instr_word in ("bne", "beq", "j"):
        # pass
        return 0, 0
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
        return REGISTERS["ra"], instr_line
    elif instr_word == 'li':
        return li_instr(instr_line)
    elif instr_word == 'la':
        return la_instr(instr_line)
    elif instr_word == 'slt':
        return slt_instr(instr_line)

    elif instr_word == 'syscall':
        return syscall_instr()

    elif instr_word == 'nop':
        return 0, 0
    else:
        print("Invalid Instruction Set ", instr_word, " !!! Aborting...")
        Throw_error_instr.error_occurred(PC)

        return len(lines)

# rm_comments()
# main()
