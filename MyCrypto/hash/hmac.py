import sys
sys.path.append("../..")
import hmac
from MyCrypto.utils.bitarray import bitarray
from MyCrypto.hash.sha_utils import Digest
from MyCrypto.hash.sha1 import SHA1
from MyCrypto.hash.sha3 import SHA3_512

class HMAC:
    
    def __init__(self, hash_func:callable):
        self._hash_func = hash_func
        self._n = hash_func.digest_size * 8
        self._b = hash_func.hmac_size
        self._ipad = bitarray.concat([bitarray(0x36, 8)]*(self._b//8))
        self._opad = bitarray.concat([bitarray(0x5C, 8)]*(self._b//8))
    
    def __call__(self, key:bytes, data:bytes) -> bytes:
        # padding key
        if len(key) > self._b//8:
            key = self._hash_func(key).digest
        key = bitarray.from_bytes(key)
        k = bitarray.concat((key, bitarray(0, self._b-len(key))))
        # process data
        data = bitarray.from_bytes(data)
        si = k ^ self._ipad
        data = bitarray.concat((si, data))
        data = self._hash(data)
        so = k ^ self._opad
        data = bitarray.concat((so, data))
        data = self._hash(data)
        return Digest(data.to_bytes())
    
    def _hash(self, data:bitarray) -> bitarray:
        data = self._hash_func(data.to_bytes()).digest
        return bitarray.from_bytes(data)

if __name__ == '__main__':
    message = b'The quick brown fox jumps over the lazy dog'
    key = b'Secret'
    
    stdsha1hmac = hmac.new(key, message, digestmod='sha1')
    mysha1hmac = HMAC(SHA1())
    print(stdsha1hmac.hexdigest())
    print(mysha1hmac(key, message).hexdigest)
    
    stdsha3hmac = hmac.new(key, message, digestmod='sha3_512')
    mysha3hmac = HMAC(SHA3_512())
    print(stdsha3hmac.hexdigest())
    print(mysha3hmac(key, message).hexdigest)
