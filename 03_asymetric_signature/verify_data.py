def hash(scentence):
    h = 0                      # initialise h
    for letter in scentence:   # for eacht letter in a sentence
        number = ord(letter)   # get a letter from the scentence to be hashed

        h = (h << 4) + number  # shift h 4 bits left, add in a letter
        g = h & 0xf0000000     # get the top 4 bits of h
        if g != 0:             # if the top 4 bits aren't zero,
            h = h ^ (g >> 24)  # move them to the low end of h
            h = h ^ g          # XOR g and h
    return h
        

def square_and_multiply(x, k, p=None):
    """
    Square and Multiply Algorithm
    Parameters: positive integer x and integer exponent k,
                optional modulus p
    Returns: x**k or x**k mod p when p is given
    """
    b = bin(k).lstrip('0b')
    r = 1
    for i in b:
        r = r**2
        if i == '1':
            r = r * x
        if p:
            r %= p
    return r


keyfile = open("public_key.bin", "rb")
public_key_n = int.from_bytes(keyfile.read(4), "big")
public_key_e = int.from_bytes(keyfile.read(4), "big")
keyfile.close()
print("public key:  0x%08x,0x%08x" % (public_key_n,public_key_e))

data_file = open("data.txt", "r")
data = data_file.read()
data_file.close()

data_hash = hash(data)

# convert into hex-sting
data_hash_string  = f"%08x" % data_hash
print("hash: " + data_hash_string)

signature_file = open("signature.bin", "rb")
signature = signature_file.read()
signature_file.close()

index = 0
verified = True
for b in data_hash_string:
    s = square_and_multiply(signature[index],public_key_e,public_key_n) 
    m = int(b,16)
    if s != m:
        verified = False
    index += 1

if verified == True:
    print("signature matches")
else:
    print("signature does not match")



