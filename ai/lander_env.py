import gymnasium as gym
import lander_cpp
import numpy as np
from reward import get_reward

class LanderEnv(gym.Env):
    def __init__(self):
        super().__init__()

        self.action_space = gym.spaces.Box( # What ai can return to us. The ai can return a value between 0 and 1 (throttle).
            low=0.0,
            high=1.0,
            shape=(1,),
            dtype=np.float32
        )

        self.observation_space = gym.spaces.Box( # What ai can see. The ai can see the altitude, velocity, and fuel of the rocket.
            low=np.array([0, -10, 0], dtype=np.float32), # because after normalization, velocity values become smaller. so its -10 not infinity.
            high=np.array([np.inf, np.inf, np.inf], dtype=np.float32),
            dtype=np.float32
        )

    def reset(self, seed=None, options=None):
        super().reset(seed=seed) 
        self.rocket = lander_cpp.Lander(1000, -10, 1000, 3000, 0.2, 500, 2)        
        self.counter = 0
        self.getaltitude = self.rocket.get_altitude()
        self.getVelocity = self.rocket.get_velocity()
        self.getFuel = self.rocket.get_fuel()
        observation = np.array([
            self.getaltitude/1000.0,
            self.getVelocity/100.0,
            self.getFuel/500.0
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

        observation = np.array([ # normalize the values to make it easier for the AI to learn.
            self.new_altitude / 1000.0,
            self.new_velocity / 100.0,
            self.new_fuel / 500.0
        ], dtype=np.float32)

        terminated = self.landed or self.crashed
        truncated = self.timed_out

        # why observation, reward, terminated, truncated, {}? Because knowing something inside our code isn't the same as telling PPO about it.

        return observation, reward, terminated, truncated, {}



# action_space: The rocket has one control, throttle, between 0 and 1.

# observation_space: The rocket has three measurements: altitude, velocity, and fuel.


# You don't need to specify where action comes from. Whoever calls step() supplies that argument. During training, that's Stable-Baselines3's PPO algorithm.

# Gymnasium defines the standard rules for how PPO interacts with an environment.