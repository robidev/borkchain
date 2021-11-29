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

crypted_file = open("crypted.bin", "wb")
for b in data:
    m = ord(b)
    c = square_and_multiply(m,public_key_e,public_key_n) #pow(m,public_key_e) % public_key_n
    crypted_file.write(bytes([c]))
crypted_file.close()

