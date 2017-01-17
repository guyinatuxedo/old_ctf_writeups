#Objective: Get the flag

#Solution
Ok we get a zip file. When we open it up, we get three files. One is labelled “x”, one is labeled “z” and “Harambe.jpg”. Looking at the three files, x appears to be code, z appears to be encoded data, and Harambe.jpg is an actual picture of Harambe (it could contain steganographic encrypted data). Let’s look at the code from “x”

File x:
```
data = bytearray(open('y', 'rb').read())
for i in range(len(data)):
    data[i] ^= int
open('z', 'wb').write(data)
```

This appears to be python code. Looking at it closer we can see this.

```
data = bytearray(open('y', 'rb').read())
```

This is essentially taking the data from a file named ‘y’, opened it as a binary read (you can tell from the ‘rb’), and then stores it as a byte array variable named data.

```
for i in range(len(data)):
    data[i] ^= int
```

Looking back at this, this is a for loop for every byte in the bytearray “data” it will go ahead and set data equal to the result of xoring* itself converted to an integer with another integer. Right here we do not have an integer there, we just have the word “int”.

```
open('z', 'wb').write(data)
```

And finally we have this line. Since in the loop above it changes the value of the data variable to the encrypted data, this line just opens up a file named ‘z’ as write binary (that is a result of the ‘wb’ parameter) and then writes the data variable to it. It is probably safe to assume that this script took the file y, encrypted it using xor and an unknown key, and then stored it in a file named “z” (which we have).

After looking over the script and the other files, it’s pretty safe to say that that script encrypted the text into the file ‘z’ using xor encryption. Good thing is xor is reversible, however we need the key. To that we can either turn to the harambe picture (there is nothing there), or we can brute for the key. To brute force the key, you can either do it manually, or script it out. In order for the script to work it either has to be a number less than 256 (so it can be converted to binary), or in binary so it shouldn’t be too hard to brute force it. Right now if you were to run the script it wouldn’t run due to the improper value. We can just try different keys until we get something useful. Also we will need to change the input to ‘z’ and the output to whatever we want.

After a while, you have probably found the key. The key is ‘101’. So the script should resemble something like this.

```
data = bytearray(open('z', 'rb').read())
for i in range(len(data)):
    data[i] ^= 101
open('a', 'wb').write(data)
```

Providing that the file ‘a’ does exist, and your script resembles this then the flag should be exported to a. The flag is the one below.

```
guyctf{h@r@mb3_5Mas3s_byte_3ncRTypt0n}
```





