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
![Functions Addresses](images/functions.png)


**2. Get "flag" function memory address**: 
```
gdb-peda$ info functions flag 
```

![Function Address](images/function_address.png)


**3. Finding the canary to prepare the paylaod **:

First we should puts a breakpoint on the "vulnerable" method (for example gets or fgets)

```
gdb-peda$ disas main
```
![Gets address](images/gets_address.png)

```
gdb-peda$ b *0x000000000040093b ("gets" memory address)
```

Run the binary with gdb until reaching the breakpoint

```
gdb-peda$ run
```
Execute the nex instruction of the program (it will call the "gets" where we have put the breakpoint and ask for an input, in this case we are going to write some 'A'):
```
gdb-peda$ ni
AAAAAAAAAAAAA
```
Then we have to look at the rsp register to see where our input has been stored ('A' in ASCII is 41): 
```
gdb-peda$ x/20gx $rsp
```
![RSP values](images/rsp_values.png)

If we looks closer we can see the value "0x6f54534ae2410d00", this "strange" value which is different from the others on the stack is the canary (8 bytes, the length of the word, that change in every program execution), so we have to do the buffer overflow writing the exact same value on this position. 

As the canary changes in each execution we have to print it with a format string vulnerability in order to add it to the payload (in the "canary" binary we can make a format string vulnerability in the line "printf(strcat(name, "!\n"));"). To print we should use some %p to see in which position the canary is printed, in this case is the position 17 (it is recommended to see some format strings [videos](https://www.youtube.com/watch?v=0WvrSfcdq1I)):

![RSP values](images/format_string.png)

Now, we have the canary value which will be added to our payload. The next step is to overwrite the return address of the function in order to redirect the program to the "flag" function and gets our flag. 


**4. Getting the return address of the function**






