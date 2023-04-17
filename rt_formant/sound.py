import wave
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import scipy

SAMPLING_RATE = 44100
CHUNK = 2**10
BUFF_SIZE = 2**14


class SoundStream:
    def __init__(self):
        fmt = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=fmt,
            channels=1,
            rate=SAMPLING_RATE,
            input=True,
            input_device_index=1,
            frames_per_buffer=CHUNK,
        )
        self.buff = np.zeros(BUFF_SIZE)

    def get(self):
        read_b = self.stream.get_read_available()
        data = self.stream.read(read_b)

        array = np.frombuffer(data, dtype=np.int16)
        read_len = len(array)
        
        self.buff[0:read_len] = array
        self.buff = np.roll(self.buff, -read_len)
        array = self.buff.astype(float) / 32768

        return array

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
