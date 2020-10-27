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
stringPoint2 db " ",0x0d,0x0a,0

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

mov DWORD[string first], "james"

mov DWORD[string last], " bond"

mov edi, DWORD[first]
add edi, DWORD[last]
mov DWORD[temp], edi

mov eax, DWORD[temp]
mov DWORD[fullname], eax

push DWORD[fullname]
push numberPrinter
call _printf
add esp, 0x08

exit:
; All done.
mov	eax, 0x0
call	_ExitProcess@4
; (eof)
