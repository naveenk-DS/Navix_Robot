from navigation.controller import NavigationController
from navigation.navigator import Navigator
from robot_core.actions import ActionType
from robot_core.command import CommandType, RobotCommand
from robot_core.command_executor import CommandExecutor
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState


def create_command_executor() -> CommandExecutor:
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

    return CommandExecutor(
        action_executor=action_executor,
        navigation_controller=navigation_controller,
    )


def test_execute_forward_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.MOVE_FORWARD,
        value=1.0,
    )

    message = executor.execute(command)

    assert message == "Moving forward 1.0 meter(s)."


def test_execute_left_turn_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.TURN_LEFT,
        value=90.0,
    )

    message = executor.execute(command)

    assert message == "Turned left 90.0 degree(s)."


def test_execute_right_turn_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.TURN_RIGHT,
        value=45.0,
    )

    message = executor.execute(command)

    assert message == "Turned right 45.0 degree(s)."


def test_execute_stop_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.STOP,
    )

    message = executor.execute(command)

    assert message == "Robot stopped."


def test_execute_navigation_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.NAVIGATE,
        target_x=1.0,
        target_y=0.0,
    )

    message = executor.execute(command)

    assert message == "Target reached."


def test_robot_state_changes_after_command():
    executor = create_command_executor()

    command = RobotCommand(
        command_type=CommandType.MOVE_FORWARD,
        value=1.0,
    )

    executor.execute(command)

    state = executor.action_executor.robot_state

    assert round(state.position_x, 2) == 1.0
    assert round(state.position_y, 2) == 0.0