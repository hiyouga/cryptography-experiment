import sys
sys.path.append("..")
import hashlib
from MyCrypto.utils.bitarray import bitarray
from MyCrypto.hash.sha_utils import Digest

class SHA3:
    
    def __init__(self, c:int):
        self._c = c
        self._b = 1600
        self._r = self._b - c
        self._d = c // 2
        self.digest_size = c // 16
        self._reset_data()
    
    def __call__(self, data:bytes) -> bytes:
        data = bitarray.from_bytes(data)
        data = self._sponge(data, self._d)
        return Digest(data.to_bytes())
    
    def _sponge(self, data:bitarray, dlen:int) -> bitarray:
        data = self._pad10star1(data)
        data = self._permute(data)
        dseq = data.split(self._r)
        s = bitarray(0, self._b)
        for di in dseq:
            s = self._keccak_p(s ^ bitarray.concat((di, bitarray(0, self._c))))
        z = bitarray()
        while len(z) < dlen:
            z = bitarray.concat((z, s[0:self._r]))
            s = self._keccak_p(s)
        z = self._permute(z)
        return z[0:dlen]
    
    def _pad10star1(self, data:bitarray) -> bitarray:
        q = (self._r - len(data) % self._r)//8
        if q == 1:
            data = bitarray.concat((data, bitarray(0x86, 8)))
        else:
            data = bitarray.concat((data, bitarray(0x06, 8), bitarray(0, 8*(q-2)), bitarray(0x80, 8)))
        return data
    
    def _keccak_p(self, data:bitarray, nr:int=24) -> bitarray:
        state = self._bits2state(data)
        for i in range(nr):
            state = self._round(state, self._rc[i])
        data = self._state2bits(state)
        return data
    
    def _round(self, state:list, rc:int) -> list:
        # theta step
        C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
        D = [C[(x-1)%5] ^ (C[(x+1)%5] >> 1) for x in range(5)]
        state = [[state[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        # rho and pi steps
        temp = [[None for y in range(5)] for x in range(5)]
        for x in range(5):
            for y in range(5):
                temp[y][(2*x+3*y)%5] = state[x][y] >> self._rotc[x][y]
        # chi step
        for x in range(5):
            for y in range(5):
                state[x][y] = temp[x][y] ^ ((~temp[(x+1)%5][y]) & temp[(x+2)%5][y])
        # iota step
        state[0][0] = state[0][0] ^ rc
        return state
    
    def _bits2state(self, data:bitarray) -> list:
        return [[data[64*(5*y+x):64*(5*y+x+1)] for y in range(5)] for x in range(5)]
    
    def _state2bits(self, state:list) -> bitarray:
        return bitarray.concat([state[x][y] for y in range(5) for x in range(5)])
    
    def _permute(self, b:bitarray) -> bitarray: # little order transform
        blist = b.split(8) # per byte
        return bitarray.concat([blist[i].reverse() for i in range(len(blist))])
    
    def _reset_data(self):
        rc_int = [
            0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
            0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
            0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
            0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
            0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
            0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
            0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
            0x8000000000008080, 0x0000000080000001, 0x8000000080008008
        ]
        self._rc = [bitarray(c, 64).reverse() for c in rc_int]
        self._rotc = [
            [0, 36, 3, 41, 18],
            [1, 44, 10, 45, 2],
            [62, 6, 43, 15, 61],
            [28, 55, 25, 21, 56],
            [27, 20, 39, 8, 14]
        ]

class SHA3_16(SHA3): # for birthday attack
    
    def __init__(self):
        super().__init__(32)

class SHA3_224(SHA3):
    
    def __init__(self):
        super().__init__(448)
        self.hmac_size = 1152

class SHA3_256(SHA3):
    
    def __init__(self):
        super().__init__(512)
        self.hmac_size = 1088

class SHA3_384(SHA3):
    
    def __init__(self):
        super().__init__(768)
        self.hmac_size = 832

class SHA3_512(SHA3):
    
    def __init__(self):
        super().__init__(1024)
        self.hmac_size = 576


if __name__ == '__main__':
    message = 'The quick brown fox jumps over the lazy dog'
    mysha3 = SHA3_512()
    stdsha3 = hashlib.sha3_512
    print(mysha3(message.encode('ascii')).hexdigest)
    print(stdsha3(message.encode('ascii')).hexdigest())
