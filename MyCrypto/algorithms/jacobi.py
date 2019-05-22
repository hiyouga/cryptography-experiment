def jacobi(m, n):
    if n <= 0:
        raise Exception
    if m == 1 or m == 0:
        return m
    if m % n == 0:
        return 0
    if n&1 and m>n:
        return jacobi(m%n, n)
    if m&1 and n&1 and m<n:
        if m%4==3 and n%4==3:
            return -jacobi(n, m)
        else:
            return jacobi(n, m)
    if n&1 and m==2:
        if n%8==1 or n%8==7:
            return 1
        if n%8==3 or n%8==5:
            return -1
        raise Exception
    if n&1:
        if not m&1:
            return jacobi(2, n) * jacobi(m>>1, n)
    raise Exception
