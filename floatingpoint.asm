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
num1 dd 2
num2 dd 3
numberPrinter db "%d",0x0d,0x0a,0
s0 db "num1 ( 2 ) + num2 ( 3 ) = 5",0x0d,0x0a,0
stringPrinter db "%s",0
float1 dd 2.5
s1 db "float1 ( 2.5 ) + num1 ( 2 ) = 4.5",0x0d,0x0a,0
s2 db "num1 ( 2 ) + float1 ( 2.5 ) = 4.5",0x0d,0x0a,0
float2 dd 3.5
s3 db "float1 ( 2.5 ) + float2 ( 3.5 ) = 6.0",0x0d,0x0a,0
s4 db "num2 ( 3 ) - num1 ( 2 ) = 1",0x0d,0x0a,0
s5 db "num2 ( 3 ) - float1 ( 2.5 ) = 0.5",0x0d,0x0a,0
s6 db "float2 ( 3.5 ) - num1 ( 2 ) = 1.5",0x0d,0x0a,0
s7 db "float2 ( 3.5 ) - float1 ( 2.5 ) = 1.0",0x0d,0x0a,0
s8 db "num1 ( 2 ) * num2 ( 3 ) = 6",0x0d,0x0a,0
s9 db "num1 ( 2 ) * float1 ( 2.5 ) = 5.0",0x0d,0x0a,0
s10 db "float1 ( 2.5 ) * num1 ( 2 ) = 5.0",0x0d,0x0a,0
s11 db "float1 ( 2.5 ) * float2 ( 3.5 ) = 8.75",0x0d,0x0a,0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
result resd 1
fresult resd 1

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

mov edi, 2
mov DWORD[num1], edi

mov edi, 3
mov DWORD[num2], edi

mov DWORD[result], 5

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

push s0
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(2.5)
mov DWORD[float1], edi

mov edi, __float32__(4.5)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s1
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(4.5)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s2
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(3.5)
mov DWORD[float2], edi

mov edi, __float32__(6.0)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s3
push stringPrinter
call _printf
add esp, 0x08

mov DWORD[result], 1

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

push s4
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(0.5)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s5
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(1.5)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s6
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(1.0)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s7
push stringPrinter
call _printf
add esp, 0x08

mov DWORD[result], 6

push DWORD[result]
push numberPrinter
call _printf
add esp, 0x08

push s8
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(5.0)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s9
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(5.0)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s10
push stringPrinter
call _printf
add esp, 0x08

mov edi, __float32__(8.75)
mov DWORD[fresult], edi

fld dword [fresult]
fstp qword[esp]
push format_float
call _printf
add esp, 12

push s11
push stringPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
