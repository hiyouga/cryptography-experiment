import sys
sys.path.append("../..")
from MyCrypto.algorithms.exgcd import inverse

def crt(b, m):
    ans = 0
    lcm = 1
    for mi in m:
        lcm *= mi
    for i in range(len(m)):
        tpn = lcm // m[i]
        tpr = inverse(tpn, m[i])
        ans = (ans+tpn*tpr*b[i])%lcm
    return (ans+lcm)%lcm

if __name__ == '__main__':
    print(crt([1, 2, 3], [4, 9, 11]))
