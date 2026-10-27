from unittest.mock import Mock

from voice.whisper_recognizer import WhisperSpeechRecognizer


def test_whisper_recognizer_transcribes_recorded_audio():
    recorder = Mock()
    recorder.record.return_value = "test.wav"

    recognizer = WhisperSpeechRecognizer.__new__(
        WhisperSpeechRecognizer
    )

    recognizer.recorder = recorder

    recognizer.transcribe_file = Mock(
        return_value="forward one"
    )

    result = recognizer.listen(
        duration=4,
        audio_path="test.wav",
    )

    recorder.record.assert_called_once_with(
        duration=4,
        output_path="test.wav",
    )

    recognizer.transcribe_file.assert_called_once_with(
        "test.wav"
    )

    assert result == "forward one"