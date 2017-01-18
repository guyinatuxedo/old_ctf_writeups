We are given a python script “dizzy.py”, and a text file with some UTF-8 characters “dizzy_flag”. Let’s take a look at the python script.

```
def makeMeDizzy(flag):
    cFlag = ''
    for c in flag:
        cv = ord(c) << 13
        cv = cv >> 4
        cv = cv << 1
        cv = cv >> 2
        cv = cv << 4
        cv = cv >> 4
        cv = cv << 5
        cv = cv >> 13
        cv = cv << 10
        cv = cv >> 4
        cv = cv << 7
        cv = cv >> 12
        cv += 1
        cFlag += chr(cv)
    
    f = open('dizzy_flag','wb')
    f.write(cFlag)
        
if __name__ == '__main__':
    flag = '' # This is almost a gimme
    makeMeDizzy(flag)
```


Looking at this code, we can tell that it establishes a function then imports a string from the first line of code. Proceeding that it creates an empty string variable called “cFlag”. Proceeding that it creates a for loop that will run for every letter in the imported string. The For loop takes each character, converts it to decimal using the ord function, then shifts around the bytes using a combination of the . Proceeding that, it just adds 1 to the value, converts it back into a character (which by now it is UTF-8 which is a character that isn’t ascii, or in other words on your keyboard) and adds it to the ”cFlag”. After the loop is completed it just writes the “cFlag” variable to the file we are given. Everything we did here should be able to be reverse with a python script. First let’s review the bitwise operators “<<” and “>>”.


All “<<” and “>>” do is they just shift the binary value of an integer or bits a certain amount of bits to the left or right. For instance


“1110101 >> 3 = 1110”
This operator shifts the bits 3 places to the left, effectively removing the last three bits. 


“1110 << 3 = 1110000”
This operator shifts the bits 3 places to the right, and added zeroes to the new places. So it effectively just added 3 zeroes to the end. Now notice that the end value is not the same. This is because we originally had some “1” values which were removed and replaced with “0”. So not every value can be reversed easily, but hopefully we shouldn’t have any issues.


Now it is just a matter of writing a script to undo it. It is in the same folder on my github, but just incase for whatever reason you can’t reach it here it is. Essentially it just undoes everything. Refer to the comments in the code for explanation as to what everything does.


```
#Since we are dealing with UTF-8 Encoding, we need to declare that with the comment below
# -*- coding: utf-8 -*-


#This set's up the empty string variable which will hold the flag
flag = ''


#This list conatins all of the UTF-8 characters from the encoded flag file.  Keep in mind that if you #cat the file, it will not display the characters correctly
enc = [u"ï", u"Ç", u"ç", u"Ç", u"÷", u"", u"å", u"g", u"¿", u"ó", u"a", u"ë", u"¿", u"É", u"c", u"õ", u"õ", u"ó", u"", u"¿", u"³", u"ß", u"ë", u"¿", u"ç", u"Ñ", u"ß", u"ë", u"Ù", u"É", u"Ý", u"é", u"¿", u"Å", u"Ë", u"û"]




#This is the for loop that will actually reverse the encryption process. It will run for each character #in the enc list
for c in enc:
    #Here we convert the letter to its decimal value
    cv = ord(c)
    
    #Here we reverse the binary shifting in the opposite order it was encrypted
    cv = cv << 12
    cv = cv >> 7
    cv = cv << 4
    cv = cv >> 10
    cv = cv << 13
    cv = cv >> 5
    cv = cv << 4
    cv = cv >> 4
    cv = cv << 2
    cv = cv >> 1
    cv = cv << 4
    cv = cv >> 13


    #After the shifting is complete, we add the character to the flag variable
    flag += chr(cv)
   
#Lastly after the decoding is complete, we print out the flag
print flag
```


Flag: wcsc{Ar3_y0u_d1zzy?_You_shouldnt_be}
