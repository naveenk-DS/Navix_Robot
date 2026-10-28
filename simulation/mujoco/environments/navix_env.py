"""NAVIX Gymnasium environment (MuJoCo) - first task: stay upright."""
from pathlib import Path

import gymnasium as gym
import mujoco
import numpy as np
from gymnasium import spaces

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "navix_robot.xml"

JOINTS = ["left_hip", "left_knee", "left_ankle",
          "right_hip", "right_knee", "right_ankle"]


class NavixEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, frame_skip=10, max_steps=500,
                 min_height=0.6, min_upright=0.7,
                 model_path=None, start_height=1.1, stand_height=1.1):
        super().__init__()
        self.start_height = start_height
        self.stand_height = stand_height
        self.model = mujoco.MjModel.from_xml_path(str(model_path or MODEL_PATH))
        self.data = mujoco.MjData(self.model)

        self.frame_skip = frame_skip
        self.max_steps = max_steps
        self.min_height = min_height      # torso height below this = fallen
        self.min_upright = min_upright    # cos(tilt); 0.7 is about 45 degrees
        self.steps = 0

        self._torso_id = self.model.body("torso").id
        self._jpos = self._sensor_slice([f"{j}_position" for j in JOINTS])
        self._jvel = self._sensor_slice([f"{j}_velocity" for j in JOINTS])
        self._gyro = self._sensor_slice(["torso_gyro"])
        self._accel = self._sensor_slice(["torso_acceleration"])

        n_act = self.model.nu  # 6 motors
        self.action_space = spaces.Box(-1.0, 1.0, shape=(n_act,), dtype=np.float32)
        # 6 pos + 6 vel + 3 gravity-in-body + 3 gyro + 3 accel = 21
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(21,), dtype=np.float32)

    def _sensor_slice(self, names):
        idx = []
        for n in names:
            s = self.model.sensor(n)
            adr = int(np.ravel(s.adr)[0])
            dim = int(np.ravel(s.dim)[0])
            idx.extend(range(adr, adr + dim))
        return np.array(idx)

    def _rot(self):
        return self.data.xmat[self._torso_id].reshape(3, 3)

    def _upright(self):
        return float(self._rot()[2, 2])  # 1 = perfectly upright

    def _obs(self):
        sd = self.data.sensordata
        gravity_body = -self._rot()[2, :]  # world gravity direction in body frame
        return np.concatenate([
            sd[self._jpos], sd[self._jvel], gravity_body,
            sd[self._gyro], sd[self._accel],
        ]).astype(np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[2] = self.start_height
        self.data.qpos[7:] += self.np_random.uniform(-0.02, 0.02, size=self.model.nq - 7)
        mujoco.mj_forward(self.model, self.data)
        self.steps = 0
        return self._obs(), {}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0)
        self.data.ctrl[:] = action
        mujoco.mj_step(self.model, self.data, nstep=self.frame_skip)
        self.steps += 1

        height = float(self.data.xpos[self._torso_id][2])
        upright = self._upright()
        fallen = height < self.min_height or upright < self.min_upright

        # Reward: alive bonus + uprightness - small energy / motion penalties
        reward = 1.0 + 1.0 * upright
        reward += 2.0 * float(np.exp(-20.0 * (1.0 - min(height / self.stand_height, 1.0)) ** 2))
        reward -= 0.01 * float(np.sum(np.square(action)))
        reward -= 3.0 * float(np.mean(np.square(self.data.qpos[7:])))  # stay near straight legs
        reward -= 0.05 * float(np.linalg.norm(self.data.qvel[:2]))
        if fallen:
            reward -= 5.0

        truncated = self.steps >= self.max_steps
        info = {"height": height, "upright": upright}
        return self._obs(), reward, fallen, truncated, info


SMALL_MODEL = Path(__file__).resolve().parents[1] / "models" / "navix_robot_small.xml"


def make_small_env(**kw):
    return NavixEnv(model_path=SMALL_MODEL, start_height=0.215,
                    stand_height=0.21, min_height=0.12, **kw)
