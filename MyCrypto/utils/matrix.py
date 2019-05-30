class Matrix: # A python implementation of Matrices
    
    def __init__(self, lst, dtype=float):
        assert isinstance(lst, list) and isinstance(lst[0], list)
        self.row = len(lst)
        self.col = len(lst[0])
        self.dtype = dtype
        self._matrix = [[dtype(lst[i][j]) for j in range(self.col)] for i in range(self.row)]
    
    @classmethod
    def construct(cls, row, col, fill=0, dtype=float):
        lst = [[fill for j in range(col)] for i in range(row)]
        return cls(lst, dtype=dtype)
    
    @classmethod
    def identity(cls, rank, dtype=float):
        lst = [[1 if i == j else 0 for j in range(rank)] for i in range(rank)]
        return cls(lst, dtype=dtype)
    
    @property
    def shape(self):
        return (self.row, self.col)
    
    @property
    def issquare(self):
        return self.row == self.col
    
    def copy(self):
        res = self.construct(self.row, self.col, dtype=self.dtype)
        for i in range(self.row):
            for j in range(self.col):
                res[i, j] = self[i, j]
        return res
    
    def __repr__(self):
        res = str()
        if self.dtype == float:
            rep = lambda x:str(round(x+1e-10, 6))
        else:
            rep = str
        res = '[ ' + '\n  '.join([' '.join(list(map(rep, row))) for row in self._matrix]) + ' ]'
        return res
    
    def __getitem__(self, index):
        return self._matrix[index[0]][index[1]]
    
    def __setitem__(self, index, value):
        assert isinstance(value, self.dtype)
        self._matrix[index[0]][index[1]] = value
    
    def __add__(self, obj):
        assert isinstance(obj, Matrix) and self.shape == obj.shape
        res = self.construct(self.row, self.col, dtype=self.dtype)
        for i in range(self.row):
            for j in range(self.col):
                res[i, j] = self[i, j] + obj[i, j]
        return res
    
    def __sub__(self, obj):
        assert isinstance(obj, Matrix) and self.shape == obj.shape
        res = self.construct(self.row, self.col, dtype=self.dtype)
        for i in range(self.row):
            for j in range(self.col):
                res[i, j] = self[i, j] - obj[i, j]
        return res
    
    def __mul__(self, obj):
        if isinstance(obj, self.dtype):
            res = self.construct(self.row, self.col, dtype=self.dtype)
            for i in range(self.row):
                for j in range(self.col):
                    res[i, j] = self[i, j] * obj
            return res
        else:
            assert isinstance(obj, Matrix) and self.col == obj.row
            res = self.construct(self.row, obj.col, dtype=self.dtype)
            for i in range(self.row):
                for j in range(obj.col):
                    temp = self.dtype(0)
                    for k in range(self.col):
                        temp += self[i, k] * obj[k, j]
                    res[i, j] = temp
            return res
    
    def __truediv__(self, obj):
        assert isinstance(obj, Matrix) and self.col == obj.row and obj.issquare
        return self.__mul__(obj.inv())
    
    def __pow__(self, obj):
        assert isinstance(obj, int) and self.issquare and obj >= -1
        if obj == -1:
            return self.inv()
        res = self.identity(self.row, dtype=self.dtype)
        temp = self.copy()
        while obj:
            if obj & 1:
                res = res * temp
            temp = temp * temp
            obj >>= 1
        return res
    
    def __eq__(self, obj):
        assert isinstance(obj, Matrix) and obj.shape == self.shape
        for i in range(self.row):
            for j in range(self.col):
                if not self[i, j] == obj[i, j]:
                    return False
        return True
    
    def transpose(self):
        res = self.construct(self.col, self.row, dtype=self.dtype)
        for i in range(self.col):
            for j in range(self.row):
                res[i, j] = self[j, i]
        return res
    
    def _cofactor_matrix(self, row, col):
        assert self.row > 1 and row <= self.row and col <= self.col
        res = self.construct(self.row-1, self.col-1, dtype=self.dtype)
        for i in range(self.row):
            if i == row:
                continue
            for j in range(self.col):
                if j == col:
                    continue
                ii = i-1 if i > row else i
                jj = j-1 if j > col else j
                res[ii, jj] = self[i, j]
        return res
    
    def alg_cofactor(self, row, col):
        assert self.issquare
        return (self.dtype(-1)**(row+col)) * self._cofactor_matrix(row, col).det()
    
    def det(self):
        assert self.issquare
        if self.row == 1:
            return self[0, 0]
        res = self.dtype(0)
        for i in range(self.row):
            res += self[0, i] * self.alg_cofactor(0, i)
        return res
    
    def inv(self):
        assert self.issquare
        det = self.det()
        res = self.construct(self.row, self.col, dtype=self.dtype)
        for i in range(self.row):
            for j in range(self.col):
                res[i, j] = self.alg_cofactor(j, i) / det
        return res

if __name__ == '__main__':
    A = Matrix([[1, 2, 5], [2, 1, -9], [8, 9, 1]])
    B = Matrix([[3, 3, 7], [4, 1, 0], [-8, 4, 3]])
    print(A)
    print(B)
    print(A+B)
    print(A-B)
    print(A-A)
    print(A*B)
    print(A/B)
    print(A/A)
    print(A**3)
    print(A**-1)
