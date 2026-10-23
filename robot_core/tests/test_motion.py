from robot_core.motion import SimulatedMotionController


def test_simulated_move_forward(capsys):
    controller = SimulatedMotionController()

    controller.move_forward(1.0)

    captured = capsys.readouterr()

    assert captured.out == "[SIMULATION] Moving forward 1.0 meter(s).\n"


def test_simulated_stop(capsys):
    controller = SimulatedMotionController()

    controller.stop()

    captured = capsys.readouterr()

    assert captured.out == "[SIMULATION] Robot stopped.\n"
