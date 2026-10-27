import re

from robot_core.command import CommandType, RobotCommand


class CommandParser:
    def parse(self, text: str) -> RobotCommand:
        command = self._normalize(text)

        # STOP
        if command == "stop":
            return RobotCommand(
                command_type=CommandType.STOP,
            )

        # MOVE FORWARD
        match = re.fullmatch(
            r"(?:move\s+)?forward\s+([0-9]+(?:\.[0-9]+)?)"
            r"(?:\s+meters?)?",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.MOVE_FORWARD,
                value=float(match.group(1)),
            )

        # TURN LEFT
        match = re.fullmatch(
            r"turn\s+left\s+([0-9]+(?:\.[0-9]+)?)"
            r"(?:\s+degrees?)?",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.TURN_LEFT,
                value=float(match.group(1)),
            )

        # TURN RIGHT
        match = re.fullmatch(
            r"turn\s+right\s+([0-9]+(?:\.[0-9]+)?)"
            r"(?:\s+degrees?)?",
            command,
        )

        if match:
            return RobotCommand(
                command_type=CommandType.TURN_RIGHT,
                value=float(match.group(1)),
            )

        # NAVIGATE TO X Y
        match = re.fullmatch(
            r"go\s+([0-9]+(?:\.[0-9]+)?)"
            r"\s+([0-9]+(?:\.[0-9]+)?)",
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

    def _normalize(self, text: str) -> str:
        command = text.strip().lower()

        # Remove punctuation.
        command = re.sub(r"[,!?]", "", command)

        # Remove the NAVIX wake word/name.
        command = re.sub(r"^\s*navix[\s,:-]*", "", command)

        # Normalize multiple spaces.
        command = re.sub(r"\s+", " ", command)

        return command.strip()
