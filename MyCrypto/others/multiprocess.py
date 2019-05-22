import timeit
import multiprocessing

def f(x, y):
    k = 0
    for i in range(10):
        k = k * i
    return x*y

def norp():
    k = [i for i in range(100000)]
    for i in k:
        f(i, i+1)

def mulp():
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    res_list = list()
    for i in range(100000):
        res = pool.apply_async(func=f, args=(i,i+1))
        res_list.append(res)
    pool.close()
    pool.join()
    codes = [res.get() for res in res_list]

if __name__ == "__main__":
    t1 = timeit.Timer('norp()', setup='from __main__ import norp')
    t2 = timeit.Timer('mulp()', setup='from __main__ import mulp')
    print('{:.10f}'.format(t1.timeit(1)))
    print('{:.10f}'.format(t2.timeit(1)))
