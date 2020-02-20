# -*- coding: utf-8 -*-
"""
Christian Teeples
"""
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

###############################################################################
def readWaveFile(fileName):
    data, samplerate = sf.read(fileName)
    return data, samplerate
###############################################################################
def lowPassFilter(originalSignal, fs, fc, L, window):
    ft = fc/fs
    M = L - 1
    #N = np.arange(0, M, 1)
    h = []
    w = []
    n = 0
    while n < L:
        if (n != (M/2)):
            h.append((np.sin(2*np.pi*ft*(n - M/2)))/(np.pi*(n - M/2)))
        elif (n == (M/2)):
            h.append(2*ft)
        if (window != False):
            w.append(0.54 - 0.46 * np.cos((2 * np.pi * n) / M))
        n = n + 1
    if(window != False):
        h = np.multiply(h, w)
    newSignal = np.convolve(originalSignal, h)
    return newSignal, h
###############################################################################
dataList, sampleRate = readWaveFile('P_9_2.wav')
filteredSignalH, filter_coefficientsH = lowPassFilter(dataList, sampleRate, 7500, 101, False)
filteredSignalW, filter_coefficientsW = lowPassFilter(dataList, sampleRate, 7500, 101, True)
x1, y1 = freqz(filter_coefficientsH, 1)
x2, y2 = freqz(filter_coefficientsW, 1)

lineH, = plt.plot(x1, abs(y1))
lineW, = plt.plot(x2, abs(y2))
#plt.legend([lineH, lineW], ['original', 'windowed'])
plt.title('Frequency Response')
plt.show()

sf.write('cleanMusic.wav', filteredSignalW, sampleRate)



 