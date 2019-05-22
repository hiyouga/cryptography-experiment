import sys
sys.path.append("../..")
from MyCrypto.aes.aes import AES, GF2_8

class Fast_AES(AES):
    
    def __init__(self, raw_key):
        super().__init__(raw_key)
        self._reset_f_data()
    
    def fast_run(self, data, method='encrypt'):
        if method == 'encrypt':
            return self._fast_encrypt(data, self._te_box, self._f_keys, self._f_s_box)
        elif method == 'decrypt':
            return self._fast_decrypt(data, self._td_box, self._f_keys_inv, self._f_s_box_inv)
    
    @staticmethod
    def _fast_encrypt(data, te, k, sbox):
        s = [data>>96, data>>64&0xffffffff, data>>32&0xffffffff, data&0xffffffff]
        s = [s[i] ^ k[i] for i in range(4)]
        for i in range(1, 10):
            tmp0 = te[0][s[0]>>24] ^ te[1][s[1]>>16&0xff] ^ te[2][s[2]>>8&0xff] ^ te[3][s[3]&0xff] ^ k[4*i]
            tmp1 = te[0][s[1]>>24] ^ te[1][s[2]>>16&0xff] ^ te[2][s[3]>>8&0xff] ^ te[3][s[0]&0xff] ^ k[4*i+1]
            tmp2 = te[0][s[2]>>24] ^ te[1][s[3]>>16&0xff] ^ te[2][s[0]>>8&0xff] ^ te[3][s[1]&0xff] ^ k[4*i+2]
            tmp3 = te[0][s[3]>>24] ^ te[1][s[0]>>16&0xff] ^ te[2][s[1]>>8&0xff] ^ te[3][s[2]&0xff] ^ k[4*i+3]
            s = [tmp0, tmp1, tmp2, tmp3]
        tmp0 = (sbox[s[0]>>24]<<24 | sbox[s[1]>>16&0xff]<<16 | sbox[s[2]>>8&0xff]<<8 | sbox[s[3]&0xff]) ^ k[40]
        tmp1 = (sbox[s[1]>>24]<<24 | sbox[s[2]>>16&0xff]<<16 | sbox[s[3]>>8&0xff]<<8 | sbox[s[0]&0xff]) ^ k[41]
        tmp2 = (sbox[s[2]>>24]<<24 | sbox[s[3]>>16&0xff]<<16 | sbox[s[0]>>8&0xff]<<8 | sbox[s[1]&0xff]) ^ k[42]
        tmp3 = (sbox[s[3]>>24]<<24 | sbox[s[0]>>16&0xff]<<16 | sbox[s[1]>>8&0xff]<<8 | sbox[s[2]&0xff]) ^ k[43]
        return (tmp0<<96 | tmp1<<64 | tmp2<<32 | tmp3)
    
    @staticmethod
    def _fast_decrypt(data, td, k, sbox):
        s = [data>>96, data>>64&0xffffffff, data>>32&0xffffffff, data&0xffffffff]
        s = [s[i] ^ k[40+i] for i in range(0, 4)]
        for i in range(9, 0, -1):
            tmp0 = td[0][s[0]>>24] ^ td[1][s[3]>>16&0xff] ^ td[2][s[2]>>8&0xff] ^ td[3][s[1]&0xff] ^ k[4*i]
            tmp1 = td[0][s[1]>>24] ^ td[1][s[0]>>16&0xff] ^ td[2][s[3]>>8&0xff] ^ td[3][s[2]&0xff] ^ k[4*i+1]
            tmp2 = td[0][s[2]>>24] ^ td[1][s[1]>>16&0xff] ^ td[2][s[0]>>8&0xff] ^ td[3][s[3]&0xff] ^ k[4*i+2]
            tmp3 = td[0][s[3]>>24] ^ td[1][s[2]>>16&0xff] ^ td[2][s[1]>>8&0xff] ^ td[3][s[0]&0xff] ^ k[4*i+3]
            s = [tmp0, tmp1, tmp2, tmp3]
        tmp0 = (sbox[s[0]>>24]<<24 | sbox[s[3]>>16&0xff]<<16 | sbox[s[2]>>8&0xff]<<8 | sbox[s[1]&0xff]) ^ k[0]
        tmp1 = (sbox[s[1]>>24]<<24 | sbox[s[0]>>16&0xff]<<16 | sbox[s[3]>>8&0xff]<<8 | sbox[s[2]&0xff]) ^ k[1]
        tmp2 = (sbox[s[2]>>24]<<24 | sbox[s[1]>>16&0xff]<<16 | sbox[s[0]>>8&0xff]<<8 | sbox[s[3]&0xff]) ^ k[2]
        tmp3 = (sbox[s[3]>>24]<<24 | sbox[s[2]>>16&0xff]<<16 | sbox[s[1]>>8&0xff]<<8 | sbox[s[0]&0xff]) ^ k[3]
        return (tmp0<<96 | tmp1<<64 | tmp2<<32 | tmp3)
    
    def _reset_f_data(self):
        self._f_s_box = [self._s_box[i, j].data for i in range(self._s_box.row) for j in range(self._s_box.col)]
        self._f_s_box_inv = [self._s_box_inv[i, j].data for i in range(self._s_box_inv.row) for j in range(self._s_box_inv.col)]
        self._f_keys = list()
        for key in self._keys:
            for j in range(key.col):
                self._f_keys.append(AES.merge_bit([key[i, j].data for i in range(key.row)], 8))
        self._f_keys_inv = list()
        for key in self._keys_inv:
            for j in range(key.col):
                self._f_keys_inv.append(AES.merge_bit([key[i, j].data for i in range(key.row)], 8))
        self._generate_te()
        self._generate_td()
    
    def _generate_te(self):
        self._te_box = (list(), list(), list(), list())
        for i in range(2**8):
            si = self._f_s_box[i]
            gi = [(GF2_8(j) * GF2_8(si)).data for j in range(1, 4)]
            self._te_box[0].append(AES.merge_bit((gi[1], gi[0], gi[0], gi[2]), 8))
            self._te_box[1].append(AES.merge_bit((gi[2], gi[1], gi[0], gi[0]), 8))
            self._te_box[2].append(AES.merge_bit((gi[0], gi[2], gi[1], gi[0]), 8))
            self._te_box[3].append(AES.merge_bit((gi[0], gi[0], gi[2], gi[1]), 8))
    
    def _generate_td(self):
        self._td_box = (list(), list(), list(), list())
        for i in range(2**8):
            si = self._f_s_box_inv[i]
            gi = [(GF2_8(j) * GF2_8(si)).data for j in [9, 11, 13, 14]]
            self._td_box[0].append(AES.merge_bit((gi[3], gi[0], gi[2], gi[1]), 8))
            self._td_box[1].append(AES.merge_bit((gi[1], gi[3], gi[0], gi[2]), 8))
            self._td_box[2].append(AES.merge_bit((gi[2], gi[1], gi[3], gi[0]), 8))
            self._td_box[3].append(AES.merge_bit((gi[0], gi[2], gi[1], gi[3]), 8))


if __name__ == '__main__':
    key = 0x0f1571c947d9e8590cb7add6af7f6798
    plaintext = 0x0123456789abcdeffedcba9876543210
    fast_aes = Fast_AES(key)
    code = fast_aes.run(plaintext)
    print(hex(code))
    print(hex(fast_aes.run(code, method='decrypt')))
    code2 = fast_aes.fast_run(plaintext)
    print(hex(code2))
    print(hex(fast_aes.fast_run(code2, method='decrypt')))
