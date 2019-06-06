import sys
sys.path.append("../..")
import math
import random
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import inverse
from MyCrypto.dsa.dsa import DSA

class Schnorr(DSA):
    
    def __init__(self, paramFile=None):
        super().__init__(paramFile)
        self._byteLen = math.ceil(math.ceil(math.log2(self._data['p']))/8)
    
    def genKey(self) -> tuple:
        sk = random.randint(1, self._data['q']-1)
        pk = quick_power(inverse(self._data['g'], self._data['p']), sk, self._data['p'])
        return (sk, pk)
    
    def sign(self, m:bytes, sk:int) -> tuple:
        r = random.randint(1, self._data['q']-1)
        x = quick_power(self._data['g'], r, self._data['p'])
        e = self._hash(m + x.to_bytes(self._byteLen, byteorder='big'))
        y = (r + sk*e) % self._data['q']
        return (e, y)
    
    def verify(self, m:bytes, sign:tuple, pk:int) -> bool:
        e, y = sign
        x = (quick_power(self._data['g'], y, self._data['p']) * quick_power(pk, e, self._data['p'])) % self._data['p']
        h = self._hash(m + x.to_bytes(self._byteLen, byteorder='big'))
        return e == h
    

if __name__ == '__main__':
    message = b'message'
    dsa = Schnorr()
    sk, pk = dsa.genKey()
    sign = dsa.sign(message, sk)
    print(sign)
    print(dsa.verify(message, sign, pk))
