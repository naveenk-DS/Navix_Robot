from robot_core.command import CommandType, RobotCommand


def test_move_command():
    command = RobotCommand(
        command_type=CommandType.MOVE_FORWARD,
        value=1.0,
    )

    assert command.command_type == CommandType.MOVE_FORWARD
    assert command.value == 1.0


def test_navigation_command():
    command = RobotCommand(
        command_type=CommandType.NAVIGATE,
        target_x=3.0,
        target_y=2.0,
    )

    assert command.command_type == CommandType.NAVIGATE
    assert command.target_x == 3.0
    assert command.target_y == 2.0