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

