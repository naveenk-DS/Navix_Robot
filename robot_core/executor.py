from dataclasses import dataclass

from robot_core.actions import Action, ActionType
from robot_core.motion import MotionController
from robot_core.safety import SafetyChecker


@dataclass
class ExecutionResult:
    success: bool
    message: str


class ActionExecutor:
    def __init__(
        self,
        safety_checker: SafetyChecker,
        motion_controller: MotionController,
    ) -> None:
        self.safety_checker = safety_checker
        self.motion_controller = motion_controller

    def execute(self, action: Action) -> ExecutionResult:
        allowed, safety_message = self.safety_checker.validate(action)

        if not allowed:
            return ExecutionResult(
                success=False,
                message=safety_message,
            )

        if action.action_type == ActionType.MOVE_FORWARD:
            self.motion_controller.move_forward(action.value)

            return ExecutionResult(
                success=True,
                message=f"Moving forward {action.value} meter(s).",
            )

        if action.action_type == ActionType.STOP:
            self.motion_controller.stop()

            return ExecutionResult(
                success=True,
                message="Robot stopped.",
            )

        return ExecutionResult(
            success=False,
            message="Unsupported action.",
        )