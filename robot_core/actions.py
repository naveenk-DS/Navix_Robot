from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    MOVE_FORWARD = "move_forward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    STOP = "stop"


@dataclass
class Action:
    action_type: ActionType
    value: float = 0.0