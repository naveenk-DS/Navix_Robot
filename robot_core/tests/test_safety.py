from robot_core.actions import Action, ActionType
from robot_core.safety import SafetyChecker


def test_safe_move():
    checker = SafetyChecker()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    allowed, message = checker.validate(action)

    assert allowed is True
    assert message == "Action allowed."


def test_zero_distance_rejected():
    checker = SafetyChecker()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=0,
    )

    allowed, message = checker.validate(action)

    assert allowed is False


def test_large_distance_rejected():
    checker = SafetyChecker()

    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=3.0,
    )

    allowed, message = checker.validate(action)

    assert allowed is False


def test_stop_always_allowed():
    checker = SafetyChecker()

    action = Action(
        action_type=ActionType.STOP,
    )

    allowed, message = checker.validate(action)

    assert allowed is True
