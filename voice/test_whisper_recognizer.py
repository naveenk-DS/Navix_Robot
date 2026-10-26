import pytest

from voice.whisper_recognizer import WhisperSpeechRecognizer


def test_whisper_recognizer_requires_microphone_implementation():
    recognizer = WhisperSpeechRecognizer.__new__(
        WhisperSpeechRecognizer
    )

    with pytest.raises(NotImplementedError):
        recognizer.listen()