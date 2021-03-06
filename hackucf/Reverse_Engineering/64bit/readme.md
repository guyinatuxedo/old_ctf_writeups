Ok let’s look at the file first, and see what it is.

```
file 64bit
```

So we know it is a 64 bit linux executable file (64 bit ELF). Let's make it executable then run it to see what happens.

```
chmod +x 64bit
./64bit
```

So it asks us for a passkey, and when we give it one it says how much of a failure we are and terminates the program. It’s time 
to fire it up in IDA and see what the program actually does. Keep in mind, we will need to use IDA 64 bit instead of 32 bit.


When we open up IDA, let’s look in the strings tab to see what is there. To do this just go to view, then open subviews, then 
strings. When we do that we see the following strings.

```
Enter key:
Win :3
Try again
;*3$\
```

Well we have already seen the “Enter key:” and “Try again” strings, but the “Win :3” string looks like it might lead us to 
something useful. When we double click on that string, it brings us to the main function’s assembly code. We can view pseudocode 
for that function by pressing tab while we are in the main functions assembly code. Looking at the code, we can tell that it 
first print’s out “Enter key:”, then it scans for input, takes that input and runs it through a function called “encrypt”, then 
compares the output of that function to the hex value “0xdeadbeef”. If they match then it prints out the flag. So let’s look at 
decrypt (You can just double click on it to view it).


Looking at it, all it does is it accepts input (which would be what the previous function scanned) and xors it with the decimal 
“1234” (in hex it’s “0x4d2”). If you don’t know what xoring is it basically just looks at the individual bits, if they are the 
same it outputs a 0. If they aren’t then it outputs a 1. Thing about this is it is reversible. So we know what it is xoring the 
input by, and we know what value it wants. So we can just xor the hex value “0x4d2” with “0xdeadbeef” and that should give us the
value we need to win. To do this I used python in terminal, but there are a million different tools you can use. Below are the 
commands I used to do this (btw in python the xor operator is “^”)

```
python
print 0xdeadbeef ^ 0x4d2
```

With that it should print out the decimal value “3735927357”. When we take that decimal value and give it to the program as a 
flag, it tells us we have won. Looking at the challenge it tells us that the key is the flag, so it isn’t in a traditional format.


Flag: 3735927357





