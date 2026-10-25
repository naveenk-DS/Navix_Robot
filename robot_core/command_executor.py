from navigation.controller import NavigationController
from navigation.target import NavigationTarget
from robot_core.actions import Action, ActionType
from robot_core.command import CommandType, RobotCommand
from robot_core.executor import ExecutionResult


class CommandExecutor:
    def __init__(
        self,
        action_executor,
        navigation_controller: NavigationController,
    ) -> None:
        self.action_executor = action_executor
        self.navigation_controller = navigation_controller

    def execute(self, command: RobotCommand) -> str:
        if command.command_type == CommandType.MOVE_FORWARD:
            result = self.action_executor.execute(
                Action(
                    action_type=ActionType.MOVE_FORWARD,
                    value=command.value,
                )
            )

            return result.message

        if command.command_type == CommandType.TURN_LEFT:
            result = self.action_executor.execute(
                Action(
                    action_type=ActionType.TURN_LEFT,
                    value=command.value,
                )
            )

            return result.message

        if command.command_type == CommandType.TURN_RIGHT:
            result = self.action_executor.execute(
                Action(
                    action_type=ActionType.TURN_RIGHT,
                    value=command.value,
                )
            )

            return result.message

        if command.command_type == CommandType.STOP:
            result = self.action_executor.execute(
                Action(
                    action_type=ActionType.STOP,
                )
            )

            return result.message

        if command.command_type == CommandType.NAVIGATE:
            target = NavigationTarget(
                x=command.target_x,
                y=command.target_y,
            )

            return self.navigation_controller.navigate_to(
                target=target,
            )

        return "Unsupported command."