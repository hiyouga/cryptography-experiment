class Digest:
    
    def __init__(self, data:bytes):
        self.digest = data
        self.digest_size = len(data) * 8
        self.hexdigest = format(int.from_bytes(data, byteorder='big'), '0{:d}x'.format(self.digest_size//4))
        self.bindigest = format(int.from_bytes(data, byteorder='big'), '0{:d}b'.format(self.digest_size))
