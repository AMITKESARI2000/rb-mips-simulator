import re

file = open("testingswap.s", "r")
lines = file.readlines()
file.close()

# Global Storages
RAM = []
ram_iter = 0
ram_label = {}

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

#Removing all comments and unnecessary white spaces
while i<len(lines):
    lines[i] = lines[i].strip().lower()
    # print(i, line)

    if re.findall(r"# *", lines[i]) or (re.findall(r"^\n", lines[i]) and len(lines[i]=='\n'.length())):
        # print("it is a comment")  # comment can be added in middle also
        # print (lines[i])
        lines.remove(lines[i])
        i-=1
    i+=1

i=0
while i < len(lines):

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
            line = lines[i][6:]
            line = re.sub(r',','',line)
            line = line.split(sep=' ')
            if len(line)>0:
                RAM.append(list(map(int,line)))
                print(RAM)
            ram_iter +=1
    i += 1