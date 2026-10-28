from pathlib import Path
import time

import mujoco
import mujoco.viewer


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

    orientation_sensor = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_SENSOR,
        "torso_orientation",
    )

    orientation_address = model.sensor_adr[
        orientation_sensor
    ]

    with mujoco.viewer.launch_passive(
        model,
        data,
    ) as viewer:

        last_print = 0.0

        while viewer.is_running():

            mujoco.mj_step(model, data)

            current_time = data.time

            if current_time - last_print >= 0.5:

                quat = data.sensordata[
                    orientation_address:
                    orientation_address + 4
                ]

                print(
                    f"time={current_time:.2f} "
                    f"torso_quaternion={quat}"
                )

                last_print = current_time

            viewer.sync()

            time.sleep(0.002)


if __name__ == "__main__":
    main()