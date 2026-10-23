from robot_core.actions import Action, ActionType


MAX_MOVE_DISTANCE = 2.0


class SafetyChecker:
    def validate(self, action: Action) -> tuple[bool, str]:
        if action.action_type == ActionType.STOP:
            return True, "Action allowed."

        if action.action_type == ActionType.MOVE_FORWARD:
            if action.value <= 0:
                return False, "Move distance must be greater than zero."

            if action.value > MAX_MOVE_DISTANCE:
                return False, (
                    f"Move distance exceeds the safety limit of "
                    f"{MAX_MOVE_DISTANCE} meters."
                )

            return True, "Action allowed."

        return False, "Unsupported action."
