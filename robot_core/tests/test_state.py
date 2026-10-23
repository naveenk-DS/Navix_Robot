from robot_core.state import RobotState, RobotStatus


def test_default_robot_state():
    state = RobotState()

    assert state.status == RobotStatus.IDLE
    assert state.position_x == 0.0
    assert state.position_y == 0.0
    assert state.heading == 0.0


def test_robot_state_position():
    state = RobotState(
        status=RobotStatus.MOVING,
        position_x=1.0,
        position_y=2.0,
        heading=90.0,
    )

    assert state.status == RobotStatus.MOVING
    assert state.position_x == 1.0
    assert state.position_y == 2.0
    assert state.heading == 90.0


def test_robot_stopped_state():
    state = RobotState(
        status=RobotStatus.STOPPED,
    )

    assert state.status == RobotStatus.STOPPED
    assert state.heading == 0.0


def test_robot_heading():
    state = RobotState(heading=180.0)

    assert state.heading == 180.0