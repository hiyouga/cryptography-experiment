import sys
sys.path.append("../..")
import hashlib
from MyCrypto.utils.bitarray import bitarray
from MyCrypto.hash.sha_utils import Digest

class SHA1:
    
    def __init__(self):
        self._reset_data()
    
    def __call__(self, data:bytes) -> Digest:
        data = bitarray.from_bytes(data)
        chunks = self._padding(data)
        h0, h1, h2, h3, h4 = self._h
        for chunk in chunks:
            w = chunk.split(32)
            for i in range(16, 80): # 32 words -> 80 words
                w.append((w[i-3]^w[i-8]^w[i-14]^w[i-16])<<1)
            a, b, c, d, e = h0, h1, h2, h3, h4
            for i in range(80):
                if 0 <= i <= 19:
                    f = (b & c) | ((~b) & d)
                    k = bitarray(0x5A827999, 32)
                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = bitarray(0x6ED9EBA1, 32)
                elif 40 <= i <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = bitarray(0x8F1BBCDC, 32)
                elif 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = bitarray(0xCA62C1D6, 32)
                temp = (a<<5) + f + e + k + w[i]
                a, b, c, d, e = temp, a, b<<30, c, d
            h0, h1, h2, h3, h4 = h0+a, h1+b, h2+c, h3+d, h4+e
        digest = bitarray.concat((h0, h1, h2, h3, h4))
        return Digest(digest.to_bytes())
    
    def _padding(self, data:bitarray) -> bitarray:
        mlen = len(data)
        data = bitarray.concat((data, bitarray(1, 1)))
        plen = (-mlen-65) % 512
        data = bitarray.concat((data, bitarray(0, plen)))
        data = bitarray.concat((data, bitarray(mlen, 64)))
        return data.split(512)
    
    def _reset_data(self):
        self._h = (
            bitarray(0x67452301, 32),
            bitarray(0xEFCDAB89, 32),
            bitarray(0x98BADCFE, 32),
            bitarray(0x10325476, 32),
            bitarray(0xC3D2E1F0, 32)
        )
        self.digest_size = 20
        self.hmac_size = 512


if __name__ == '__main__':
    message = 'The quick brown fox jumps over the lazy dog'
    mysha1 = SHA1()
    stdsha1 = hashlib.sha1
    print(mysha1(message.encode('ascii')).hexdigest)
    print(stdsha1(message.encode('ascii')).hexdigest())
