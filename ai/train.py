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

# Create a NEW PPO model from scratch
model = PPO("MlpPolicy", env, verbose=1, device="cpu")
  
# Train with our new reward system
model.learn(total_timesteps=200_000)

# Save separately from the previous models
model.save("ai/ppo_lander_v1_reward_v2.zip")

print("TRAINING COMPLETE")
env.close()
