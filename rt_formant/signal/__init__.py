

import numpy as np
import scipy
import sys
from rt_formant.sound import BUFF_SIZE, SAMPLING_RATE

from scipy import signal

def normalized_fft(data):
    window = signal.hamming(len(data)) 
    return np.fft.fft(window * data) / len(data)


xgraph = np.linspace(0, SAMPLING_RATE, BUFF_SIZE)


def cepstrum(data):
    window = signal.hamming(len(data)) 
    return np.real(np.fft.ifft(np.log(sys.float_info.epsilon + np.abs(np.fft.fft(window * data)))))


def lifter(data, cutoff = 0.002):
    cep = cepstrum(data)
    cep[int(SAMPLING_RATE * cutoff): -int(SAMPLING_RATE * cutoff)] = 0
    return np.exp(np.real(np.fft.fft(cep))) / len(data)

def unlifter(data, cutoff = 0.002):
    cep = cepstrum(data)
    cep[0:int(SAMPLING_RATE * cutoff)] = 0
    cep[-int(SAMPLING_RATE * cutoff):] = 0
    return np.exp(np.real(np.fft.fft(cep))) / len(data)

def detect_peaks(data):
    peaks, _ = scipy.signal.find_peaks(np.log(data), prominence=0.5)
    return xgraph[peaks]

def detect_peaks_raw(data):
    peaks, _ = scipy.signal.find_peaks(np.log(data), prominence=0.5)
    return peaks