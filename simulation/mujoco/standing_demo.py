from pathlib import Path
import time

import mujoco
import mujoco.viewer

from simulation.mujoco.joint_controller import (
    MuJoCoJointController,
)


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "navix_robot.xml"
)


def main() -> None:
    model = mujoco.MjModel.from_xml_path(
        str(MODEL_PATH)
    )
    data = mujoco.MjData(model)

    controller = MuJoCoJointController(
        model=model,
        data=data,
        kp=20.0,
        kd=2.0,
    )

    # Initial standing pose.
    standing_pose = {
        "left_hip": 0.0,
        "left_knee": 0.0,
        "left_ankle": 0.0,
        "right_hip": 0.0,
        "right_knee": 0.0,
        "right_ankle": 0.0,
    }

    with mujoco.viewer.launch_passive(
        model,
        data,
    ) as viewer:

        while viewer.is_running():

            for joint_name, target in standing_pose.items():
                controller.set_joint_target(
                    joint_name,
                    target,
                )

            mujoco.mj_step(model, data)

            viewer.sync()

            time.sleep(0.002)

        controller.stop()


if __name__ == "__main__":
    main()