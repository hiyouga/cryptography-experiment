import sys
sys.path.append("../..")
import os
import random
from MyCrypto.algorithms.exgcd import gcd, inverse

class Knapsack:
    
    def __init__(self):
        self._data = Knapsack._genKey()
    
    def run(self, data, method='encrypt'):
        if method == 'encrypt':
            return Knapsack._encrypt(data, self._data['b'])
        elif method == 'decrypt':
            return Knapsack._decrypt(data, self._data['w'], self._data['invr'], self._data['q'])
    
    def from_file(self, fn, method='encrypt'):
        if method == 'encrypt':
            insize, outsize = 8, 16
        elif method == 'decrypt':
            insize, outsize = 16, 8
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        with open(fn, 'rb') as fin:
            while True:
                byte = fin.read(insize)
                if not byte:
                    break
                data = int.from_bytes(byte, byteorder='little')
                output.write(self.run(data, method).to_bytes(outsize, byteorder='little'))
        output.close()
    
    @staticmethod
    def _encrypt(m, b):
        c = 0
        for k in b[::-1]:
            c += k * (m&1)
            m >>= 1
        assert m == 0
        return c
    
    @staticmethod
    def _decrypt(c, w, invr, q):
        c = (c*invr)%q
        m = 0
        for i, k in enumerate(w[::-1]):
            if c >= k:
                m ^= 1<<i
                c -= k
        assert c == 0
        return m
    
    @staticmethod
    def _genKey(n=64):
        s = 0
        klist = list()
        for i in range(n):
            k = random.randint(s+2, 2*s+2)
            s += k
            klist.append(k)
        q = random.randint(s+2, 2*s+2)*2+1
        r = q
        while gcd(r, q) != 1:
            r = random.randint(2, q-1)
        invr = inverse(r, q)
        b = [(k*r)%q for k in klist]
        return {'w': klist, 'b': b, 'q': q, 'r': r, 'invr': invr}


if __name__ == '__main__':
    ks = Knapsack()
    data = 0b10110001100111001110
    code = ks.run(data, method='encrypt')
    print(hex(data))
    print(hex(code))
    print(hex(ks.run(code, method='decrypt')))
    ks.from_file('../testdata/text.txt', method='encrypt')
    ks.from_file('../testdata/output_text.txt', method='decrypt')
