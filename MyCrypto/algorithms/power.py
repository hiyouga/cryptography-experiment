def power(a, n, m):
    res = 1
    a %= m
    for i in range(n):
        res = (res * a) % m
    return res

def quick_power(a, n, m):
    res = 1
    a %= m
    while n:
        if n & 1:
            res = (res * a) % m
        a = (a * a) % m
        n >>= 1
    return res

if __name__ == '__main__':
    import timeit
    
    print(power(13, 10000, 10007))
    print(quick_power(13, 10000, 10007))
    
    t1 = timeit.Timer('power(10, 1000000, 10007)', setup='from __main__ import power')
    t2 = timeit.Timer('quick_power(10, 1000000, 10007)', setup='from __main__ import quick_power')
    print('Classical power:{:.10f}'.format(t1.timeit(1)))
    print('Quick power:{:.10f}'.format(t2.timeit(1)))
