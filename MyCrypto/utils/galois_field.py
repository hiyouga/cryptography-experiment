class GF: # A python implementation of Galois Field GF(2^n)
    
    def __init__(self, data, order):
        assert isinstance(data, int)
        self.data = data
        self.order = order
        if order == 1:
            self.modulo = 0b10 # x
        elif order == 2:
            self.modulo = 0b111 # x^2+x+1
        elif order == 3:
            self.modulo = 0b1011 # x^3+x+1
        elif order == 4:
            self.modulo = 0b10011 # x^4+x+1
        elif order == 8:
            self.modulo = 0b100011011 # x^8+x^4+x^3+x+1
        elif order == 16:
            self.modulo = 0b10001000000001011 # x^16+x^12+x^3+x+1
        elif order == 0:
            self.modulo = 0 # cannot do multiply
        else:
            raise Exception
    
    def __call__(self, data=None):
        if data is None:
            data = self.data
        return self.__class__(data=data, order=self.order)
    
    def __repr__(self):
        if self.order == 0:
            return format(self.data, 'b')
        return format(self.data, '0{:d}b'.format(self.order))
    
    def __eq__(self, obj):
        if isinstance(obj, int):
            return self.data == obj
        elif isinstance(obj, self.__class__):
            return self.data == obj.data
        else:
            raise Exception
    
    def __lshift__(self, obj):
        assert isinstance(obj, int)
        return self(self.data << obj)
    
    def __rshift__(self, obj):
        assert isinstance(obj, int)
        return self(self.data >> obj)
    
    def __add__(self, obj):
        assert isinstance(obj, self.__class__)
        return self(self.data ^ obj.data)
    
    def __sub__(self, obj):
        assert isinstance(obj, self.__class__)
        return self(self.data ^ obj.data)
    
    def __mul__(self, obj):
        assert isinstance(obj, self.__class__) and self.modulo != 0
        temp = self.data
        multi = (obj.data & 1) * temp
        for i in range(1, self.order):
            temp = self._xtimes(temp)
            multi ^= (((obj.data >> i) & 1) * temp)
        return self(multi)
    
    def __pow__(self, obj):
        assert isinstance(obj, int) and obj >= -1
        if obj == -1:
            return self.inv
        res, temp = self(1), self()
        while obj:
            if obj & 1:
                res = res * temp
            temp = temp * temp
            obj >>= 1
        return res
    
    def __truediv__(self, obj):
        assert isinstance(obj, self.__class__)
        return self.__mul__(obj.inv)
    
    def __floordiv__(self, obj):
        assert isinstance(obj, self.__class__)
        diff = self.deg - obj.deg
        pos = self.deg
        res = 0
        if diff < 0:
            return self(res)
        temp, div = self.data, obj.data
        while diff >= 0:
            res <<= 1
            if temp & (1 << pos):
                temp ^= (div << diff)
                res ^= 1
            pos, diff = pos - 1, diff - 1
        return self(res)
    
    def __mod__(self, obj):
        assert isinstance(obj, self.__class__)
        diff = self.deg - obj.deg
        pos = self.deg
        if diff < 0:
            return self()
        res, div = self.data, obj.data
        while diff >= 0:
            if res & (1 << pos):
                res ^= (div << diff)
            pos, diff = pos - 1, diff - 1
        return self(res)
    
    def _xtimes(self, x):
        assert isinstance(x, int)
        if x & (1 << (self.order-1)):
            return (x << 1) ^ self.modulo
        else:
            return x << 1
    
    @property
    def inv(self):
        if self.data == 0:
            raise Exception
        x1, x0 = self(1), self(0)
        y1, y0 = self(0), self(1)
        a, b = self(self.modulo), self()
        q = a//b
        r1, r0 = b, a%b
        while not r0 == 0:
            x1, x0 = x0, x1-q*x0
            y1, y0 = y0, y1-q*y0
            q = r1//r0
            r1, r0 = r0, r1%r0
        return y0
    
    @property
    def deg(self):
        if self.data == 0:
            return -1
        else:
            return self.data.bit_length() - 1
    
    @staticmethod
    def gcd(a, b):
        if b == 0:
            return a
        return GF.gcd(b, a%b)
    
    @staticmethod
    def exgcd(a, b):
        x1, x0 = a(1), a(0)
        y1, y0 = a(0), a(1)
        q = a//b
        r1, r0 = b, a%b
        while not r0 == 0:
            x1, x0 = x0, x1-q*x0
            y1, y0 = y0, y1-q*y0
            q = r1//r0
            r1, r0 = r0, r1%r0
        return r1, x0, y0


if __name__ == '__main__':
    a = GF(0b0010001, order=8)
    b = GF(0b1101001, order=8)
    print('a\t', a)
    print('b\t', b)
    print('a.deg\t', a.deg)
    print('a^-1\t', a**-1)
    print('a+b\t', a+b)
    print('a-b\t', a-b)
    print('a*b\t', a*b)
    print('a//b\t', a//b)
    print('a%b\t', a%b)
    print('a/b\t', a/b)
    print('a/a\t', a/a)
    print('gcd(a,b)\t', GF.gcd(a, b))
    print('exgcd(a,b)\t', GF.exgcd(a, b))
    d, x, y = GF.exgcd(a, b)
    print('x*a+y*b\t', x*a+y*b)
