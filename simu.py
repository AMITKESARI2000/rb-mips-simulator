import re

file = open("testingswap.s", "r")
lines = file.readlines()
file.close()

# Global Storages
RAM = [];
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

while i < len(lines):
    lines[i] = lines[i].strip().lower()
    # print(i, line)

    # COMMENTS
    if re.findall(r"# *", lines[i]):
        print("it is a comment")  # comment can be added in middle also
        i += 1
        continue

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
    i += 1
