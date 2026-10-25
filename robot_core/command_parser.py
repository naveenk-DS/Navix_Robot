import re

from robot_core.command import CommandType, RobotCommand


class CommandParser:
    def parse(self, text: str) -> RobotCommand:
        command = text.strip().lower()

        if command == "stop":
            return RobotCommand(
                command_type=CommandType.STOP,
            )

        match = re.fullmatch(
            r"forward\s+([0-9]+(?:\.[0-9]+)?)",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.MOVE_FORWARD,
                value=float(match.group(1)),
            )

        match = re.fullmatch(
            r"turn\s+left\s+([0-9]+(?:\.[0-9]+)?)",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.TURN_LEFT,
                value=float(match.group(1)),
            )

        match = re.fullmatch(
            r"turn\s+right\s+([0-9]+(?:\.[0-9]+)?)",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.TURN_RIGHT,
                value=float(match.group(1)),
            )

        match = re.fullmatch(
            r"go\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.NAVIGATE,
                target_x=float(match.group(1)),
                target_y=float(match.group(2)),
            )

        raise ValueError(
            f"Unsupported command: {text}"
        )