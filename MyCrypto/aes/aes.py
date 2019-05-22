import sys
sys.path.append("../..")
from MyCrypto.utils.galois_field import GF
from MyCrypto.utils.matrix import Matrix

class GF2_8(GF):
    
    def __init__(self, data, order=8):
        super().__init__(data, order)

class AES:
    
    def __init__(self, raw_key):
        self._reset_data()
        self._reset_key(raw_key)
    
    def run(self, data, method='encrypt'):
        if method == 'encrypt':
            return self._encrypt(data)
        elif method == 'decrypt':
            return self._decrypt(data)
    
    def _encrypt(self, data):
        data = AES.split_bit(data, 128, 16)
        state = [[data[i+j*4] for j in range(4)] for i in range(4)]
        state = Matrix(state, dtype=GF2_8)
        state = state + self._keys[0]
        for i in range(1, 10):
            self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_cols(state)
            state = self._add_round_key(state, self._keys[i])
        self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self._keys[10])
        data = [state[i, j].data for j in range(4) for i in range(4)]
        data = AES.merge_bit(data, 8)
        return data
    
    def _decrypt(self, data):
        data = AES.split_bit(data, 128, 16)
        state = [[data[i+j*4] for j in range(4)] for i in range(4)]
        state = Matrix(state, dtype=GF2_8)
        state = state + self._keys_inv[10]
        for i in range(9, 0, -1):
            self._sub_bytes_inv(state)
            state = self._shift_rows_inv(state)
            state = self._mix_cols_inv(state)
            state = self._add_round_key(state, self._keys_inv[i])
        self._sub_bytes_inv(state)
        state = self._shift_rows_inv(state)
        state = self._add_round_key(state, self._keys_inv[0])
        data = [state[i, j].data for j in range(4) for i in range(4)]
        data = AES.merge_bit(data, 8)
        return data
    
    def _sub_bytes(self, state):
        for i in range(state.row):
            for j in range(state.col):
                state[i, j] = self._s_box[AES.split_bit(state[i, j].data, 8, 2)]
    
    def _sub_bytes_inv(self, state):
        for i in range(state.row):
            for j in range(state.col):
                state[i, j] = self._s_box_inv[AES.split_bit(state[i, j].data, 8, 2)]
    
    def _shift_rows(self, state):
        mat_data = [[state[i, j].data for j in range(state.col)] for i in range(state.row)]
        for i in range(4):
            for j in range(i):
                mat_data[i].append(mat_data[i].pop(0))
        return Matrix(mat_data, dtype=GF2_8)
    
    def _shift_rows_inv(self, state):
        mat_data = [[state[i, j].data for j in range(state.col)] for i in range(state.row)]
        for i in range(4):
            for j in range(i):
                mat_data[i].insert(0, mat_data[i].pop())
        return Matrix(mat_data, dtype=GF2_8)
    
    def _mix_cols(self, state):
        transform = [
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2]
        ]
        transform = Matrix(transform, dtype=GF2_8)
        return transform * state
    
    def _mix_cols_inv(self, state):
        transform = [
            [0xe, 0xb, 0xd, 0x9],
            [0x9, 0xe, 0xb, 0xd],
            [0xd, 0x9, 0xe, 0xb],
            [0xb, 0xd, 0x9, 0xe]
        ]
        transform = Matrix(transform, dtype=GF2_8)
        return transform * state
    
    def _add_round_key(self, state, key):
        return state + key
    
    def _reset_data(self):
        s_matrix = [[i*16+j for j in range(16)] for i in range(16)]
        s_matrix = Matrix(s_matrix, dtype=GF2_8)
        a_matrix = [[1 if j in [i, (i+4)%8, (i+5)%8, (i+6)%8, (i+7)%8] else 0 for j in range(8)] for i in range(8)]
        c_matrix = [[1], [1], [0], [0], [0], [1], [1], [0]]
        a_matrix = Matrix(a_matrix, dtype=GF2_8)
        c_matrix = Matrix(c_matrix, dtype=GF2_8)
        for i in range(s_matrix.row):
            for j in range(s_matrix.col):
                if s_matrix[i, j] != GF2_8(0):
                    s_matrix[i, j] = s_matrix[i, j].inv
                temp = AES.split_bit(s_matrix[i, j].data, 8, 8)[::-1]
                temp = [[i] for i in temp]
                x_matrix = Matrix(temp, dtype=GF2_8)
                temp = a_matrix * x_matrix + c_matrix
                temp = [temp[i, 0].data for i in range(temp.row)][::-1]
                temp = [AES.merge_bit(temp, 1)][0]
                s_matrix[i, j] = GF2_8(temp)
        self._s_box = s_matrix
        is_matrix = [[i*16+j for j in range(16)] for i in range(16)]
        is_matrix = Matrix(is_matrix, dtype=GF2_8)
        b_matrix = [[1 if j in [(i+2)%8, (i+5)%8, (i+7)%8] else 0 for j in range(8)] for i in range(8)]
        d_matrix = [[1], [0], [1], [0], [0], [0], [0], [0]]
        b_matrix = Matrix(b_matrix, dtype=GF2_8)
        d_matrix = Matrix(d_matrix, dtype=GF2_8)
        for i in range(is_matrix.row):
            for j in range(is_matrix.col):
                temp = AES.split_bit(is_matrix[i, j].data, 8, 8)[::-1]
                temp = [[i] for i in temp]
                ix_matrix = Matrix(temp, dtype=GF2_8)
                temp = b_matrix * ix_matrix + d_matrix
                temp = [temp[i, 0].data for i in range(temp.row)][::-1]
                temp = [AES.merge_bit(temp, 1)][0]
                is_matrix[i, j] = GF2_8(temp)
                if is_matrix[i, j] != GF2_8(0):
                    is_matrix[i, j] = is_matrix[i, j].inv
        self._s_box_inv = is_matrix
        self._rcon_c = [GF2_8(1)]
        for i in range(9):
            self._rcon_c.append(GF2_8(2)*self._rcon_c[-1])
    
    def _reset_key(self, raw_key):
        def _rot_word(x):
            x = x[:]
            x.append(x.pop(0))
            return x
        def _sub_word(x):
            x = x[:]
            for i in range(len(x)):
                x[i] = self._s_box[AES.split_bit(x[i].data, 8, 2)]
            return x
        def _rcon(i):
            x = [GF2_8(0) for i in range(4)]
            x[0] = self._rcon_c[i]
            return x
        
        keys = []
        cur_key = AES.split_bit(raw_key, 128, 16)
        cur_key = [[cur_key[i+j*4] for j in range(4)] for i in range(4)]
        cur_key = Matrix(cur_key, dtype=GF2_8)
        keys.append(cur_key)
        for i in range(10):
            w = [cur_key[j, 3] for j in range(4)]
            x = _rot_word(w)
            y = _sub_word(x)
            z = [y[j] + _rcon(i)[j] for j in range(4)]
            new_key = Matrix.construct(4, 4, dtype=GF2_8)
            for j in range(4):
                new_key[j, 0] = cur_key[j, 0] + z[j]
            for r in range(3):
                for j in range(4):
                    new_key[j, r+1] = new_key[j, r] + cur_key[j, r+1]
            cur_key = new_key
            keys.append(cur_key)
        self._keys = keys
        self._keys_inv = [self._mix_cols_inv(keys[i]) if (0<i<len(keys)-1) else keys[i] for i in range(len(keys))]
    
    @staticmethod
    def split_bit(data, length, time):
        ''' split data to tuple '''
        assert length % time == 0
        split_len = length // time
        results = list()
        for t in range(time):
            results.insert(0, data & ((1 << split_len) - 1))
            data >>= split_len
        return results
    
    @staticmethod
    def merge_bit(data, length):
        ''' merge data tuple '''
        result = 0
        for d in data:
            result <<= length
            result ^= d
        return result

if __name__ == '__main__':
    key = 0x0f1571c947d9e8590cb7add6af7f6798
    plaintext = 0x0123456789abcdeffedcba9876543210
    aes = AES(key)
    code = aes.run(plaintext)
    print(hex(code))
    print(hex(aes.run(code, method='decrypt')))
