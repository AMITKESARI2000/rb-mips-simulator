  .data
  N: .word 3, 3, 4, 3
  Tir: .asciiz "Tirutsava 2020 is lub\n"
  Val: .asciiz "Value of i is: "

  .text
  .globl main

main:
  li $t0, 3            #k = 3
  li $t1, 0            #i = 0

  la $s0, N                     #load addr of N array
  lw $s1, 0($s0)                #store element in register
  j cond

loop:
  add $s2, $s0, $zero           #addr stored for looping is init with start addr
  addi $t1, $t1, 2              #i += 2

  sll $t1, $t1, 2               #i << 2 for adding in addr
  add $s2, $s2, $t1             #move addr to particular index
  srl $t1, $t1, 2               #i >> 2 for loop

  lw $s1, 0($s2)                #load particluar index value in register

  cond:
    bne $s1, $t0, loop      #save[i] != 4

print:
  li $v0, 4
  la $a0, Tir
  syscall

  li $v0, 4
  la $a0, Val
  syscall

  li $v0, 1
  add $a0, $t1, $zero
  syscall

exit:
  li $v0, 10
  syscall