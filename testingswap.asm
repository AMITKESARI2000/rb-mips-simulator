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
    #test: add $s0 , $s1 , $s2
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