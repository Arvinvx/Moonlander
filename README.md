# Lunar Moon Landing

A lunar lander simulation with a reinforcement learning agent that learns to control the engine throttle.

I'm building this project to learn how C++ physics, Python, and reinforcement learning work together. It is still in development, and I am experimenting with the reward function and training settings.

## How it works

The simulator models vertical movement under lunar gravity. The agent reads three values: altitude, vertical velocity, and remaining fuel. It then chooses a throttle value between `0` and `1`.

- **C++** handles movement, fuel use, and landing status.
- **pybind11** makes the C++ simulator available in Python.
- **Gymnasium** connects the simulator to the training algorithm.
- **PPO**, from Stable-Baselines3, learns the throttle policy using rewards.

The reward function is in `ai/reward.py`.

## Project structure

```text
.
├── ai/
│   ├── train.py                # PPO training
│   ├── eval.py                 # Model evaluation
│   ├── lander_env.py           # Gymnasium environment
│   ├── reward.py               # Reward rules
│   └── lander_cpp.pyd          # Compiled Windows extension
├── cpp/
│   ├── Lander.h                # Simulator interface
│   ├── Lander.cpp              # Physics and landing logic
│   ├── bindings.cpp            # Python bindings
│   └── main.cpp                # Standalone C++ example
├── model/
│   └── ppo_lander_v1_reward_v5.zip
├── experiments/
│   └── legacy_mlp_agent.py     # Early MLP experiment
├── assets/
│   └── image.png
├── .gitignore
└── README.md
```

The script in `experiments/` is an older experiment. It may need changes to work with the current code.

## Setup

The current scripts use Windows DLL loading and expect `g++` on `PATH`.

Install the Python dependencies:

```bash
python -m pip install numpy gymnasium stable-baselines3 pybind11
```

You also need the `lander_cpp` extension. The included `ai/lander_cpp.pyd` must match your Python version, system architecture, and compiler runtime. If it does not, you will need to rebuild it from the C++ sources. Build instructions are still being documented.

Run the following commands from the repository root.

## Evaluate the model

```bash
python ai/eval.py
```

This loads `model/ppo_lander_v1_reward_v5.zip` and runs 100 episodes. It reports landings, crashes, timeouts, success rate, and average reward.

Actions are sampled from the policy, so results can vary. All episodes use the same starting conditions.

## Train a model

```bash
python ai/train.py
```

The script trains a new PPO agent with `MlpPolicy` on the CPU for about 200,000 timesteps. It saves to `model/ppo_lander_v1_reward_v5.zip`, replacing the existing checkpoint.

## Environment

| Setting | Current value |
|---|---|
| Starting altitude | 1,000 m |
| Starting vertical velocity | -10 m/s |
| Starting fuel | 500 units |
| Throttle range | 0 to 1 |
| Time per step | 1 second |
| Episode limit | 300 steps |

Negative velocity means downward movement. Ground contact below -5 m/s is counted as a crash.

Before reaching the agent, altitude is divided by 1,000, velocity by 100, and fuel by 500. This keeps the input values closer in scale.

## Current state

The v5 checkpoint is experimental. A confirmed success rate has not been recorded yet.

The simulator uses constant gravity and mass. It currently supports vertical movement only. The next steps are improving the reward function, recording evaluation results, and testing different starting conditions.
