import sys
sys.path.append("../..")
import os
import math
import random
import hashlib
from MyCrypto.utils.bitarray import bitarray
from MyCrypto.utils.residue_field import RF
from MyCrypto.ecc.ecc import ECC

class SM2:
    
    def __init__(self):
        self._reset_data()
        self._G = ECC(a=self._a, b=self._b, field=self._RF_q, x=self._gx, y=self._gy)
        self._byteLen = math.ceil(math.ceil(math.log2(self._q))/8)
        self._HashFunc = hashlib.sha512 # longer hash accelerates this algorithm
        self._v = self._HashFunc().digest_size * 8
    
    def encrypt_file(self, fn:str, PK:ECC):
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        with open(fn, 'rb') as fin:
            M = fin.read()
            M = self._bytes2bits(M)
            C = self.encrypt_data(M, PK)
            C = self._bits2bytes(C)
            output.write(C)
        output.close()
    
    def decrypt_file(self, fn:str, SK:int):
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        with open(fn, 'rb') as fin:
            C = fin.read()
            C = self._bytes2bits(C)
            M = self.decrypt_data(C, SK)
            M = self._bits2bytes(M)
            output.write(M)
        output.close()
    
    def encrypt_data(self, M:bitarray, PK:ECC) -> bitarray:
        k = random.randint(1, self._n-1)
        c1 = k * self._G
        c1 = self._bytes2bits(self._point2bytes(c1))
        p2 = k * PK
        x2 = self._bytes2bits(self._elem2bytes(p2.x))
        y2 = self._bytes2bits(self._elem2bytes(p2.y))
        t = self._kdf(bitarray.concat((x2, y2)), len(M))
        c2 = M ^ t
        c3 = self._hash(bitarray.concat((x2, M, y2)))
        C = bitarray.concat((c1, c3, c2))
        return C
    
    def decrypt_data(self, C:bitarray, SK:int) -> bitarray:
        c1, C = C[:self._byteLen*8*2+8], C[self._byteLen*8*2+8:]
        c3, c2 = C[:self._v], C[self._v:]
        c1 = self._bytes2point(self._bits2bytes(c1))
        p2 = SK * c1
        x2 = self._bytes2bits(self._elem2bytes(p2.x))
        y2 = self._bytes2bits(self._elem2bytes(p2.y))
        t = self._kdf(bitarray.concat((x2, y2)), len(c2))
        M = c2 ^ t
        u = self._hash(bitarray.concat((x2, M, y2)))
        assert u == c3
        return M
    
    def generate_keys(self) -> tuple:
        d = random.randint(1, self._n-2)
        return (d, d * self._G)
    
    def _reset_data(self): # SM2 Constants
        self._a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        self._b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
        self._q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        self._n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
        self._gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
        self._gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
        class RF_q(RF):
            def __init__(self, data, modulo=self._q):
                super().__init__(data, modulo)
        self._RF_q = RF_q
    
    def _int2bytes(self, x:int, k:int) -> bytes: # 3.2.2
        return x.to_bytes(k, byteorder='big')
    
    def _bytes2int(self, m:bytes) -> int: # 3.2.3
        return int.from_bytes(m, byteorder='big')
    
    def _bits2bytes(self, b:bitarray) -> bytes: # 3.2.4
        return b.to_bytes()
    
    def _bytes2bits(self, b:bytes) -> bitarray: # 3.2.5
        return bitarray.from_bytes(b)
    
    def _elem2bytes(self, e:RF) -> bytes: # 3.2.6
        return self._int2bytes(e.data, self._byteLen)
    
    def _bytes2elem(self, s:bytes) -> RF: # 3.2.7
        return self._RF_q(self._bytes2int(s))
    
    def _elem2int(self, e:RF) -> int: # 3.2.8
        return e.data
    
    def _point2bytes(self, p:ECC, method='uncompressed') -> bytes: # 3.2.9
        assert p.isInfty == False
        x1 = self._elem2bytes(p.x)
        if method == 'uncompressed':
            y1 = self._elem2bytes(p.y)
            PC = 0x04
            return bytes([PC]) + x1 + y1
    
    def _bytes2point(self, s:bytes, method='uncompressed') -> ECC: # 3.2.10
        PC, x1, y1 = s[0], s[1:1+self._byteLen], s[1+self._byteLen:]
        xp = self._bytes2elem(x1)
        if method == 'uncompressed':
            assert PC == 4
            yp = self._bytes2elem(y1)
        assert self._G.belong(xp, yp)
        return self._G(xp, yp)
    
    def _hash(self, z:bitarray) -> bitarray: # 3.4.2
        z = self._bits2bytes(z)
        x = self._HashFunc(z).digest()
        return self._bytes2bits(x)
    
    def _kdf(self, z:bitarray, klen:int) -> bitarray: # 3.4.3
        ct = bitarray(1, 32)
        t = bitarray()
        for i in range(math.ceil(klen/self._v)):
            t = bitarray.concat((t, self._hash(bitarray.concat((z, ct)))))
            ct = ct + bitarray(1, 32)
        return t[:klen]


if __name__ == '__main__':
    import time
    t0 = time.time()
    sm2 = SM2()
    t1 = time.time()
    sk, pk = sm2.generate_keys()
    t2 = time.time()
    print('Initial time:{:.5f}'.format(t1-t0))
    print('Genkeys time:{:.5f}'.format(t2-t1))
    sm2.encrypt_file('../testdata/text.txt', pk)
    sm2.decrypt_file('../testdata/output_text.txt', sk)
