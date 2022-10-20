# used for editing wave files
import wave
# for basic mathematic operations
import numpy as np
# for using with wave functions
import struct
# for using plots
import matplotlib.pyplot as plt


# # frequency of FSK
# frequency_list = [1000.0, 2000.0]  # Hz
# # number of symbol types. for mFSK 2 is enough.
# num_frequency = 2
# # sample duration in seconds
# duration = 0.001 # seconds

# audio file name
audiofilename = "tx_data.wav"

# open audio file
audiofile = wave.open(audiofilename, 'r')
# get number of frames in file
fileSize = audiofile.getparams()[3]  # n
# get sample rate of recorded file
sample_rate = audiofile.getparams()[2]  # fs
# tamanho do sinal em segundos
time_len = fileSize / sample_rate  # tx
# gere um vetor de 0 a time_len igualmente espaçado com fileSize pontos
t = np.linspace(0, time_len, fileSize)

audio = []
for i in range(fileSize):
    x = audiofile.readframes(1)
    audio.append(struct.unpack('h', x))

audio_list = []
for i in audio:
    audio_list.append(i[0])

# eixo x do fft
freq = np.fft.fftfreq(fileSize) * fileSize
# mascara para obter somentes valores positivos
mascara = freq > 0

# calculo da fft sobre sinal s
fft_calculo = 2.0 * np.abs(np.fft.fft(audio_list) / fileSize)

plt.figure(1)
plt.title("Sinal original")
plt.plot(t, audio_list)

plt.figure(2)
plt.title("Sinal da fft")
plt.plot(freq[mascara], fft_calculo[mascara])
plt.show()

# -- Obtem frequencia exata -- #

index = []
val = 0
for i in fft_calculo[mascara]:
    if i > 6000:
        index.append(val)
    val += 1

# print(index)

for i in index:
    if 990 < i < 1010:
        print('Mil')
    elif 1990 < i < 2010:
        print('Dois mil')
