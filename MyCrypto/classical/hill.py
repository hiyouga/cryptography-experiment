import sys
sys.path.append("../..")
from MyCrypto.utils.matrix import Matrix
from MyCrypto.utils.residue_field import RF

class RF_95(RF):
    
    def __init__(self, data, modulo=95):
        super().__init__(data, modulo)

def hill(x, key, m, method='encrypt'):
    if method == 'encrypt':
        code = str()
        for i in range(0, len(x), m):
            mx = Matrix.construct(1, m, dtype=RF_95)
            for j in range(m):
                mx[0, j] = RF_95(ord(x[i+j])-ord(' '))
            my = mx * key
            for j in range(m):
                code += chr(int(str(my[0, j]))+ord(' '))
        return code
    elif method == 'decrypt':
        text = str()
        key_inv = key.inv()
        for i in range(0, len(x), m):
            mx = Matrix.construct(1, m, dtype=RF_95)
            for j in range(m):
                mx[0, j] = RF_95(ord(x[i+j])-ord(' '))
            my = mx * key_inv
            for j in range(m):
                text += chr(int(str(my[0, j]))+ord(' '))
        return text

def cracker(text, code, m, s=0):
    if (s+m)*m > len(text):
        return -1
    mx = Matrix.construct(m, m, dtype=RF_95)
    my = Matrix.construct(m, m, dtype=RF_95)
    for i in range(m):
        for j in range(m):
            mx[i, j] = RF_95(ord(text[(s+i)*m+j])-ord(' '))
            my[i, j] = RF_95(ord(code[(s+i)*m+j])-ord(' '))
    try:
        return mx.inv()*my
    except Exception:
        return cracker(text, code, m, s+1)

if __name__ == '__main__':
    import time
    m = 3
    key = Matrix([[3, 9, 1], [6, 5, 1], [3, 4, 9]], dtype=RF_95)
    text = 'Today is 2019/3/19, this is a sunny day, we feel happy :-)'
    while len(text) % m != 0:
        text += ' '
    code = hill(text, key, m)
    print(code)
    print(hill(code, key, m, method='decrypt'))
    t1 = time.time()
    print(cracker(text, code, m))
    t2 = time.time()
    print('Crack Time:{:.10f}'.format(t2-t1))
