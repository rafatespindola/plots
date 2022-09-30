import logging
from Subcamada import Subcamada
from enum import Enum
import ByteUtils


class State(Enum):
    f1 = 0
    f2 = 1
    f3 = 2
    f4 = 3
    f5 = 4
    f6 = 5
    f7 = 6
    f8 = 7
    end = 8


class Codificador(Subcamada):

    def __init__(self):
        Subcamada.__init__(self, None, 3)
        self.disable_timeout()
        self.dealers = {
            State.f1: self.f1,
            State.f2: self.f2,
            State.f3: self.f3,
            State.f4: self.f4,
            State.f5: self.f5,
            State.f6: self.f6,
            State.f7: self.f7,
            State.f8: self.f8
        }
        self.state = State.f1
        self.buffer = []  # sequencia de frequências para transmitir
        self.byte_count = 0  # aponta em qual byte estamos lendo na sequencia
        self.bit_count = 0  # aponta em qual bit estamos lendo na sequencia de bytes
        logging.basicConfig(level=logging.INFO)  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    def envia(self, quadro):
        self.buffer = []
        self.bit_count = 0
        self.byte_count = 0
        self.set_initial_state(quadro)

        while self.bit_count <= (len(quadro.data) * 8) and self.state != State.end:
            logging.info('Cod.envia: bit_count: ' + str(self.bit_count))
            logging.info('Cod.envia: byte_count: ' + str(self.byte_count))
            logging.info('Cod.envia: State: ' + str(self.state))
            self.handle_mef(quadro)

        print(self.buffer)
        quadro.freq_seq = self.buffer
        self.lower.envia(quadro)

    def set_initial_state(self, quadro):
        bits = self.next_two_bits(quadro)
        first_bit = bits[0]
        second_bit = bits[1]

        if first_bit == 0:
            if second_bit == 0:
                self.state = State.f1
            else:
                self.state = State.f2
        else:
            if second_bit == 0:
                self.state = State.f3
            else:
                self.state = State.f4

        logging.info('Cod.set_inicial_state:' + str(self.state))

    def set_next_state(self, bits):
        first_bit = bits[0]
        second_bit = bits[1]
        if self.state == State.f1:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f5
                else:
                    self.state = State.f2
            else:
                if second_bit == 0:
                    self.state = State.f3
                else:
                    self.state = State.f4
        elif self.state == State.f2:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f1
                else:
                    self.state = State.f6
            else:
                if second_bit == 0:
                    self.state = State.f3
                else:
                    self.state = State.f4
        elif self.state == State.f3:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f1
                else:
                    self.state = State.f2
            else:
                if second_bit == 0:
                    self.state = State.f7
                else:
                    self.state = State.f4
        elif self.state == State.f4:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f1
                else:
                    self.state = State.f2
            else:
                if second_bit == 0:
                    self.state = State.f3
                else:
                    self.state = State.f8
        elif self.state == State.f5:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f1
                else:
                    self.state = State.f6
            else:
                if second_bit == 0:
                    self.state = State.f7
                else:
                    self.state = State.f8
        elif self.state == State.f6:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f5
                else:
                    self.state = State.f2
            else:
                if second_bit == 0:
                    self.state = State.f7
                else:
                    self.state = State.f8
        elif self.state == State.f7:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f5
                else:
                    self.state = State.f6
            else:
                if second_bit == 0:
                    self.state = State.f3
                else:
                    self.state = State.f8
        elif self.state == State.f8:
            if first_bit == 0:
                if second_bit == 0:
                    self.state = State.f5
                else:
                    self.state = State.f6
            else:
                if second_bit == 0:
                    self.state = State.f7
                else:
                    self.state = State.f4

    def handle_mef(self, quadro):
        current_dealer = self.dealers[self.state]
        return current_dealer(quadro)

    def next_two_bits(self, quadro):
        self.byte_count = self.bit_count // 8
        bit_count = self.bit_count % 8

        logging.info('Cod.next_two_bits byte geral: ' + str(self.byte_count))
        logging.info('Cod.next_two_bits bit local: ' + str(bit_count))

        first_bit = ByteUtils.get_bit(quadro.data[self.byte_count], 7 - bit_count)
        second_bit = ByteUtils.get_bit(quadro.data[self.byte_count], 6 - bit_count)

        logging.info('Cod.next_two_bits first: ' + str(first_bit))
        logging.info('Cod.next_two_bits second: ' + str(second_bit))

        return first_bit, second_bit

    def f1(self, quadro):
        self.buffer.append(0)
        self.next_step_mef(quadro)

    def f2(self, quadro):
        self.buffer.append(1)
        self.next_step_mef(quadro)

    def f3(self, quadro):
        self.buffer.append(2)
        self.next_step_mef(quadro)

    def f4(self, quadro):
        self.buffer.append(3)
        self.next_step_mef(quadro)

    def f5(self, quadro):
        self.buffer.append(4)
        self.next_step_mef(quadro)

    def f6(self, quadro):
        self.buffer.append(5)
        self.next_step_mef(quadro)

    def f7(self, quadro):
        self.buffer.append(6)
        self.next_step_mef(quadro)

    def f8(self, quadro):
        self.buffer.append(7)
        self.next_step_mef(quadro)

    def next_step_mef(self, quadro):
        self.bit_count += 2
        logging.info('Cod.next_step_mef bit_count: ' + str(self.bit_count))
        if self.bit_count >= len(quadro.data) * 8:
            logging.info('Cod.next_step_mef State atual: END' )
            self.state = State.end
        else:
            logging.info('Cod.next_step_mef: Ainda não acabou a MEF')
            next_two_bits = self.next_two_bits(quadro)
            self.set_next_state(next_two_bits)
