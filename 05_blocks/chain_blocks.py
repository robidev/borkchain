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
# initialise borkchain
print("generate initial transaction with 5 coins as output, on address: 0x%08x" % 0x00d102f5)
initial_transaction = generate_transaction([], [{'value':4,'pubkey_hash':0x00d102f5}])
initial_transaction_hash = generate_transaction_hash(initial_transaction)
print("initial transaction hash: 0x%08x" % initial_transaction_hash )


# with only one transaction, you hash it concatinated with itself
merkle = hash(initial_transaction_hash.to_bytes(4,'big') + initial_transaction_hash.to_bytes(4,'big')) 
print("merkle tree with only 1 transaction: 0x%08x" % merkle)

print("generate first block with only initial transaction, and some default values")
block = generate_block(0x0,merkle,[initial_transaction],int(time()), 0x000fffff) # append transaction
block['nonce'] = 1337
prev_hash = generate_block_hash(block)

print("generate a list of blocks to be used as ledger, and add the one block")
borkchain_ledger = []
borkchain_ledger.append(block) # append block

###########################################################################################

# generate new block with transaction
new_block = generate_block(prev_hash,0xDEADBEEF,[],int(time()), 0x07ffffff) # append transaction

print("creating transaction 1 with output value: %i, and public key hash: 0x%08x" % (4,0x00d102f5))
t1 = generate_transaction([], [{'value':4,'pubkey_hash':0x00d102f5}])
new_block['transactions'].append(t1) # add transaction to new block

print("creating transaction 2 with output value: %i, and public key hash: 0x%08x" % (3,0x1))
t2 = generate_transaction([], [{'value':4,'pubkey_hash':0x1}])
new_block['transactions'].append(t2) # add transaction to new block

print("creating transaction 3 with output value: %i, and public key hash: 0x%08x" % (5,0x2))
t3 = generate_transaction([], [{'value':4,'pubkey_hash':0x2}])
new_block['transactions'].append(t3) # add transaction to new block

print("creating transaction 3 with output value: %i, and public key hash: 0x%08x" % (5,0x2))
t3 = generate_transaction([], [{'value':4,'pubkey_hash':0x2}])
new_block['transactions'].append(t3) # add transaction to new block

print("creating transaction 3 with output value: %i, and public key hash: 0x%08x" % (5,0x2))
t3 = generate_transaction([], [{'value':4,'pubkey_hash':0x2}])
new_block['transactions'].append(t3) # add transaction to new block

print("creating transaction 3 with output value: %i, and public key hash: 0x%08x" % (5,0x2))
t3 = generate_transaction([], [{'value':4,'pubkey_hash':0x2}])
new_block['transactions'].append(t3) # add transaction to new block

print("creating transaction 3 with output value: %i, and public key hash: 0x%08x" % (5,0x2))
t3 = generate_transaction([], [{'value':4,'pubkey_hash':0x2}])
new_block['transactions'].append(t3) # add transaction to new block

print("calculate merkle tree...")
merkle = generate_merkle_tree(new_block['transactions'])
new_block['merkle_transaction_hash'] = merkle
print("merkle tree hash: 0x%08x" % merkle)

# add new block to borkchain
new_block['nonce'] = 1337
borkchain_ledger.append(new_block) 
print("block hash: 0x%08x" % generate_block_hash(new_block))


