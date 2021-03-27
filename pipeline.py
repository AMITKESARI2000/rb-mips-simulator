import simu as simu
import re

CLOCK_OF_GOD = 0


class HWUnits:
    def __init__(self, current_instr_line, stalls_left, disassembled_instr, frwd):
        self.current_instr_line = current_instr_line
        self.stalls_left = stalls_left
        self.disassembled_instr = []
        self.instr_breakdown(current_instr_line)
        self.frwd = frwd

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

        # Check current instr (like add) dependency on prev instrs
        if len(Pipeline_units[0].disassembled_instr == 4):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, self.frwd)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw

                    if Pipeline_units[0].disassembled_instr[2] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].disassembled_instr[3] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd)

        # Check current instr (like sw) dependency on prev instrs
        elif (len(Pipeline_units[0].disassembled_instr == 3)) and (Pipeline_units[0].disassembled_instr[0] == "sw"):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw

                    if Pipeline_units[0].disassembled_instr[1] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd, False)

        # Check current instr (like lw) dependency on prev instrs
        elif (len(Pipeline_units[0].disassembled_instr == 3)) and (Pipeline_units[0].disassembled_instr[0] == "lw"):
            for k in range(0, 2):
                if len(Pipeline_units[k].disassembled_instr == 4):  # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "sw"):  # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[2][3:5]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].disassembled_instr == 3)) and (
                        Pipeline_units[k].disassembled_instr[0] == "lw"):  # Check crnt instr dep on prev instr like lw

                    if Pipeline_units[0].disassembled_instr[2][3:5] == Pipeline_units[k].disassembled_instr[1]:
                        self.is_stall(k, self.frwd, False)

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

if input("Data Forwarding is disabled by default. Want to enable?(y/n): ").lower() == "y":
    forward_enable = True
    print("Data Forwarding Enabled")

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
    # NOTE for me: +++++++++++++++++++++++++++++++fetch_line = instr_word + instr_line+++++++++++++++++++++++++++++++++++++++++++++++++
    return fetch_line


while not is_Program_Done:
    CLOCK_OF_GOD += 1

    # If Stall came, percolate it downwards.
    # IF
    if Pipeline_units[0].stalls_left:
        CLOCK_OF_GOD += 1
    else:
        fetch_line = instruction_fetch()

    # ID/RF
    if Pipeline_units[1].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(1):
            Pipeline_units[i].stalls_left += 1
    else:
        instr_word, instr_line = simu.find_instr_type(fetch_line)
        Pipeline_units[1].current_instr_line += 1

    # EX
    if Pipeline_units[2].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(2):
            Pipeline_units[i].stalls_left += 1
    else:
        result_ALU = simu.execute_ALU(instr_word, instr_line)
        # Returns a single result everytime. Eg- sum for add/sub, memory address with offset for lw/sw
        Pipeline_units[2].current_instr_line += 1

    # MEM
    if Pipeline_units[3].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(3):
            Pipeline_units[i].stalls_left += 1
    else:
        if instr_word in ("lw", "sw"):
            result_MEM = simu.memory_op(instr_word, instr_line, result_ALU)
            Pipeline_units[3].current_instr_line += 1
        else:
            pass_to_nextHW(3)

    # WB
    if Pipeline_units[4].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(4):
            Pipeline_units[i].stalls_left += 1
    else:
        if instr_word in ("sw"):
            pass_to_nextHW(4)
        else:
            if instr_word in ("lw"):
                successfull_write = simu.write_back_op(instr_line, result_MEM)
            elif instr_word in ("add", "sub"):
                successfull_write = simu.write_back_op(instr_line, result_ALU)

            Pipeline_units[4].current_instr_line += 1
            if not successfull_write:
                print("Error in Write Back stage. Aborting...")
                is_Program_Done = True

    if Pipeline_units[4].current_instr_line == simu.REGISTERS["ra"]:
        is_Program_Done = True

# Console Prints
print("Final Memory state: \n", simu.RAM)
print("=" * 100)
print("Register values: \n", simu.REGISTERS)
print("=" * 100)
print("Total Clock Cycles: ", CLOCK_OF_GOD)
print("IPC: ", CLOCK_OF_GOD / simu.REGISTERS['ra'])
