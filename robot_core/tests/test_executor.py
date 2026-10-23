from robot_core.actions import Action, ActionType
from robot_core.executor import ActionExecutor


def test_move_forward_execution():
    executor = ActionExecutor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    result = executor.execute(action)

    assert result.success is True
    assert result.message == "Moving forward 1.0 meter(s)."


def test_stop_execution():
    executor = ActionExecutor()

    action = Action(
        action_type=ActionType.STOP,
    )

    result = executor.execute(action)

    assert result.success is True
    assert result.message == "Robot stopped."


def test_invalid_move_distance():
    executor = ActionExecutor()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=0,
    )

    result = executor.execute(action)

    assert result.success is False
