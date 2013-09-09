import os, sys
import itertools
from Crypto.Util.number import bytes_to_long, long_to_bytes
import puzzle; reload(puzzle); from puzzle import *;
import signature; reload(signature); from signature import *

# Parameters
puz_params = dict(
    NUM_BLOCKS=1024*1024*8*2,
    BLOCK_SIZE=1024/2,
    ITERS=20,
    )

serv_params = dict(
    CHUNK=100
    )

globals().update(puz_params)


# Default low-level file access
def make_file(fname, num_blocks, block_size):
    fd = os.open(fname, os.O_RDONLY | os.O_DIRECT) # Avoids filesystem cache
    #fd = os.open(fname, os.O_RDONLY)
    f = os.fdopen(fd, 'rb')
    def query(idx):
        assert idx < num_blocks
        f.seek(idx*block_size)
        b = 0
        r = ''
        while b < block_size:
            c = min(2048, block_size-b)
            r += f.read(c)
            b += c
        assert len(r) == block_size
        return r
    return query

def make_PoRMiner(puzzle, sigscheme, pkey, skey):
    index_from_state = lambda sol: hash(sol) % puzzle.num_blocks

    def attempt(puz, nonce):
        state = '%s:%s:%s' % (puz, pkey, nonce)
        sigs = []
        for i in xrange(puzzle.iters):
            # Access the file
            idx = index_from_state(state)
            block = puzzle.fquery(idx)
            # Sign the data
            message = '%s:%s:%s' % (puz, nonce, hash(block))
            sig = sigscheme.sign(message, skey)
            sigs.append(sig)
            state = puz + nonce + sig

        final = SHA.SHA1Hash(state).digest()
        return final, sigs

    def mine(puz, tries=None):
        assert type(puz) is str
        if tries is None: print("Mining indefinitely")
        else: print("Mining, %d tries" % tries)
        for i in itertools.count() if tries is None else xrange(tries):
            if (i % 10 == 0): print("Attempt %d..." % i)
            nonce = os.urandom(20)
            final, sigs = attempt(puz, nonce)
            if check_difficulty(difficulty, final):
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

ssd_fname = "random_8gb.dat"
harddisk_fname = "/media/amiller/asus-backup-7_12/home/blockplayerdata/harddisk_8gb.dat"
fquery = make_file(ssd_fname, NUM_BLOCKS, BLOCK_SIZE)
difficulty = 32.
sigscheme = DegenerateSignatureScheme(1024)
puzzle = PoRPuzzle(fquery, sigscheme, NUM_BLOCKS, BLOCK_SIZE, ITERS, difficulty)
pkey, skey = sigscheme.generate()
miner = make_PoRMiner(puzzle, sigscheme, pkey, skey)

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
