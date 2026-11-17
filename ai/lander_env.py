import gymnasium as gym
import lander_cpp
import numpy as np
from reward import get_reward

class LanderEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.action_space = gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(1,),
            dtype=np.float32
        )

        self.observation_space = gym.spaces.Box(
            low=np.array([0, -np.inf, 0], dtype=np.float32),
            high=np.array([np.inf, np.inf, np.inf], dtype=np.float32),
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed) 
        self.rocket = lander_cpp.Lander(1000, -50, 1000, 3000, 0.2, 500, 2)
        self.counter = 0
        self.getaltitude = self.rocket.get_altitude()
        self.getVelocity = self.rocket.get_velocity()
        self.getFuel = self.rocket.get_fuel()
        observation = np.array([
            self.getaltitude,
            self.getVelocity,
            self.getFuel
        ], dtype=np.float32)
        

        return observation, {}

    def step(self, action):
        self.counter += 1
        self.throttle = action.item()  # here we ask ai to give us a value between 0 and 1 (thrust).
        self.rocket.set_throttle(self.throttle)
        self.fuel_before = self.rocket.get_fuel()
        self.previous_altitude = self.rocket.get_altitude()
        self.rocket.move(1.0)
        self.rocket_status = self.rocket.get_status()
        self.new_altitude = self.rocket.get_altitude()
        self.new_velocity = self.rocket.get_velocity()
        self.new_fuel = self.rocket.get_fuel()
        self.landed = self.rocket_status == lander_cpp.LanderStatus.LANDED
        self.crashed = self.rocket_status == lander_cpp.LanderStatus.CRASHED
        self.timed_out = self.counter >= 300 and self.rocket_status == lander_cpp.LanderStatus.FLYING

        reward = get_reward(
        self.landed,
        self.crashed,
        self.timed_out,
        self.fuel_before,
        self.new_fuel,
        1.0,
        self.new_velocity,
        self.new_altitude,
        self.previous_altitude
    )

        observation = np.array([ # So why create observation again? Because PPO expects those three numbers together in one NumPy array, not as three separate variables.
            self.new_altitude,
            self.new_velocity,
            self.new_fuel
        ], dtype=np.float32)

        terminated = self.landed or self.crashed
        truncated = self.timed_out

        # why observation, reward, terminated, truncated, {}? Because knowing something inside our code isn't the same as telling PPO about it.

        return observation, reward, terminated, truncated, {}



# action_space: The rocket has one control, throttle, between 0 and 1.

# observation_space: The rocket has three measurements: altitude, velocity, and fuel.