class ECC:
    
    def __init__(self, a, b, field, x=None, y=None, isInfty=False):
        if not (isinstance(a, field) and isinstance(b, field)):
            a, b = field(a), field(b)
        assert 4*a**3+27*b**2 != field(0)
        if not isInfty:
            if not (isinstance(x, field) and isinstance(y, field)):
                x, y = field(x), field(y)
            assert y*y == x**3+a*x+b
        self.a = a
        self.b = b
        self.field = field
        self.x = x
        self.y = y
        self.isInfty = isInfty
    
    @classmethod
    def INFTY(cls, a, b, field):
        return cls(a=a, b=b, field=field, isInfty=True)
    
    def __call__(self, x=None, y=None, isInfty=None):
        if x is None and y is None:
            if isInfty is None:
                isInfty = self.isInfty
            if not isInfty:
                x, y = self.x, self.y
        else:
            isInfty = False
        return self.__class__(a=self.a, b=self.b, field=self.field, x=x, y=y, isInfty=isInfty)
    
    def belong(self, x, y):
        return y*y == x**3+self.a*x+self.b
    
    def __repr__(self):
        if self.isInfty:
            return 'Infty'
        return '({:s}, {:s})'.format(str(self.x), str(self.y))
    
    def __eq__(self, obj):
        assert self._isvalid(obj)
        if self.isInfty or obj.isInfty:
            return self.isInfty and obj.isInfty
        else:
            return self.x == obj.x and self.y == obj.y
    
    def __neg__(self):
        if self.isInfty:
            return self()
        return self(self.x, -self.y)
    
    def __add__(self, obj):
        assert self._isvalid(obj)
        if self.isInfty:
            return obj()
        if obj.isInfty:
            return self()
        if self == -obj:
            return self(isInfty=True)
        if self == obj:
            lamda = (3*self.x*self.x+self.a)/(2*self.y)
        else:
            lamda = (obj.y-self.y)/(obj.x-self.x)
        xr = lamda*lamda-self.x-obj.x
        yr = lamda*(self.x-xr)-self.y
        return self(xr, yr)
    
    def __sub__(self, obj):
        assert self._isvalid(obj)
        return self.__add__(-obj)
    
    def __mul__(self, obj):
        assert isinstance(obj, int)
        temp = self()
        res = self(isInfty=True)
        while obj:
            if obj & 1:
                res = res + temp
            temp = temp + temp
            obj >>= 1
        return res
    
    def __rmul__(self, obj):
        assert isinstance(obj, int)
        return self * obj
    
    def _isvalid(self, obj):
        if isinstance(obj, self.__class__) and self.field == obj.field and self.a == obj.a and self.b == obj.b:
            return True
        return False

if __name__ == '__main__':
    import sys
    sys.path.append("../..")
    from MyCrypto.utils.residue_field import RF
    
    class RF_23(RF):
        def __init__(self, data, modulo=23):
            super().__init__(data, modulo)
    
    o = ECC.INFTY(a=1, b=1, field=RF_23)
    p = o(x=3, y=10)
    q = o(x=9, y=7)
    r = -p
    print(o)
    print(p)
    print(q)
    print(r)
    print(p+q)
    print(p+r)
    print(p*233)
