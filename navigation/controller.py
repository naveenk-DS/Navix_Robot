from navigation.navigator import Navigator
from navigation.target import NavigationTarget


class NavigationController:
    def __init__(self, navigator: Navigator) -> None:
        self.navigator = navigator

    def navigate_to(
        self,
        target: NavigationTarget,
        max_steps: int = 100,
    ) -> str:
        for _ in range(max_steps):
            message = self.navigator.navigate_to_target(target)

            if message == "Target reached.":
                return message

        return "Navigation stopped: maximum steps reached."
