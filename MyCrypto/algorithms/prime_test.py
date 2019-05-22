import sys
sys.path.append("../..")
import random
from MyCrypto.algorithms.jacobi import jacobi
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.exgcd import gcd

def miller_rabin(n):
    q = n-1
    k = 0
    while not q & 1:
        q >>= 1
        k += 1
    a = random.randint(2, n-2)
    if quick_power(a, q, n) == 1:
        return True
    for j in range(k):
        if quick_power(a, q<<j, n) == (n-1):
            return True
    return False

def fermat(n):
    a = random.randint(2, n-2)
    d = gcd(a, n)
    if d > 1:
        return False
    if quick_power(a, n-1, n) != 1:
        return False
    return True

def solovay_stassen(n):
    a = random.randint(2, n-2)
    r = quick_power(a, (n-1)>>1, n)
    if r != 1 and r != n-1:
        return False
    s = (jacobi(a, n)+n)%n
    if r != s:
        return False
    return True

def primeTest(n, prob = 0.0001, method = 'miller_rabin'):
    if method == 'miller_rabin':
        conf = 1
        while conf >= prob:
            if not miller_rabin(n):
                return False
            conf *= 1/4
        return True
    if method == 'fermat':
        conf = 1
        while conf >= prob:
            if not fermat(n):
                return False
            conf *= 1/2
        return True
    if method == 'solovay_stassen':
        conf = 1
        while conf >= prob:
            if not solovay_stassen(n):
                return False
            conf *= 1/2
        return True

if __name__ == '__main__':
    import timeit
    
    n = 2**1279-1
    if primeTest(n, method='miller_rabin'):
        print('Is prime.')
    else:
        print('Not a prime.')
    if primeTest(n, method='fermat'):
        print('Is prime.')
    else:
        print('Not a prime.')
    if primeTest(n, method='solovay_stassen'):
        print('Is prime.')
    else:
        print('Not a prime.')
    
    t1 = timeit.Timer('primeTest(2**1279-1, method=\'miller_rabin\')', setup='from __main__ import primeTest')
    t2 = timeit.Timer('primeTest(2**1279-1, method=\'fermat\')', setup='from __main__ import primeTest')
    t3 = timeit.Timer('primeTest(2**1279-1, method=\'solovay_stassen\')', setup='from __main__ import primeTest')
    print('miller_rabin:',t1.timeit(1))
    print('fermat:',t2.timeit(1))
    print('solovay stassen:',t3.timeit(1))
