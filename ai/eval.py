import os
import shutil
import numpy as np

# Load the C++ dependencies
dll_dir = os.path.dirname(shutil.which("g++"))
handle = os.add_dll_directory(dll_dir)

import lander_cpp
from lander_env import LanderEnv
from stable_baselines3 import PPO

# TEST = 1 -> PPO picks the action (shows what the policy outputs)
# TEST = 2 -> force full throttle (checks whether the C++ engine brakes)
TEST = 2
N_EPISODES = 1

# Load our trained AI
env = LanderEnv()
model = PPO.load("ai/ppo_lander_v1_reward_v3.zip", device="cpu")

successes = 0
crashes = 0
timeouts = 0
total_rewards = []


for i in range(N_EPISODES):
    observation, info = env.reset()
    done = False
    episode_reward = 0.0

    while not done:
        action, _ = model.predict(observation, deterministic=False)
        print("AI throttle:", action.item())

        if TEST == 2:
            action = np.array([1.0], dtype=np.float32)

        observation, reward, terminated, truncated, info = env.step(action)

        if TEST == 2:
            print("Velocity:", observation[1])

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
print(f"Total attempts: {N_EPISODES}")
print(f"Successful landings: {successes}")
print(f"Crashes: {crashes}")
print(f"Timeouts: {timeouts}")
print(f"Success rate: {successes/N_EPISODES*100:.2f}%")
print(f"Average reward: {sum(total_rewards)/N_EPISODES:.2f}")

env.close()