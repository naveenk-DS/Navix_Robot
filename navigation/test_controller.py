from navigation.controller import NavigationController
from navigation.navigator import Navigator
from navigation.target import NavigationTarget

from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState


def create_controller() -> NavigationController:
    state = RobotState()

    executor = ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
        robot_state=state,
    )

    navigator = Navigator(executor)

    return NavigationController(navigator)


def test_navigation_controller_reaches_target():
    controller = create_controller()

    target = NavigationTarget(
        x=3.0,
        y=0.0,
    )

    message = controller.navigate_to(
        target=target,
        max_steps=10,
    )

    state = controller.navigator.executor.robot_state

    assert message == "Target reached."
    assert round(state.position_x, 2) == 3.0
    assert round(state.position_y, 2) == 0.0
