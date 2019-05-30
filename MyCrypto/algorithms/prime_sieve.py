import math

def naive(n):
    primes = []
    for i in range(2, n+1):
        isPrime = True
        j = 2
        while j * j <= i:
            if (i % j == 0):
                isPrime = False
                break
            j += 1
        if isPrime:
            primes.append(i)
    return primes

def sieve(n):
    primes = [x if x&1 else 0 for x in range(n+1)]
    primes[1] = 0
    for i in range(3, int(math.sqrt(n)), 2):
        if primes[i]:
            for j in range(i+i, n, i):
                if primes[j] % primes[i] == 0:
                    primes[j] = 0
    return [2] + [x for x in primes if x]

def sieveV2(n):
    n = (n - 3) // 2
    primes = [2*x+3 for x in range(n+1)]
    for i in range(int(math.sqrt(2*n)/2)):
        if primes[i]:
            for j in range(3*(i+1), n+1, 2*i+3):
                primes[j] = 0
    return [2] + [x for x in primes if x]

def sieveV3(n):
    n = (n - 3) // 2
    primes = [2*x+3 for x in range(n+1)]
    for i in range(int(math.sqrt(2*n)/2)):
        if primes[i]:
            for j in range(i*(2*i+6)+3, n+1, 2*i+3):
                primes[j] = 0
    return [2] + [x for x in primes if x]

def sieveRange(primes, low, width):
    check = [(x+low) if x&1 else 0 for x in range(width)]
    for p in primes:
        for i in range(low//p+1, (low+width)//p+1):
            if i*p-low >= width:
                break
            check[i*p-low] = 0
    addons = [x for x in check if x]
    return addons

def sieveInf(n):
    DIV = 100000000
    primes = sieveV2(DIV)
    for i in range(DIV, n, DIV):
        primes += sieveRange(primes, i, DIV)
    return primes

if __name__ == '__main__':
    import timeit
    t1 = timeit.Timer('naive(10000)', setup='from __main__ import naive')
    t2 = timeit.Timer('sieve(10000)', setup='from __main__ import sieve')
    t3 = timeit.Timer('sieveV2(10000)', setup='from __main__ import sieveV2')
    t4 = timeit.Timer('sieveV3(10000)', setup='from __main__ import sieveV3')
    #tn = timeit.Timer('sieveInf(1000000000)', setup='from __main__ import sieveInf')
    print('Naive method:{:.5f}'.format(t1.timeit(1)))
    print('Eratosthenes sieve V1:{:.5f}'.format(t2.timeit(1)))
    print('Eratosthenes sieve V2:{:.5f}'.format(t3.timeit(1)))
    print('Eratosthenes sieve V3:{:.5f}'.format(t4.timeit(1)))
    #print('Eratosthenes sieve Inf:{:.5f}'.format(tn.timeit(1)))
