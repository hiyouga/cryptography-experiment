import sys
sys.path.append("../..")
import os
import multiprocessing
from MyCrypto.aes.fast_aes import Fast_AES

class AES_block(Fast_AES):
    
    def __init__(self, raw_key, mode='ecb', iv=None, fast=True, parallel=False):
        super().__init__(raw_key)
        mode_dict = {'ecb': self._ecb, 'cbc': self._cbc, 'cfb': self._cfb}
        len_dict = {'ecb': 16, 'cbc': 16, 'cfb': 1}
        self._iv = iv
        self._run_mode = mode_dict[mode]
        self._length = len_dict[mode]
        self._process = self.fast_run if fast else self.run
        self._parallel = parallel
    
    def from_file(self, fn, method='encrypt'):
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        datas = list()
        with open(fn, 'rb') as fin:
            while True:
                byte = fin.read(self._length)
                if not byte:
                    break
                datas.append(int.from_bytes(byte, byteorder='little'))
        codes = self._run_mode(datas, method)
        for code in codes:
            output.write(code.to_bytes(self._length, byteorder='little'))
        output.close()
    
    @staticmethod
    def _sub_parallel_run(func, datas, tbox, keys, sbox):
        return [func(data, tbox, keys, sbox) for data in datas]
    
    @staticmethod
    def _parallel_run(func, datas, tbox, keys, sbox):
        cores = min([len(datas), multiprocessing.cpu_count()])
        pool = multiprocessing.Pool(cores)
        res_list = list()
        length = len(datas)
        for i in range(0, length, length//cores):
            data_part = datas[i:i+length//cores]
            res = pool.apply_async(AES_block._sub_parallel_run, args=(func, data_part, tbox, keys, sbox))
            res_list.append(res)
        pool.close()
        pool.join()
        codes = list()
        for res in res_list:
            codes += res.get()
        return codes
    
    def _ecb(self, datas, method):
        if self._parallel:
            if method == 'encrypt':
                codes = AES_block._parallel_run(self._fast_encrypt, datas, self._te_box, self._f_keys, self._f_s_box)
            elif method == 'decrypt':
                codes = AES_block._parallel_run(self._fast_decrypt, datas, self._td_box, self._f_keys_inv, self._f_s_box_inv)
        else:
            codes = [self._process(data, method) for data in datas]
        return codes
    
    def _cbc(self, datas, method):
        codes = list()
        if method == 'encrypt':
            temp = self._iv
            for data in datas:
                code = self._process(data ^ temp, method)
                temp = code
                codes.append(code)
            return codes
        elif method == 'decrypt':
            temp = self._iv
            for data in datas:
                codes.append(self._process(data, method) ^ temp)
                temp = data
            return codes
    
    def _cfb(self, datas, method):
        codes = list()
        if method == 'encrypt':
            temp = self._iv
            for data in datas:
                code = (self._process(temp, method='encrypt') >> 120) ^ data
                temp = ((temp << 8) & ((1 << 128)-1)) ^ code
                codes.append(code)
        elif method == 'decrypt':
            temp = self._iv
            for data in datas:
                codes.append((self._process(temp, method='encrypt') >> 120) ^ data)
                temp = ((temp << 8) & ((1 << 128)-1)) ^ data
        return codes
    
    def _ofb(self, datas, method):
        pass


if __name__ == '__main__':
    import time
    multiprocessing.freeze_support()
    key = 0x0f1571c947d9e8590cb7add6af7f6798
    iv =  0xea50c189a1bc6154e1abf87091504321
    aes_block = AES_block(key, mode='ecb', iv=iv, fast=True, parallel=False)
    t1 = time.time()
    aes_block.from_file('../testdata/text.txt', method='encrypt')
    t2 = time.time()
    aes_block.from_file('../testdata/output_text.txt', method='decrypt')
    t3 = time.time()
    print('Encrypt time: {:.5f}'.format(t2-t1))
    print('Decrypt time: {:.5f}'.format(t3-t2))
