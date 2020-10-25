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
numberPrinter db "%d",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
bob resb 6480
bob2 resb 1721720

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

xor edi, edi
mov esi, 162
imul esi, 2
add edi, esi
mov esi, 9
imul esi, 5
add edi, esi
mov esi, 1
imul esi, 8
add edi, esi
sub edi, 191
imul edi, 4
add edi, bob
mov	DWORD[edi],	2
xor edi, edi
mov esi, 33110
imul esi, 5
add edi, esi
mov esi, 6622
imul esi, 5
add edi, esi
mov esi, 86
imul esi, 5
add edi, esi
mov esi, 1
imul esi, 5
add edi, esi
sub edi, 6971
imul edi, 4
add edi, bob2
mov	DWORD[edi],	5
xor edi, edi
mov esi, 162
imul esi, 2
add edi, esi
mov esi, 9
imul esi, 5
add edi, esi
mov esi, 1
imul esi, 8
add edi, esi
sub edi, 191
imul edi, 4
add edi, bob
push	DWORD[edi]
push numberPrinter
call _printf
add esp, 0x08
xor edi, edi
mov esi, 33110
imul esi, 5
add edi, esi
mov esi, 6622
imul esi, 5
add edi, esi
mov esi, 86
imul esi, 5
add edi, esi
mov esi, 1
imul esi, 5
add edi, esi
sub edi, 6971
imul edi, 4
add edi, bob2
push	DWORD[edi]
push numberPrinter
call _printf
add esp, 0x08
exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
