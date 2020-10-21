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
; initialized data
;-----------------------------
section .data USE32
stringPrinter db "%s",0
numberPrinter db "%d",0x0d,0x0a,0

;-----------------------------
; uninitialized data
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
Bob resb 6480
Bob2 resb 1721720

;-----------------------------
; Code! (execution starts at _main
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
add edi, Bob
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
add edi, Bob2
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
add edi, Bob
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
add edi, Bob2
push	DWORD[edi]
push numberPrinter
call _printf
add esp, 0x08

exit:

; All done.
mov	eax, 0x0
call	_ExitProcess@4

; (eof)
