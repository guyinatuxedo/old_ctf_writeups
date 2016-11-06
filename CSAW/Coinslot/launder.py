#import the library which we will use
from pwn import *

#this sets up the socket connection which will be used
conn = remote('misc.chal.csaw.io',8000)

#this will establish the array that will store all of the values for laundering
currency = [10000.0, 5000.0, 1000.0, 500.0, 100.0, 50.0, 20.0, 10.0, 5.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.01]

#this will establish the variable use to count the iterations
iteration = 0

#This is the loop that will sort the money
while(1==1):

	#This adds one to the variable iteration to keep track of the amount of times this loop has run
	iteration += 1
	
	#This retrieves the value from the server that we money value that we will be sorting
	wanted = float(conn.recvline()[1:])

	#This just prints the amount that we are going to sort
	print "amount to be laundered is " + str(wanted)

	#This is the for loop that will actually do the sorting by seeing how many times each monetary amount defined in the array currency into the requested value 
	for i in currency:

		#This does the simple calc by dividing the sorting value by the current i value
		div = int(wanted/i)

		#This prints off the result of the above calculation
		print str(i) + " goes into " + str(wanted) + " " + str(div) + " times."
		
		#This actually writes the remaining valueof the amount left to be sorted and saves it to the wanted variable, then sends the information over to the server
		wanted = round((wanted - (div*i)), 2)
		conn.sendline(str(div))

		#This prints out the amount left to be sorted
		print str(wanted) + " is left to be laundered"

	#This prints out that it is done sorting the money, prints out the amount of times it has sorted money, and the output from the server
	print "done laundering mondey " + str(iteration)
	print conn.recvline()
	
