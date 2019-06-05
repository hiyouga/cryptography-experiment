import sys
sys.path.append("../..")
import math
import random
import hashlib
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import inverse

class Schnorr:
    
    def __init__(self, p:int, q:int, a:int):
        assert quick_power(a, q, p) == 1
        self._p = p
        self._q = q
        self._a = a
        self._hashFunc = hashlib.sha1
        self._byteLen = math.ceil(math.ceil(math.log2(self._p))/8)
    
    def genKey(self) -> tuple:
        sk = random.randint(1, self._q-1)
        pk = quick_power(inverse(self._a, self._p), sk, self._p)
        return (sk, pk)
    
    def sign(self, m:bytes, sk:int) -> tuple:
        r = random.randint(1, self._q-1)
        x = quick_power(self._a, r, self._p)
        e = self._hash(m + x.to_bytes(self._byteLen, byteorder='big'))
        y = (r + sk*e) % self._q
        return (e, y)
    
    def verify(self, m:bytes, sign:tuple, pk:int) -> bool:
        e, y = sign
        x = (quick_power(self._a, y, self._p) * quick_power(pk, e, self._p)) % self._p
        h = self._hash(m + x.to_bytes(self._byteLen, byteorder='big'))
        return e == h
    
    def _hash(self, m:bytes) -> int:
        assert isinstance(m, bytes)
        return int(self._hashFunc(m).hexdigest(), base=16) % self._q
    

if __name__ == '__main__':
    message = b'message'
    dsa = Schnorr(p=23, q=11, a=8)
    sk, pk = dsa.genKey()
    sign = dsa.sign(message, sk)
    print(sign)
    print(dsa.verify(message, sign, pk))
