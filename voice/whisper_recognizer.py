from faster_whisper import WhisperModel

from voice.interface import SpeechRecognizer
from voice.microphone import MicrophoneRecorder


class WhisperSpeechRecognizer(SpeechRecognizer):
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8",
        recorder: MicrophoneRecorder | None = None,
    ) -> None:
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

        self.recorder = recorder or MicrophoneRecorder()

    def transcribe_file(self, audio_path: str) -> str:
        segments, _ = self.model.transcribe(
            audio_path,
            beam_size=5,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    def listen(
        self,
        duration: float = 4.0,
        audio_path: str = "voice_command.wav",
    ) -> str:
        recorded_file = self.recorder.record(
            duration=duration,
            output_path=audio_path,
        )

        return self.transcribe_file(recorded_file)