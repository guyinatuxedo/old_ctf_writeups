#this imports the two libraries, pwntools and rstr (what we will use to solvv)
from pwn import *
import rstr

#This establishes the connection that we will use
conn = remote('misc.chal.csaw.io', 8001)

#This line will take the first line of text from the server, which is junk
conn.recv()

#This is the loop that will perform all of the work
while True:
	
	#This will store the regex expression from the variable
	exp = conn.recv()


	#This will check to ensure that we don't have a flag, and we didn't make an issue
	if 'Irregular' in exp:
		print exp
		break
	if 'flag' in exp:
		print exp
		break

	#This will find a string value that meets the regex expression
	val = rstr.xeger(exp)
	print "String meeting regex value is: " + val

	#The server will not accept responses with a space in it, so we have to 
	while '\n' in val[:-1]:
		print 'Extra line found in string value, correcting'
		val = rstr.xeger(exp)
		print "New string: " + val	
	
	#And finall send the server back the response to proceede to the next level
	conn.send(val)
