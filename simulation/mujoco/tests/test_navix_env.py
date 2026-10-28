import numpy as np
from stable_baselines3.common.env_checker import check_env

from simulation.mujoco.environments.navix_env import NavixEnv


def test_env_passes_sb3_check():
    check_env(NavixEnv(), warn=True)


def test_reset_and_step_shapes():
    env = NavixEnv()
    obs, _ = env.reset(seed=0)
    assert obs.shape == (21,)
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    assert obs.shape == (21,)
    assert np.isfinite(obs).all()
    assert np.isfinite(reward)


def test_episode_ends():
    env = NavixEnv(max_steps=50)
    env.reset(seed=0)
    for _ in range(60):
        _, _, terminated, truncated, _ = env.step(env.action_space.sample())
        if terminated or truncated:
            return
    raise AssertionError("episode never ended")
