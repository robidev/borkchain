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


keyfile = open("private_key.bin", "rb")
private_key_n = int.from_bytes(keyfile.read(4), "big")
private_key_d = int.from_bytes(keyfile.read(4), "big")
keyfile.close()
print("private key:  0x%08x,0x%08x" % (private_key_n,private_key_d))


data_file = open("data.txt", "r")
data = data_file.read()
data_file.close()

data_hash = hash(data)

# convert into hex-sting
data_hash_string  = f"%08x" % data_hash
print("hash: " + data_hash_string)

# encrypt hash with private key, and store in signature
signature_file = open("signature.bin", "wb")
for b in data_hash_string:
    m = int(b,16)
    s = square_and_multiply(m,private_key_d,private_key_n) 
    signature_file.write(bytes([s]))
signature_file.close()

