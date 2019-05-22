import sys
sys.path.append("../..")
import random
from MyCrypto.ecc.ecc import ECC

class ElGamal:
    
    def __init__(self, g, n):
        self.g = g
        self.n = n
    
    def genKey(self):
        d = random.randint(1, n-1)
        return (d * self.g, d)
    
    def encrypt(self, m, pk):
        x = self.g(isInfty=True)
        while x.isInfty:
            k = random.randint(1, self.n-1)
            x = k * pk
        return (k * self.g, m + x)
    
    def decrypt(self, c, sk):
        x = sk * c[0]
        return c[1] - x

if __name__ == '__main__':
    from MyCrypto.utils.residue_field import RF
    
    class RF_211(RF):
        
        def __init__(self, data, modulo=211):
            super().__init__(data, modulo)
    
    # Global
    G = ECC(a=0, b=-4, field=RF_211, x=2, y=2)
    n = 240
    elgamal = ElGamal(G, n)
    # Alice
    pk, sk = elgamal.genKey()
    print(pk, sk)
    # Bob
    m = G*3
    print(m)
    c = elgamal.encrypt(m, pk)
    # Channel
    print(c)
    # Alice
    print(elgamal.decrypt(c, sk))
