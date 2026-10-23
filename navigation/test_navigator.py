from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState

from navigation.navigator import Navigator
from navigation.target import NavigationTarget


def create_navigator() -> Navigator:
    state = RobotState()

    executor = ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
        robot_state=state,
    )

    return Navigator(executor)


def test_distance_to_target():
    navigator = create_navigator()

    distance = navigator.distance_to_target(
        target_x=3.0,
        target_y=4.0,
    )

    assert distance == 5.0


def test_angle_to_target():
    navigator = create_navigator()

    angle = navigator.angle_to_target(
        target_x=1.0,
        target_y=1.0,
    )

    assert round(angle, 2) == 45.0


def test_target_reached():
    navigator = create_navigator()

    assert navigator.is_target_reached(
        target_x=0.02,
        target_y=0.02,
    )


def test_target_not_reached():
    navigator = create_navigator()

    assert not navigator.is_target_reached(
        target_x=1.0,
        target_y=1.0,
    )


def test_navigate_to_target():
    navigator = create_navigator()

    message = navigator.navigate_to(
        target_x=1.0,
        target_y=0.0,
    )

    state = navigator.executor.robot_state

    assert message == "Moving forward 1.0 meter(s)."
    assert round(state.position_x, 2) == 1.0
    assert round(state.position_y, 2) == 0.0
    assert state.heading == 0.0

def test_navigation_target():
    target = NavigationTarget(
        x=3.0,
        y=2.0,
    )

    assert target.x == 3.0
    assert target.y == 2.0


def test_navigation_target():
    target = NavigationTarget(
        x=3.0,
        y=2.0,
    )

    assert target.x == 3.0
    assert target.y == 2.0


def test_navigate_to_target_object():
    navigator = create_navigator()

    target = NavigationTarget(
        x=1.0,
        y=0.0,
    )

    message = navigator.navigate_to_target(target)

    state = navigator.executor.robot_state

    assert message == "Moving forward 1.0 meter(s)."
    assert round(state.position_x, 2) == 1.0
    assert round(state.position_y, 2) == 0.0