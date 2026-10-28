"""Train / watch a PPO policy on NavixEnv.

Train:  python -m reinforcement_learning.train_ppo --steps 1000000
Watch:  python -m reinforcement_learning.train_ppo --watch runs/navix_ppo
"""
import argparse
import time

import mujoco.viewer
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv

from simulation.mujoco.environments.navix_env import NavixEnv, make_small_env


def train(steps, save_path, small=False):
    env = make_vec_env(make_small_env if small else NavixEnv, n_envs=8, vec_env_cls=SubprocVecEnv)
    model = PPO("MlpPolicy", env, verbose=1, device="cpu",
                tensorboard_log="runs/tb")
    model.learn(total_timesteps=steps)
    model.save(save_path)
    print("Saved:", save_path)


def watch(path, small=False):
    model = PPO.load(path, device="cpu")
    env = make_small_env(max_steps=2000) if small else NavixEnv(max_steps=2000)
    obs, _ = env.reset()
    with mujoco.viewer.launch_passive(env.model, env.data) as viewer:
        while viewer.is_running():
            action, _ = model.predict(obs, deterministic=True)
            obs, _, terminated, truncated, _ = env.step(action)
            viewer.sync()
            time.sleep(0.02)
            if terminated or truncated:
                obs, _ = env.reset()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=1_000_000)
    ap.add_argument("--save", default="runs/navix_ppo")
    ap.add_argument("--small", action="store_true")
    ap.add_argument("--watch", default=None, help="path to saved model")
    args = ap.parse_args()
    watch(args.watch, args.small) if args.watch else train(args.steps, args.save, args.small)
