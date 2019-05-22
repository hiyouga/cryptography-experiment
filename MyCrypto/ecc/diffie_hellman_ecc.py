import sys
sys.path.append("../..")
import random
from MyCrypto.ecc.ecc import ECC

class DH:
    
    def __init__(self, g, n):
        self.g = g
        self.n = n
    
    def genKey(self):
        d = random.randint(1, n-1)
        return (d * self.g, d)
    
    def genCipher(self, pk, sk):
        return pk * sk


if __name__ == '__main__':
    from MyCrypto.utils.residue_field import RF
    
    class RF_211(RF):
        
        def __init__(self, data, modulo=211):
            super().__init__(data, modulo)
    
    # Global
    G = ECC(a=0, b=-4, field=RF_211, x=2, y=2)
    n = 240
    dh = DH(G, n)
    # User
    pkA, skA = dh.genKey()
    pkB, skB = dh.genKey()
    print(pkA, skA)
    print(pkB, skB)
    # Key
    print(dh.genCipher(pkB, skA))
    print(dh.genCipher(pkA, skB))
