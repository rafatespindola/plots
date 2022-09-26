import poller


class Subcamada(poller.Callback):

    def __init__(self, source, tout):
        poller.Callback.__init__(self, source, tout)
        self.upper = None
        self.lower = None

    def envia(self, quadro):
        raise NotImplementedError('abstract')

    def recebe(self, quadro):
        raise NotImplementedError('abstract')

    def conecta(self, superior):
        self.upper = superior
        superior.lower = self
