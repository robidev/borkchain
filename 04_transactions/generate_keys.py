from math import gcd
from random import random, seed
from time import time


def hash(scentence):
    h = 0                      # initialise h
    for letter in scentence:   # for eacht letter in a sentence
        number = letter   # get a letter from the scentence to be hashed

        h = (h << 4) + number  # shift h 4 bits left, add in a letter
        g = h & 0xf0000000     # get the top 4 bits of h
        if g != 0:             # if the top 4 bits aren't zero,
            h = h ^ (g >> 24)  # move them to the low end of h
            h = h ^ g          # XOR g and h
    return h
        

p = 11# prime 1
q = 19 # prime 2

n = p * q
phi = (p - 1) * (q - 1)

print("p:" + str(p) +" q:" + str(q) +" n:" + str(n) +" phi:" + str(phi))

seed(time())
suggested_e = int(random()*0xffff)
print("finding no common demoninator except 1 for a number near:" + str(suggested_e))

# finding no common demoninator except 1 for a number near e
e = -1
for temp in range(suggested_e,0xffffffff):
    if gcd(temp, p-1) == 1: # e and p have no common factors except 1)
        if gcd(temp, q-1) == 1: # e and p have no common factors except 1)
            e = temp
            break

if e == -1:
    print("error: could not find e with lowest denominator 1 for " + str(suggested_e))
    exit()
print(e)

d = -1
for d_temp in range(1,0xffffffff):
    if ((e*d_temp)-1)%phi==0:
        d = d_temp
        break

if d == -1:
    print("error: could not find d in e*d==1(mod phi)")
    exit()
print(d)




print("public key:  0x%08x,0x%08x" % (n,e))
print("public key hash: 0x%08x" % hash(n.to_bytes(4,byteorder='big') + e.to_bytes(4,byteorder='big')))
print("private key: 0x%08x,0x%08x" % (n,d))



keyfile = open("public_key.bin", "wb")
keyfile.write((n).to_bytes(4,byteorder='big'))
keyfile.write((e).to_bytes(4,byteorder='big'))
keyfile.close()

keyfile = open("private_key.bin", "wb")
keyfile.write((n).to_bytes(4,byteorder='big'))
keyfile.write((d).to_bytes(4,byteorder='big'))
keyfile.close()




