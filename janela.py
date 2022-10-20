import wave
import numpy as np
import struct
import matplotlib.pyplot as plt


audiofilename = "tx_data.wav"
audiofile = wave.open(audiofilename, 'r')
fileSize = audiofile.getparams()[3]  # n
sample_rate = audiofile.getparams()[2]  # fs
time_len = fileSize / sample_rate  # tx

print(audiofile.getparams())

audio = []
for i in range(fileSize):
    x = audiofile.readframes(1)
    audio.append(struct.unpack('h', x))

# 0,2399 - 2400,4799 - 4800,7199 - 7200,9599

audio_list = []
for i in audio:
    audio_list.append(i[0])

freq = np.fft.fftfreq(fileSize) * sample_rate
mascara = freq > 0

print(len(freq))

fft_calculo = 2.0 * np.abs(np.fft.fft(audio_list) / fileSize)

x = freq[mascara][175:750]
y = fft_calculo[mascara][175:750]

plt.close(1)
plt.figure(1)
plt.title("Sinal da fft - Padrão")
plt.plot(freq[mascara], fft_calculo[mascara])
plt.show()

plt.close(2)
plt.figure(2)
plt.title("Sinal da fft- Com Zoom")
plt.plot(x, y)
plt.show()

plt.close(3)
plt.figure(3)
plt.title("Sinal no tempo")
plt.plot(audio_list[0:2400])
plt.show()

plt.close(4)
plt.figure(4)
plt.title("Sinal no tempo")
plt.plot(audio_list[2400:4800])
plt.show()

plt.close(5)
plt.figure(5)
plt.title("Sinal no tempo")
plt.plot(audio_list[4800:7200])
plt.show()

plt.close(6)
plt.figure(6)
plt.title("Sinal no tempo")
plt.plot(audio_list[7200:9599])
plt.show()

# index = []
# val = 0
# for i in fft_calculo[mascara]:
#     if i > 6000:
#         index.append(val)
#     val += 1
#
# for i in index:
#     if 990 < i < 1010:
#         print('Mil')
#     elif 1990 < i < 2010:
#         print('Dois mil')


