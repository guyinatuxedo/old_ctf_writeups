Credit to HackUCF CTF Workshop 9/25/16 for showing me how to solve this

#Challenge

Only true hackers can see the image in this magic PNG....
nc crypto.chal.csaw.io 8000
Author: Sophia D'Antoine
*There is a download to a file named sleeping_dist.py

This is called Sleeping Guard, and was a crypto challenge from CSAW Quals 2016 ctf worth 50 points.

#Solution 

Well when we try to netcat into the server (I attached the output as ncoutput), we get a giant wall of text (may or may not be an encrypted image). If you look through it, you can tell that it is Base64. Feel free to google how to know that. Also if you look at the python script that it gives us, it encodes a .png image in Base64. Let’s have a look at that script now.

```
import base64
from twisted.internet import reactor, protocol
import os

PORT = 9013

import struct
def get_bytes_from_file(filename):  
    return open(filename, "rb").read()  
    
KEY = "[CENSORED]"

def length_encryption_key():
    return len(KEY)

def get_magic_png():
    image = get_bytes_from_file("./sleeping.png")
    encoded_string = base64.b64encode(image)
    key_len = length_encryption_key()
    print 'Sending magic....'
    if key_len != 12:
        return ''
    return encoded_string
    

class MyServer(protocol.Protocol):
    def connectionMade(self):
        resp = get_magic_png()
        self.transport.write(resp)

class MyServerFactory(protocol.Factory):
    protocol = MyServer

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
}
```

If you look through the script, we can see that it is indeed Base64 encryption. In addition to that we can see that the encryption key it uses is 12 bytes long. Let's try to base64 decode the image.

```
nc crypto.chal.csaw.io 8000 | base64 --decode > decoded.png
```

Now since we have the file decoded, we will try to open it. Upon trying to open and view it, we find out that we cannot. This is because that the file is still encrypted with some form of encryption. Since it is a low level challenge, it is a pretty safe guess to assume that it is XOR encryption. To decrypt the file we will need to get the key. Luckily for us we can get the key, if we can XOR the file (or apart of it) with the decrypted value. Since it is a png file we already know the first part of the file which will be the header. Headers basically say what the file is. So we can open up any normal png file with a hex editor and copy and paste the first 12 bytes (recall that they key is twelve bytes) and xor it against the first 12 bytes of the encrypted data. I used bless for this.

PNG header bytes:
```
89 50 4E 47 0D 0A 1A 0A 00 00 00 0D
```

Encrypted png header bytes:
```
DE 3F 0F 2F 52 4B 45 41 65 79 21 32
```

Now to actually XOR the two headers, you can go about it multiple ways. You can use some online service, interactive shell, or script it out like what I did. The script I used is below, along with the decimal and ascii values of the flag.

key_xor.py

```
#First we set the list that will contain the header bytes of a png file
a = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d]

#This list contains the header bytes of the encrypted png file
b = [0xde, 0x3f, 0x0f, 0x2f, 0x52, 0x4b, 0x45, 0x41, 0x65, 0x79, 0x21, 0x32]

#This sets the list the we will store the decrypted values
data = []

#This for loop will decrypt the values
for i in range(12):
    print "Xoring " + str(a[i]) + str(b[i])
    data.append(a[i] ^ b[i])

#Just printing some output of the above loop, this will be in decimal format
print data
print "Converting decimal to ascii"

#This sets the string variable that will store the converted decimal value
key = ""

#This loop will convert the decimal value to ascii
for i in range(12):
    key += chr(data[i])

#This prints out the key
print key
}
```

Decimal Key Value:
```
“[87, 111, 65, 104, 95, 65, 95, 75, 101, 121, 33, 63]
```

ASCII Key Value
```
WoAh_A_Key!?
```

Now that we have the key, we can try to go ahead and xor that key with the rest of the encrypted data. I did this using a script, you can do so as you please. I posted my script below.

Pic_xor.py
```
#First we establish the key we found earlier as a bytearray
key = bytearray([0x57, 0x6f, 0x41, 0x68, 0x5f, 0x41, 0x5f, 0x4b, 0x65, 0x79, 0x21, 0x3f])

#Now we establish the encrypted png data as a bytearray
edata = bytearray(open('out.png', 'rb').read())

#Now we establish the function which will do the xor decryption
def xor(edata, key):
    l = len(key)
    return bytearray((
        (edata[i] ^ key[i % l]) for i in range(0,len(edata))
    ))

#Now we actually run the dexoring function and write it to a file
with open('dexored.png', 'w') as file_:
    file_.write(xor(edata,key))
```

And after that, we are left with a wonderful picture, dexored.png. Just viewing the picture, will give you the flag.








