from math import gcd


p = 11# prime 1
q = 19 # prime 2

n = p * q
phi = (p - 1) * (q - 1)

print("p:" + str(p) +" q:" + str(q) +" n:" + str(n) +" phi:" + str(phi))


suggested_e = 1337
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
print("private key: 0x%08x,0x%08x" % (n,d))

keyfile = open("public_key.bin", "wb")
keyfile.write((n).to_bytes(4,byteorder='big'))
keyfile.write((e).to_bytes(4,byteorder='big'))
keyfile.close()

keyfile = open("private_key.bin", "wb")
keyfile.write((n).to_bytes(4,byteorder='big'))
keyfile.write((d).to_bytes(4,byteorder='big'))
keyfile.close()




