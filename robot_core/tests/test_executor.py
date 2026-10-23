from robot_core.actions import Action, ActionType
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker


def create_executor() -> ActionExecutor:
    return ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
    )


def test_move_forward_execution(capsys):
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    result = executor.execute(action)

    captured = capsys.readouterr()

    assert result.success is True
    assert result.message == "Moving forward 1.0 meter(s)."
    assert captured.out == "[SIMULATION] Moving forward 1.0 meter(s).\n"


def test_stop_execution(capsys):
    executor = create_executor()

    action = Action(
        action_type=ActionType.STOP,
    )

    result = executor.execute(action)

    captured = capsys.readouterr()

    assert result.success is True
    assert result.message == "Robot stopped."
    assert captured.out == "[SIMULATION] Robot stopped.\n"


def test_invalid_move_distance():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=0,
    )

    result = executor.execute(action)

    assert result.success is False
    assert result.message == "Move distance must be greater than zero."


def test_unsafe_large_move_does_not_reach_motion():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=3.0,
    )

    result = executor.execute(action)

    assert result.success is False
    assert result.message == (
        "Move distance exceeds the safety limit of 2.0 meters."
    )