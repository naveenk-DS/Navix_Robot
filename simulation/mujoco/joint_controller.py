from __future__ import annotations

import mujoco


class MuJoCoJointController:
    """Simple PD position controller for NAVIX joints."""

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        kp: float = 20.0,
        kd: float = 2.0,
    ) -> None:
        self.model = model
        self.data = data
        self.kp = kp
        self.kd = kd

        self.joint_names = (
            "left_hip",
            "left_knee",
            "left_ankle",
            "right_hip",
            "right_knee",
            "right_ankle",
        )

        self.actuator_names = (
            "left_hip_motor",
            "left_knee_motor",
            "left_ankle_motor",
            "right_hip_motor",
            "right_knee_motor",
            "right_ankle_motor",
        )

        self.joint_ids = {
            name: mujoco.mj_name2id(
                model,
                mujoco.mjtObj.mjOBJ_JOINT,
                name,
            )
            for name in self.joint_names
        }

        self.actuator_ids = {
            name: mujoco.mj_name2id(
                model,
                mujoco.mjtObj.mjOBJ_ACTUATOR,
                name,
            )
            for name in self.actuator_names
        }

    def set_joint_target(
        self,
        joint_name: str,
        target_angle: float,
    ) -> None:
        if joint_name not in self.joint_ids:
            raise ValueError(
                f"Unknown joint: {joint_name}"
            )

        actuator_name = f"{joint_name}_motor"

        joint_id = self.joint_ids[joint_name]
        actuator_id = self.actuator_ids[actuator_name]

        qpos_address = self.model.jnt_qposadr[joint_id]
        dof_address = self.model.jnt_dofadr[joint_id]

        current_position = self.data.qpos[qpos_address]
        current_velocity = self.data.qvel[dof_address]

        position_error = (
            target_angle - current_position
        )

        velocity_error = -current_velocity

        torque = (
            self.kp * position_error
            + self.kd * velocity_error
        )

        gear = self.model.actuator_gear[
            actuator_id, 0
        ]

        if abs(gear) > 1e-8:
            control = torque / gear
        else:
            control = torque

        control_min = self.model.actuator_ctrlrange[
            actuator_id, 0
        ]

        control_max = self.model.actuator_ctrlrange[
            actuator_id, 1
        ]

        control = max(
            control_min,
            min(control_max, control),
        )

        self.data.ctrl[actuator_id] = control

    def stop(self) -> None:
        self.data.ctrl[:] = 0.0