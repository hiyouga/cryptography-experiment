import sys
sys.path.append("../..")
from MyCrypto.des.s_des import S_DES

class Double_SDES:
    
    def __init__(self, key1, key2):
        self.sdes1 = S_DES(key1)
        self.sdes2 = S_DES(key2)
    
    def encrypt(self, text):
        code = self.sdes1.run(text, method='encrypt')
        code = self.sdes2.run(code, method='encrypt')
        return code
    
    def decrypt(self, code):
        text = self.sdes2.run(code, method='decrypt')
        text = self.sdes1.run(text, method='decrypt')
        return text


def mitm(texts, codes):
    ''' meet-in-the-middle '''
    code_to_key1 = dict()
    for key1 in range(2**10):
        s_des = S_DES(key1)
        cipher = s_des.run(texts[0], method='encrypt')
        if cipher in code_to_key1:
            code_to_key1[cipher].append(key1)
        else:
            code_to_key1[cipher] = [key1]
    for key2 in range(2**10):
        s_des = S_DES(key2)
        plaintext = s_des.run(codes[0], method='decrypt')
        if plaintext in code_to_key1:
            for key1 in code_to_key1[plaintext]:
                double_sdes = Double_SDES(key1, key2)
                if not [i for i in range(1, len(text)) if double_sdes.encrypt(texts[i]) != codes[i]]:
                    return key1, key2
    return -1


if __name__ == '__main__':
    key1 = 0b1010000010
    key2 = 0b1100101011
    double_sdes = Double_SDES(key1, key2)
    text = [0b01000101, 0b11010101, 0b11100111, 0b10110111]
    code = [double_sdes.encrypt(t) for t in text]
    print(list(map(bin, text)))
    print(list(map(bin, code)))
    print(list(map(bin, (key1, key2))))
    print(list(map(bin, mitm(text, code))))
