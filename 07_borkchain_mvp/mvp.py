from time import time


def hash(scentence):
    h = 0                      # initialise h
    for letter in scentence:   # for eacht letter in a sentence
        number = letter#ord(letter)   # get a letter from the scentence to be hashed

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
    the algortithm factorizes k into powers of 2, and 
    """
    b = bin(k).lstrip('0b') # convert to bit-sequence string, and remove leading '0b'
    r = 1                   # we split up k by factors of 2, as a^(A+B) == a^A * a^B, e.g. 5^9 == 5^1 * 5^8
    for i in b:             # for each bit do,
        r = r**2            # calculate the power-value based on this bit position (i.e. 1,2,4,8,16,32,64,128,...)
        if i == '1':        # if bit is set in k; we multiply it with x
            r = r * x       # multiply bit-position value with x, and assign back to r
        if p:               # if a modulo is set, 
            r %= p          # then perform immediately, to prevent overflow. a^(A+B) mod c == a^A mod c * a^B mod c
    return r                # return result


def sign(data, private_key):
    private_key_n = private_key[0]
    private_key_d = private_key[1]
    #print("private key:  0x%08x,0x%08x" % (private_key_n,private_key_d))

    data_hash = hash(data)                      # hash the data to be signed
    data_hash_string  = f"%08x" % data_hash     # convert into hex-sting for processing
    #print("hash: " + data_hash_string)

    # encrypt hash with private key, and store in signature
    signature = []
    for b in data_hash_string:  # for each hex value
        m = int(b,16)           # convert to numbers between 0 and 15(nibbles), to ensure result fits in a byte
        s = square_and_multiply(m,private_key_d,private_key_n) # square and multiply; the RSA encrypt function when used with a coprime
        signature.append(bytes([s]))
    return signature


def verify(data, signature, public_key):
    public_key_n = public_key[0]
    public_key_e = public_key[1]

    # print("public key:  0x%08x,0x%08x" % (public_key_n,public_key_e))
    data_hash = hash(data)                      # hash data to be checked
    data_hash_string  = f"%08x" % data_hash     # convert into hex-sting for processing
    #print("hash: " + data_hash_string)

    index = 0
    verified = True
    for b in data_hash_string:
        #print("s: %i" % int(signature[index][0]))
        s = square_and_multiply(int(signature[index][0]),public_key_e,public_key_n) # decrypt signature with RSA public key
        m = int(b,16) # convert to numbers between 0 and 15(nibbles), to ensure result fits in a byte
        if s != m:    # check if this nibble matches the decrypted signature
            verified = False
            break
        index += 1
    return verified


def generate_block(previous_hash, merkle_transactions_hash, transactions_list,time = None, nBits = 0x00ffffff):
    return {
        'previous_block_hash': previous_hash,         # int
        'merkle_root_hash': merkle_transactions_hash, # int
        'time': time,                                 # int
        'nBits': nBits,                               # int
        'nonce': None,                                # int
        'transactions': transactions_list             # []
    }


def generate_block_hash(block):
    data = block['previous_block_hash'].to_bytes(4, byteorder='big')
    data += block['merkle_root_hash'].to_bytes(4, byteorder='big')
    data += block['time'].to_bytes(4, byteorder='big')
    data += block['nBits'].to_bytes(4, byteorder='big')
    data += block['nonce'].to_bytes(4, byteorder='big')
    return hash(data)


def generate_transaction(in_list,out_list):
    return {
        'tx_in_count': len(in_list),    # int
        'tx_in': in_list,               # []
        'tx_out_count': len(out_list),  # int
        'tx_out': out_list,             # []
        'time': int(time())             # int() seconds since epoch
    }


def generate_transaction_hash(transaction):
    data = transaction['tx_in_count'].to_bytes(4, byteorder='big')
    for input_item in transaction['tx_in']:
        data += input_item['TXID'].to_bytes(4, byteorder='big')
        data += input_item['index'].to_bytes(4, byteorder='big')
        data += input_item['pubkey'][0].to_bytes(4, byteorder='big')
        data += input_item['pubkey'][1].to_bytes(4, byteorder='big')

        for sig_bytes in input_item['signature']:
            data += sig_bytes # warning, may be an issue

    data += transaction['tx_out_count'].to_bytes(4, byteorder='big')
    for out_item in transaction['tx_out']:
        data += out_item['value'].to_bytes(4, byteorder='big')
        data += out_item['pubkey_hash'].to_bytes(4, byteorder='big')

    data += transaction['time'].to_bytes(4, byteorder='big')
    return hash(data)


def add_input(in_list, TXID, index, owned_pubkey, signature=None):
    in_list.append({
            'TXID': TXID,           # int
            'index': index,         # int
            'pubkey': owned_pubkey, # int[2]
            'signature': signature  # bytes[8]
        })


def add_output(out_list, value, pubkey_hash_receipient):
    out_list.append({
            'value': value,                         # int
            'pubkey_hash': pubkey_hash_receipient   # int
    })

# find item on borkchain_ledger
def get_transaction_details(TXID):
    global borkchain_ledger
    for blocks in borkchain_ledger:
        for transaction in blocks['transactions']:
            if TXID == generate_transaction_hash(transaction):  
                return transaction #return the found transaction {}
    return None

# call to fill in signature for a defined in
def add_input_signature(input_item,out_list,owned_private_key):
    data = input_item['TXID'].to_bytes(4, byteorder='big')
    data += input_item['index'].to_bytes(4, byteorder='big')
    data += input_item['pubkey'][0].to_bytes(4, byteorder='big')
    data += input_item['pubkey'][1].to_bytes(4, byteorder='big')
    for out_item in out_list:
        data += out_item['value'].to_bytes(4, byteorder='big')
        data += out_item['pubkey_hash'].to_bytes(4, byteorder='big')
    input_item['signature'] =  sign(data, owned_private_key)
    return input_item


def verify_signature(input_item,output_list):
    data = input_item['TXID'].to_bytes(4, byteorder='big')
    data += input_item['index'].to_bytes(4, byteorder='big')
    data += input_item['pubkey'][0].to_bytes(4, byteorder='big')
    data += input_item['pubkey'][1].to_bytes(4, byteorder='big')
    for out_item in output_list:
        data += out_item['value'].to_bytes(4, byteorder='big')
        data += out_item['pubkey_hash'].to_bytes(4, byteorder='big')
    return verify(data, input_item['signature'],input_item['pubkey'])


def find_transaction(input_item):
    global borkchain_ledger
    for blocks in borkchain_ledger:
        for transaction in blocks['transactions']:            
            for in_item in transaction['tx_in']:
                if input_item['TXID'] == in_item['TXID']:
                    return True # found a transaction
    return False


def check_transaction(transaction):
    available_amount = 0
    for input_item in transaction['tx_in']:
        tx_detail = get_transaction_details(input_item['TXID'])
        if tx_detail == None:
            print("error: could not find input in transaction history output")
            return False
        #get the tx_out at index
        tx_out = tx_detail['tx_out'][input_item['index']]

        if hash(input_item['pubkey'][0].to_bytes(4, byteorder='big') + input_item['pubkey'][1].to_bytes(4, byteorder='big')) != tx_out['pubkey_hash']:
            print("error: hash(pubkey) of input did not match output pubkey_hash of referenced previous transaction")
            print("i.e. you are not authorised to use this transaction as input")
            return False

        if find_transaction(input_item) == True:
            print("error: found duplicate transaction, you cannot reference an input twice")
            return False

        if verify_signature(input_item,transaction['tx_out']) == False:
            print("error: transaction signature verification failed")
            print("i.e. the public key does not match the signature, this means the private and public key do not pair up")
            return False

        available_amount += tx_out['value']

    amount = available_amount
    for output_item in transaction['tx_out']:
        amount -= output_item['value']
    # check balance
    if amount < 0:
        print("error: more spend then received")
        return False
    print("amount in transaction: %i, left: %i" % (available_amount, amount))
    return True


def generate_merkle_tree(transactions):
    amount_transactions = len(transactions)
    merkle = []
    for index in range(0,amount_transactions,2):
        h1 = generate_transaction_hash(transactions[index])
        if index+1 < amount_transactions:
            h2 = generate_transaction_hash(transactions[index+1])
        else:
            h2 = generate_transaction_hash(transactions[index])
        merkle.append(hash(h1.to_bytes(4, byteorder='big') + h2.to_bytes(4, byteorder='big')))

    while True:
        merkle_lenght = len(merkle)
        print("merkle length: %i" % merkle_lenght)
        if merkle_lenght > 1:
            temp = []
            for index in range(0,merkle_lenght,2):
                h1 = merkle[index]
                if index + 1 < merkle_lenght:
                    h2 = merkle[index + 1]
                else:
                    h2 = merkle[index]
                temp.append(hash(h1.to_bytes(4, byteorder='big') + h2.to_bytes(4, byteorder='big')))
            merkle = temp
        else:
            return merkle[0]

##########################################################################################
# load key
public_key = [0] * 2
with open("public_key.bin", "rb") as keyfile:
    public_key[0] = int.from_bytes(keyfile.read(4), "big")
    public_key[1] = int.from_bytes(keyfile.read(4), "big")
public_key_hash = hash(public_key[0].to_bytes(4, byteorder='big') + public_key[1].to_bytes(4, byteorder='big'))
print("public key:  0x%08x,0x%08x" % (public_key[0],public_key[1]))
print("public key hash: 0x%08x" % public_key_hash)


##########################################################################################
# initialise borkchain
print("generate initial transaction with 5 coins as output, on address: 0x%08x" % public_key_hash)
initial_transaction = generate_transaction([], [{'value':5,'pubkey_hash':public_key_hash}])
initial_transaction_hash = generate_transaction_hash(initial_transaction)
print("initial transaction hash: 0x%08x" % initial_transaction_hash )

print("generate first block with only initial transaction, and some default values")
merkle = hash(initial_transaction_hash.to_bytes(4,'big') + initial_transaction_hash.to_bytes(4,'big')) # with only one transaction, you hash it concatinated with itself
block = generate_block(0x0,merkle,[initial_transaction],int(time()), 0x000fffff) # append transaction
block['nonce'] = 0
prev_hash = generate_block_hash(block)

print("generate a list of blocks to be used as ledger, and add the one block")
borkchain_ledger = []
borkchain_ledger.append(block) # append block

##########################################################################################

# generate transaction
in_l = []
out_l = []
add_input(in_l,initial_transaction_hash,0,public_key) # take input from initial transaction, with 4 coins
add_output(out_l,2,0x20000000) # transfer 2 coins to new account
add_output(out_l,2,public_key_hash) # transfer 2 coins back

print("sign the transaction input with our private key(this has to match the input public key, which has to match the previous` transaction output key-hash), to prove we are the owner of the coins")
private_key = [0] * 2
with open("private_key.bin", "rb") as keyfile:
    private_key[0] = int.from_bytes(keyfile.read(4), "big")
    private_key[1] = int.from_bytes(keyfile.read(4), "big")
print("private key: 0x%08x,0x%08x" % (private_key[0],private_key[1]))

# in this case there is only one input
add_input_signature(in_l[0], out_l, private_key)
private_key = [0] * 2 #erase key in memory after use


t = generate_transaction(in_l,out_l)
print("the transaction is generated with signed inputs and output, with TXID(hash): 0x%08x" % generate_transaction_hash(t))

###########################################################################################
# generate new block with transaction
print("generate a new block to add the transaction to")
new_block = generate_block(prev_hash,0xDEADBEEF,[],int(time()), 0x05ffffff) # append transaction
if check_transaction(t) == True:
    new_block['transactions'].append(t) # add transaction to new block
    print("transaction verified and added to block")

#merkle tree
merkle = generate_merkle_tree(new_block['transactions'])
new_block['merkle_transaction_hash'] = merkle

###########################################################################################
# do proof of work, to become eligable to add to the chain
block_hash = -1
for i in range(0x0,0xffffffff):
    new_block['nonce'] = i
    h = generate_block_hash(new_block)
    if h < new_block['nBits']:
        print("found: %i hash: 0x%08x" % (i,h))
        block_hash = h
        break

if block_hash != -1:
    # add new block to borkchain
    borkchain_ledger.append(new_block) 
    print("new block added to borkchain ledger")
else:
    print("error: could not find nonce")
###########################################################################################
# let others check validity of proof of work



