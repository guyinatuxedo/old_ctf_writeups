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
