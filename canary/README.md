# Easy Buffer Overflow 
_Just some tips to remeber how to resolve easy buffer overflows_

## Tips 📝
**1.  Check the typical "win" or "flag" function on the binary with gdb (it's recommended to have [PEDA](https://github.com/longld/peda) installed to see registers and the program instructions in a prettier way).**

To open the binary with gdb:
```
gdb binary
```
To see the differents functions on the binary: 
```
gdb-peda$ info functions
```
![FunctionsAddresses](images/functions.png)


**2. Get "flag" function memory address**: 
```
gdb-peda$ info functions flag 
```

![FunctionAddres](images/function_address.png)


**3. Modify "main" returns memory address**:

First we should puts a breakpoint on the "vulnerable" method (for example gets or fgets)

```
gdb-peda$ disas main
```
![Functions](images/gets_address.png)

```
gdb-peda$ b *0x000000000040093b ("gets" memory address)
```

Run the binary with gdb until reach the breakpoint

```
gdb-peda$ run
```
Execute the nex instruction of the program (it will call the gets where we have put the breakpoint and ask for an input):
```
gdb-peda$ ni
AAAAAAAAAAAAA
```
Then we have to look at the rsp register to see where our input has been stored: 
```
gdb-peda$ x/20gx $rsp
```


**4. asd**

