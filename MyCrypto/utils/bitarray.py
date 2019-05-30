import math

class bitarray: # A python implementation of bitarray
    
    def __init__(self, data:int=0, length:int=0):
        self._data = data
        self._length = length
    
    def __repr__(self) -> str:
        if self._length == 0:
            return ''
        return format(self._data, '0{:d}b'.format(self._length))
    
    def __len__(self) -> int:
        return self._length
    
    def __eq__(self, obj:'bitarray') -> bool:
        assert isinstance(obj, bitarray) and self._length == obj._length
        return self._data == obj._data
    
    def __invert__(self) -> 'bitarray':
        return bitarray(self._data^((1<<self._length)-1), self._length)
    
    def __and__(self, obj:'bitarray') -> 'bitarray':
        assert isinstance(obj, bitarray) and self._length == obj._length
        return bitarray(self._data&obj._data, self._length)
    
    def __or__(self, obj:'bitarray') -> 'bitarray':
        assert isinstance(obj, bitarray) and self._length == obj._length
        return bitarray(self._data|obj._data, self._length)
    
    def __xor__(self, obj:'bitarray') -> 'bitarray':
        assert isinstance(obj, bitarray) and self._length == obj._length
        return bitarray(self._data^obj._data, self._length)
    
    def __lshift__(self, obj:int) -> 'bitarray': # cyclic lshift
        assert isinstance(obj, int) and self._length != 0
        obj %= self._length
        return self.concat((self[obj:], self[:obj]))
    
    def __rshift__(self, obj:int) -> 'bitarray': # cyclic rshift
        assert isinstance(obj, int) and self._length != 0
        obj %= self._length
        return self.concat((self[-obj:], self[:-obj]))
    
    def __add__(self, obj:'bitarray') -> 'bitarray': # mod addition
        assert isinstance(obj, bitarray) and len(self) == len(obj)
        return bitarray((self._data+obj._data)&((1<<self._length)-1), self._length)
    
    def __getitem__(self, obj:slice) -> 'bitarray': # index or slice
        if isinstance(obj, int):
            return bitarray(int(str(self)[obj], 2), 1)
        if isinstance(obj, slice):
            s = str(self)[obj]
            if s != '':
                return bitarray(int(s, 2), len(s))
            else:
                return bitarray()
    
    def split(self, obj:int) -> list: # split to bitarray list each length is obj
        assert isinstance(obj, int) and self._length % obj == 0
        return [self[i*obj:(i+1)*obj] for i in range(self._length//obj)]
    
    @staticmethod
    def concat(objlist:list) -> 'bitarray': # concatenate bitarray list
        assert isinstance(objlist, list) or isinstance(objlist, tuple)
        res = bitarray()
        for obj in objlist:
            res._data = (res._data<<obj._length)^obj._data
            res._length += obj._length
        return res
    
    def to_integer(self) -> int:
        return self._data
    
    def to_bytes(self, byteorder='big') -> bytes:
        return self.to_integer().to_bytes(math.ceil(self._length/8), byteorder=byteorder)
    
    @staticmethod
    def from_bytes(b:bytes, byteorder='big') -> 'bitarray':
        return bitarray(int.from_bytes(b, byteorder=byteorder), len(b)*8)
    
    def reverse(self) -> 'bitarray':
        if self._length == 0:
            return bitarray()
        else:
            return bitarray(int(str(self)[::-1], 2), self._length)


if __name__ == '__main__':
    a = bitarray(0b011001, 6)
    b = bitarray(0b011110, 6)
    print('a', a)
    print('b', b)
    print('~a', ~a)
    print('a+b', a+b)
    print('a&b', a&b)
    print('a|b', a|b)
    print('a^b', a^b)
    print('a>>1', a>>1)
    print('a<<1', a<<1)
    print('concat(a,b)', bitarray.concat((a, b)))
    print('a.split(2)', a.split(2))
    print('a[1:4]', a[1:4])
    print('a[4]', a[4])
    print('a.to_integer()', a.to_integer())
    print('a.to_bytes()', a.to_bytes())
    print('bitarray.from_bytes(b\'\\x19\')', bitarray.from_bytes(b'\x19'))
