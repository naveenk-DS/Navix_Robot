from pathlib import Path

import mujoco

from simulation.mujoco.motor_controller import (
    MuJoCoMotorController,
)


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "navix_robot.xml"
)


def test_motor_controller():
    model = mujoco.MjModel.from_xml_path(
        str(MODEL_PATH)
    )
    data = mujoco.MjData(model)

    controller = MuJoCoMotorController(
        model=model,
        data=data,
    )

    controller.set_all([
        0.5,    # left hip
        -0.5,   # left knee
        0.25,   # left ankle
        -0.25,  # right hip
        0.3,    # right knee
        -0.2,   # right ankle
    ])

    assert data.ctrl[0] == 0.5
    assert data.ctrl[1] == -0.5
    assert data.ctrl[2] == 0.25
    assert data.ctrl[3] == -0.25
    assert data.ctrl[4] == 0.3
    assert data.ctrl[5] == -0.2

    controller.stop()

    assert all(value == 0.0 for value in data.ctrl)