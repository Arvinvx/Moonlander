# Moonlander

A lunar lander simulation with a reinforcement learning agent that learns to control the engine throttle.

I'm building this project to learn how C++ physics, Python, and reinforcement learning work together. It is still in development, and I am experimenting with the reward function and training settings.

**Lander V2.1 is the best model currently available for this project and the recommended version to use.** Lander V1 is old, is no longer recommended, and has been removed from the current files.

## How it works

The simulator models vertical movement under lunar gravity. The agent reads three values: altitude, vertical velocity, and remaining fuel. It then chooses a throttle value between `0` and `1`.

Each episode starts with a random altitude, descent speed, mass, and maximum thrust. During flight, noise is added to the throttle and sensor readings so the agent has to handle changing conditions.

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
│   ├── lander-v2.zip           # Earlier checkpoint used for further training
│   └── lander-v2.1             # Recommended checkpoint (ZIP archive without .zip)
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

## Model versions

| Version | Current use |
|---|---|
| Lander V2.1 | Best available model for this project, selected by the project author. Used by the evaluation script. |
| Lander V2 | Earlier checkpoint. Used as the starting point for V2.1 training. |
| Lander V1 | Old model, no longer recommended. Its `ppo_lander_v1_reward_v5.zip` checkpoint has been removed from the current files. |

The V2.1 file is named `model/lander-v2.1`. It contains a Stable-Baselines3 ZIP checkpoint even though its filename does not end in `.zip`. The scripts use this exact path.

## Evaluate the model

```bash
python ai/eval.py
```

The evaluation script loads `model/lander-v2.1` and runs 100 episodes on the CPU. It prints the throttle at each step, then reports landings, crashes, timeouts, success rate, and average reward.

The checkpoint path is set in the script's `PPO.load(...)` call. To evaluate V2 instead, set this path to `model/lander-v2.zip`.

With `TEST = 1`, the agent chooses actions using `deterministic=True`, so it does not sample random policy actions. Starting conditions, throttle noise, and sensor noise are still random, so results can vary between runs. The script does not set a fixed seed.

The final report still has the old heading `PPO V1 RESULTS`. The loaded checkpoint is V2.1; the heading does not identify the model version.

`TEST = 2` replaces the policy action with full throttle to check engine braking. Environment noise still applies. This mode checks the simulator and should not be reported as the agent's performance.

## Train a model

```bash
python ai/train.py
```

The script first calls Gymnasium's environment checker, then loads `model/lander-v2.zip` and continues PPO training on the CPU for about 100,000 more timesteps. It uses the policy and settings stored in that checkpoint.

The output is `model/lander-v2.1`, which replaces the existing V2.1 checkpoint. Make a copy first if you want to keep the current model. Running training again starts from V2 each time; it does not automatically continue from V2.1.

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

This is still a learning project. V2.1 is the current recommended model, but the project remains experimental. No measured success rate or comparison between versions is published here yet. Record the checkpoint, environment settings, and evaluation results when comparing runs.

The simulator currently supports vertical movement only. Gravity is constant, and mass does not decrease as fuel is burned.

Two environment details still need attention:

- In `reset()`, the variable named `fuel` is passed as the C++ constructor's mass argument. This randomizes mass between 450 and 550 kg, while actual fuel starts at 500 units.
- Noisy altitude and fuel observations are not clipped. They can fall below the declared observation-space bounds near the ground or when fuel is low, which can cause the environment checker to fail.

The next steps are checking these environment details, improving the reward function, and recording repeatable evaluation results.
