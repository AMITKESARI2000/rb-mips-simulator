# rb_mips_simulator

### Developers:
* Amit Kesari (CS19B003)
* Anu Anand Annu (CS19B044)

### Simulate MIPS Architecture instruction sets
* Main starting file is **gui.py** located in phase 1 folder
* The simulator supports the following MIPS instructions: 
  * add/sub
  * bne/beq
  * jmp
  * lw/sw
  * lui
  * addi  
  * sll/srl
  * li/la
  * slt
  
* The simulator supports at least 4 KB of memory.
* The simulator reads in an assembly file(.asm), executes the instructions, and in the end display
the contents of the registers, and the memory.
* Language used for development: Python.
* The GUI for the simulator has been developed to be simplistic and functional using Tkinter. 
* Tries to point out syntax errors and shows erroneous line. 

  
---

### Phase 2
In phase 2 we are implementing pipeline so that the throughput can be increased.

* The main file is **pipeline.py**
* All 5 stages (IF, ID/RF, EX, MEM, WB) have been modularised.
* Stalls have been added according to data dependencies only
* Structural hazards have been removed assuming writing in 1st half of the cycle and reading in 2nd half of the cycle.

Note: 
* We were unable to complete the phase 2. We tried implementing all the 5 HW units as objects and tried to find and accumulate the stalls based on the data dependency between the instructions.
* But somehow we were not able to properly deal with branch statements properly due to which any program having loops runs only a single time.
* We tried to compare and jump to that instruction point but were unable to do so somehow, sorry.


