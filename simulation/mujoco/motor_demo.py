from pathlib import Path
import time

import mujoco
import mujoco.viewer

from simulation.mujoco.motor_controller import (
    MuJoCoMotorController,
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

    controller = MuJoCoMotorController(
        model=model,
        data=data,
    )

    with mujoco.viewer.launch_passive(
        model,
        data,
    ) as viewer:

        start_time = time.time()

        while viewer.is_running():

            elapsed = time.time() - start_time

            # Move the left hip motor back and forth.
            control = 0.5 if int(elapsed * 2) % 2 == 0 else -0.5

            controller.set_motor(
                "left_hip_motor",
                control,
            )

            # Keep the other motors stopped.
            controller.set_motor(
                "left_knee_motor",
                0.0,
            )

            controller.set_motor(
                "right_hip_motor",
                0.0,
            )

            controller.set_motor(
                "right_knee_motor",
                0.0,
            )

            mujoco.mj_step(model, data)

            viewer.sync()

            time.sleep(0.002)

        controller.stop()


if __name__ == "__main__":
    main()