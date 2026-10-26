from abc import ABC, abstractmethod


class SpeechRecognizer(ABC):
    @abstractmethod
    def listen(self) -> str:
        """Listen to speech and return recognized text."""
        raise NotImplementedError


class TextSpeechRecognizer(SpeechRecognizer):
    def listen(self) -> str:
        return input("Voice command: ")