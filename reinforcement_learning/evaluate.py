"""Evaluate a trained NAVIX PPO policy: survival, height, drift."""
import argparse

import numpy as np
from stable_baselines3 import PPO

from simulation.mujoco.environments.navix_env import NavixEnv, make_small_env


def evaluate(path, episodes=20, push=0.0, small=False):
    model = PPO.load(path, device="cpu")
    env = make_small_env(max_steps=500) if small else NavixEnv(max_steps=500)
    lengths, heights, drifts = [], [], []
    for ep in range(episodes):
        obs, _ = env.reset(seed=ep)
        h = []
        for t in range(500):
            if push and t == 100:           # optional sideways shove
                env.data.qvel[1] += push
            action, _ = model.predict(obs, deterministic=True)
            obs, _, terminated, truncated, info = env.step(action)
            h.append(info["height"])
            if terminated or truncated:
                break
        lengths.append(t + 1)
        heights.append(np.mean(h[-100:]))
        drifts.append(float(np.linalg.norm(env.data.qpos[:2])))
    print(f"episodes:        {episodes}")
    print(f"mean length:     {np.mean(lengths):.0f} / 500")
    print(f"survived full:   {sum(l >= 500 for l in lengths)} / {episodes}")
    print(f"final height:    {np.mean(heights):.2f} m (min {np.min(heights):.2f})")
    print(f"drift from start:{np.mean(drifts):.2f} m")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="runs/navix_ppo")
    ap.add_argument("--small", action="store_true")
    ap.add_argument("--push", type=float, default=0.0)
    a = ap.parse_args()
    evaluate(a.path, push=a.push, small=a.small)
