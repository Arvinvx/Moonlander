import os
import shutil

dll_dir = os.path.dirname(shutil.which("g++"))
handle = os.add_dll_directory(dll_dir)

from lander_env import LanderEnv 
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

env = LanderEnv()

# Check that Gymnasium can use our rocket
check_env(env)
print("ENVIRONMENT CHECK PASSED")


model = PPO.load("model/lander-v2", env=env, device="cpu")

model.learn(total_timesteps=100_000)

model.save("model/lander-v2.1")

print("TRAINING COMPLETE")
env.close()
