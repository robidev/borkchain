
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
        


print("the alphabet in ordinal (ord):")
print("letter | number (ASCII value)")
for letter in "abcdefghijklmnopqrstuvwxyz_":
    print("   " + letter + "  =>  " + str(ord(letter)))
print("")

print("lets hash some data:")
data_to_be_hashed = "this_is_a_scentence"
print("the data we will hash: " + data_to_be_hashed)
resulting_hash = hash(data_to_be_hashed)
print("hash: " + hex(resulting_hash))
print("")
data_to_be_hashed = "ecnetnecs_a_si_siht"
print("the reverse we will hash: " + data_to_be_hashed)
resulting_hash = hash(data_to_be_hashed)
print("hash: " + hex(resulting_hash))
