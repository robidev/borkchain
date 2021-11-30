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


##########################################################################################
# initialise borkchain

block = generate_block(0x0,0x00001337,[],int(time()), 0x000fffff) # append transaction
block['nonce'] = 1337
prev_hash = generate_block_hash(block)


borkchain_ledger = []
borkchain_ledger.append(block) # append block

###########################################################################################
nBits = 0x0fffffff
old_nonce = 0
interval = 2016

for index in range(0,0xffff):
    timestamp = (int(time()*10000000) & 0xffffffff)
    new_block = generate_block(prev_hash,0xDEADBEEF,[],timestamp, nBits) # append transaction

    # do proof of work, to become eligable to add to the chain
    block_hash = -1
    for i in range(0x00000000,0xffffffff,1):
        new_block['nonce'] = ((i + old_nonce) & 0xffffffff)
        h = generate_block_hash(new_block)
        if h < new_block['nBits']:
            #print("found: %i hash: 0x%08x" % (i,h))
            block_hash = h
            old_nonce = i
            break

    if block_hash != -1:
        # add new block to borkchain
        borkchain_ledger.append(new_block) 
        #print("new block added to borkchain ledger")
    else:
        print("error: could not find nonce")
    
    if index % (interval+1) == interval:
        avg = 0
        for i in range(index-interval,index):
            avg += borkchain_ledger[i]['time'] - borkchain_ledger[i-1]['time']
        avg = avg / interval
        #check average resolve time
        print("resolve-time: %i" % avg)
        if avg < 250:
            nBits = (nBits >> 1 & 0x8fffffff)+(int(nBits/3)) # make problem harder
        else:             
            nBits = (nBits << 1 | 0x1)-(int(nBits/3)) # make problem easier
        print("nBits: 0x%08x" % nBits)

###########################################################################################
# let others check validity of proof of work



