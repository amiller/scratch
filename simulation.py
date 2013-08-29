import os, sys
import itertools

# Parameters
puz_params = dict(
    NUM_BLOCKS=1024*1024,
    BLOCK_SIZE=1024,
    ITERS=20,
    )

serv_params = dict(
    CHUNK=100
    )

globals().update(puz_params)

# Default (degenerate) signature scheme
def gen_keys(): return 'key0xx', 'key0xx'
def check_signature(pubkey, message, signature): 
    return signature == hash((pubkey,message))
def sign_message(privkey, message): return hash((privkey,message))
privkey, pubkey = gen_keys()

# Default low-level file access
def make_file(fname, num_blocks, block_size):
    f = open(fname,'rb')
    def query(idx):
        assert idx < num_blocks
        f.seek(idx*block_size)
        r = f.read(block_size)
        assert len(r) == block_size
        return r
    return query

# Checker for our puzzle scheme
def make_puzzle_checker(fquery, num_blocks, block_size, iters, difficulty):
    index_from_state = lambda sol: hash(sol) % num_blocks
    check_difficulty = lambda final, difficulty: True
    def check(puz, solution, proof):
        """
        puz: puzzle identifier (just a string)
        solution: a pubkey and a nonce
        proof: a sequence of signatures (length: iters)
        """
        assert type(puz) is str
        pubkey, nonce = solution
        assert type(nonce) is str

        # Requires accessing the file
        state = '%s%s' % (puz, solution)
        assert len(proof) == iters
        for i,sig in enum(proof):
            # Access the file
            idx = index_from_state(state)
            block = fquery(idx)
            # Check the signature
            if not check_signature(pubkey, block, sig): return False
            state = puz + sig

        # Final check
        final = hash(state)
        return check_difficulty(final, difficulty)

def make_miner(pubkey, privkey, fquery, num_blocks, block_size, iters, difficulty):
    index_from_state = lambda sol: hash(sol) % num_blocks
    check_difficulty = lambda final, difficulty: False
    def attempt(puz, pubkey, nonce):
        state = '%s%s' % (puz, (pubkey, nonce))
        sigs = []
        for i in range(iters):
            # Access the file
            idx = index_from_state(state)
            block = fquery(idx)
            # Check the signature
            sig = sign_message(privkey, (puz, nonce, block))
            sigs.append(sig)
            state = puz + str(sig)
        final = hash(state)
        return final, sigs

    def mine(puz, tries=None):
        assert type(puz) is str
        if tries is None: print("Mining indefinitely")
        else: print("Mining, %d tries" % tries)
        for i in itertools.count() if tries is None else xrange(tries):
            if (i % 10 == 0): print("Attempt %d..." % i)
            nonce = os.urandom(20)
            final, sigs = attempt(puz, pubkey, nonce)
            if check_difficulty(puz, difficulty):
                print("Solution found!")
                return nonce, sigs
    return mine

# Tests
def make_random_file(fname, num_bytes):
    ctr = 0
    block_size = 1024*1024
    f = open(fname, 'wb')
    print("Writing %d random bytes to %s..." % (num_bytes, fname))
    while ctr < num_bytes:
        b = min(block_size, num_bytes-ctr)
        ctr += b
        f.write(os.urandom(b))
    print("Done")

ssd_fname = "random_1gb.dat"
harddisk_fname = "/media/amiller/asus-backup-7_12/home/blockplayerdata/harddisk_1gb.dat"
fquery = make_file(harddisk_fname, NUM_BLOCKS, BLOCK_SIZE)
difficulty = 1.0
miner = make_miner(pubkey, privkey, fquery, NUM_BLOCKS, BLOCK_SIZE, ITERS, difficulty)

class Streamer(object):
    """
    """
    def __init__(self, callback):
        self.callback = callback

    def query(self, index):
        raise NotImplemented

class SequentialStreamer(Streamer):
    def __init__(self, callback, filepath):
        self.callback = callback
    def query(self, index):
        pass
