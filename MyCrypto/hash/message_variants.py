import hashlib

def vary_msg(m:str, d:int) -> list:
    mlist = [m]
    words = m.split(' ')
    r = len(words) - 1
    counter = [(0, [0] * r)]
    while len(mlist) < d:
        k, count = counter.pop(0)
        for i in range(k, r):
            if len(mlist) == d:
                break
            count[i] += 1
            counter.append((i, list(count)))
            #print(count) # for debug
            var = words[0]
            for j in range(r):
                var += ' ' + '\b ' * count[j] + words[j+1]
            mlist.append(var)
            count[i] -= 1
    return mlist

if __name__ == '__main__':
    out = vary_msg('I like Python!', 10)
    md5 = hashlib.md5
    print('Displayed message:')
    for m in out:
        print(m, '|', md5(m.encode('ascii')).hexdigest())
    print('Raw message:')
    for m in out:
        print(str(m.encode()) + '\t' + str(md5(m.encode('ascii')).hexdigest()))
