from __future__ import annotations

import mujoco


class MuJoCoMotorController:
    """Controls NAVIX motors inside the MuJoCo simulation."""

    MOTOR_NAMES = (
        "left_hip_motor",
        "left_knee_motor",
        "left_ankle_motor",
        "right_hip_motor",
        "right_knee_motor",
        "right_ankle_motor",
    )

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
    ) -> None:
        self.model = model
        self.data = data

        self.motor_ids = {
            name: mujoco.mj_name2id(
                model,
                mujoco.mjtObj.mjOBJ_ACTUATOR,
                name,
            )
            for name in self.MOTOR_NAMES
        }

        missing = [
            name
            for name, motor_id in self.motor_ids.items()
            if motor_id < 0
        ]

        if missing:
            raise ValueError(
                f"Missing MuJoCo motors: {missing}"
            )

    def set_motor(self, motor_name: str, control: float) -> None:
        if motor_name not in self.motor_ids:
            raise ValueError(
                f"Unknown motor: {motor_name}"
            )

        motor_id = self.motor_ids[motor_name]

        # MuJoCo actuator control range is -1 to +1.
        control = max(-1.0, min(1.0, control))

        self.data.ctrl[motor_id] = control

    def set_all(self, controls: list[float]) -> None:
        if len(controls) != len(self.MOTOR_NAMES):
            raise ValueError(
                f"Expected {len(self.MOTOR_NAMES)} controls, "
                f"got {len(controls)}."
            )

        for name, control in zip(self.MOTOR_NAMES, controls):
            self.set_motor(name, control)

    def stop(self) -> None:
        self.data.ctrl[:] = 0.0