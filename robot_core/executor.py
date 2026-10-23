from dataclasses import dataclass

from robot_core.actions import Action, ActionType


@dataclass
class ExecutionResult:
    success: bool
    message: str


class ActionExecutor:
    def execute(self, action: Action) -> ExecutionResult:
        if action.action_type == ActionType.MOVE_FORWARD:
            if action.value <= 0:
                return ExecutionResult(
                    success=False,
                    message="Move distance must be greater than zero.",
                )

            return ExecutionResult(
                success=True,
                message=f"Moving forward {action.value} meter(s).",
            )

        if action.action_type == ActionType.STOP:
            return ExecutionResult(
                success=True,
                message="Robot stopped.",
            )

        return ExecutionResult(
            success=False,
            message="Unsupported action.",
        )
