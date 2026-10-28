from __future__ import annotations

import time

import mujoco
import mujoco.viewer

from simulation.mujoco.balance_controller import BalanceController


MODEL_PATH = "simulation/mujoco/models/navix_robot.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    controller = BalanceController(
        model,
        data,
        kp_balance=0.8,
    )

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            controller.update()

            mujoco.mj_step(model, data)

            viewer.sync()

            time.sleep(model.opt.timestep)

    controller.stop()


if __name__ == "__main__":
    main()