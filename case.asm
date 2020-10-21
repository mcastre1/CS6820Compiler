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
bob dd 3
s0 db "this is not it",0x0d,0x0a,0
stringPrinter db "%s",0
s1 db "this is not it either",0x0d,0x0a,0
s2 db "this is it.",0x0d,0x0a,0
s3 db "why did i not find it?",0x0d,0x0a,0
s4 db "this is after the case.",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

mov edi, 3
mov DWORD[bob], edi

mov edi, DWORD[bob]
cmp edi, 1
jnz _endcase_0
push s0
push stringPrinter
call _printf
add esp, 0x08

jmp _endswitch_0
_endcase_0:
mov edi, DWORD[bob]
cmp edi, 2
jnz _endcase_1
push s1
push stringPrinter
call _printf
add esp, 0x08

jmp _endswitch_0
_endcase_1:
mov edi, DWORD[bob]
cmp edi, 3
jnz _endcase_2
push s2
push stringPrinter
call _printf
add esp, 0x08

jmp _endswitch_0
_endcase_2:
push s3
push stringPrinter
call _printf
add esp, 0x08


_endswitch_0:
push s4
push stringPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
