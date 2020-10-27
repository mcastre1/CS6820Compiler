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
stringPoint0 db "james",0x0d,0x0a,0
stringPoint1 db " bond",0x0d,0x0a,0
stringPoint2 db "",0x0d,0x0a,0
stringPrinter db "%s",0

;-----------------------------
; Unitialiazed vars
;-----------------------------
section .bss USE32
temp resd 1
temp2 resd 1
temp3 resd 1
temp4 resd 1
first resb 128
last resb 128
fullname resb 128

;-----------------------------
; Code! (execution starts at _main)
;-----------------------------
section .code USE32
_main:

;STRING ASSIGNMENT 
;string first = "james";
mov ecx, 0
cld
mov esi, stringPoint0
mov edi, first
copy0:
mov cl, byte[esi]
add cl, 1
movsb
loop copy0

;STRING ASSIGNMENT 
;string last = " bond";
mov ecx, 0
cld
mov esi, stringPoint1
mov edi, last
copy1:
mov cl, byte[esi]
add cl, 1
movsb
loop copy1

;STRING DECLARATION (EMPTY STRING)
;string fullname;
mov ecx, 0
cld
mov esi, stringPoint2
mov edi, fullname
copy2:
mov cl, byte[esi]
add cl, 1
movsb
loop copy2

;STRING CONCAT
;fullname = first + last;
mov ecx, 0
cld
mov esi, first
mov edi, fullname 
copy3:
mov cl, byte[esi]
add cl, 1
movsb
loop copy3

dec edi
dec edi
dec edi
mov esi, last
concat4:
mov cl, byte[esi]
add cl, 1
movsb
loop concat4

push fullname
push stringPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
