from faster_whisper import WhisperModel

from voice.interface import SpeechRecognizer


class WhisperSpeechRecognizer(SpeechRecognizer):
    def __init__(
        self,
        model_size: str = "tiny",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

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

    def listen(self) -> str:
        raise NotImplementedError(
            "Microphone recording will be added in the next step."
        )