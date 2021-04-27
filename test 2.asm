.data
    arr: .word 10, 60, 40, 70, 20, 30, 90, 100, 0, 80, 50

.text
.globl main

main:
    lui $s0, 0x1001
    li $t0, 0
    lw

exit:
    jr $ra