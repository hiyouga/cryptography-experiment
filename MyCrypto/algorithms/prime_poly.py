import sys
sys.path.append("../..")
from MyCrypto.utils.galois_field import GF

class GF_0(GF):
    
    def __init__(self, data, order):
        super().__init__(data, order=0) # cannot do multiply
        self.data = data
        self.order = order

def find_primePoly(n):
    primePoly = list()
    r = GF_0(2**(2**n-1)+1, order=2**n)
    for i in range(2**n, 2**(n+1)):
        p = GF_0(i, order=2**n)
        prime = True
        for k in range(2, i):
            if p % GF_0(k, order=2**n) == 0:
                prime = False
                break
        if prime:
            if r % p == 0:
                if not [k for k in range(1, 2**n-2) if GF_0(2**k+1, order=2**n) % p == 0]:
                    primePoly.append(GF_0(p.data, order=n+1))
    return primePoly

if __name__ == '__main__':
    print(find_primePoly(5))
