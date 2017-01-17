This is a challenge from the trnd micro ctf 2016, and was worth 100 points.

First thing we pop open the file and see what type of protocols we have

ARP
ESP
ISAKMP
NBNS
TCP
TELNET

ARP is just address resolution, so it probably won’t hold anything of value (at least that we should visit first). ESP is a form of encryption that is a part of the IPSec suite, so there is probably something worth of value in there. ISAKMP is a the Internet Security Association and Key Management Protocol, so it probably manages the keys for the EPS encryption. NBNS is NetBIOS name system is like a limited DNS service, so we probably won’t want to start our search there. TCP is used to establish and maintain a network connection, so that might be a good place to start. Telnet is a cli remoting protocol that is unencrypted so that will probably be the best place to start. To look at it just follow the tcp stream of the telnet packets.

Doing this reveals the telnet session. It gives us some things like credentials for the system, the output for an ifconfig. We see some currently established network connections from several different netstat commands. Next we see IP XFRM which is a protocol that is used to encrypt ip communications (remember ESP), which the command gives us the current state of the encrypted communications, along with the keys and everything needed to decrypt the ESP packets.  

Now to actually get around to decrypting it. We find four entries, in which we will decode all four. Below is an example of an entry 


```
src 1.1.1.11 dst 1.1.1.10
    proto esp spi 0xfab21777 reqid 16389 mode tunnel
    replay-window 32 flag 20
    auth hmac(sha1) 0x11cf27c5b3357a5fd5d26d253fffd5339a99b4d1
    enc cbc(aes) 0xfa19ff5565b1666d3dd16fcfda62820da44b2b51672a85fed155521bedb243ee
```


We will need several pieces of data in order to decrypt an entry. Firstly we will need the source (src) and destination (dst) ip address. The source ip address is “1.1.1.1” and destination ip is “1.1.1.10”. Secondly we will need the spi. The spi (Security Parameter Indexes used to identify the SA) in this case is “0xfab21777”. Thirdly we will need to know what encryption protocol and key it uses. This uses AES-CBC [RFC3602] encryption and the encryption key is 

```
“0xfa19ff5565b1666d3dd16fcfda62820da44b2b51672a85fed155521bedb243ee”
```

astly we will need to know what authentication protocol and key it uses. It uses HMAC-SHA-1-96 [RFC2404] and the key it uses is “0x11cf27c5b3357a5fd5d26d253fffd5339a99b4d1”. After this we will have all of the information need to decrypt this entry. To decrypt it navigate to edit>preferences>protocols>esp, check everything then click the “edit” button for ESP SAs (SA stands for Security Association which is a one way cryptographically protected connection).

Edit>Preferences>ESP

![alt tag](http://i.imgur.com/pEp1rst.png)



















