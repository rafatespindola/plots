import logging
# from serial import Serial
from Aplicacao import Aplicacao
from Codificador import Codificador
from Trasmissor import Transmissor
import poller
import sys

if __name__ == '__main__':
    # Create serial port
    # serial_port = Serial(sys.argv[1], 9600)
    logging.basicConfig(level=logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR, CRITICAL


    # Create layers
    # enq = Enquadramento(serial_port, 5)
    # arq = Arq(4)
    # ses = Sessao(5)
    app = Aplicacao()
    cod = Codificador()
    tms = Transmissor()

    # Connect layers. The lower connects to upper
    # enq.conecta(arq)
    # arq.conecta(ses)
    # ses.conecta(app)
    cod.conecta(app)
    tms.conecta(cod)

    # Create Poller
    sched = poller.Poller()

    # Add callbacks
    # sched.adiciona(enq)
    sched.adiciona(app)

    # Run
    sched.despache()
