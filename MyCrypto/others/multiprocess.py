import timeit
import multiprocessing

def f(x, y):
    for i in range(20000):
        x = x + x * y
    return x

def norp():
    k = [i for i in range(50)]
    res = [f(i, i+1) for i in k]
    return res

def mulp():
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cores)
    res_list = list()
    for i in range(50):
        res = pool.apply_async(func=f, args=(i, i+1))
        res_list.append(res)
    pool.close()
    pool.join()
    res_all = [res.get() for res in res_list]
    return res_all

if __name__ == "__main__":
    t1 = timeit.Timer('norp()', setup='from __main__ import norp')
    t2 = timeit.Timer('mulp()', setup='from __main__ import mulp')
    print('{:.10f}'.format(t1.timeit(1)))
    print('{:.10f}'.format(t2.timeit(1)))
