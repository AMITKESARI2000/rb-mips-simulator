import simu as simu
import re

CLOCK_OF_GOD = 0


class HWUnits:
    def __init__(self, current_instr_line, stalls_left, dissambled_instr, frwd):
        self.current_instr_line = 0
        self.stalls_left = 0
        self.dissambled_instr = []
        self.frwd = False

    def instr_breakdown(self, current_instr_line):
        line = simu.lines[current_instr_line].strip()
        line = line.split(sep=" ", maxsplit=1)

        self.dissambled_instr.append(line[0].strip())  # as sw functionality is different
        line[1] = re.findall(r"\$\w?\w\w?\w", line[1])
        for l in line[1]:
            l = l.strip()[1:]
            self.dissambled_instr.append(l)
        print(self.dissambled_instr)
        return self.dissambled_instr

    def check_for_stall(self, current_instr_line):
        print(1, Pipeline_units[0].disammbled_instr)
        print(2, Pipeline_units[1].disammbled_instr)
        print(3, Pipeline_units[2].disammbled_instr)
        print(4, Pipeline_units[3].disammbled_instr)
        print(5, Pipeline_units[4].disammbled_instr)

        # Check current instr (like add) dependency on prev instrs
        if len(Pipeline_units[0].dissambled_instr == 4):
            for k in range (0,2):
                if len(Pipeline_units[k].dissambled_instr == 4):     # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].dissambled_instr[2] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].dissambled_instr[3] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "sw"):     # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].dissambled_instr[2] == Pipeline_units[k].dissambled_instr[2][3:5]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].dissambled_instr[3] == Pipeline_units[k].dissambled_instr[2][3:5]:
                        self.is_stall(k, self.frwd)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "lw"):     # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].dissambled_instr[2] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd)
                    elif Pipeline_units[0].dissambled_instr[3] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd)

        # Check current instr (like sw) dependency on prev instrs
        elif (len(Pipeline_units[0].dissambled_instr == 3)) and (Pipeline_units[0].dissambled_instr[0] == "sw"):
            for k in range (0,2):
                if len(Pipeline_units[k].dissambled_instr == 4):     # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].dissambled_instr[1] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "sw"):     # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].dissambled_instr[1] == Pipeline_units[k].dissambled_instr[2][3:5]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "lw"):     # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].dissambled_instr[1] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd, False)

        # Check current instr (like lw) dependency on prev instrs
        elif (len(Pipeline_units[0].dissambled_instr == 3)) and (Pipeline_units[0].dissambled_instr[0] == "lw"):
            for k in range (0,2):
                if len(Pipeline_units[k].dissambled_instr == 4):     # Check crnt instr dep on prev instr like add
                    if Pipeline_units[0].dissambled_instr[2][3:5] == Pipeline_units[k].dissambled_instr[1]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "sw"):     # Check crnt instr dep on prev instr like sw
                    if Pipeline_units[0].dissambled_instr[2][3:5] == Pipeline_units[k].dissambled_instr[2][3:5]:
                        self.is_stall(k, self.frwd, False)
                elif (len(Pipeline_units[k].dissambled_instr == 3)) and (Pipeline_units[k].dissambled_instr[0] == "lw"):     # Check crnt instr dep on prev instr like lw
                    if Pipeline_units[0].dissambled_instr[2][3:5] == Pipeline_units[k].dissambled_instr[1]:
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


Pipeline_units = [HWUnits(current_instr_line=simu.PC, stalls_left=0, dissambled_instr=HWUnits.instr_breakdown(simu.PC)),  # IF
                  HWUnits(current_instr_line=simu.PC, stalls_left=0, dissambled_instr=HWUnits.instr_breakdown(simu.PC)),  # ID
                  HWUnits(current_instr_line=simu.PC, stalls_left=0, dissambled_instr=HWUnits.instr_breakdown(simu.PC)),  # EX
                  HWUnits(current_instr_line=simu.PC, stalls_left=0, dissambled_instr=HWUnits.instr_breakdown(simu.PC)),  # MEM
                  HWUnits(current_instr_line=simu.PC, stalls_left=0, dissambled_instr=HWUnits.instr_breakdown(simu.PC))]  # WB

# Pipeline_units[1].instr_breakdown(12)

is_Program_Done = False

simu.rm_comments()
simu.pre_data_process()


def pass_to_nextHW(index):
    # If stage is not being used no stalls are there and data is forwarded to next stage
    Pipeline_units[index].current_instr_line = Pipeline_units[index].current_instr_line + 1


def instruction_fetch():
    fetch_line = simu.lines[Pipeline_units[0].current_instr_line]
    Pipeline_units[0].current_instr_line = Pipeline_units[0].current_instr_line + 1
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
        Pipeline_units[1].current_instr_line = Pipeline_units[1].current_instr_line + 1

    # EX
    if Pipeline_units[2].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(2):
            Pipeline_units[i].stalls_left += 1
    else:
        simu.execute_ALU(instr_word, instr_line)
        Pipeline_units[2].current_instr_line = Pipeline_units[2].current_instr_line + 1

    # MEM
    if Pipeline_units[3].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(3):
            Pipeline_units[i].stalls_left += 1
    else:
        Pipeline_units[3].current_instr_line = simu.PC - 3

    # WB
    if Pipeline_units[4].stalls_left:
        CLOCK_OF_GOD += 1
        for i in range(4):
            Pipeline_units[i].stalls_left += 1
    else:
        Pipeline_units[4].current_instr_line = simu.PC - 4

    if Pipeline_units[4].current_instr_line == simu.REGISTERS["ra"]:
        is_Program_Done = True

# Console Prints
print("Final Memory state: \n", simu.RAM)
print("=" * 100)
print("Register values: \n", simu.REGISTERS)
print("=" * 100)
print("Total Clock Cycles: ", CLOCK_OF_GOD)
print("IPC: ", CLOCK_OF_GOD / simu.REGISTERS['ra'])
