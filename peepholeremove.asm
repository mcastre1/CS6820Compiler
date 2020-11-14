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
format_float: db "%f", 10, 0
x dd 3
y dd 4
z dd 5
numberPrinter db "%d",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
result resd 1

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

mov edi, 3
mov DWORD[x], edi

mov edi, 4
mov DWORD[y], edi

mov edi, 5
mov DWORD[z], edi

mov edi, 32
imul edi, 3
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[result], eax

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
