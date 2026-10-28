from pathlib import Path

import mujoco

from simulation.mujoco.joint_controller import (
    MuJoCoJointController,
)


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "navix_robot.xml"
)


def test_joint_controller():
    model = mujoco.MjModel.from_xml_path(
        str(MODEL_PATH)
    )

    data = mujoco.MjData(model)

    controller = MuJoCoJointController(
        model=model,
        data=data,
    )

    controller.set_joint_target(
        "left_hip",
        0.5,
    )

    left_hip_motor_id = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_ACTUATOR,
        "left_hip_motor",
    )

    assert data.ctrl[left_hip_motor_id] != 0.0

    controller.stop()

    assert all(value == 0.0 for value in data.ctrl)