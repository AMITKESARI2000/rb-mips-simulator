import simu
import re

CLOCK_OF_GOD = 0
STALL_OF_GOD = 0


class HWUnits:
    def __init__(self, current_instr_line, stalls_left, disassembled_instr, frwd):
        self.current_instr_line = current_instr_line
        self.stalls_left = stalls_left
        self.disassembled_instr = []
        # if current_instr_line - base_instr_line_PC >= 0:
        #     self.instr_breakdown(current_instr_line)
        self.frwd = frwd
        self.data = []

    @staticmethod
    def instr_breakdown(current_instr_line):
        disassembled_instr = []
        # print("crl: ",current_instr_line)
        line = simu.lines[current_instr_line].strip()
        line = line.split(sep=" ", maxsplit=1)

        disassembled_instr.append(line[0].strip())  # as sw functionality is different
        line[1] = re.findall(r"\$\w?\w\w?\w", line[1])
        for l in line[1]:
            l = l.strip()[1:]
            disassembled_instr.append(l)
        # print(self.disassembled_instr)
        return disassembled_instr

    def check_for_stall(self, index_of_HWunit, current_instr_line, existence_of_instr_line=None):

        if existence_of_instr_line is None:
            existence_of_instr_line = [0, 0, 0]
        global STALL_OF_GOD
        # Checking existence of instructions
        # print("++++++++++++++++++++++++++++++")
        s = 0

        existence_of_instr_line[0] = True  # current_instr_line - base_instr_line_PC >= 0
        existence_of_instr_line[1] = (
                Pipeline_units[0].disassembled_instr != [])  # current_instr_line - base_instr_line_PC - 1 >= 0
        existence_of_instr_line[2] = (
                Pipeline_units[1].disassembled_instr != [])  # current_instr_line - base_instr_line_PC - 2 >= 0

        # print(existence_of_instr_line[1])
        # print(existence_of_instr_line[2])

        # Breaking down of instructions
        if existence_of_instr_line[2]:
            Pipeline_units[2].disassembled_instr = Pipeline_units[1].disassembled_instr.copy()
            # print(2, Pipeline_units[2].disassembled_instr)

        if existence_of_instr_line[1]:
            Pipeline_units[1].disassembled_instr = Pipeline_units[0].disassembled_instr.copy()
            # print(1, Pipeline_units[1].disassembled_instr)

        if existence_of_instr_line[0]:
            Pipeline_units[0].disassembled_instr = self.instr_breakdown(current_instr_line)
            # print(0, Pipeline_units[0].disassembled_instr)

        # print(00, Pipeline_units[0].disassembled_instr)
        # print(11, Pipeline_units[1].disassembled_instr)
        # print(22, Pipeline_units[2].disassembled_instr)
        # print("---------------------------")

        # Checking for how many instructions to be check for dependencies.
        t = -1
        if existence_of_instr_line[0]:
            t = 0

        if existence_of_instr_line[1]:
            t = 1

        if existence_of_instr_line[2]:
            t = 2

        # Check current instr (like add or sub) dependency on prev instrs
        if Pipeline_units[0].disassembled_instr[0] in ("add", "sub"):

            for k in range(1, t + 1):

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub", "slt"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "addi":
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                if s:
                    break

        # Check current instr (like addi) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in "addi":

            for k in range(1, t + 1):
                s = 0

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    STALL_OF_GOD += 1
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "addi":
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                if s:
                    break

        # Check current instr (like sw) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in "sw":

            for k in range(1, t + 1):
                s = 0

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "addi":
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                if s:
                    break

        # Check current instr (like lw) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in "lw":

            for k in range(1, t + 1):
                s = 0

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "addi":
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                if s:
                    break

        # Check current instr (like lui, li) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in ("lui", "li", "la"):

            for k in range(1, t + 1):
                s = 0

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                if s:
                    break

        # Check current instr (like bne) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in ("bne", "beq"):
            for k in range(1, t + 1):
                s = 0

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub", "slt"):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[0].disassembled_instr[0] in "addi":
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, self.frwd)

                if s:
                    break
        return s

    @staticmethod
    def is_stall(dep_instr, frwd):

        stall = 0
        if dep_instr == 1 and frwd is False:
            stall += 2

        elif dep_instr == 2 and frwd is False:
            stall += 1

        elif dep_instr == 1 and frwd is True:
            stall += 1

        elif dep_instr == 2 and frwd is True:
            stall += 0

        print("Stall count return: " + str(stall), "for ", Pipeline_units[0].disassembled_instr)
        # self.stalls_left += stall
        global STALL_OF_GOD
        STALL_OF_GOD += stall
        return stall


# ############# Program Execution starts ############
forward_enable = False
is_Program_Done = False

simu.rm_comments()
simu.pre_data_process()
base_instr_line_PC = simu.PC

if input("Data Forwarding is disabled by default. Want to enable?(y): ").lower() == "y":
    forward_enable = True
    print("Data Forwarding Enabled")
else:
    print("Data Forwarding Disabled")

Pipeline_units = [
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # IF
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # ID
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # EX
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # MEM
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable)]  # WB


def pass_to_nextHW(index_of_HWunit):
    # If stage is not being used no stalls are there and data is forwarded to next stage
    Pipeline_units[index_of_HWunit].current_instr_line += 1


def instruction_fetch():
    fetch_line = simu.lines[Pipeline_units[0].current_instr_line]
    Pipeline_units[0].current_instr_line += 1
    # fetch_line is instr_word + instr_line
    return fetch_line


last_checked_stall_line = 0
while not is_Program_Done:
    for i in range(5):        Pipeline_units[i].stalls_left = max(0, Pipeline_units[i].stalls_left - 1)
    CLOCK_OF_GOD += 1
    print("." * 100)
    print("In Clock Cycle ", CLOCK_OF_GOD)

    # ....................................................................................................
    # WB
    if len(Pipeline_units[4].data) < 1:
        pass_to_nextHW(4)
        print("Pass WB")
    else:
        (instr_word, instr_line, result_ALU_MEM) = Pipeline_units[4].data[0]
        Pipeline_units[4].data.pop(0)
        successful_write = 1
        if instr_word not in ("sw", "bne", "beq", "jr", "j", "nop"):

            # In lw result from memory is used
            if instr_word in "lw":
                result_MEM = result_ALU_MEM
                successful_write = simu.write_back_op(instr_line, result_MEM)

            # In add/sub result from ALU is used
            elif instr_word in ("add", "sub", "lui", "addi", "li", "sll", "srl", "slt"):
                result_ALU = result_ALU_MEM
                successful_write = simu.write_back_op(instr_line, result_ALU)

            if successful_write == -1:
                # print("Error in Write Back stage. Aborting...")
                is_Program_Done = True

        print("Executed WB on line ", instr_word, instr_line)

    # .......................................................................................................
    # MEM
    if len(Pipeline_units[3].data) < 1:
        pass_to_nextHW(3)
        print("Pass MEM")
    else:
        (instr_word, instr_line, result_ALU) = Pipeline_units[3].data[0]
        Pipeline_units[3].data.pop(0)
        if instr_word in ("lw", "sw"):
            result_MEM = simu.memory_op(instr_word, instr_line, result_ALU)
            Pipeline_units[3].current_instr_line += 1
            Pipeline_units[4].data.append((instr_word, instr_line, result_MEM))
        else:
            pass_to_nextHW(3)
            Pipeline_units[4].data.append((instr_word, instr_line, result_ALU))

        print("Executed MEM on line ", instr_word, instr_line)

    # ..............................................................................................................
    # EX
    if len(Pipeline_units[2].data) < 1:
        pass_to_nextHW(2)
        print("Pass EX")
    else:

        (instr_word, instr_line) = Pipeline_units[2].data[0]
        Pipeline_units[2].data.pop(0)
        (result_ALU, instr_line) = simu.execute_ALU(instr_word, instr_line)

        # Returns a single result everytime along with disassembled instr.
        # Eg- sum for add/sub, memory address with offset for lw/sw

        Pipeline_units[2].current_instr_line += 1

        # Moving data to next unit
        Pipeline_units[3].data.append((instr_word, instr_line, result_ALU))

        print("Executed EX on line ", instr_word, instr_line)

    # ......................................................................................................
    # ID/RF

    if len(Pipeline_units[1].data) < 1 or Pipeline_units[1].stalls_left:
        pass_to_nextHW(1)
        print("Pass ID/RF")
    else:

        # ======Stall checking=======
        nop = ["nop", [0, 0]]
        if (last_checked_stall_line != Pipeline_units[0].current_instr_line - 1):
            Pipeline_units[1].stalls_left += Pipeline_units[1].check_for_stall(1, current_instr_line=Pipeline_units[
                                                                                                         0].current_instr_line - 1)

        if Pipeline_units[1].stalls_left and instr_word != 'nop':
            last_checked_stall_line = Pipeline_units[0].current_instr_line - 1
            for i in range(Pipeline_units[1].stalls_left):
                Pipeline_units[2].data.insert(0, nop)
                # Pipeline_units[1].data.insert(0, "nop")

            Pipeline_units[0].stalls_left = Pipeline_units[1].stalls_left
            # Pipeline_units[1].data.pop(0)
            fetch_line = nop

        else:
            fetch_line = Pipeline_units[1].data[0]
            Pipeline_units[1].data.pop(0)
            (instr_word, instr_line) = simu.find_instr_type(fetch_line)

            # Moving data to next unit
            Pipeline_units[2].data.append((instr_word, instr_line))

            if instr_word in ("bne", "beq", "j"):

                # Checking branch instructions and using only IF and ID/RF stages for it
                if instr_word == "bne":
                    return_bne_line = simu.bne_instr(instr_line, Pipeline_units[0].current_instr_line - 1)
                    if return_bne_line != Pipeline_units[0].current_instr_line:
                        for i in range(5):
                            Pipeline_units[i].current_instr_line = return_bne_line - i
                        if len(Pipeline_units[1].data):
                            Pipeline_units[1].data.pop(len(Pipeline_units[1].data) - 1)
                        STALL_OF_GOD += 1
                elif instr_word == "beq":
                    return_bne_line = simu.beq_instr(instr_line, Pipeline_units[0].current_instr_line - 1)
                    if return_bne_line != Pipeline_units[0].current_instr_line:
                        for i in range(5):
                            Pipeline_units[i].current_instr_line = return_bne_line - i
                        if len(Pipeline_units[1].data):
                            Pipeline_units[1].data.pop(len(Pipeline_units[1].data) - 1)
                        STALL_OF_GOD += 1
                elif instr_word == "j":
                    return_bne_line = simu.j_instr(instr_line)
                    if return_bne_line != Pipeline_units[0].current_instr_line:
                        for i in range(5):
                            Pipeline_units[i].current_instr_line = return_bne_line - i
                        if len(Pipeline_units[1].data):
                            Pipeline_units[1].data.pop(len(Pipeline_units[1].data) - 1)
                        STALL_OF_GOD += 1

        # else:

        Pipeline_units[1].current_instr_line += 1

        print("Executed ID/RF on line ", fetch_line)

    # .......................................................................................................
    # If Stall came, percolate it downwards.
    # IF
    if Pipeline_units[0].stalls_left or Pipeline_units[0].current_instr_line >= simu.REGISTERS["ra"]:
        # If stall is there OR the stage has executed all the instructions and is sitting idle.
        CLOCK_OF_GOD += 0
        print("Execute nop in IF")

    else:
        # While filling up the pipeline in the start
        if Pipeline_units[0].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(0)
            print("Pass IF")
        else:
            fetch_line = instruction_fetch()
            # Moving data to next unit
            Pipeline_units[1].data.append(fetch_line)
            print("Executed IF on line ", fetch_line)

    # Call syscalls
    if len(simu.syscall_array) and Pipeline_units[0].current_instr_line - 1 == simu.syscall_array[0]:
        simu.syscall_instr(simu.syscall_array[0])
        simu.syscall_array.pop(0)

    # Check if WB has reached last stage
    if (len(Pipeline_units[2].data) == 0) and (len(Pipeline_units[2].data) == 0) and (len(
            Pipeline_units[3].data) == 0) and (len(Pipeline_units[4].data) == 0) and Pipeline_units[
        0].current_instr_line >= simu.REGISTERS["ra"]:
        is_Program_Done = True

# Console Prints
# CLOCK_OF_GOD -= 1
print("Final Memory state: \n", simu.RAM)
print("=" * 100)
print("Register values: \n", simu.REGISTERS)
print("=" * 100)
print("Total Clock Cycles: ", CLOCK_OF_GOD)
print("Total Stalls: ", STALL_OF_GOD)
# print("CPI: ", CLOCK_OF_GOD / (STALL_OF_GOD + 1))
print("IPC: ", (CLOCK_OF_GOD / (STALL_OF_GOD + 1)) ** -1)
