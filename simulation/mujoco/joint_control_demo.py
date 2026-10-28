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

    target_angle = 0.5

    with mujoco.viewer.launch_passive(
        model,
        data,
    ) as viewer:

        start_time = time.time()

        while viewer.is_running():

            elapsed = time.time() - start_time

            # Alternate between two target positions.
            if int(elapsed / 2.0) % 2 == 0:
                target = target_angle
            else:
                target = -target_angle

            controller.set_joint_target(
                "left_hip",
                target,
            )

            # Keep the remaining joints at zero.
            controller.set_joint_target(
                "left_knee",
                0.0,
            )

            controller.set_joint_target(
                "right_hip",
                0.0,
            )

            controller.set_joint_target(
                "right_knee",
                0.0,
            )

            mujoco.mj_step(model, data)

            viewer.sync()

            time.sleep(0.002)

        controller.stop()


if __name__ == "__main__":
    main()