import math

import pygame

from robot_core.actions import Action, ActionType
from robot_core.executor import ActionExecutor
from robot_core.motion import SimulatedMotionController
from robot_core.safety import SafetyChecker
from robot_core.state import RobotState


WIDTH = 1000
HEIGHT = 700

SCALE = 80
GRID_SIZE = 1.0

BACKGROUND = (25, 25, 25)
GRID_COLOR = (55, 55, 55)
ROBOT_COLOR = (80, 200, 120)
TEXT_COLOR = (230, 230, 230)


def world_to_screen(x: float, y: float) -> tuple[int, int]:
    screen_x = int(WIDTH / 2 + x * SCALE)
    screen_y = int(HEIGHT / 2 - y * SCALE)

    return screen_x, screen_y


def draw_grid(screen: pygame.Surface) -> None:
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    for x in range(0, WIDTH, SCALE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, HEIGHT),
        )

    for y in range(0, HEIGHT, SCALE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y),
        )

    pygame.draw.line(
        screen,
        (100, 100, 100),
        (center_x, 0),
        (center_x, HEIGHT),
        2,
    )

    pygame.draw.line(
        screen,
        (100, 100, 100),
        (0, center_y),
        (WIDTH, center_y),
        2,
    )


def draw_robot(
    screen: pygame.Surface,
    state: RobotState,
) -> None:
    center_x, center_y = world_to_screen(
        state.position_x,
        state.position_y,
    )

    angle = math.radians(-state.heading)

    tip_length = 35
    side_length = 25

    tip = (
        center_x + math.cos(angle) * tip_length,
        center_y + math.sin(angle) * tip_length,
    )

    left_angle = angle + math.radians(140)
    right_angle = angle - math.radians(140)

    left = (
        center_x + math.cos(left_angle) * side_length,
        center_y + math.sin(left_angle) * side_length,
    )

    right = (
        center_x + math.cos(right_angle) * side_length,
        center_y + math.sin(right_angle) * side_length,
    )

    pygame.draw.polygon(
        screen,
        ROBOT_COLOR,
        [tip, left, right],
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (center_x, center_y),
        4,
    )


def draw_hud(
    screen: pygame.Surface,
    state: RobotState,
    font: pygame.font.Font,
) -> None:
    lines = [
        "NAVIX 2D SIMULATOR",
        "",
        f"Status : {state.status.value}",
        f"X      : {state.position_x:.2f} m",
        f"Y      : {state.position_y:.2f} m",
        f"Heading: {state.heading:.1f}°",
        "",
        "W / UP    Move forward",
        "A / LEFT  Turn left",
        "D / RIGHT Turn right",
        "SPACE     Stop",
        "R         Reset",
        "ESC       Exit",
    ]

    y = 20

    for line in lines:
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (20, y))
        y += 25


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NAVIX Robot - 2D Simulator")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    robot_state = RobotState()

    executor = ActionExecutor(
        safety_checker=SafetyChecker(),
        motion_controller=SimulatedMotionController(),
        robot_state=robot_state,
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    action = Action(
                        action_type=ActionType.MOVE_FORWARD,
                        value=0.1,
                    )

                    executor.execute(action)

                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    action = Action(
                        action_type=ActionType.TURN_LEFT,
                        value=15.0,
                    )

                    executor.execute(action)

                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    action = Action(
                        action_type=ActionType.TURN_RIGHT,
                        value=15.0,
                    )

                    executor.execute(action)

                elif event.key == pygame.K_SPACE:
                    action = Action(
                        action_type=ActionType.STOP,
                    )

                    executor.execute(action)

                elif event.key == pygame.K_r:
                    robot_state = RobotState()

                    executor = ActionExecutor(
                        safety_checker=SafetyChecker(),
                        motion_controller=SimulatedMotionController(),
                        robot_state=robot_state,
                    )

        screen.fill(BACKGROUND)

        draw_grid(screen)
        draw_robot(screen, robot_state)
        draw_hud(screen, robot_state, font)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()