import sys
sys.path.append("../..")
import random
import hashlib
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import inverse
from MyCrypto.algorithms.prime_test import primeTest

class DSA:
    
    def __init__(self, paramFile=None):
        self._data = dict()
        self._paramFile = paramFile
        self._hashFunc = hashlib.sha1
        self._resetData()
    
    def genKey(self) -> tuple:
        sk = random.randint(1, self._data['q']-1)
        pk = quick_power(self._data['g'], sk, self._data['p'])
        return (sk, pk)
    
    def sign(self, m, sk:int) -> tuple:
        k = random.randint(1, self._data['q']-1)
        r = quick_power(self._data['g'], k, self._data['p']) % self._data['q']
        s = (inverse(k, self._data['q'])*(self._hash(m) + sk*r)) % self._data['q']
        return (r, s)
    
    def verify(self, m, sign:tuple, pk:int) -> bool:
        r, s = sign
        w = inverse(s, self._data['q'])
        u1 = (self._hash(m) * w) % self._data['q']
        u2 = (r * w) % self._data['q']
        v = ((quick_power(self._data['g'], u1, self._data['p']) * quick_power(pk, u2, self._data['p'])) % self._data['p']) % self._data['q']
        return v == r
    
    def _resetData(self):
        if self._paramFile is not None:
            with open(self._paramFile, 'r', encoding='utf-8') as f:
                filedata = f.readlines()
                assert len(filedata) == 3
                self._data['p'] = int(filedata[0].strip())
                self._data['q'] = int(filedata[1].strip())
                self._data['g'] = int(filedata[2].strip())
        else:
            self._data = self._genParam(l=1024, n=160)
            with open('param.txt', 'w', encoding='utf-8') as f:
                f.write("{:d}\n{:d}\n{:d}".format(self._data['p'], self._data['q'], self._data['g']))
    
    def _genParam(self, l:int, n:int, seedlen:int=None) -> tuple:
        if seedlen is None:
            seedlen = n
        assert seedlen >= n
        outlen = self._hashFunc().digest_size * 8    
        t = l//outlen - 1
        b = l - 1 - t * outlen
        q = None
        dps = 0
        while q is None:
            dps = random.random()
            u = self._hash(dps) % 2**(n-1)
            temp_q = 2**(n-1) + u + 1 - (u % 2)
            if primeTest(temp_q, prob = 0.001, method='miller_rabin'):
                q = temp_q
        offset = 1
        for counter in range(4*l):
            w = (self._hash(dps+offset+0) % 2**seedlen) % 2**b
            for j in range(1, t+1):
                w ^= self._hash(dps+offset+j) % 2**seedlen
                w <<= outlen
            x = w + 2**(l-1)
            c = x % (2 * q)
            p = x - (c - 1)
            if p >= 2**(l-1) and primeTest(p, prob = 0.001, method='miller_rabin'):
                e = (p - 1) // q
                while True:
                    h = random.randint(2, p - 2)
                    g = quick_power(h, e, p)
                    if g > 1:
                        return {'p': p, 'q': q, 'g': g}
            offset += t + 1
    
    def _hash(self, m) -> int:
        if isinstance(m, int) or isinstance(m, float):
            m = str(m).encode()
        if isinstance(m, str):
            m = m.encode()
        assert isinstance(m, bytes)
        return int(self._hashFunc(m).hexdigest(), base=16)
    

if __name__ == '__main__':
    message = 'message'
    dsa = DSA()
    sk, pk = dsa.genKey()
    sign = dsa.sign(message, sk)
    print(sign)
    print(dsa.verify(message, sign, pk))
