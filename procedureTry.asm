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

;-----------------------------
; Initialiazed vars
;-----------------------------
section .data USE32
s0 db "before was 3",0x0d,0x0a,0
stringPrinter db "%s",0
numberPrinter db "%d",0x0d,0x0a,0
s1 db "passin = 5",0x0d,0x0a,0
bob dd 3
s2 db "bob = 3",0x0d,0x0a,0
s3 db "bob = 5",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
passin resd 1

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

jmp afterprocedures
changenum1:
push s0
push stringPrinter
call _printf
add esp, 0x08

push DWORD[passin]
push numberPrinter
call _printf
add esp, 0x08

push s1
push stringPrinter
call _printf
add esp, 0x08

mov DWORD[passin], 5

push DWORD[passin]
push numberPrinter
call _printf
add esp, 0x08

;END procedure
ret

changenum2:
push s0
push stringPrinter
call _printf
add esp, 0x08

push DWORD[passin]
push numberPrinter
call _printf
add esp, 0x08

push s1
push stringPrinter
call _printf
add esp, 0x08

mov DWORD[passin], 5

push DWORD[passin]
push numberPrinter
call _printf
add esp, 0x08

;END procedure
ret

afterprocedures:
mov edi, 3
mov DWORD[bob], edi

mov eax, DWORD[bob]
mov DWORD[passin], eax
call changenum1
add 	esp, 0x04

push s2
push stringPrinter
call _printf
add esp, 0x08

push DWORD[bob]
push numberPrinter
call _printf
add esp, 0x08

mov eax, DWORD[bob]
mov DWORD[passin], eax
call changenum2
add 	esp, 0x04
mov eax, DWORD[passin]
mov DWORD[bob], eax

push s3
push stringPrinter
call _printf
add esp, 0x08

push DWORD[bob]
push numberPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
