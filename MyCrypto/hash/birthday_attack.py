import random
from MyCrypto.hash.sha3 import SHA3_16

def birthday_attack(hash_func):
    log_dict = dict()
    hash_num = 0
    attempt_count = 0
    while True:
        hash_num += random.random()
        digest = hash_func(str(hash_num).encode('ascii')).hexdigest
        if attempt_count % 100 == 0:
            print(attempt_count)
        if digest in log_dict:
            return (attempt_count, str(hash_num), log_dict[digest])
        log_dict[digest] = str(hash_num)
        attempt_count += 1


if __name__ == '__main__':
    print(birthday_attack(SHA3_16()))
