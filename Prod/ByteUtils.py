# Classe que realiza get, set e clear de bits, sendo passado o bit que deve ser processado dentro de um byte.
def get_bit(val, n):
    return (val & (1 << n)) >> n


def set_bit(val, n):
    return val | (1 << n)


def clear_bit(val, n):
    return val & ~(1 << n)
