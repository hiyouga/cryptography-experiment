import sys
sys.path.append("../..")
from MyCrypto.des.des_utils import DES_base

class S_DES(DES_base):
    
    def __init__(self, raw_key, _round=2):
        self._round = _round
        self._reset_data()
        self._reset_key(raw_key)
    
    def run(self, data, method='encrypt'):
        ''' do encryption or decryption for binary data '''
        data = S_DES.permutation(data, self._ip, 8) # 8bits
        left_data, right_data = S_DES.split_bit(data, 8, 2) # 8bits -> 4bits * 2
        if method == 'encrypt':
            iteration = range(self._round)
        if method == 'decrypt':
            iteration = range(self._round-1, -1, -1)
        for i in iteration:
            left_data, right_data = right_data, left_data ^ self._round_function(right_data, self.keys[i])
        output = S_DES.merge_bit((right_data, left_data), 4) # 4bits * 2 -> 8bits
        output = S_DES.permutation(output, self._ip_inv, 8) # 8bits
        return output
    
    def _round_function(self, data, key):
        ''' the round function '''
        right_extended = S_DES.permutation(data, self._extend, 4) # 4ibts -> 8bits
        presult = right_extended ^ key
        s_box_inputs = S_DES.split_bit(presult, 8, 2) # 8bits -> 4bits * 2
        s_box_outputs = [self._sbox_function(s_box_inputs[i], self._s_box[i]) for i in range(2)]
        output = S_DES.merge_bit(s_box_outputs, 2) # 2bits * 2 -> 4bits
        output = S_DES.permutation(output, self._permute, 4) # 4bits
        return output
    
    @staticmethod
    def _sbox_function(data, s_box):
        ''' choose data from sbox '''
        row = (S_DES.get_bit(data, 3) << 1) ^ (data & 1) # 2bits
        col = (data >> 1) & ((1 << 2) - 1) # 2bits
        return s_box[row*4+col]
    
    def _reset_key(self, key):
        ''' reset keys of S-DES '''
        self.keys = list()
        key = S_DES.permutation(key, self._pc1, 10) # 10bits
        left_key, right_key = S_DES.split_bit(key, 10, 2) # 10bits -> 5bits * 2
        for i in range(self._round):
            left_key, right_key = S_DES.cyclic_lshift(left_key, 5, self._lshift[i]), S_DES.cyclic_lshift(right_key, 5, self._lshift[i])
            key = S_DES.merge_bit((left_key, right_key), 5) # 5bits * 2 -> 10bits
            key = S_DES.permutation(key, self._pc2, 10) # 10bits -> 8bits
            self.keys.append(key)
    
    def _reset_data(self):
        ''' reset basic data of S-DES '''
        self._ip = [2, 6, 3, 1, 4, 8, 5, 7]
        self._ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self._extend = [4, 1, 2, 3, 2, 3, 4, 1]
        self._permute = [2, 4, 3, 1]
        self._s_box = [
            [1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2],
            [0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3]
        ]
        self._pc1 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self._pc2 = [6, 3, 7, 4, 8, 5, 10, 9]
        self._lshift = [1, 2]

if __name__ == '__main__':
    key = 0b1010000010
    s_des = S_DES(key)
    data = 0b10111101
    code = s_des.run(data)
    text = s_des.run(code, method='decrypt')
    print(bin(data))
    print(bin(code))
    print(bin(text))
