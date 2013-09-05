from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Hash import SHA

def check_difficulty(difficulty, s):
    # Assume s is uniformly random in len(s)
    assert type(s) is str
    assert type(difficulty) in (float, int, long)
    difficulty = float(difficulty)
    n = len(s)*8
    assert difficulty < n
    target = pow(2, n - difficulty)
    x = bytes_to_long(s)
    return x < target

# Default puzzle
class Puzzle(object):
    def generate(self):
        raise NotImplemented

    def check_solution(self, puz, pkey, solution, proof):
        raise NotImplemented

class PoRPuzzle(Puzzle):
    def __init__(self, fquery, sigscheme, num_blocks, block_size, iters, difficulty):
        self.fquery = fquery
        self.sigscheme = sigscheme
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.iters = iters
        self.difficulty = difficulty

    def generate(self):
        return "puzid:1234"

    def check_solution(self, puz, pkey, solution, proof):
        index_from_state = lambda sol: hash(sol) % self.num_blocks

        assert type(puz) is str
        nonce = solution
        assert type(nonce) is str

        # Requires accessing the file
        state = '%s:%s:%s' % (puz, pkey, nonce)
        assert len(proof) == self.iters
        for i,sig in enum(proof):
            # Access the file
            idx = index_from_state(state)
            block = self.fquery(idx)
            # Check the signature
            if not self.sigscheme.verify(block, sig, pkey): return False
            state = puz + nonce + sig

        # Final check
        final = SHA1.SHA1Hash(state).digest()
        return check_difficulty(difficulty, final)
