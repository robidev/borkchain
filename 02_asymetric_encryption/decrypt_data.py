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


data_file = open("crypted.bin", "rb")
data = data_file.read()
data_file.close()

message = ""
for b in data:
    c = int(b)
    m_decrypt = square_and_multiply(c,private_key_d,private_key_n) #pow(c,private_key_d) % public_key_n
    message += str(chr(m_decrypt))

print("decrypted message: " + message)
