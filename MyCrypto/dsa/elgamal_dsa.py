import sys
sys.path.append("../..")
import random
import hashlib
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import gcd, inverse

class ElGamal:
    
    def __init__(self, q:int, a:int):
        self._q = q
        self._a = a
        self._hash = lambda m: int(hashlib.sha1(m).hexdigest(), base=16)
    
    def genKey(self) -> tuple:
        sk = random.randint(2, self._q-2)
        pk = quick_power(self._a, sk, self._q)
        return (sk, pk)
    
    def sign(self, m:bytes, sk:int) -> tuple:
        k = None
        while k is None:
            temp_k = random.randint(3, self._q-2)
            if gcd(temp_k, self._q-1) == 1:
                k = temp_k
        s1 = quick_power(self._a, k, self._q)
        s2 = (inverse(k, self._q-1) * ((self._hash(m) % self._q) - sk * s1)) % (self._q - 1)
        return (s1, s2)
    
    def verify(self, m:bytes, sign:tuple, pk:int) -> bool:
        s1, s2 = sign
        v1 = quick_power(self._a, (self._hash(m) % self._q), self._q)
        v2 = (quick_power(pk, s1, self._q) * quick_power(s1, s2, self._q)) % self._q
        return v1 == v2
    

if __name__ == '__main__':
    message = b'message'
    dsa = ElGamal(q=19, a=10)
    sk, pk = dsa.genKey()
    sign = dsa.sign(message, sk)
    print(sign)
    print(dsa.verify(message, sign, pk))    
