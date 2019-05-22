import sys
sys.path.append("../..")
from MyCrypto.des.des import DES

class DES_3round(DES):
    
    def __init__(self, raw_key):
        super().__init__(raw_key, _round=3)
    
    def run(self, data):
        left_data, right_data = DES_3round.split_bit(data, 64, 2) # 64bits -> 32bits * 2
        for i in range(self._round):
            left_data, right_data = right_data, left_data ^ self._round_function(right_data, self.keys[i])
        output = DES_3round.merge_bit((right_data, left_data), 32) # 32bits * 2 -> 64bits
        return output

class DiffCrypt(DES):
    
    def __init__(self):
        self._reset_data()
        self._reset_table()
    
    def _reset_table(self):
        table = list()
        for j in range(8):
            table.append(list()) # 8
            for bj in range(2**6):
                table[j].append(list()) # 8 * 64
                for cj in range(2**4):
                    table[j][bj].append(list()) # 8 * 64 * 16
                for bi in range(2**6):
                    ci = self._sbox_function(bi, self._s_box[j]) ^ self._sbox_function(bi ^ bj, self._s_box[j])
                    table[j][bj][ci].append(bi)
        self._in_table = table
    
    def _test_box(self, index, e_a, e_b, c):
        return [bj ^ e_a for bj in self._in_table[index][e_a ^ e_b][c]]
    
    def diff(self, data_pair, code_pair):
        data_a, data_b = data_pair
        code_a, code_b = code_pair
        l0_a, r0_a = DiffCrypt.split_bit(data_a, 64, 2)
        l0_b, r0_b = DiffCrypt.split_bit(data_b, 64, 2)
        assert r0_a == r0_b
        r3_a, l3_a = DiffCrypt.split_bit(code_a, 64, 2)
        r3_b, l3_b = DiffCrypt.split_bit(code_b, 64, 2)
        r3_xor = r3_a ^ r3_b
        l0_xor = l0_a ^ l0_b
        c_xor = DiffCrypt.permutation(r3_xor ^ l0_xor, DiffCrypt.reverse_table(self._permute), 32) # 32bits
        e_a = DiffCrypt.permutation(l3_a, self._extend, 32) # 32bits -> 48bits
        e_b = DiffCrypt.permutation(l3_b, self._extend, 32) # 32bits -> 48bits
        cs = DiffCrypt.split_bit(c_xor, 32, 8) # 32bits -> 4bits * 8
        es_a = DiffCrypt.split_bit(e_a, 48, 8) # 48bits -> 6bits * 8
        es_b = DiffCrypt.split_bit(e_b, 48, 8) # 48bits -> 6bits * 8
        test_boxes = [self._test_box(i, es_a[i], es_b[i], cs[i]) for i in range(8)] # 6bits * 8
        return test_boxes
    
    def analysis(self, text, code):
        key_sets = list()
        tbs = self.diff(text[0], code[0])
        for j in range(8):
            key_sets.append(set(tbs[j]))
        for i in range(1, len(text)):
            tbs = self.diff(text[i], code[i])
            for j in range(8):
                key_sets[j] = key_sets[j].intersection(set(tbs[j]))
        key_bits = list([[0]])
        for j in range(8):
            for r in range(len(key_bits)):
                key_bit = key_bits.pop(0)
                for k in key_sets[j]:
                    key_bits.append(key_bit+[k])
        keys = [DiffCrypt.merge_bit(k, 6) for k in key_bits] # 48bits
        pc1_extend = [8, 16, 24, 32, 40, 48, 56, 64] + self._pc1
        pc1_extend_rev = DiffCrypt.reverse_table(pc1_extend)
        pc2_extend = [9, 18, 22, 25, 35, 38, 43, 54] + self._pc2
        pc2_extend_rev = DiffCrypt.reverse_table(pc2_extend)
        for i in range(2**8):
            for k in keys:
                key = DiffCrypt.merge_bit((i, k), 48) # 48bits -> 56bits
                key = DiffCrypt.permutation(key, pc2_extend_rev, 56) # 56bits
                left_key, right_key= DiffCrypt.split_bit(key, 56, 2) # 56bits -> 28bits * 2
                for j in range(3):
                    left_key, right_key = DiffCrypt.cyclic_rshift(left_key, 28, self._lshift[j]), DiffCrypt.cyclic_rshift(right_key, 28, self._lshift[j])
                key = DiffCrypt.merge_bit((left_key, right_key), 28) # 28bits * 2 -> 56bits
                key = DiffCrypt.permutation(key, pc1_extend_rev, 64) # 56bits -> 64bits
                key = DiffCrypt.make_verify(key) # 64bits
                des_3round = DES_3round(key)
                code_test = des_3round.run(text[0][0])
                if code_test == code[0][0]:
                    return key
        return -1
    
    @staticmethod
    def reverse_table(table):
        rev_table = list()
        rev_tuples = list()
        for i, k in enumerate(table):
            rev_tuples.append((i+1, k))
        rev_tuples.sort(key=lambda x:x[1])
        for i, k in rev_tuples:
            rev_table.append(i)
        return rev_table
    
    @staticmethod
    def make_verify(key):
        ''' make a verification '''
        for i in range(8):
            presult = 1 # ODD
            for j in range(7):
                sig = DiffCrypt.get_bit(key, 8*(7-i)+(7-j))
                presult ^= sig
            key ^= (presult << (8*(7-i)))
        return key


if __name__ == '__main__':
    rawkey = 0xFE326232EA6D0D73
    des_3round = DES_3round(rawkey)
    text = [
        (0x748502CD38451097, 0x3874756438451097),
        (0x357418DA013FEC86, 0x33549847013FEC86)
    ]
    code = list()
    for (t_a, t_b) in text:
        code.append((des_3round.run(t_a), des_3round.run(t_b)))
    for c in code:
        print(hex(c[0]).upper(), hex(c[1]).upper())
    diff = DiffCrypt()
    print(hex(diff.analysis(text, code)))
    print(hex(rawkey))
