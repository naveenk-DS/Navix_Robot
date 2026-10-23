from robot_core.actions import Action, ActionType


MAX_MOVE_DISTANCE = 2.0
MAX_TURN_ANGLE = 180.0


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

        if action.action_type in (
            ActionType.TURN_LEFT,
            ActionType.TURN_RIGHT,
        ):
            if action.value <= 0:
                return False, "Turn angle must be greater than zero."

            if action.value > MAX_TURN_ANGLE:
                return False, (
                    f"Turn angle exceeds the safety limit of "
                    f"{MAX_TURN_ANGLE} degrees."
                )

            return True, "Action allowed."

        return False, "Unsupported action."