import sys
sys.path.append("../..")
import os
from MyCrypto.des.des_utils import DES_base

class DES(DES_base):
    
    def __init__(self, raw_key, _round=16):
        self._round = _round
        self._reset_data()
        self._reset_key(raw_key)
    
    def run(self, data, method='encrypt'):
        ''' do encryption or decryption for binary data '''
        data = DES.permutation(data, self._ip, 64) # 64bits
        left_data, right_data = DES.split_bit(data, 64, 2) # 64bits -> 32bits * 2
        if method == 'encrypt':
            iteration = range(self._round)
        if method == 'decrypt':
            iteration = range(self._round-1, -1, -1)
        for i in iteration:
            left_data, right_data = right_data, left_data ^ self._round_function(right_data, self.keys[i])
        output = DES.merge_bit((right_data, left_data), 32) # 32bits * 2 -> 64bits
        output = DES.permutation(output, self._ip_inv, 64) # 64bits
        return output
    
    def from_file(self, fn, method='encrypt'):
        ''' do encryption or decryption for file '''
        fdir, out_fn = os.path.split(fn)
        out_fn = 'output_' + out_fn
        out_fn = os.path.join(fdir, out_fn)
        output = open(out_fn, 'wb')
        with open(fn, 'rb') as fin:
            while True:
                byte = fin.read(8)
                if not byte:
                    break
                data = int.from_bytes(byte, byteorder='little')
                output.write(self.run(data, method).to_bytes(8, byteorder='little'))
        output.close()
    
    def _round_function(self, data, key):
        ''' the round function '''
        right_extended = DES.permutation(data, self._extend, 32) # 32bits -> 48bits
        presult = right_extended ^ key # 48bits
        s_box_inputs = DES.split_bit(presult, 48, 8) # 48bits -> 6bits * 8
        s_box_outputs = [self._sbox_function(s_box_inputs[i], self._s_box[i]) for i in range(8)]
        output = DES.merge_bit(s_box_outputs, 4) # 4bits * 8 -> 32bits
        output = DES.permutation(output, self._permute, 32) # 32bits
        return output
    
    @staticmethod
    def _sbox_function(data, s_box):
        ''' choose data from sbox '''
        row = (DES.get_bit(data, 5) << 1) ^ (data & 1) # 2bits
        col = (data >> 1) & ((1 << 4) - 1) # 4bits
        return s_box[row*16+col]
    
    def _reset_key(self, key):
        ''' reset keys of DES '''
        assert DES.verify_key(key)
        self.keys = list()
        key = DES.permutation(key, self._pc1, 64) # 64bits -> 56bits
        left_key, right_key = DES.split_bit(key, 56, 2) # 56bits -> 28bits * 2
        for i in range(self._round):
            left_key, right_key = DES.cyclic_lshift(left_key, 28, self._lshift[i]), DES.cyclic_lshift(right_key, 28, self._lshift[i])
            key = DES.merge_bit((left_key, right_key), 28) # 28bits * 2 -> 56bits
            key = DES.permutation(key, self._pc2, 56) # 56bits -> 48bits
            self.keys.append(key)
    
    def _reset_data(self):
        ''' reset basic data of DES '''
        self._ip = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
        self._ip_inv = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
        self._extend = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
        self._permute = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
        self._s_box = [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        self._pc1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
        self._pc2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
        self._lshift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

if __name__ == '__main__':
    key = 0x133457799BBCDFF1
    des = DES(key)
    data = 0x1234567890FEABCD
    code = des.run(data)
    text = des.run(code, method='decrypt')
    print(hex(data))
    print(hex(code))
    print(hex(text))
    des.from_file('../testdata/text.txt', method='encrypt')
    des.from_file('../testdata/output_text.txt', method='decrypt')
