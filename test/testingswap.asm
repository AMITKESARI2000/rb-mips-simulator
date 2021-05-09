# Assembler Directive to load the
# data segment, text segment
    .data
    .word 7
    .word 3
    .word 3, 10, 22
    line: .asciiz " \n and \n "
    Newline: .asciiz " groups of 0s \t and \n groups of 1s: "
    arr: .word 10, 60, 40, 70, 20, 30, 90, 100, 0, 80, 50
    .asciiz "hello world value: no"
    .text
    .globl main

main:
 # add $t2, $zero, $s0               #for iterating addr by i
 # add $t3, $zero, $t2               #for iterating addr by j
  #nonimp
 # add $t5, $t4, $t4               #for iterating addr by j
 # add $t6, $t7, $t8               #for iterating addr by j
 # add $t8, $t9, $t9               #for iterating addr by j
 # add $s6, $s7, $s8               #for iterating addr by j
    #test: addi $s0 , $s1 , 2
    #sll $s0, $s0, 2
    #bne $s0, $s1, test
    lui $s0, 0x1001
  	#load upper part of register s0(16) with 0x1001  s0 = 0x10010000

    lw $s1, 0($s0)

    #load s1 with the contents of memory address 0x10010000 = 7,
  	#since we loaded the data there.

    lw $s2, 4($s0)
    #load s2 with the contents of memory address 0x10010004 = 3,
  	#since we loaded the data there.

    sw $s2, 0($s0)
    #store contents of s2 into memory address 0x10010000 

    sw $s1, 4($s0)
    #store contents of s1 into memory address 0x10010004]

    jr $ra


#li    1,2,3,4,5
#lw      1, , ,2,3,4,5
#lw         , ,1,2,3,4,5
#sw              1, , ,2,3,4,5
#sw                    1,2,3,4,5



