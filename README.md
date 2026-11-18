# Moonlander

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

The script in `experiments/` is an older experiment. Its imports and reward call do not match the current code.

## Setup

The current scripts use Windows DLL loading and expect `g++` on `PATH`.

Install the Python dependencies:

```bash
python -m pip install numpy gymnasium stable-baselines3 pybind11
```

You also need the `lander_cpp` extension. The included `ai/lander_cpp.pyd` must match your Python version, system architecture, and compiler runtime. If it does not, you will need to rebuild it from the C++ sources. Build instructions are still being documented.

Run the following commands from the repository root. The scripts use relative paths for checkpoints.

## Evaluate the model

```bash
python ai/eval.py
```

The repository's evaluation script loads `model/ppo_lander_v1_reward_v5.zip` and runs 100 episodes on the CPU. It prints the throttle at each step, then reports landings, crashes, timeouts, success rate, and average reward.

The checkpoint path is set in the script's `PPO.load(...)` call. To evaluate a later checkpoint, set this path to its location. For example, use `model/lander-v2.zip` if you have placed a v2 checkpoint in `model/`.

With `TEST = 1`, actions are sampled from the policy using `deterministic=False`. Each episode also has random starting conditions and noise, so results can vary between runs. The script does not set a fixed seed.

`TEST = 2` replaces the policy action with full throttle to check engine braking. Environment noise still applies. This mode checks the simulator and should not be reported as the agent's performance.

## Train a model

```bash
python ai/train.py
```

The script first calls Gymnasium's environment checker, then loads `model/ppo_lander_v1_reward_v5.zip` and continues PPO training on the CPU for about 200,000 more timesteps. It uses the policy and settings stored in that checkpoint.

The output is `lander-v2.zip` in the repository root. Running training again uses the same v5 input and replaces that output file. It does not automatically resume from v2. To keep the output with the other checkpoints, move it into `model/` after training and use that path for evaluation.

## Environment

| Setting | Current value |
|---|---|
| Starting altitude | Random, 1,000 to 1,400 m |
| Starting vertical velocity | Random, -50 to -35 m/s |
| Lander mass | Random, 450 to 550 kg; constant during each episode |
| Starting fuel | 500 units |
| Maximum thrust | Random, 2,950 to 3,100 N |
| Lunar gravity | 1.62 m/s² |
| Fuel burn rate | 2 units per second at full throttle |
| Throttle range | 0 to 1 |
| Time per step | 1 second |
| Episode limit | 300 steps |

Negative velocity means downward movement. Ground contact below -5 m/s is counted as a crash.

Before reaching the agent, altitude is divided by 1,000, velocity by 100, and fuel by 500. This keeps the input values closer in scale.

After each step, Gaussian noise is added to the measurements: standard deviation 5 m for altitude, 2.5 m/s for velocity, and 3 fuel units. The initial observation from `reset()` has no measurement noise. Throttle also receives Gaussian noise with a standard deviation of 0.04, then is clipped to the range 0 to 1.

## Rewards

The reward function encourages downward progress and safe landings while charging for fuel and flight time:

| Event | Reward |
|---|---|
| Downward progress | +0.02 per metre |
| Fuel used | -0.02 per unit |
| Flight time | -0.02 per second |
| Safe landing | +100 |
| Crash | -100, plus an intended speed penalty |
| Timeout | -200 |

These terms are added together each step. The intended crash penalty includes `-2 × abs(velocity)`, but the C++ simulator resets velocity to zero on ground contact before Python reads it. This means the extra speed penalty currently adds nothing.

## Current state

This is still a learning project. The included v5 checkpoint is experimental, and no confirmed success rate is published here. Results need to be measured with the checkpoint and environment settings used for each run.

The simulator currently supports vertical movement only. Gravity is constant, and mass does not decrease as fuel is burned.

Two environment details still need attention:

- In `reset()`, the variable named `fuel` is passed as the C++ constructor's mass argument. This randomizes mass between 450 and 550 kg, while actual fuel starts at 500 units.
- Noisy altitude and fuel observations are not clipped. They can fall below the declared observation-space bounds near the ground or when fuel is low, which can cause the environment checker to fail.

The next steps are checking these environment details, improving the reward function, and recording repeatable evaluation results.
