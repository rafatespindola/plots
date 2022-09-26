class Quadro:

    def __init__(self):
        self.data = bytearray()
        self.freq_seq = []
        self.n_bytes = len(self.data)
        self.n_bits = self.n_bytes * 8
