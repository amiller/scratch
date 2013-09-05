from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Util import number

class SignatureScheme(object):
    def __init__(self, k):
        pass

    def generate(self):
        # generate keypair, returns (public, private)
        # might sample randomness
        raise NotImplemented

    def verify(self, message, sig, pkey):
        raise NotImplemented

    def sign(self, message, skey):
        raise NotImplemented

class DegenerateSignatureScheme(SignatureScheme):
    def generate(self):
        return 'pkey', 'skey'

    def verify(self, message, sig, pkey):
        return 'sig' == sig

    def sign(self, message, skey):
        return 'sig'

class RSASignatureScheme(SignatureScheme):
    def __init__(self, k):
        assert k in [1024,2048,4096]
        self.k = k

    def generate(self):
        k = self.k
        skey = RSA.generate(k)
        pkey = skey.publickey()
        return pkey, skey

    def verify(self, message, sig, pkey):
        return pkey.verify(message, sig)

    def sign(self, message, skey):
        s, = skey.sign(message, 0)
        sig = number.long_to_bytes(s)
        return sig

class SHA1RSASignatureScheme(SignatureScheme):
    def generate(self, k):
        assert k in [1024,2048,4096]
        skey = RSA.generate(k)
        pkey = skey.publickey()
        return pkey, skey

    def verify(self, message, sig, pkey):
        m = SHA.SHA1Hash(message).digest()
        return pkey.verify(m, sig)

    def sign(self, message, skey):
        m = SHA.SHA1Hash(message).digest()
        s, = skey.sign(m, 0)
        sig = number.long_to_bytes(s)
        return sig
