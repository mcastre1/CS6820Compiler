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
x dd 3
y dd 4
z dd 5
s0 db "ae.txt:",0x0d,0x0a,0
stringPrinter db "%s",0
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

mov edi, DWORD[x]
imul edi, DWORD[y]
mov DWORD[temp], edi

mov edi, DWORD[temp]
imul edi, DWORD[z]
mov DWORD[temp2], edi

mov eax, DWORD[temp2]
mov DWORD[result], eax

push s0
push stringPrinter
call _printf
add esp, 0x08

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

xor edi, edi
mov eax, 0x00000001
_exp_top_0:
cmp edi, DWORD[x]
jz _exp_out_0
imul eax, 3
inc edi
jmp _exp_top_0
_exp_out_0:
mov DWORD[temp], eax

mov edi, 67
sub edi, 34
mov DWORD[temp2], edi

mov edi, DWORD[temp]
add edi, DWORD[temp2]
mov DWORD[temp3], edi

xor edi, edi
mov eax, 0x00000001
_exp_top_1:
cmp edi, DWORD[x]
jz _exp_out_1
imul eax, 2
inc edi
jmp _exp_top_1
_exp_out_1:
mov DWORD[temp], eax

mov edi, 77
imul edi, DWORD[temp]
mov DWORD[temp], edi

mov edi, DWORD[temp3]
sub edi, DWORD[temp]
mov DWORD[temp2], edi

mov eax, DWORD[temp2]
mov DWORD[result], eax

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

xor edi, edi
mov eax, 0x00000001
_exp_top_2:
cmp edi, DWORD[y]
jz _exp_out_2
imul eax, 3
inc edi
jmp _exp_top_2
_exp_out_2:
mov DWORD[temp], eax

mov edi, 67
sub edi, 34
mov DWORD[temp2], edi

mov edi, DWORD[temp]
add edi, DWORD[temp2]
mov DWORD[temp3], edi

xor edi, edi
mov eax, 0x00000001
_exp_top_3:
cmp edi, DWORD[y]
jz _exp_out_3
imul eax, 2
inc edi
jmp _exp_top_3
_exp_out_3:
mov DWORD[temp], eax

mov edi, 77
imul edi, DWORD[temp]
mov DWORD[temp], edi

mov edi, DWORD[temp3]
sub edi, DWORD[temp]
mov DWORD[temp2], edi

mov eax, DWORD[temp2]
mov DWORD[result], eax

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

xor edi, edi
mov eax, 0x00000001
_exp_top_4:
cmp edi, DWORD[y]
jz _exp_out_4
imul eax, 3
inc edi
jmp _exp_top_4
_exp_out_4:
mov DWORD[temp], eax

mov edi, 67
sub edi, 34
mov DWORD[temp2], edi

mov edi, DWORD[temp]
add edi, DWORD[temp2]
mov DWORD[temp3], edi

xor edi, edi
mov eax, 0x00000001
_exp_top_5:
cmp edi, DWORD[y]
jz _exp_out_5
imul eax, 2
inc edi
jmp _exp_top_5
_exp_out_5:
mov DWORD[temp], eax

mov edi, 77
imul edi, DWORD[temp]
mov DWORD[temp], edi

mov edi, DWORD[temp]
imul edi, -1
mov DWORD[temp2], edi

mov edi, DWORD[temp3]
sub edi, DWORD[temp2]
mov DWORD[temp3], edi

mov eax, DWORD[temp3]
mov DWORD[result], eax

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
