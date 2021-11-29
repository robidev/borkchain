# A very naive implementation of a blockchain

This is a naive implementation of a blockchain. It is to show how the technology is build from the ground up, and that it is not too complex to understand.  

It starts with a basic hashing function. The hashing function used is not very good, but serves our purpose for its simplicity. it can be exchanged for more complex ones.  

Then we move on to public/private key encryption. using the RSA algorythm, it is fairly trivial to get some usable numbers. However, the values chosen are too low to provide string encryption.  

After encryption we can extend into signing my combining the hash and encrypt function.  

With thise building blocks, we can start following the bitcoin documentation, to build our own ledger, where we start with very basic blocks to get transactions going, then move into putting those transactions into chained blocks with a merkle tree and chain by hashing, and doing proof of work to limit the speed at which blocks can be added. Finally we have an MVP that shows it al combined.  


## TODO
Next steps are  

- build a service around the MVP that accepts connections, and regularly adds blocks to the chain.  
- convert it into a distributed service
- ???
- PROFIT!
