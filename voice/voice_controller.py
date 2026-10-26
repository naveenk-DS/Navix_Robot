from robot_core.command_executor import CommandExecutor
from robot_core.command_parser import CommandParser
from voice.interface import SpeechRecognizer


class VoiceController:
    def __init__(
        self,
        recognizer: SpeechRecognizer,
        parser: CommandParser,
        command_executor: CommandExecutor,
    ) -> None:
        self.recognizer = recognizer
        self.parser = parser
        self.command_executor = command_executor

    def listen_and_execute(self) -> str:
        text = self.recognizer.listen()

        command = self.parser.parse(text)

        return self.command_executor.execute(command)