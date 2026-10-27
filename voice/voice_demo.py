
from robot_core.command_executor import CommandExecutor
from robot_core.command_parser import CommandParser
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState

from navigation.controller import NavigationController
from navigation.navigator import Navigator

from voice.voice_controller import VoiceController
from voice.whisper_recognizer import WhisperSpeechRecognizer


def create_voice_controller() -> VoiceController:
    robot_state = RobotState()

    safety_checker = SafetyChecker()
    motion_controller = SimulatedMotionController()

    action_executor = ActionExecutor(
        safety_checker=safety_checker,
        motion_controller=motion_controller,
        robot_state=robot_state,
    )

    navigator = Navigator(action_executor)
    navigation_controller = NavigationController(navigator)

    command_parser = CommandParser()

    command_executor = CommandExecutor(
        action_executor=action_executor,
        navigation_controller=navigation_controller,
    )

    recognizer = WhisperSpeechRecognizer(
        model_size="tiny",
        device="cpu",
        compute_type="int8",
    )

    return VoiceController(
        recognizer=recognizer,
        parser=command_parser,
        command_executor=command_executor,
    )


def main() -> None:
    controller = create_voice_controller()

    print("NAVIX Real Voice Demo")
    print("Speak a command into your microphone.")
    print()
    print("Examples:")
    print('  "Navix, move forward 1 meter."')
    print('  "Navix, turn left 90 degrees."')
    print('  "Navix, turn right 45 degrees."')
    print('  "Navix, stop."')
    print()
    print("Press Ctrl+C to exit.")

    while True:
        try:
            print("\nListening...")

            result = controller.listen_and_execute()

            print("NAVIX:", result)

        except KeyboardInterrupt:
            print("\nExiting NAVIX Voice Demo.")
            break

        except ValueError as error:
            print("NAVIX command error:", error)

        except Exception as error:
            print("NAVIX voice error:", error)


if __name__ == "__main__":
    main()