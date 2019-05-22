def vigenere(x, key, method='encrypt'):
    if not key.islower:
        return -1
    m = len(key)
    code = str()
    if method == 'encrypt':
        if not x.islower():
            return -1
        for i in range(len(x)):
            p = ord(x[i])-ord('a')
            k = ord(key[i%m])-ord('a')
            code += chr(ord('A')+(p+k)%26)
        return code
    elif method == 'decrypt':
        if not x.isupper():
            return -1
        for i in range(len(x)):
            p = ord(x[i])-ord('A')
            k = ord(key[i%m])-ord('a')
            code += chr(ord('a')+(p-k+26)%26)
        return code


if __name__ == '__main__':
    key = 'deceptive'
    print(vigenere('wearediscoveredsaveyourself', key))
    print(vigenere('ZICVTWQNGRZGVTWAVZHCQYGLMGJ', key, method='decrypt'))
