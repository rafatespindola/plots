import matplotlib.pyplot as plt
import numpy as np
import audiofile

# numero de pontos do sinal a ser gerado
n = 1000
# tamanho do sinal a sergerado. Pode ser 200ms por exemplo
tx = 200
# frequencia angular = 2 * pi * f
w = 2.0 * np.pi / tx

# gere um vetor de 0 a tx igualmente espaçado com n pontos
t = np.linspace(0, tx, n)
# sinal 1 que em 1000 pontos se repete 2 vezes
s1 = 2.0 * np.cos(2.0 * w * t)
# sinal 2 que em 1000 pontos se repete 30 vezes
s2 = 1.0 * np.cos(30.0 * w * t)
# soma dos sinais
s = s1 + s2

# eixo x do fft
freq = np.fft.fftfreq(n) * n
# mascara para obter somentes valores positivos
mascara = freq > 0

# calculo da fft sobre sinal s
fft_calculo = 2.0 * np.abs(np.fft.fft(s) / n)

plt.figure(1)
plt.title("Sinal original")
plt.plot(t, s)

plt.figure(2)
plt.title("Sinal da fft")
plt.plot(freq[mascara], fft_calculo[mascara])
plt.show()

