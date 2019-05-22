def vernam(x, key, method='encrypt'):
    return x ^ key

if __name__ == '__main__':
    key = 0b0010011000
    print(bin(vernam(0b1001101101, key)))
    print(bin(vernam(0b1011110101, key, method='decrypt')))
