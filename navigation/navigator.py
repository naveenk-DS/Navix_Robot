import math

from robot_core.actions import Action, ActionType
from robot_core.executor import ActionExecutor


POSITION_TOLERANCE = 0.05


class Navigator:
    def __init__(self, executor: ActionExecutor) -> None:
        self.executor = executor

    def distance_to_target(
        self,
        target_x: float,
        target_y: float,
    ) -> float:
        state = self.executor.robot_state

        dx = target_x - state.position_x
        dy = target_y - state.position_y

        return math.hypot(dx, dy)

    def angle_to_target(
        self,
        target_x: float,
        target_y: float,
    ) -> float:
        state = self.executor.robot_state

        dx = target_x - state.position_x
        dy = target_y - state.position_y

        angle = math.degrees(math.atan2(dy, dx))

        return angle % 360

    def is_target_reached(
        self,
        target_x: float,
        target_y: float,
    ) -> bool:
        return (
            self.distance_to_target(target_x, target_y)
            <= POSITION_TOLERANCE
        )

    def navigate_to(
        self,
        target_x: float,
        target_y: float,
    ) -> str:
        if self.is_target_reached(target_x, target_y):
            return "Target reached."

        target_angle = self.angle_to_target(
            target_x,
            target_y,
        )

        current_heading = self.executor.robot_state.heading

        turn_angle = (target_angle - current_heading + 180) % 360 - 180

        if abs(turn_angle) > 1.0:
            if turn_angle > 0:
                action = Action(
                    action_type=ActionType.TURN_LEFT,
                    value=abs(turn_angle),
                )
            else:
                action = Action(
                    action_type=ActionType.TURN_RIGHT,
                    value=abs(turn_angle),
                )

            result = self.executor.execute(action)

            if not result.success:
                return result.message

        distance = self.distance_to_target(
            target_x,
            target_y,
        )

        move_distance = min(distance, 2.0)

        action = Action(
            action_type=ActionType.MOVE_FORWARD,
            value=move_distance,
        )

        result = self.executor.execute(action)

        return result.message