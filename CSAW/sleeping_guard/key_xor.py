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








