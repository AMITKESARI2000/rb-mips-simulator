import simu as simu
import re

CLOCK_OF_GOD = 0


class HWUnits:
    def __init__(self, current_instr_line, stalls_left):
        self.current_instr_line = 0
        self.stalls_left = 0

    def instr_breakdown(self, current_instr_line):
        line = simu.lines[current_instr_line].strip()
        line = line.split(sep=" ", maxsplit=1)

        dissambled_instr = []
        dissambled_instr.append(line[0].strip())  # as sw functionality is different
        line[1] = re.findall(r"\$\w?\w\w?\w", line[1])
        for l in line[1]:
            l = l.strip()[1:]
            dissambled_instr.append(l)
        print(dissambled_instr)
        return dissambled_instr

    def is_stall(self, current_instr_line):
        stall = 0
        dissambled_instr = self.instr_breakdown(current_instr_line)
        # sw
        if (len(dissambled_instr == 3)) and (dissambled_instr[0] == "sw"):
            stall = 2
        #     add
        elif len(dissambled_instr == 4):
            prev = self.instr_breakdown(current_instr_line - 1)
            if (dissambled_instr[2] == prev[1]) or (dissambled_instr[3] == prev[1]):
                stall = 2
        self.stalls_left += stall


Pipeline_units = [HWUnits(current_instr_line=0, stalls_left=0),  # IF
                  HWUnits(current_instr_line=0, stalls_left=0),  # ID
                  HWUnits(current_instr_line=0, stalls_left=0),  # EX
                  HWUnits(current_instr_line=0, stalls_left=0),  # MEM
                  HWUnits(current_instr_line=0, stalls_left=0)]  # WB

Pipeline_units[1].instr_breakdown(12)
