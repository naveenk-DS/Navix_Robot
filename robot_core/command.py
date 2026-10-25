from dataclasses import dataclass
from enum import Enum


class CommandType(Enum):
    MOVE_FORWARD = "move_forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"
    NAVIGATE = "navigate"


@dataclass(frozen=True)
class RobotCommand:
    command_type: CommandType
    value: float = 0.0
    target_x: float = 0.0
    target_y: float = 0.0