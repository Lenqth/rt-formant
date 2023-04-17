# -*- coding: utf-8 -*
import wave

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import scipy

sampling_rate = 44100
chunk = 2**11
buff_size = 2**14

import matplotlib.style as mplstyle
mplstyle.use('fast')

plt.figure(figsize=(12, 8))
plt.grid()

xgraph = np.linspace(0, sampling_rate, buff_size)


def draw(graph):
    plt.cla()
    plt.plot(xgraph, graph)
    plt.ylim(1e-6, 1)
    plt.xlim(0, 6000)
    plt.yscale("log")
    plt.pause(0.001)


def draw_log(*graphs):
    plt.cla()
    for graph in graphs:
        plt.plot(xgraph, graph)
    plt.ylim(1e-6, 1)
    plt.xlim(0, 6000)
    plt.yscale("log")
    plt.pause(0.0001)


def normalized_fft(data):
    return np.fft.fft(data) / len(data)


def cepstrum(data):
    return np.fft.ifft(np.log(np.abs(np.fft.fft(data))))


def lifter(data, cutoff = 0.003):
    cep = cepstrum(data)
    cep[int(sampling_rate * cutoff) :] = 0
    return np.exp(np.fft.fft(cep)) / len(data)


def detect_peak(data):
    peaks, _ = scipy.signal.find_peaks(np.log(data), prominence=0.3)
    result = np.zeros_like(data)
    for i in peaks:
        result[i] = 1
    return result


def main():
    fmt = pyaudio.paInt16
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=fmt,
        channels=1,
        rate=sampling_rate,
        input=True,
        input_device_index=1,
        frames_per_buffer=chunk,
    )

    try:
        buff = np.zeros(buff_size)
        buff_window = 0

        while True:
            data = stream.read(chunk)

            array = np.frombuffer(data, dtype=np.int16)
            buff[buff_window : buff_window + chunk] = array
            buff_window = (buff_window + chunk) % buff_size

            array = buff.astype(float) / 32768

            freq = np.abs(normalized_fft(array))
            lifter_array = lifter(array)
            peak_of_lifter = detect_peak(lifter_array)
            draw_log(freq, lifter_array, peak_of_lifter)

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
