import simu
import re
import cache

global CLOCK_OF_GOD, STALL_OF_GOD, prev_stall, PIPELINE_DETAILS, temp_pipeline
CLOCK_OF_GOD = 0
STALL_OF_GOD = 0
prev_stall = 0
PIPELINE_DETAILS = []
temp_pipeline = []


class HWUnits:
    def __init__(self, current_instr_line, stalls_left, disassembled_instr):
        global forward_enable
        self.current_instr_line = current_instr_line
        self.stalls_left = stalls_left
        self.disassembled_instr = []
        # if current_instr_line - base_instr_line_PC >= 0:
        #     self.instr_breakdown(current_instr_line)
        self.frwd = forward_enable
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
        global STALL_OF_GOD, prev_stall
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

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

                elif Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub", "slt"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

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

                elif Pipeline_units[k].disassembled_instr[0] in ("addi", "sll", "srl"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                if s:
                    break

        # Check current instr (like ("addi", "sll","srl") dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in ("addi", "sll", "srl"):

            for k in range(1, t + 1):
                s = 0

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

                elif Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    STALL_OF_GOD += 1
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in ("addi", "sll", "srl"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                if s:
                    break

        # Check current instr (like sw) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in "sw":

            for k in range(1, t + 1):
                s = 0

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in ("addi", "sll", "srl"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                if s:
                    break

        # Check current instr (like lw) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in "lw":

            for k in range(1, t + 1):
                s = 0

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub"):  # Check crnt instr dep on prev instr like add

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in "sw":  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in "lw":  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, False)

                elif Pipeline_units[k].disassembled_instr[0] in ("addi", "sll", "srl"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                if s:
                    break

        # Check current instr (like lui, li) dependency on prev instrs

        elif Pipeline_units[0].disassembled_instr[0] in ("lui", "li", "la"):

            for k in range(1, t + 1):
                s = 0

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

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

                # global prev_stall
                if prev_stall == 2 and k == 2:
                    break

                if Pipeline_units[1].disassembled_instr[0] in ("bne", "beq"):
                    self.stalls_left += 1
                    STALL_OF_GOD += 1
                    print("stall: " + str(self.stalls_left), "in ", Pipeline_units[1].disassembled_instr)
                    s = 1

                elif Pipeline_units[k].disassembled_instr[0] in (
                        "add", "sub", "slt"):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

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

                elif Pipeline_units[k].disassembled_instr[0] in ("addi", "sll", "srl"):
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)
                    elif Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                elif Pipeline_units[k].disassembled_instr[0] in ("lui", "li", "la"):
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        s = self.is_stall(k, forward_enable)

                if s:
                    break
        # global prev_stall
        prev_stall = s
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
global forward_enable, is_Program_Done, base_instr_line_PC
forward_enable = False
is_Program_Done = False
base_instr_line_PC = 0

Pipeline_units = [
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # IF
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # ID
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # EX
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # MEM
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[])]  # WB

def program_execution():
    global forward_enable, is_Program_Done
    simu.rm_comments()
    simu.pre_data_process()
    global base_instr_line_PC
    base_instr_line_PC = simu.PC

    if forward_enable:
        print("Data Forwarding Enabled")
    else:
        print("Data Forwarding Disabled")

    global Pipeline_units
    Pipeline_units = [
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # IF
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # ID
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # EX
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[]),  # MEM
        HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[])]  # WB


def pass_to_nextHW(index_of_HWunit):
    # If stage is not being used no stalls are there and data is forwarded to next stage
    Pipeline_units[index_of_HWunit].current_instr_line += 1


def instruction_fetch():
    fetch_line = simu.lines[Pipeline_units[0].current_instr_line]
    Pipeline_units[0].current_instr_line += 1
    # fetch_line is instr_word + instr_line
    return fetch_line


def pipelining():
    global temp_pipeline, PIPELINE_DETAILS
    last_checked_stall_line = 0
    last_stall_line_MEM = 0
    global is_Program_Done, CLOCK_OF_GOD, STALL_OF_GOD
    while not is_Program_Done:
        for i in range(5):
            Pipeline_units[i].stalls_left = max(0, Pipeline_units[i].stalls_left - 1)
        CLOCK_OF_GOD += 1
        PIPELINE_DETAILS.append(temp_pipeline)
        temp_pipeline = []
        print("." * 100)
        print("In Clock Cycle: ", CLOCK_OF_GOD)
        temp_pipeline.append("In Clock Cycle: " + str(CLOCK_OF_GOD))

        # ....................................................................................................
        # WB
        if len(Pipeline_units[4].data) < 1:
            pass_to_nextHW(4)
            print("Pass WB")
            temp_pipeline.append("Pass WB")
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

                # Console Printing of syscall
                for s in simu.syscall_array:
                    sl = s[1].strip()
                    sl = sl.split(sep=" ")
                    sl[0] = sl[0].strip()
                    sl[1] = sl[1].strip()[1:-1]
                    # sl[2] = sl[2].strip()

                    if (sl[0] == instr_word) and (sl[1] == instr_line[0]):
                        simu.syscall_instr(s[0])

                if successful_write == -1:
                    # print("Error in Write Back stage. Aborting...")
                    is_Program_Done = True

            print("Executed WB on line ", instr_word, instr_line)
            temp_pipeline.append("Executed WB on line " + str(instr_word) + str(instr_line))

        # .......................................................................................................
        # MEM
        if len(Pipeline_units[3].data) < 1:
            pass_to_nextHW(3)
            print("Pass MEM")
            temp_pipeline.append("Pass MEM")
        else:
            (instr_word, instr_line, result_ALU) = Pipeline_units[3].data[0]
            Pipeline_units[3].data.pop(0)
            if instr_word in ("lw", "sw"):

                # ======Stall checking=======
                result_MEM, stalls_MEM = simu.memory_op(instr_word, instr_line, result_ALU, forward_enable)
                if instr_word == "lw":
                    nop = ["nop", [0, 0], 0]

                    if last_stall_line_MEM != Pipeline_units[0].current_instr_line - 1:
                        Pipeline_units[3].stalls_left += stalls_MEM
                        STALL_OF_GOD += stalls_MEM

                    if Pipeline_units[3].stalls_left and instr_word != 'nop':
                        print("Mem Operation taking ", stalls_MEM, " cycles")
                        last_stall_line_MEM = Pipeline_units[0].current_instr_line - 1
                        for i in range(Pipeline_units[3].stalls_left - 1):
                            Pipeline_units[4].data.insert(0, nop)
                            # Pipeline_units[1].data.insert(0, "nop")

                        Pipeline_units[0].stalls_left = Pipeline_units[3].stalls_left
                        Pipeline_units[1].stalls_left = Pipeline_units[3].stalls_left
                        Pipeline_units[2].stalls_left = Pipeline_units[3].stalls_left
                        # Pipeline_units[1].data.pop(0)
                        fetch_line = nop

                Pipeline_units[4].data.append((instr_word, instr_line, result_MEM))
                Pipeline_units[3].current_instr_line += 1
            else:
                pass_to_nextHW(3)
                Pipeline_units[4].data.append((instr_word, instr_line, result_ALU))

            if forward_enable:
                simu.write_back_op(instr_line, result_ALU)

            print("Executed MEM on line ", instr_word, instr_line)
            temp_pipeline.append("Executed MEM on line " + str(instr_word) + str(instr_line))

        # ..............................................................................................................
        # EX
        if len(Pipeline_units[2].data) < 1 or Pipeline_units[2].stalls_left:
            pass_to_nextHW(2)
            print("Pass EX")
            temp_pipeline.append("Pass EX")
        else:

            (instr_word, instr_line) = Pipeline_units[2].data[0]
            Pipeline_units[2].data.pop(0)
            (result_ALU, instr_line) = simu.execute_ALU(instr_word, instr_line, forward_enable)

            # Returns a single result everytime along with disassembled instr.
            # Eg- sum for add/sub, memory address with offset for lw/sw

            Pipeline_units[2].current_instr_line += 1

            # Moving data to next unit
            Pipeline_units[3].data.append((instr_word, instr_line, result_ALU))

            # SIMPLE FIX
            # if (instr_word in ("add", "sub", "lui", "addi", "li", "sll", "srl", "slt")) and forward_enable:
            #     successful_write = simu.write_back_op(instr_line, result_ALU)

            print("Executed EX on line ", instr_word, instr_line)
            temp_pipeline.append("Executed EX on line " + str(instr_word) + str(instr_line))

        # ......................................................................................................
        # ID/RF

        if len(Pipeline_units[1].data) < 1 or Pipeline_units[1].stalls_left:
            pass_to_nextHW(1)
            print("Pass ID/RF")
            temp_pipeline.append("Pass ID/RF")
        else:

            # ======Stall checking=======
            nop = ["nop", [0, 0]]
            fetch_line = Pipeline_units[1].data[0]
            (instr_word, instr_line) = simu.find_instr_type(fetch_line)
            if last_checked_stall_line != Pipeline_units[0].current_instr_line - 1:
                # and (instr_word not in ("j", "bne")):
                Pipeline_units[1].stalls_left += \
                    Pipeline_units[1].check_for_stall(1, current_instr_line=Pipeline_units[0].current_instr_line - 1)

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
                        return_bne_line = simu.bne_instr(instr_line, Pipeline_units[0].current_instr_line - 1,
                                                         forward_enable)
                        if return_bne_line != Pipeline_units[0].current_instr_line:
                            Pipeline_units[0].current_instr_line = return_bne_line
                            STALL_OF_GOD += 1
                            Pipeline_units[0].stalls_left += 1
                    elif instr_word == "beq":
                        return_bne_line = simu.beq_instr(instr_line, Pipeline_units[0].current_instr_line - 1,
                                                         forward_enable)
                        if return_bne_line != Pipeline_units[0].current_instr_line:
                            Pipeline_units[0].current_instr_line = return_bne_line
                            STALL_OF_GOD += 1
                            Pipeline_units[0].stalls_left += 1

                    elif instr_word == "j":
                        return_bne_line = simu.j_instr(instr_line)
                        Pipeline_units[0].current_instr_line = return_bne_line
                        STALL_OF_GOD += 1
                        Pipeline_units[0].stalls_left += 1

            # else:

            Pipeline_units[1].current_instr_line += 1

            print("Executed ID/RF on line ", fetch_line)
            temp_pipeline.append("Executed ID/RF on line " + str(fetch_line))

        # .......................................................................................................
        # If Stall came, percolate it downwards.
        # IF
        if Pipeline_units[0].stalls_left or Pipeline_units[0].current_instr_line >= simu.REGISTERS["ra"]:
            # If stall is there OR the stage has executed all the instructions and is sitting idle.
            CLOCK_OF_GOD += 0
            print("Execute nop in IF")
            temp_pipeline.append("Execute nop in IF")

        else:
            # While filling up the pipeline in the start
            if Pipeline_units[0].current_instr_line - base_instr_line_PC < 0:
                pass_to_nextHW(0)
                print("Pass IF")
                temp_pipeline.append("Pass IF")
            else:
                fetch_line = instruction_fetch()
                # Moving data to next unit
                Pipeline_units[1].data.append(fetch_line)
                print("Executed IF on line ", fetch_line)
                temp_pipeline.append("Executed IF on line " + str(fetch_line))

        # Call syscalls
        # if len(simu.syscall_array) and Pipeline_units[0].current_instr_line - 1 == simu.syscall_array[0]:
        #     simu.syscall_instr(simu.syscall_array[0])
        #     simu.syscall_array.pop(0)

        # Check if WB has reached last stage
        if (len(Pipeline_units[2].data) == 0) and (len(Pipeline_units[2].data) == 0) and \
                (len(Pipeline_units[3].data) == 0) and (len(Pipeline_units[4].data) == 0) and \
                Pipeline_units[0].current_instr_line >= simu.REGISTERS["ra"]:
            is_Program_Done = True
            PIPELINE_DETAILS.append(temp_pipeline)


def print_info():
    global temp_pipeline, PIPELINE_DETAILS
    # print()
    # print("*" * 20, "CONSOLE", "*" * 20)
    # while len(simu.syscall_array):
    #     simu.syscall_instr(simu.syscall_array[0])
    #     simu.syscall_array.pop(0)
    # print("*" * 20, "CONSOLE", "*" * 20, "\n")
    # Console Prints

    print("Final Memory state: \n", simu.RAM)
    print("=" * 100)
    print("Register values: \n", simu.REGISTERS)
    print("=" * 100)
    print("Total Clock Cycles: ", CLOCK_OF_GOD)
    print("Total Stalls: ", STALL_OF_GOD)
    print("Total Cache Miss: ", cache.CACHE_MISS)
    # print("CPI: ", CLOCK_OF_GOD / (STALL_OF_GOD + 1))
    print("IPC: ", (CLOCK_OF_GOD / (STALL_OF_GOD + 1)) ** -1)
    print(forward_enable)
