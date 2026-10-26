from navigation.controller import NavigationController
from navigation.navigator import Navigator
from robot_core.command_executor import CommandExecutor
from robot_core.command_parser import CommandParser
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState
from voice.interface import SpeechRecognizer
from voice.voice_controller import VoiceController


class FakeSpeechRecognizer(SpeechRecognizer):
    def __init__(self, text: str) -> None:
        self.text = text

    def listen(self) -> str:
        return self.text


def create_voice_controller(
    command: str,
) -> VoiceController:
    state = RobotState()

    action_executor = ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
        robot_state=state,
    )

    navigator = Navigator(action_executor)

    navigation_controller = NavigationController(
        navigator
    )

    command_executor = CommandExecutor(
        action_executor=action_executor,
        navigation_controller=navigation_controller,
    )

    return VoiceController(
        recognizer=FakeSpeechRecognizer(command),
        parser=CommandParser(),
        command_executor=command_executor,
    )


def test_voice_forward_command():
    controller = create_voice_controller(
        "forward 1"
    )

    message = controller.listen_and_execute()

    assert message == "Moving forward 1.0 meter(s)."


def test_voice_stop_command():
    controller = create_voice_controller(
        "stop"
    )

    message = controller.listen_and_execute()

    assert message == "Robot stopped."


def test_voice_navigation_command():
    controller = create_voice_controller(
        "go 1 0"
    )

    message = controller.listen_and_execute()

    assert message == "Target reached."