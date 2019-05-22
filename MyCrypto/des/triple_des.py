import sys
sys.path.append("../..")
from MyCrypto.des.des import DES

class Triple_DES:
    
    def __init__(self, key1, key2):
        self.des1 = DES(key1)
        self.des2 = DES(key2)
    
    def encrypt(self, text):
        code = self.des1.run(text, method='encrypt')
        code = self.des2.run(code, method='decrypt')
        code = self.des1.run(code, method='encrypt')
        return code
    
    def decrypt(self, code):
        text = self.des1.run(code, method='decrypt')
        text = self.des2.run(text, method='encrypt')
        text = self.des1.run(text, method='decrypt')
        return text

if __name__ == '__main__':
    key1 = 0x133457799BBCDFF1
    key2 = 0x0E329232EA6D0D73
    triple_des = Triple_DES(key1, key2)
    data = 0x1234567890ABCDEF
    code = triple_des.encrypt(data)
    text = triple_des.decrypt(code)
    print(hex(data))
    print(hex(code))
    print(hex(text))
