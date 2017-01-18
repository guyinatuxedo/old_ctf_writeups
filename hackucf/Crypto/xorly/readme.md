Let’s take a look at the source code for the python script.

```
#!/usr/bin/env python2


def encrypt(plaintext, key):


    ciphertext = []
    for i in xrange(0, len(plaintext)):
        ciphertext.append(ord(plaintext[i]) ^ ord(key[i%len(key)]))


    return ''.join(map(chr, ciphertext))


decrypt = encrypt


'''
I'll give you a sample of how this works:


Plaintext:
"Here is a sample. Pay close attention!"


Ciphertext: (encoded in hex)
2e0c010d46000048074900090b191f0d484923091f491004091a1648071d070d081d1a070848


Flag: (encoded in hex, encrypted with the same key)
0005120f1d111c1a3900003712011637080c0437070c0015
'''
```

So looking at this code, we can tell that this program establishes a function which takes two inputs. That function will then xor those two inputs and output that. The function for xor is “^”. Xor works by comparing the actual binary. If both are the same, it outputs a 0. If not it outputs a 1


Xor example
```
1 ^ 0 = 1
1 ^ 1 = 0
0 ^ 0 = 0
0 ^ 1 = 1
```
Xor reversible example
```
0 ^ 1 = 1
0 ^ 1 = 1
0 ^ 0 = 0
1 ^ 1 = 0
```

So in order to decrypt this, we will need the key it was xored with since xor is reversible. You can xor the output with the input, and that will give you the key. In the comments, we can see that it gives us plaintext, and ciphertext. So we just need to xor those two things together and that should give us the key.

```
#We establish the input, and output as variables
input = "Here is a sample. Pay close attention!"
output = "2e0c010d46000048074900090b191f0d484923091f491004091a1648071d070d081d1a070848".decode("hex")


#We set up the variable which will store the key
key = []


#This for loop will run the xoring
for i in xrange(0, len(input)):
    key.append(ord(input[i]) ^ ord(output[i%len(output)]))


#This for loop wil print out each item in the flag list
for i in range(0, len(key)):
    print chr(key[i])
```

After running this, we get “fish” repeating. Because of that we can tell the “fish” is the key. So now that we have the encrypted flag, and the key we can just xor those two things together and get the flag.

```
#We establish the variables which will store the key, and the encrypted flag
key = "fish"
encf = "0005120f1d111c1a3900003712011637080c0437070c0015".decode("hex")


#We establish the flag list
flag = []


#We xor the key, and the encrypted data together and store it in the flag list
for i in xrange(0, len(encf)):
        flag.append(ord(encf[i]) ^ ord(key[i%len(key)]))


#Here we join the list, and convert it all back to ascii and print the flag
print ''.join(map(chr, flag))
```



Flag: flag{xor_is_the_new_aes}
