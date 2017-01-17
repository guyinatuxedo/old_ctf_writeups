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
