# Lunar Moon Landing

This is a work in progress: a small lunar-lander simulation and a reinforcement-learning agent that is learning how to land it. The project is still being experimented on, so the reward rules, model files, and training setup may change.

## How it works

The lander physics are written in C++ in `cpp/`. `cpp/bindings.cpp` exposes the `Lander` class to Python as `lander_cpp`. The Python environment in `ai/lander_env.py` wraps that simulation in a Gymnasium interface with three observations: altitude, vertical velocity, and fuel. The agent controls engine throttle from 0 to 1.

Training uses PPO from Stable-Baselines3. `ai/reward.py` contains the current reward rules, which encourage a safe landing and penalize crashes, excessive descent speed, fuel use, and long flights. These rules are still being tuned.

## Running the experiments

The Python scripts expect the project dependencies to be installed, including Gymnasium, NumPy, Stable-Baselines3, and the `lander_cpp` extension. The extension is built from the C++ sources with pybind11; a compatible C++ compiler must also be available. On Windows, the scripts currently look for `g++` on `PATH` to locate its runtime DLLs.

From the repository root:

```bash
python ai/train.py
python ai/eval.py
```

Training saves a model under `ai/`. Evaluation currently loads `ai/ppo_lander_v1_reward_v3.zip` and runs 300 attempts. The checked-in model archives are snapshots from different experiments, not a final or guaranteed-performing agent.

## Current state

This repository is an experiment in progress. Training settings, reward shaping, model naming, and the native-extension build steps still need cleanup. Results should be treated as exploratory until they have been reproduced and compared consistently.
