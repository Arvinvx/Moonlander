import os
import shutil

# Load the C++ dependencies
dll_dir = os.path.dirname(shutil.which("g++"))
handle = os.add_dll_directory(dll_dir)

import lander_cpp
from lander_env import LanderEnv
from stable_baselines3 import PPO

# Load our trained AI
env = LanderEnv()
model = PPO.load("ppo_lander_v1.zip", device="cpu")

successes = 0
crashes = 0
timeouts = 0
total_rewards = []

# Test 100 landing attempts
for i in range(100):
    observation, info = env.reset()
    done = False
    episode_reward = 0.0

    while not done:
        action, _ = model.predict(observation, deterministic=False)

        observation, reward, terminated, truncated, info = env.step(action)

        episode_reward += reward
        done = terminated or truncated

    status = env.rocket.get_status()

    if status == lander_cpp.LanderStatus.LANDED:
        result = "LANDED"
        successes += 1
    elif status == lander_cpp.LanderStatus.CRASHED:
        result = "CRASHED"
        crashes += 1
    else:
        result = "TIMEOUT"
        timeouts += 1

    total_rewards.append(episode_reward)

    print(f"Episode {i+1}: {result} | Reward: {episode_reward:.2f}")

# Final research results
print("\n===== PPO V1 RESULTS =====")
print(f"Total attempts: 100")
print(f"Successful landings: {successes}")
print(f"Crashes: {crashes}")
print(f"Timeouts: {timeouts}")
print(f"Success rate: {successes}%")
print(f"Average reward: {sum(total_rewards)/100:.2f}")

env.close()