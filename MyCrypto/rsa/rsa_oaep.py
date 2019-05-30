import sys
sys.path.append("../..")
import os
import math
import random
import hashlib
import multiprocessing
from MyCrypto.rsa.rsa import RSA

class RSA_OAEP(RSA):
    
    def __init__(self, pkFile=None, skFile=None, akFile=None, fastDecrypt=True, parallel=False):
        super().__init__(pkFile=pkFile, skFile=skFile, akFile=akFile, fastDecrypt=fastDecrypt)
        self._parallel = parallel
        self._Hash = hashlib.sha1
        self._hLen = self._Hash().digest_size
        self._k = math.ceil(self._data['n'].bit_length()/8)
        self._lHash = self._Hash(''.encode()).digest()
    
    def from_file(self, fn, method='encrypt'):
        if method == 'encrypt':
            insize = 64
        elif method == 'decrypt':
            insize = self._k
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        datas = list()
        with open(fn, 'rb') as fin:
            while True:
                byte = fin.read(insize)
                if not byte:
                    break
                datas.append(byte)
        outs = self._padding_run(datas, method)
        for out in outs:
            output.write(out)
        output.close()
    
    def _padding_run(self, datas, method='encrypt'):
        if method == 'encrypt' and self._canEncrypt:
            if self._parallel:
                return self._parallel_run(self._oaep_encrypt, datas, self._k, self._hLen, self._lHash, self._Hash, self._data['pk'])
            else:
                return [self._oaep_encrypt(data, self._k, self._hLen, self._lHash, self._Hash, self._data['pk']) for data in datas]
        elif method == 'decrypt' and self._canDecrypt:
            if self._parallel:
                return self._parallel_run(self._oaep_decrypt, datas, self._k, self._hLen, self._lHash, self._Hash, self._data['sk'], self._data['ak'], self._canFast)
            else:
                return [self._oaep_decrypt(data, self._k, self._hLen, self._lHash, self._Hash, self._data['sk'], self._data['ak'], self._canFast) for data in datas]
        else:
            print('invaild request')
    
    @staticmethod
    def _sub_parallel_run(func, datas, k, hLen, lHash, Hash, psk, ak, canFast):
        return [func(data, k, hLen, lHash, Hash, psk, ak, canFast) for data in datas]
    
    def _parallel_run(self, func, datas, k, hLen, lHash, Hash, psk, ak=None, canFast=False):
        cores = min([len(datas), multiprocessing.cpu_count()])
        pool = multiprocessing.Pool(cores)
        res_list = list()
        length = len(datas)
        for i in range(0, length, length//cores):
            data_part = datas[i:i+length//cores]
            res = pool.apply_async(self._sub_parallel_run, args=(func, data_part, k, hLen, lHash, Hash, psk, ak, canFast))
            res_list.append(res)
        pool.close()
        pool.join()
        outs = list()
        for res in res_list:
            outs += res.get()
        return outs
    
    @staticmethod
    def _oaep_encrypt(data, k, hLen, lHash, Hash, pk, ak=None, canFast=False):
        assert len(data) <= k-2*hLen-2
        EM = RSA_OAEP._emEncoding(data, k, hLen, lHash, Hash)
        m = RSA_OAEP._os2ip(EM)
        c = RSA_OAEP._encrypt(m, pk)
        return RSA_OAEP._i2osp(c, k)
    
    @staticmethod
    def _oaep_decrypt(data, k, hLen, lHash, Hash, sk, ak=None, canFast=False):
        assert len(data) == k
        assert k >= 2*hLen+2
        c = RSA_OAEP._os2ip(data)
        if canFast:
            m = RSA_OAEP._fast_decrypt(c, ak)
        else:
            m = RSA_OAEP._decrypt(c, sk)
        EM = RSA_OAEP._i2osp(m, k)
        return RSA_OAEP._emDecoding(EM, k, hLen, lHash, Hash)
    
    @staticmethod
    def _emEncoding(M, k, hLen, lHash, Hash):
        PS = RSA_OAEP._i2osp(0, k-len(M)-2*hLen-2)
        DB = lHash + PS + RSA_OAEP._i2osp(0x01, 1) + M
        seed = RSA_OAEP._i2osp(random.randint(256**(hLen//2), 256**hLen-1), hLen)
        dbMask = RSA_OAEP._MGF1(seed, k-hLen-1, hLen, Hash)
        maskedDB = RSA_OAEP._xor(DB, dbMask)
        seedMask = RSA_OAEP._MGF1(maskedDB, hLen, hLen, Hash)
        maskedSeed = RSA_OAEP._xor(seed, seedMask)
        EM = RSA_OAEP._i2osp(0x00, 1) + maskedSeed + maskedDB
        return EM
    
    @staticmethod
    def _emDecoding(EM, k, hLen, lHash, Hash):
        Y, maskedSeed, maskedDB = EM[0], EM[1:hLen+1], EM[hLen+1:]
        assert Y == 0
        seedMask = RSA_OAEP._MGF1(maskedDB, hLen, hLen, Hash)
        seed = RSA_OAEP._xor(maskedSeed, seedMask)
        dbMask = RSA_OAEP._MGF1(seed, k-hLen-1, hLen, Hash)
        DB = RSA_OAEP._xor(maskedDB, dbMask)
        lHash, PSM = DB[:hLen], DB[hLen:]
        assert lHash == lHash
        idx = 0
        while PSM[idx] == 0:
            idx += 1
        if PSM[idx] == 1:
            return PSM[idx+1:]
        else:
            assert False
    
    @staticmethod
    def _MGF1(mgf_seed, mask_len, hLen, Hash):
        T = bytes()
        for i in range(math.ceil(mask_len/hLen)):
            C = RSA_OAEP._i2osp(i, 4)
            T += Hash(mgf_seed + C).digest()
        return T[:mask_len]
    
    @staticmethod
    def _xor(x, y):
        assert len(x) == len(y)
        length = len(x)
        x = RSA_OAEP._os2ip(x)
        y = RSA_OAEP._os2ip(y)
        z = x ^ y
        return RSA_OAEP._i2osp(z, length)
    
    @staticmethod
    def _i2osp(x, xLen):
        return x.to_bytes(xLen, byteorder='big')
    
    @staticmethod
    def _os2ip(octet):
        return int.from_bytes(octet, byteorder='big')

    
if __name__ == '__main__':
    import time
    multiprocessing.freeze_support()
    t0 = time.time()
    rsa = RSA_OAEP(fastDecrypt=True, parallel=False)
    t1 = time.time()
    rsa.from_file('../testdata/text.txt', method='encrypt')
    t2 = time.time()
    rsa.from_file('../testdata/output_text.txt', method='decrypt')
    t3 = time.time()
    print('Initial time:{:.5f}'.format(t1-t0))
    print('Encrypt time:{:.5f}'.format(t2-t1))
    print('Decrypt time:{:.5f}'.format(t3-t2))
