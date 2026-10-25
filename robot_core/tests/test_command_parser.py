import pytest

from robot_core.command import CommandType
from robot_core.command_parser import CommandParser


def test_parse_stop():
    parser = CommandParser()

    command = parser.parse("stop")

    assert command.command_type == CommandType.STOP


def test_parse_forward():
    parser = CommandParser()

    command = parser.parse("forward 1.5")

    assert command.command_type == CommandType.MOVE_FORWARD
    assert command.value == 1.5


def test_parse_turn_left():
    parser = CommandParser()

    command = parser.parse("turn left 90")

    assert command.command_type == CommandType.TURN_LEFT
    assert command.value == 90.0


def test_parse_turn_right():
    parser = CommandParser()

    command = parser.parse("turn right 45")

    assert command.command_type == CommandType.TURN_RIGHT
    assert command.value == 45.0


def test_parse_navigation():
    parser = CommandParser()

    command = parser.parse("go 3 2")

    assert command.command_type == CommandType.NAVIGATE
    assert command.target_x == 3.0
    assert command.target_y == 2.0


def test_parse_unsupported_command():
    parser = CommandParser()

    with pytest.raises(ValueError):
        parser.parse("dance")