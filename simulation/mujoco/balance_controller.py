from __future__ import annotations

import mujoco

from simulation.mujoco.orientation import quaternion_to_pitch
from simulation.mujoco.joint_controller import MuJoCoJointController


class BalanceController:
    """Simple pitch-based balance controller for NAVIX."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        kp_balance: float = 0.8,
    ) -> None:
        self.model = model
        self.data = data
        self.kp_balance = kp_balance

        self.joint_controller = MuJoCoJointController(
            model,
            data,
            kp=20.0,
            kd=2.0,
        )

        self.orientation_sensor_id = mujoco.mj_name2id(
            model,
            mujoco.mjtObj.mjOBJ_SENSOR,
            "torso_orientation",
        )

        if self.orientation_sensor_id < 0:
            raise ValueError("Missing torso_orientation sensor")

    def get_pitch(self) -> float:
        """Return torso pitch angle in degrees."""

        sensor_adr = self.model.sensor_adr[self.orientation_sensor_id]

        quaternion = self.data.sensordata[
            sensor_adr : sensor_adr + 4
        ]

        return quaternion_to_pitch(quaternion.tolist())

    def update(self) -> float:
        """Apply a simple correction based on torso pitch."""

        pitch = self.get_pitch()

        correction = -self.kp_balance * pitch

        # Apply correction to both hip joints.
        self.joint_controller.set_joint_target(
            "left_hip",
            correction,
        )

        self.joint_controller.set_joint_target(
            "right_hip",
            correction,
        )

        return pitch

    def stop(self) -> None:
        self.joint_controller.stop()