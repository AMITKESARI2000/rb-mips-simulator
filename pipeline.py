import simu as simu
import re

CLOCK_OF_GOD = 0


class HWUnits:
    def __init__(self, current_instr_line, stalls_left, disassembled_instr, frwd):
        self.current_instr_line = current_instr_line
        self.stalls_left = stalls_left
        self.disassembled_instr = []
        if current_instr_line - base_instr_line_PC >= 0:
            self.instr_breakdown(current_instr_line)
        self.frwd = frwd
        self.data = []

    def instr_breakdown(self, current_instr_line):
        line = simu.lines[current_instr_line].strip()
        line = line.split(sep=" ", maxsplit=1)

        self.disassembled_instr.append(line[0].strip())  # as sw functionality is different
        line[1] = re.findall(r"\$\w?\w\w?\w", line[1])
        for l in line[1]:
            l = l.strip()[1:]
            self.disassembled_instr.append(l)
        print(self.disassembled_instr)
        return self.disassembled_instr

    def check_for_stall(self, current_instr_line):
        print(1, Pipeline_units[0].disassembled_instr)
        print(2, Pipeline_units[1].disassembled_instr)
        print(3, Pipeline_units[2].disassembled_instr)
        print(4, Pipeline_units[3].disassembled_instr)
        print(5, Pipeline_units[4].disassembled_instr)

        # Check current instr (like add or sub) dependency on prev instrs
        if len(Pipeline_units[0].disassembled_instr) == 4 and (
                Pipeline_units[0].disassembled_instr[0] in ("add", "sub")):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, False)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, False)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, False)

        # Check current instr (like sw) dependency on prev instrs
        elif (len(Pipeline_units[0].disassembled_instr == 3)) and (Pipeline_units[0].disassembled_instr[0] == "sw"):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, False)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, False)

        # Check current instr (like lw) dependency on prev instrs
        elif (len(Pipeline_units[0].disassembled_instr == 3)) and (Pipeline_units[0].disassembled_instr[0] == "lw"):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr) == 4:  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, False)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, False)

        elif len(Pipeline_units[0].disassembled_instr) == 4 and (Pipeline_units[0].disassembled_instr[0] in "addi"):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, False)

                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, False)

    def is_stall(self, dep_instr, frwd):

        stall = 0
        if dep_instr == 0 and frwd == False:
            stall += 2
        elif dep_instr == 1 and frwd == False:
            stall += 1
        elif dep_instr == 0 and frwd == True:
            stall += 1
        elif dep_instr == 1 and frwd == True:
            stall += 0
        self.stalls_left += stall


# ############# Program Execution starts ############
forward_enable = False
is_Program_Done = False

simu.rm_comments()
simu.pre_data_process()
base_instr_line_PC = simu.PC

if input("Data Forwarding is disabled by default. Want to enable?(y/n): ").lower() == "y":
    forward_enable = True
    print("Data Forwarding Enabled")

Pipeline_units = [
    HWUnits(current_instr_line=simu.PC, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # IF
    HWUnits(current_instr_line=simu.PC - 1, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # ID
    HWUnits(current_instr_line=simu.PC - 2, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # EX
    HWUnits(current_instr_line=simu.PC - 3, stalls_left=0, disassembled_instr=[], frwd=forward_enable),  # MEM
    HWUnits(current_instr_line=simu.PC - 4, stalls_left=0, disassembled_instr=[], frwd=forward_enable)]  # WB


def pass_to_nextHW(index_of_HWunit):
    # If stage is not being used no stalls are there and data is forwarded to next stage
    Pipeline_units[index_of_HWunit].current_instr_line += 1


def instruction_fetch():
    fetch_line = simu.lines[Pipeline_units[0].current_instr_line]
    Pipeline_units[0].current_instr_line += 1
    # NOTE for me: +++++++++++++++++++++++++++++++fetch_line = instr_word + instr_line+++++++++++++++++++++++++++++++++++++++++++++++++
    return fetch_line


while not is_Program_Done:
    CLOCK_OF_GOD += 1

    # If Stall came, percolate it downwards.
    # IF
    if Pipeline_units[0].stalls_left or Pipeline_units[0].current_instr_line == simu.REGISTERS["ra"]:
        # If stall is there OR the stage has executed all the instructions and is sitting idle.
        CLOCK_OF_GOD += 1
    else:
        # While filling up the pipeline in the start
        if Pipeline_units[0].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(0)
        else:
            fetch_line = instruction_fetch()

            # Moving data to next unit
            Pipeline_units[1].data.append(fetch_line)

    # ID/RF
    if Pipeline_units[1].stalls_left or Pipeline_units[1].current_instr_line == simu.REGISTERS["ra"]:
        CLOCK_OF_GOD += 1
        for i in range(1):
            Pipeline_units[i].stalls_left += 1
    else:
        # While filling up the pipeline in the start
        if Pipeline_units[1].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(1)
        else:
            fetch_line = Pipeline_units[1].data[0]
            Pipeline_units[1].data.pop(0)
            (instr_word, instr_line) = simu.find_instr_type(fetch_line)
            Pipeline_units[1].current_instr_line += 1

            # Moving data to next unit
            Pipeline_units[2].data.append((instr_word, instr_line))

    # EX
    if Pipeline_units[2].stalls_left or Pipeline_units[2].current_instr_line == simu.REGISTERS["ra"]:
        CLOCK_OF_GOD += 1
        for i in range(2):
            Pipeline_units[i].stalls_left += 1
    else:
        # While filling up the pipeline in the start
        if Pipeline_units[2].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(2)
        else:
            (instr_word, instr_line) = Pipeline_units[2].data[0]
            Pipeline_units[2].data.pop(0)
            (result_ALU, instr_line) = simu.execute_ALU(instr_word, instr_line)
            # Returns a single result everytime along with disassembled instr. Eg- sum for add/sub, memory address with offset for lw/sw
            Pipeline_units[2].current_instr_line += 1

            # Moving data to next unit
            Pipeline_units[3].data.append((instr_word, instr_line,result_ALU))

    # MEM
    if Pipeline_units[3].stalls_left or Pipeline_units[3].current_instr_line == simu.REGISTERS["ra"]:
        CLOCK_OF_GOD += 1
        for i in range(3):
            Pipeline_units[i].stalls_left += 1
    else:
        # While filling up the pipeline in the start
        if Pipeline_units[3].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(3)
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

    # WB
    if Pipeline_units[4].stalls_left or Pipeline_units[4].current_instr_line == simu.REGISTERS["ra"]:
        CLOCK_OF_GOD += 1
        for i in range(4):
            Pipeline_units[i].stalls_left += 1
    else:
        # While filling up the pipeline in the start
        if Pipeline_units[4].current_instr_line - base_instr_line_PC < 0:
            pass_to_nextHW(4)
        else:
            (instr_word, instr_line, result_ALU_MEM) = Pipeline_units[4].data[0]
            Pipeline_units[4].data.pop(0)
            successful_write = 1
            if instr_word in ("sw"):
                pass_to_nextHW(4)
            else:
                # In lw result from memory is used
                if instr_word in ("lw"):
                    result_MEM = result_ALU_MEM
                    successful_write = simu.write_back_op(instr_line, result_MEM)

                # In add/sub result from ALU is used
                elif instr_word in ("add", "sub", "lui", "addi", "li", "sll", "srl", "slt"):
                    result_ALU = result_ALU_MEM
                    successful_write = simu.write_back_op(instr_line, result_ALU)

                Pipeline_units[4].current_instr_line += 1

                if successful_write == -1:
                    print("Error in Write Back stage. Aborting...")
                    is_Program_Done = True

    # Check if WB has reached last stage
    if Pipeline_units[4].current_instr_line == simu.REGISTERS["ra"]:
        is_Program_Done = True

# Console Prints
print("Final Memory state: \n", simu.RAM)
print("=" * 100)
print("Register values: \n", simu.REGISTERS)
print("=" * 100)
print("Total Clock Cycles: ", CLOCK_OF_GOD)
print("IPC: ", CLOCK_OF_GOD / simu.REGISTERS['ra'])
