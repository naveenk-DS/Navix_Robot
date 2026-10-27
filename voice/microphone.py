import pyaudio
import wave

import os
import sys

# Inside your record function, add this right before 'p = pyaudio.PyAudio()':
# This hides the messy ALSA driver outputs
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

p = pyaudio.PyAudio()

# Restore standard error output immediately after PyAudio starts up
sys.stderr = stderr


class MicrophoneRecorder:
    def __init__(self, channels=1, rate=16000, chunk=1024):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk

    # Change "output_filepath" to "output_path"
    def record(self, output_path, duration=4):
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        frames = []

        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Update this line to use output_path as well
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return output_path

