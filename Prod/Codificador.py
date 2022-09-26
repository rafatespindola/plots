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

    def envia(self, quadro):
        self.bit_count = 0
        self.byte_count = 0
        self.set_initial_state(quadro)

        while self.bit_count < (len(quadro.data) * 8):
            self.handle_mef(quadro)

        # TODO ajustar aqui
        # self.lower.envia(self.buffer)
        print(self.buffer)
        self.buffer = []

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

        first_bit = ByteUtils.get_bit(quadro.data[self.byte_count], bit_count)
        second_bit = ByteUtils.get_bit(quadro.data[self.byte_count], bit_count)

        return first_bit, second_bit

    def f1(self, quadro):
        self.buffer.append(0)
        self.buffer.append(0)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f2(self, quadro):
        self.buffer.append(0)
        self.buffer.append(1)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f3(self, quadro):
        self.buffer.append(1)
        self.buffer.append(0)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f4(self, quadro):
        self.buffer.append(1)
        self.buffer.append(1)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f5(self, quadro):
        self.buffer.append(0)
        self.buffer.append(0)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f6(self, quadro):
        self.buffer.append(0)
        self.buffer.append(1)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f7(self, quadro):
        self.buffer.append(1)
        self.buffer.append(0)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)

    def f8(self, quadro):
        self.buffer.append(1)
        self.buffer.append(1)

        self.bit_count += 2
        next_two_bits = self.next_two_bits(quadro)
        self.set_next_state(next_two_bits)
