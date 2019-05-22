import sys
sys.path.append("../..")
from MyCrypto.algorithms.exgcd import gcd, inverse

def affine(x, key, mod=26, method='encrypt'):
    a, b = key
    if gcd(a, mod) != 1:
        return -1
    if method == 'encrypt':
        if not x.islower():
            return -1
        forward = dict()
        for i in range(26):
            forward[chr(ord('a')+i)] = chr(ord('A')+(a*i+b)%mod)
        code = str()
        for c in x:
            code += forward[c]
        return code
    elif method == 'decrypt':
        if not x.isupper():
            return -1
        backward = dict()
        for i in range(26):
            backward[chr(ord('A')+i)] = chr(ord('a')+(i-b+mod)*inverse(a, mod)%mod)
        code = str()
        for c in x:
            code += backward[c]
        return code
    else:
        return -1

if __name__ == '__main__':
    key = (25, 3)
    s = 'cryptography'
    print(affine(s, key))
    print(affine('BMFOKPXMDOWF', key, method='decrypt'))
