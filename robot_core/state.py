from dataclasses import dataclass
from enum import Enum


class RobotStatus(Enum):
    IDLE = "idle"
    MOVING = "moving"
    STOPPED = "stopped"


@dataclass
class RobotState:
    status: RobotStatus = RobotStatus.IDLE
    position_x: float = 0.0
    position_y: float = 0.0
