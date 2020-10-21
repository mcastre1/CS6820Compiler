;-----------------------------
; exports
;-----------------------------
global _main
EXPORT _main

;-----------------------------
; imports
;-----------------------------
extern _ExitProcess@4
extern _printf
extern _scanf

;-----------------------------
; Initialiazed vars
;-----------------------------
section .data USE32
num2 dd 3
s0 db "basics.txt:",0x0d,0x0a,0
stringPrinter db "%s",0
numberPrinter db "%d",0x0d,0x0a,0
s1 db "enter a number:",0x0d,0x0a,0
int_format db "%i", 0
s2 db "the number is:",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
num1 resd 1
num3 resd 1
mynum resd 1

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

mov edi, 3
mov DWORD[num2], edi

mov edi, DWORD[num2]
mov DWORD[num3], edi

mov edi, DWORD[num3]
add edi, 10
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num3], eax

mov edi, DWORD[num3]
add edi, DWORD[num2]
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num2], eax

mov edi, 2
imul edi, 5
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num1], eax

mov edi, DWORD[num3]
imul edi, DWORD[num2]
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num1], eax

mov edi, 8
sub edi, 5
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num2], eax

mov edi, 8
sub edi, 5
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[num2], eax

xor edi, edi
mov eax, 0x00000001
_exp_top_0:
cmp edi, 6
jz _exp_out_0
imul eax, 8
inc edi
jmp _exp_top_0
_exp_out_0:
mov DWORD[temp], eax

mov eax, DWORD[temp]
mov DWORD[num3], eax

push s0
push stringPrinter
call _printf
add esp, 0x08

push DWORD[num1]
push numberPrinter
call _printf
add esp, 0x08

push DWORD[num2]
push numberPrinter
call _printf
add esp, 0x08

push DWORD[num3]
push numberPrinter
call _printf
add esp, 0x08

push s1
push stringPrinter
call _printf
add esp, 0x08

pusha
push mynum
push dword int_format
call _scanf
add esp, 0x04
popa

push s2
push stringPrinter
call _printf
add esp, 0x08

push DWORD[mynum]
push numberPrinter
call _printf
add esp, 0x08

push s2
push stringPrinter
call _printf
add esp, 0x08

mov edi, DWORD[mynum]
add edi, 6
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[mynum], eax

push DWORD[mynum]
push numberPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
