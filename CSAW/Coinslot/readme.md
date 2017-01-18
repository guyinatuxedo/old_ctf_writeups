Credit to the HackUCF CTF Workshop 9/25/16 for showing me how to do this.

#Challenge

Hope #Change #Obama2008
nc misc.chal.csaw.io 8000

This challenge is a misc challenge from CSAW 2016 Quals worth 25 points.

#Solution

The first line isn’t very helpful, probably just a joke. The line below that indicates that we need to connect to a server. If you’re in linux you can just type in that command (provided you have netcat installed). When you do that you should see something similar to the pic on page 3.

Now looking on that pic, it seems as they want to give us a money amount, and sort it into an array of values based upon fitting as many top level entries in the array as possible. After we successfully sort out one level, it will bring us to the next. With challenges like these, the ctf will want you to script out the process. It will try to stop you by requiring the task to be done like 500 times, all correct, and done within like 5 seconds each. Trust me, I’ve tried to do challenges like this by hand, it’s much better to script it out.

Now for this challenge i’ve used python with a library known as pwntools. To install it use the following command.

```
sudo pip install pwntools
```

After that you will need to code it. You can use google, or just look at the commented code script I made below.  Keep in mind that when it gets the flag, the server will output a variable since it can’t convert a string to a float that has words in it. Also it will be missing the first letter since the script removes the first character since there is a dollar sign there. Also keep in mind that some of the comments down below are formatted to be in two lines, however they should be one.

Flag:
Flag{started-from-the-bottom-now-my-whole-team-fucking-here}

I’ve posted the final output of the script with the flag on the next page.

```
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
    
    #This retrieves the value from the server that we money value that we will be sorting. It will  
    Remove the first character from the string to get rid of the dollar sign.
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
```    






