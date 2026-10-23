from robot_core.actions import Action, ActionType
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState


def create_executor() -> ActionExecutor:
    return ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
        robot_state=RobotState(),
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

def test_move_updates_robot_state():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.status.value == "moving"
    assert executor.robot_state.position_x == 1.0


def test_stop_updates_robot_state():
    executor = create_executor()

    action = Action(
        action_type=ActionType.STOP,
    )

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.status.value == "stopped"


def test_unsafe_move_does_not_update_robot_state():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=3.0,
    )

    result = executor.execute(action)

    assert result.success is False
    assert executor.robot_state.status.value == "idle"
    assert executor.robot_state.position_x == 0.0


def test_move_forward_heading_zero():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    executor.robot_state.heading = 0.0

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.position_x == 1.0
    assert round(executor.robot_state.position_y, 10) == 0.0


def test_move_forward_heading_90():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    executor.robot_state.heading = 90.0

    result = executor.execute(action)

    assert result.success is True
    assert round(executor.robot_state.position_x, 10) == 0.0
    assert executor.robot_state.position_y == 1.0


def test_move_forward_heading_180():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    executor.robot_state.heading = 180.0

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.position_x == -1.0
    assert round(executor.robot_state.position_y, 10) == 0.0


def test_move_forward_heading_270():
    executor = create_executor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    executor.robot_state.heading = 270.0

    result = executor.execute(action)

    assert result.success is True
    assert round(executor.robot_state.position_x, 10) == 0.0
    assert executor.robot_state.position_y == -1.0

def test_turn_left_updates_heading():
    executor = create_executor()

    action = Action(
        action_type=ActionType.TURN_LEFT,
        value=15.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert result.message == "Turned left 15.0 degree(s)."
    assert executor.robot_state.heading == 15.0


def test_turn_right_updates_heading():
    executor = create_executor()

    action = Action(
        action_type=ActionType.TURN_RIGHT,
        value=15.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert result.message == "Turned right 15.0 degree(s)."
    assert executor.robot_state.heading == 345.0


def test_turn_left_wraps_heading():
    executor = create_executor()

    executor.robot_state.heading = 350.0

    action = Action(
        action_type=ActionType.TURN_LEFT,
        value=15.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.heading == 5.0


def test_turn_right_wraps_heading():
    executor = create_executor()

    executor.robot_state.heading = 5.0

    action = Action(
        action_type=ActionType.TURN_RIGHT,
        value=15.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert executor.robot_state.heading == 350.0
