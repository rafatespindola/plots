class Quadro:

    def __init__(self):
        self.data = bytearray()  # Dados em bytes que a aplicação enviou
        self.freq_seq = []  # Lista de frequências equivalentes aos dados da aplicação
        self.n_bytes = len(self.data)  # Quantidade de bytes dos dados
        self.n_bits = self.n_bytes * 8  # Quantidade de bits dos dados
