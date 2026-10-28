from voice.microphone import MicrophoneRecorder


def test_microphone_recorder_configuration():
    recorder = MicrophoneRecorder(rate=16000, channels=1)

    assert recorder.rate == 16000
    assert recorder.channels == 1
