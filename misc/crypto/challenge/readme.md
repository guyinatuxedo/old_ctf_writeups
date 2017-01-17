#Challenge

Here is a PCAP file. In the PCAP file there is a secret transmission. Your mission should you choose to accept, find the transmission. The transmission will be in the flag{<insert string here>} format.

#Solution

The first thing that you have to do is look at the PCAP the file.The PCAP file has two tcp streams (0 & 1). The first stream is a download for a python script. The second is a communications using the script that holds the encrypted message. The first thing that you need to do is look at the TCP stream for 0, and then you can tell that it is a python Download. You can strip the file via file > export object. It will export a .pyc file which is a compiled python file. I decompiled it using Uncompyle6 (excuse my spelling) (see attached). Proceeding that the code exported should math below.

```
import socket
from Crypto import Random
rand = Random.new()
from Crypto.Cipher import AES
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.188.129', 54321))
welcome = s.recv(1024).strip('\n')
print welcome
g = s.recv(1024).strip('\n').split('g:')[1]
print g
p = s.recv(1024).strip('\n').split('p:')[1]
print p
A = s.recv(1024).strip('\n').split('A:')[1]
print A
prompt = s.recv(1024).strip('\n')
print prompt
A = int(A)
g = int(g)
p = int(p)
b = int(rand.read(8).encode('hex'), 16)
B = pow(g, b, p)
s.send(str(B))
my_key = pow(A, b, p)
print 'secret key: {}'.format(my_key)
msg = s.recv(1024).strip('\n')
print '********************'
print 'encrypted message:'
print msg.encode('hex')
print ''
plain = ''
for i in msg.split('\n'):
    if not i.startswith('Good data!'):
        aes_key = hex(my_key).strip('0x').strip('L')
        while len(aes_key) < 32:
            aes_key = '0' + aes_key

        obj = AES.new(aes_key.decode('hex'), AES.MODE_CBC, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        plain += obj.decrypt(i)

print plain
```

Now there are a couple of key things to note in this code. The first is that there are several variables A, g, p, b, and B. The bulk of these variables are given in the second tcp stream. The second is that it uses AES encryption, and it uses hex. The third important thing is how it gets a value for B, which it is derived using the python pow() function. Let’s say you have pow(x, y, z). This is equivalent to x^y % z. ^ is for exponential so it is x to the y power. Then % is for modulus, which basically means it divides a number by z long handed, then outputs the remainder. So pow(x, y, z) is the remainder of x^y power long handed divided by z. In this case B, which is our AES encryption key is determine by pow(g, b, p). We have a and p, however we need to find b. This can be done by using bdcalc and then inputting the following commands. Essentially we are just doing pow(x, g, p) with x being a random number until the solution ends up being B.

```
> x=123114413580763739;g=429072158523821662;p=594830787528835483  # INPUT
> b=1;for k in (1..p) do b=modmul(b,g,p);breakif(b==x) done;
  println("The discrete log of ",x," to the base ",g," mod ",p," is ", k)
```

The discrete log of 123114413580763739 to the base 429072158523821662 mod 594830787528835483 is 747027

Now the final stage is at hand. Now we have to write a python script to decrypt it. Since we have all of the values now we just have to have the message. Essentially in the second tcp sequence it gives us the text that was encrypted, however since it was hex we would have to take the hex value for it. Proceeding that we just redesign or make an entirely new script to decode it.

```
rom Crypto import Random
from Crypto.Cipher import AES

g=429072158523821662
p=594830787528835483
A=313868463457946531
B=123114413580763739

print pow(g,747027,p)
b=747027

msg_hex="476f6f642064617461210a09f5d9d2c41db04aee983854244cc3435a6daa90d3e186b509c3ac9d4a94dc440a"
msg=msg_hex.decode('hex')
print 'encrypted message:'
print msg.encode('hex')
msg=msg.strip('\n')

plain = ''
my_key = pow(A, b, p)
for i in msg.split('\n'):
    if not i.startswith('Good data!'):
            aes_key = hex(my_key).strip('0x').strip('L')
            while len(aes_key) < 32:
                    aes_key = '0' + aes_key
            obj=AES.new(aes_key.decode('hex'),AES.MODE_CBC,'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            plain += obj.decrypt(i)

print plain
```

The flag should be “flag{breaking_dh_like_the_nsa!}”
