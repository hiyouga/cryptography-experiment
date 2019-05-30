class Ext_RF: # A python implementation of Galois Field GF[x]/(p(x))
    
    def __init__(self, data, poly, base):
        assert len(poly) > 0
        self.order = len(poly) - 1
        self.base = base
        self.data = [base(0) for i in range(len(poly))] # data[-1] should be 0 except it equals poly
        if isinstance(data, tuple) or isinstance(data, list):
            assert len(data) <= len(poly)
            for i in range(len(data)):
                if not isinstance(data[i], base):
                    self.data[i] = base(data[i])
                else:
                    self.data[i] = data[i]
        elif isinstance(data, int):
            self.data[0] = base(data)
        else:
            raise Exception
        for i in range(len(poly)):
            if not isinstance(poly[i], base):
                self.poly = list(map(base, poly))
            else:
                self.poly = list(poly)
    
    def __repr__(self):
        return '(' + '-'.join(map(str, self.data[-2::-1])) + ')'
    
    def __call__(self, data=None):
        if data is None:
            data = self.data
        return self.__class__(data=data, poly=self.poly, base=self.base)
    
    def __eq__(self, obj):
        assert isinstance(obj, self.__class__) and self.poly == obj.poly
        return self.data == obj.data
    
    def __lshift__(self, obj):
        assert isinstance(obj, int) and obj <= self.order
        temp = list(self.data)
        for i in range(obj, self.order):
            temp[i] = temp[i-obj]
        for i in range(0, obj):
            temp[i] = self.base(0)
        return self(temp)
    
    def __rshift__(self, obj):
        assert isinstance(obj, int) and obj <= self.order
        temp = list(self.data)
        for i in range(0, self.order-obj):
            temp[i] = temp[i+obj]
        for i in range(self.order-obj, self.order):
            temp[i] = self.base(0)
        return self(temp)
    
    def __neg__(self):
        res = self()
        for i in range(self.order):
            res.data[i] = -self.data[i]
        return res
    
    def __add__(self, obj):
        assert isinstance(obj, self.__class__) and self.poly == obj.poly
        res = self()
        for i in range(self.order):
            res.data[i] = self.data[i] + obj.data[i]
        return res
    
    def __sub__(self, obj):
        assert isinstance(obj, self.__class__) and self.poly == obj.poly
        res = self()
        for i in range(self.order):
            res.data[i] = self.data[i] - obj.data[i]
        return res
    
    def __mul__(self, obj):
        if isinstance(obj, int) or isinstance(obj, self.base):
            res = self()
            for i in range(self.order):
                res.data[i] = self.data[i] * obj
            return res
        elif isinstance(obj, self.__class__) and self.poly == obj.poly:
            assert self.poly == obj.poly
            temp = self()
            res = temp * obj.data[0]
            for i in range(1, self.order):
                temp = self._xtimes(temp)
                res = res + temp * obj.data[i]
            return res
        else:
            raise Exception
    
    def __rmul__(self, obj):
        return self.__mul__(obj)
    
    def __truediv__(self, obj):
        return self.__mul__(obj.inv)
    
    def __pow__(self, obj):
        assert isinstance(obj, int) and obj >= -1
        if obj == -1:
            return self.inv
        res = self(1)
        temp = self()
        while obj:
            if obj & 1:
                res = res * temp
            temp = temp * temp
            obj >>= 1
        return res
    
    def __floordiv__(self, obj):
        assert isinstance(obj, self.__class__) and self.poly == obj.poly
        diff = self.deg - obj.deg
        pos = self.deg
        res = self(0)
        if diff < 0:
            return res
        temp = self()
        while diff >= 0:
            t = temp.data[pos] / obj.data[pos-diff]
            res.data[diff] = t
            div = obj << diff
            for i in range(pos):
                temp.data[i] = temp.data[i] - t * div.data[i]
            pos, diff = pos - 1, diff - 1
        return res
    
    def __mod__(self, obj):
        assert isinstance(obj, self.__class__) and self.poly == obj.poly
        diff = self.deg - obj.deg
        pos = self.deg
        res = self()
        if diff < 0:
            return res
        while diff >= 0:
            t = res.data[pos] / obj.data[pos-diff]
            div = obj << diff
            for i in range(pos):
                res.data[i] = res.data[i] - t * div.data[i]
            res.data[pos] = self.base(0)
            pos, diff = pos - 1, diff - 1
        return res
    
    def _xtimes(self, x):
        if x.deg == self.order-1:
            t = x.data[self.order-1] / self.poly[-1]
            x = x << 1
            for i in range(self.order):
                x.data[i] = x.data[i] - t * self.poly[i]
        else:
            x = x << 1
        return x
    
    @property
    def deg(self):
        res = -1
        for i in range(len(self.data)):
            if self.data[i] != self.base(0):
                res = i
        return res
    
    @property
    def inv(self):
        if self.deg == -1:
            raise Exception
        x1, x0 = self(1), self(0)
        y1, y0 = self(0), self(1)
        a, b = self(self.poly), self()
        q = a//b
        r1, r0 = b, a%b
        while not r0.deg == -1:
            x1, x0 = x0, x1-q*x0
            y1, y0 = y0, y1-q*y0
            q = r1//r0
            r1, r0 = r0, r1%r0
        assert r1.deg == 0
        return y0*(r1.data[0].inv)


if __name__ == '__main__':
    import sys
    sys.path.append("../..")
    from MyCrypto.utils.residue_field import RF
    
    ''' Towering Extension '''
    
    class RF_3(RF):
        def __init__(self, data, modulo=3):
            super().__init__(data, modulo)
    
    poly = (1, 0, 1)
    
    class RF_3_2(Ext_RF):
        
        def __init__(self, data, poly=poly, base=RF_3):
            super().__init__(data, poly, base)
    
    print('RF_3^2')
    a = RF_3_2((1, 2))
    b = RF_3_2((0, 2))
    print('a', a)
    print('b', b)
    print('a<<1', a<<1)
    print('a>>1', a>>1)
    print('a+b', a+b)
    print('a-b', a-b)
    print('a*b', a*b)
    print('a/b', a/b)
    print('a//b', a//b)
    print('a%b', a%b)
    print('a^-1', a.inv)
    print('a/a', a/a)
    print('a**2', a**2)
    assert a == b * (a//b) + a%b
    
    poly2 = ((0, 1), (0, 0), (1, 0))
    
    class RF_3_4(Ext_RF):
        
        def __init__(self, data, poly=poly2, base=RF_3_2):
            super().__init__(data, poly, base)
    
    print('RF_3^4')
    p = RF_3_4(((1, 0), (0, 1)))
    q = RF_3_4(((0, 0), (1, 0)))
    print('p', p)
    print('q', q)
    print('p>>1', p>>1)
    print('p<<1', p<<1)
    print('p+q', p+q)
    print('p-q', p-q)
    print('p*q', p*q)
    print('p/q', p/q)
    print('p//q', p//q)
    print('p%q', p%q)
    print('p/p', p/p)
    assert p == q * (p//q) + p%q
    
    
    poly3 = (((0, 0), (1, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((1, 0), (0, 0)))
    
    class RF_3_12(Ext_RF):
        
        def __init__(self, data, poly=poly3, base=RF_3_4):
            super().__init__(data, poly, base)
    
    print('RF_3^12')
    p = RF_3_12(2)
    print('p', p)
    print('p/p', p/p)
