This solution assumes you have gone back and went through Repetition 1. I’m not going to repeat everything. First let’s try to run the script from the first challenge and see what happens. Since this is a different challenge we will need to change the port. To do that change the port on the line that establishes the port (it’s the part that is in red).

```
conn = remote('ctf.hackucf.org', 10101)
```

To

```
conn = remote('ctf.hackucf.org', 10102)
```

Once the challenge gets to the end, it asks us for the first value added. So this just adds an additional aspect to the challenge, but it shouldn’t be too hard. Just edit the code to record the first value, then send it when it gets to the end. I posted the code which I made to solve this challenge, complete with comments. Keep in mind when the script finishes, it will crash but it will print out the flag before that. Keep in mind that like the first, when this script finishes it crashes but it prints out the flag.

```
#These comments assume that you have been through Repetition 2
#This imports the pwntools library
from pwn import *


#This sets up the remote connection to the challenge
conn = remote('ctf.hackucf.org', 10102)


#This prints out the first two lines from the challenge
print conn.recvline()
print conn.recvline()


#This sets up two string variables which will be used in the while loop
c = ""
b = ""


while True:
    
    b = conn.recvline()
    print b
    b = b.replace("Value: ", "")
    b = b.replace("Repeat: ", "")
    #This loop will trigger upon the first iteration, and store the value it sends in a variable
    if c=="":
        c = b
    #This will check to see if it has reached the end of the challenge, and print out the original value
    if "Good job!" in b:
        print conn.recvline()
        print conn.recvline()
        print "sending: " + c
        conn.sendline(c)
        print conn.recvline()
    #This will just send the value normally, provided it hasn't reached the end of the challenge
    else:
        print "sending: " + b
        conn.sendline(b)
```





