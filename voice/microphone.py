import os
import sys
import wave

import pyaudio


class MicrophoneRecorder:
    def __init__(self, channels=1, rate=16000, chunk=1024):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk

    def record(self, output_path, duration=4):
        # Silence noisy ALSA messages only while PyAudio starts up
        saved_stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")
        try:
            p = pyaudio.PyAudio()
        finally:
            sys.stderr.close()
            sys.stderr = saved_stderr

        sample_width = p.get_sample_size(pyaudio.paInt16)
        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames = []
        for _ in range(int(self.rate / self.chunk * duration)):
            frames.append(stream.read(self.chunk, exception_on_overflow=False))

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(frames))

        return output_path