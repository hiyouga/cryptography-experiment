import sys
sys.path.append("../..")
import os
import random
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import inverse
from MyCrypto.algorithms.prime_test import primeTest

class RSA:
    
    def __init__(self, pkFile=None, skFile=None, akFile=None, fastDecrypt=True):
        self._data = dict()
        self._canEncrypt = False
        self._canDecrypt = False
        self._canFast = False
        self._pkFile = pkFile
        self._skFile = skFile
        self._akFile = akFile
        self._fastDecrypt = fastDecrypt
        self._resetData()
    
    def run(self, data, method='encrypt'):
        if method == 'encrypt' and self._canEncrypt:
            return self._encrypt(data, self._data['pk'])
        elif method == 'decrypt' and self._canDecrypt:
            if self._canFast:
                return self._fast_decrypt(data, self._data['ak'])
            else:
                return self._decrypt(data, self._data['sk'])
        else:
            print('invaild request')
    
    def from_file(self, fn, method='encrypt'):
        if method == 'encrypt':
            insize, outsize = 128, 256
        elif method == 'decrypt':
            insize, outsize = 256, 128
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
    def _encrypt(data, keys):
        e, n = keys
        assert data < n
        return quick_power(data, e, n)
    
    @staticmethod
    def _decrypt(data, keys):
        d, n = keys
        return quick_power(data, d, n)
    
    @staticmethod
    def _fast_decrypt(data, keys):
        dp, dq, xp, xq, p, q, n = keys
        vp = quick_power(data, dp, p)
        vq = quick_power(data, dq, q)
        return (vp*xp+vq*xq)%n
    
    def _resetData(self):
        if self._pkFile is not None and self._skFile is not None:
            self._data['e'], self._data['n'] = RSA._loadFile(self._pkFile)
            self._data['d'], _ = RSA._loadFile(self._skFile)
            self._canEncrypt, self._canDecrypt = True, True
        elif self._pkFile is not None:
            self._data['e'], self._data['n'] = RSA._loadFile(self._pkFile)
            self._canEncrypt = True
        elif self._skFile is not None:
            self._data['d'], self._data['n'] = RSA._loadFile(self._skFile)
            self._canDecrypt = True
        else:
            self._data = RSA._genKey()
            self._canEncrypt, self._canDecrypt = True, True
            RSA._saveFile('pk.txt', (self._data['e'], self._data['n']))
            RSA._saveFile('sk.txt', (self._data['d'], self._data['n']))
            RSA._saveFile('ak.txt', (self._data['p'], self._data['q']))
        if self._akFile is not None:
            self._data['p'], self._data['q'] = RSA._loadFile(self._akFile)
        if self._fastDecrypt and 'p' in self._data:
            self._data['xp'] = self._data['q'] * inverse(self._data['q'], self._data['p'])
            self._data['xq'] = self._data['p'] * inverse(self._data['p'], self._data['q'])
            self._data['dp'] = self._data['d'] % (self._data['p']-1)
            self._data['dq'] = self._data['d'] % (self._data['q']-1)
            self._canFast = True
        self._data['pk'] = (self._data['e'], self._data['n']) if self._canEncrypt else None
        self._data['sk'] = (self._data['d'], self._data['n']) if self._canDecrypt else None
        self._data['ak'] = (self._data['dp'], self._data['dq'], self._data['xp'], self._data['xq'], self._data['p'], self._data['q'], self._data['n']) if self._canFast else None
    
    @staticmethod
    def _loadFile(fn):
        with open(fn, 'r', encoding='utf-8') as f:
            filedata = f.readlines()
            assert len(filedata) == 2
            return (int(filedata[0].strip()), int(filedata[1].strip()))
    
    @staticmethod
    def _saveFile(fn, datas):
        with open(fn, 'w', encoding='utf-8') as f:
            f.write("{:d}\n{:d}".format(datas[0], datas[1]))
    
    @staticmethod
    def _genKey():
        primeList = list()
        while len(primeList) != 2:
            p = RSA._genPrime()
            if primeTest(p, prob = 0.001, method='miller_rabin'):
                primeList.append(p)
        p, q = primeList[0], primeList[1]
        n = p * q
        phi = (p-1) * (q-1)
        d = -1
        while d == -1:
            e = random.randint(phi//2, phi) # avoid small e
            d = inverse(e, phi)
        return {'e': e, 'd': d, 'n': n, 'p': p, 'q': q}
    
    @staticmethod
    def _genPrime(n=513):
        p = 0
        for i in range(n-1):
            if random.random() < 0.5:
                p ^= 1
            else:
                p ^= 0
            p <<= 1
        p ^= 1 # must be odd
        return p

if __name__ == '__main__':
    import time
    rsa = RSA()
    data = 1145141919810
    cipher = rsa.run(data, method='encrypt')
    print(cipher)
    print(rsa.run(cipher, method='decrypt'))
    t1 = time.time()
    rsa.from_file('../testdata/text.txt', method='encrypt')
    t2 = time.time()
    rsa.from_file('../testdata/output_text.txt', method='decrypt')
    t3 = time.time()
    print('Encrypt time:{:.5f}'.format(t2-t1))
    print('Decrypt time:{:.5f}'.format(t3-t2))
