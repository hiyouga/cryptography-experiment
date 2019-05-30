import sys
sys.path.append("../..")
from MyCrypto.algorithms.power import quick_power
from MyCrypto.algorithms.prime_sieve import sieveV3

def eular(n):
    m = n
    if not m & 1:
        m >>= 1
    for p in range(3, m+1):
        if m % p == 0:
            while m % p == 0:
                m //= p
            break
    if m != 1:
        return None
    if n & 1:
        phi = n//p*(p-1)
    else:
        phi = n//2//p*(p-1)
    return phi

def naive_pr(n):
    if n == 2:
        return [1]
    if n == 4:
        return [3]
    phi = eular(n)
    if not phi:
        return None
    res = list()
    for i in range(2, n):
        if not [j for j in range(2, phi) if quick_power(i, j, n) == 1]:
            res.append(i)
    return res

def naive_fact(n):
    fact = list()
    for i in range(2, n+1):
        if n % i == 0:
            fact.append(i)
            while n % i == 0:
                n //= i
        if n == 1:
            break
    return fact

def advance_fact(n): # slower than naive method ?
    fact = list()
    for p in sieveV3(n):
        if n % p == 0:
            fact.append(p)
    return fact

def advance_pr(n):
    if n == 2:
        return [1]
    if n == 4:
        return [3]
    phi = eular(n)
    if not phi:
        return None
    factors = naive_fact(phi)
    res = list()
    for i in range(2, n):
        if not [x for x in factors if quick_power(i, phi//x, n) == 1]:
            res.append(i)
    return res

if __name__ == '__main__':
    import timeit
    print(naive_pr(25))
    print(advance_pr(25))
    t1 = timeit.Timer('naive_pr(361)', setup='from __main__ import naive_pr')
    t2 = timeit.Timer('advance_pr(361)', setup='from __main__ import advance_pr')
    print('naive prime root:', t1.timeit(1))
    print('advance prime root:', t2.timeit(1))
