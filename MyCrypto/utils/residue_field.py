class RF: # A python implementation of Residue field GF(p)
    
    def __init__(self, data, modulo):
        assert isinstance(data, int) and isinstance(modulo, int)
        self.data = data % modulo
        self.modulo = modulo
    
    def __call__(self, data=None):
        if data is None:
            data = self.data
        return self.__class__(data=data, modulo=self.modulo)
    
    def __repr__(self):
        return str(self.data)
    
    def __neg__(self):
        return self(-self.data)
    
    def __eq__(self, obj):
        if isinstance(obj, int):
            return self.data == obj
        elif isinstance(obj, self.__class__):
            return self.data == obj.data
        else:
            raise Exception
    
    def __add__(self, obj):
        assert isinstance(obj, self.__class__)
        return self(self.data + obj.data)
    
    def __sub__(self, obj):
        assert isinstance(obj, self.__class__)
        return self(self.data - obj.data)
    
    def __mul__(self, obj):
        if isinstance(obj, int):
            return self(self.data * obj)
        elif isinstance(obj, self.__class__):
            return self(self.data * obj.data)
        else:
            raise Exception
    
    def __rmul__(self, obj):
        return self.__mul__(obj)
    
    def __truediv__(self, obj):
        assert isinstance(obj, self.__class__)
        return self.__mul__(obj.inv)
    
    def __pow__(self, obj):
        assert isinstance(obj, int) and obj >= -1
        if obj == -1:
            return self.inv
        res, temp = 1, self.data
        while obj:
            if obj & 1:
                res = (res * temp) % self.modulo
            temp = (temp * temp) % self.modulo
            obj >>= 1
        return self(res)
    
    @property
    def inv(self):
        if self.data == 0:
            raise Exception
        x1, x0 = 1, 0
        y1, y0 = 0, 1
        a, b = self.modulo, self.data
        q = a//b
        r1, r0 = b, a%b
        while r0 != 0:
            x1, x0 = x0, x1-q*x0
            y1, y0 = y0, y1-q*y0
            q = r1//r0
            r1, r0 = r0, r1%r0
        assert r1 == 1
        return self(y0)

if __name__ == '__main__':
    a = RF(3, 23)
    b = RF(5, 23)
    print('a', a)
    print('b', b)
    print('a+b', a+b)
    print('a-b', a-b)
    print('a*b', a*b)
    print('a/b', a/b)
    print('a/a', a/a)
    print('a^3', a**3)
    print('a^-1', a**-1)
