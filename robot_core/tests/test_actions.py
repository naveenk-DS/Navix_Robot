from robot_core.actions import Action, ActionType


def test_move_forward():
    action = Action(
        action_type=ActionType.MOVE_FORWARD,
        value=1.0,
    )

    assert action.action_type == ActionType.MOVE_FORWARD
    assert action.value == 1.0


def test_stop():
    action = Action(
        action_type=ActionType.STOP,
    )

    assert action.action_type == ActionType.STOP
    assert action.value == 0.0
